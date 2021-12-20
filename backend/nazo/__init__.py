import warnings
from typing import Any, Dict, List

from nazo.configs import TOP_N
from nazo.utils import load_audio, md5
from nazo.core import audio_to_pitches, midi_to_pitches, pitches_to_series, score
from nazo.utils import get_audio_files
from nazo.db import Database
import numpy as np

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

    def make_midi_database(self, path, is_dir=True, save_meta=False):
        song_list = np.loadtxt(f'{path}/songList.txt', delimiter='\n', dtype=str)
        for idx, (file_path, file_name, _) in enumerate(sorted(get_audio_files(path, is_dir=is_dir, extensions=set(['.mid'])), key=lambda l: l[1])):
            title = ' '.join(song_list[idx].split('\t')[1:3]).strip('-')
            song_id = md5(file_path)
            if song_id not in self.song_hashes:
                pitches = midi_to_pitches(file_path)
                self.song_hashes.add(song_id)
                meta = {
                    "_id": song_id,
                    "label": file_name,
                    "title": title,
                }
                self.db.insert_pitches(pitches, meta=meta, save_meta=save_meta)
                meta["pitches"] = pitches_to_series(pitches)
                self.pitches.append(meta)
            else:
                if self.verbose:
                    print(f"Skipped duplicated file {file_name}")

    def query(self, audio, preloaded=False) -> List[Dict[str, Any]]:
        y, sr = audio if preloaded else load_audio(audio)
        query_pitches = audio_to_pitches(y, sr)
        results = []
        for song in self.pitches:
            dist = score(query_pitches, song["pitches"])
            results.append({
                "title": song["title"],
                "dist": dist,
                "label": song["label"]
            })
        results = sorted(results, key=lambda d: d["dist"])
        return results[0: TOP_N]
