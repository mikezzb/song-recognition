import warnings
import numpy as np
from typing import Any, Dict, List
from nazo.utils import md5
from nazo.core import midi_to_pitches, pitches_to_series
from nazo.utils import get_audio_files
from nazo.db import Database

# Ignore librosa load mp3 warning
warnings.filterwarnings('ignore')

class Nazo:
    def __init__(self, db_uri, db_name="nazo", verbose=False) -> None:
        self.db = Database(db_uri, db_name)
        self.verbose = verbose
        self.song_hashes = set([])
        self.pitches = []
        self.__load_midi_database()

    def __load_midi_database(self) -> None:
        raw = self.db.load_all_pitches()
        print('All Loaded')
        for song in raw:
            self.song_hashes.add(song["_id"])
            self.pitches.append({
                "_id": song["_id"],
                "pitches": pitches_to_series(song["pitches"])
            })
        print(f"Loaded pitches of {len(self.song_hashes)} songs.")
        # self.song_hashes = set([song["_id"] for song in raw])

    def make_midi_database(self, path, is_dir=True):
        for file_path, file_name, _ in get_audio_files(path, is_dir=is_dir, extensions=set(['.mid'])):
            song_id = md5(file_path)
            if song_id not in self.song_hashes:
                pitches = midi_to_pitches(file_path)
                self.db.insert_pitches(song_id, pitches)
                self.song_hashes.add(song_id)
            else:
                if self.verbose:
                    print(f"Skipped dup file {file_name}")

    def audio_to_pitches(self, path, is_dir=True, save=True):
        pass

    def query(self, audio, preloaded=False) -> List[Dict[str, Any]]:
        pass
