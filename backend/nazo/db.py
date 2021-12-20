from typing import List
from pymongo import MongoClient
from nazo.configs import DATA_CONFIGS, MODE

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

    def insert_pitches(self, pitches: list, meta: dict, save_meta: bool):
        meta["mode"] = MODE
        if save_meta:
            self.metadata.insert(meta)
        meta["pitches"] = pitches
        self.pitches.insert(meta)

    def load_all_pitches(self):
        return self.pitches.find({})
