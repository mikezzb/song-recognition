import librosa
import traceback
import warnings
from typing import Any, Dict, List
from kishikan.configs import RANKING_NUM, ROUDING, SAMPLE_RATE
from kishikan.utils import get_audio_files, md5, offset_to_seconds
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
                y, sr = librosa.load(file_path, mono=True, sr=SAMPLE_RATE)
                fp = fingerprint(y, sr=sr, verbose=self.verbose)
                if save:
                    # Add song hash in db
                    self.db.insert_fingerprints(fp, audio_md5)
                    self.song_hashes.add(audio_md5)
                    self.db.insert_song(audio_md5, meta={
                        "name": file_name,
                        "ext": file_ext,
                    })
                else:
                    return fp
            except Exception as e:
                traceback.print_exc()
                print(f'Failed to fingerprint {file_path}:\n{e}')

    def match(self, audio, preloaded=False) -> List[Dict[str, Any]]:
        # Fingerprint the input song
        y, sr = audio if preloaded else librosa.load(audio, mono=True, sr=SAMPLE_RATE)
        fps = set(fingerprint(y, sr=sr, verbose=self.verbose))
        # Find matching songs in db
        songs_matches = self.db.match_fingerprints(fps)
        # Rank songs
        total_matches = sum([d["matches"] for d in songs_matches.values()])
        ranks = []
        # Sort the matching songs by num matches, and retain only top NUM_RANKING songs
        for id, song in sorted(songs_matches.items(), key=lambda k_v: k_v[1]['matches'], reverse=True)[:RANKING_NUM]:
            # Fetch song metadata in db, and concat with prediction info in ranking
            song_meta = self.db.get_song(id)
            song["offset"] = offset_to_seconds(song["offset"])
            song["confidence"] = round(song["matches"] / total_matches, ROUDING)  # current song num matches / total matches
            song_meta.update(song)
            ranks.append(song_meta)
        return ranks
