import traceback
import warnings
import numpy as np
from typing import Any, Dict, List

from kishikan.configs import MODE, TOP_N
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
        files = get_audio_files(path, is_dir=is_dir)
        n_files = len(files)
        for idx, (file_path, file_name, file_ext) in enumerate(files):
            audio_md5 = md5(file_path)
            if audio_md5 in self.song_hashes:
                if self.verbose:
                    print(f'Skipped duplicated fingerprinting for {file_path}...')
                continue
            try:
                print(f"({idx + 1}/{n_files}) Fingerprinting for {file_name}{file_ext}...")
                y, sr = load_audio(file_path)
                fps = fingerprint(y, sr=sr, verbose=self.verbose)
                num_fps = len(fps)
                # Add song hash in db
                self.song_hashes.add(audio_md5)
                if save_meta:
                    meta = get_song_metadata(file_path)
                    meta["ext"] = file_ext
                    meta["mode"] = MODE
                else:
                    meta = None
                self.db.insert_song(audio_md5, num_fps, file_name, meta)
                self.db.insert_fingerprints(fps, audio_md5)
            except Exception as e:
                traceback.print_exc()
                print(f'Failed to fingerprint {file_path}:\n{e}')

    def match(self, audio, preloaded=False, meta=True) -> List[Dict[str, Any]]:
        # Fingerprint the input song
        y, sr = audio if preloaded else load_audio(audio)
        fps = fingerprint(y, sr=sr, verbose=self.verbose)
        num_fps = len(fps)
        if num_fps == 0:
            return None
        # Find matching songs in db
        songs_occ = self.db.match_fingerprints(fps)
        rank = []
        for id, stat in songs_occ.items():
            if stat["matches"] <= 2:
                continue
            max_offset_pair = max(stat["offsets"].items(), key=lambda k: k[1])
            # print(stat["offsets"])
            rank.append((id, max_offset_pair[1], max_offset_pair[0]))
        top_n = sorted(rank, key=lambda t: t[1], reverse=True)[:TOP_N]
        top_n_total_matches = sum([matches for _, matches, _ in top_n])
        top_n_songs = []
        # Sort the matching songs by num matches, and retain only top NUM_RANKING songs
        for id, matches, start_offset in top_n:
            # Fetch song metadata in db, and concat with prediction info in ranking
            song = self.db.get_song(id, meta=meta)
            song["match"] = round(matches / top_n_total_matches, 4)
            song["offset"] = offset_to_seconds(start_offset)
            top_n_songs.append(song)
        return top_n_songs
