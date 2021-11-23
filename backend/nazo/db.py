from collections import defaultdict
from typing import Dict, List, Tuple
from librosa.core import pitch
from pymongo import MongoClient

from nazo.configs import DATA_CONFIGS

class Database:
    def __init__(self, uri: str, name: str) -> None:
        client = MongoClient(uri)
        self.db = client[name]  # Collection
        self.pitches = self.db["pitches"]
        self.songs = self.db["songs"]
        self.metadata = client[DATA_CONFIGS["METADATA_DB_NAME"]]['metadata']

    def get_song_hashes(self) -> List[str]:
        songs = list(self.songs.aggregate([
            {
                "$group": {
                    "_id": "$_id"
                }
            }
        ]))
        return [song["_id"] for song in songs]

    def insert_pitches(self, id, pitches, title):
        self.pitches.insert({
            "_id": id,
            "pitches": pitches,
            "title": title,
        })

    def load_all_pitches(self):
        return self.pitches.find({})
