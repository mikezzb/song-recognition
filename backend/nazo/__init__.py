import warnings
from typing import Any, Dict, List
from nazo.configs import TOP_N
from nazo.utils import load_audio, md5
from nazo.core import audio_to_pitches, midi_to_pitches, pitches_to_series, score
from nazo.utils import get_audio_files
from nazo.db import Database

# Ignore librosa load mp3 warning
warnings.filterwarnings('ignore')

class Nazo:
    def __init__(self, db_uri, db_name="nazo", verbose=False) -> None:
        self.db = Database(db_uri, db_name)
        self.verbose = verbose
        self.song_hashes = set([])
        self.__load_midi_database()

    def __load_midi_database(self) -> None:
        self.pitches = list(self.db.load_all_pitches())
        for song in self.pitches:
            self.song_hashes.add(song["_id"])
            song["pitches"] = pitches_to_series(song["pitches"])
        print(f"Loaded pitches of {len(self.song_hashes)} songs.")

    def make_midi_database(self, path, is_dir=True):
        for file_path, file_name, _ in get_audio_files(path, is_dir=is_dir, extensions=set(['.mid'])):
            song_id = md5(file_path)
            if song_id not in self.song_hashes:
                pitches = midi_to_pitches(file_path)
                self.db.insert_pitches(song_id, pitches, file_name)
                self.song_hashes.add(song_id)
            else:
                if self.verbose:
                    print(f"Skipped dup file {file_name}")

    def query(self, audio, preloaded=False) -> List[Dict[str, Any]]:
        y, sr = audio if preloaded else load_audio(audio)
        query_pitches = audio_to_pitches(y, sr)
        # print(query_pitches)
        results = []
        for song in self.pitches:
            dist = score(query_pitches, song["pitches"])
            # print((song["_id"], dist))
            results.append((song["title"], dist))
        results = sorted(results, key=lambda t: t[1])
        return results[0:TOP_N]
