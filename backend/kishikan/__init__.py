import traceback
import warnings
import numpy as np
from typing import Any, Dict, List

from kishikan.configs import SAMPLE_RATE, TOP_N
from kishikan.utils import get_song_metadata, load_audio, get_audio_files, max_sliding_window, md5, offset_to_seconds, parallel
from kishikan.core import fingerprint
from kishikan.db import Database

# Ignore librosa load mp3 warning
warnings.filterwarnings('ignore')

class Kishikan:
    def __init__(self, db_uri, db_name="kishikan", verbose=False) -> None:
        self.db = Database(db_uri, db_name)
        self.verbose = verbose
        self.__load_song_hashes()

    def __load_song_hashes(self) -> None:
        self.song_hashes = set(self.db.get_song_hashes())
        print(f"{len(self.song_hashes)} fingerprinted songs in db")

    def fingerprint(self, path, is_dir=True, save_meta=False):
        for file_path, file_name, file_ext in get_audio_files(path, is_dir=is_dir):
            audio_md5 = md5(file_path)
            if audio_md5 in self.song_hashes:
                if self.verbose:
                    print(f'Skipped duplicated fingerprinting for {file_path}...')
                return
            try:
                print(f"Fingerprinting for {file_name}{file_ext}...")
                y, sr = load_audio(file_path)
                fps = fingerprint(y, sr=sr, verbose=self.verbose)
                num_fps = len(fps)
                # Add song hash in db
                self.song_hashes.add(audio_md5)
                if save_meta:
                    meta = get_song_metadata(file_path)
                    meta["ext"] = file_ext
                else:
                    meta = None
                self.db.insert_song(audio_md5, num_fps, meta=meta)
                self.db.insert_fingerprints(fps, audio_md5)
            except Exception as e:
                traceback.print_exc()
                print(f'Failed to fingerprint {file_path}:\n{e}')

    def match(self, audio, preloaded=False) -> List[Dict[str, Any]]:
        # Fingerprint the input song
        y, sr = audio if preloaded else load_audio(audio)
        fps = fingerprint(y, sr=sr, verbose=self.verbose)
        num_fps = len(fps)
        if num_fps == 0:
            return None
        # Find matching songs in db
        songs_occ = self.db.match_fingerprints(fps)
        # Rank songs
        query_offset_min = min(fps, key=lambda t: t[1])[1]
        query_offset_max = max(fps, key=lambda t: t[1])[1]
        query_offset_range = query_offset_max - query_offset_min

        scores = []
        ranks = []

        for id, stat in songs_occ.items():
            match_offsets_range = stat["max_offset"] - stat["min_offset"]
            counts = np.full(match_offsets_range + 1, 0)
            # convert offset-offset_matches dict to array with count or 0 as element
            for offset, matches in stat["offsets"].items():
                counts[offset - stat["min_offset"]] = matches
            num_matches_in_query_range, start_offset = max_sliding_window(counts, query_offset_range)
            scores.append((id, num_matches_in_query_range, start_offset))
            # print(stat)
            # print(num_matches_in_query_range)
            # print(f"matches {num_matches_in_query_range} in k = {query_offset_range}")

        scores = sorted(scores, key=lambda t: t[1], reverse=True)
        top_n = scores[:TOP_N]
        top_n_total_matches = sum([matches for _, matches, _ in top_n])

        # Sort the matching songs by num matches, and retain only top NUM_RANKING songs
        for id, matches, start_offset in top_n:
            # Fetch song metadata in db, and concat with prediction info in ranking
            song = self.db.get_song(id)
            song["match"] = round(matches / top_n_total_matches, 4)
            song["offset"] = offset_to_seconds(start_offset)
            ranks.append(song)
        return ranks
