import librosa
import traceback
import warnings
import numpy as np
from itertools import groupby
from typing import Any, Dict, List

from numpy.core.fromnumeric import sort
from kishikan.configs import RANKING_NUM, ROUDING, SAMPLE_RATE
from kishikan.utils import get_audio_files, max_sliding_window, md5, offset_to_seconds
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

    def fingerprint(self, path, is_dir=True, save=True):
        for file_path, file_name, file_ext in get_audio_files(path, is_dir=is_dir):
            audio_md5 = md5(file_path)
            if audio_md5 in self.song_hashes and save:
                print(f'Skipped duplicated fingerprinting for {file_path}...')
                continue
            try:
                print(f"Fingerprinting for {file_name}{file_ext}...")
                y, sr = librosa.load(file_path, sr=SAMPLE_RATE)
                fps = fingerprint(y, sr=sr, verbose=self.verbose)
                num_fps = len(fps)
                if save:
                    # Add song hash in db
                    self.db.insert_fingerprints(fps, audio_md5)
                    self.song_hashes.add(audio_md5)
                    self.db.insert_song(audio_md5, meta={
                        "name": file_name,
                        "ext": file_ext,
                        "num_fingerprints": num_fps
                    })
                else:
                    return fps
            except Exception as e:
                traceback.print_exc()
                print(f'Failed to fingerprint {file_path}:\n{e}')

    def match(self, audio, preloaded=False) -> List[Dict[str, Any]]:
        # Fingerprint the input song
        y, sr = audio if preloaded else librosa.load(audio, mono=False, sr=SAMPLE_RATE)
        fps = fingerprint(y, sr=sr, verbose=self.verbose)
        num_fps = len(fps)
        print(f'num fingerprints {num_fps}')
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
            counts = np.zeros(match_offsets_range + 1)
            # convert offset-offset_matches dict to array with count or 0 as element
            for offset, matches in stat["offsets"].items():
                counts[offset + stat["min_offset"]] = matches
            num_matches_in_query_range, start_offset = max_sliding_window(counts, query_offset_range)
            scores.append((id, num_matches_in_query_range, start_offset))
            # print(stat)
            # print(num_matches_in_query_range)
            # print(f"matches {num_matches_in_query_range} in k = {query_offset_range}")

        scores = sorted(scores, key=lambda t: t[1], reverse=True)

        # Sort the matching songs by num matches, and retain only top NUM_RANKING songs
        for id, matches, start_offset in scores[:RANKING_NUM]:
            # Fetch song metadata in db, and concat with prediction info in ranking
            song = self.db.get_song(id)
            song["matches"] = matches
            song["offset"] = offset_to_seconds(start_offset)
            ranks.append(song)
        return ranks
