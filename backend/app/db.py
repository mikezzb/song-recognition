import os
import numpy as np
from pymongo import MongoClient

class Database:
    def __init__(self, uri: str) -> None:
        client = MongoClient(uri)
        self.db = client["songs"]
        self.metadata = self.db['metadata']

    def get_song(self, id) -> dict:
        return self.metadata.find_one({"_id": id}, {"extra": 0})

    def get_songs(self, ids: np.ndarray) -> dict:
        return self.metadata.find({"_id": {"$in": ids}}, {"extra": 0})

    def get_all_songs(self, mode) -> dict:
        return self.metadata.find({"mode": mode}, {"extra": 0, "mode": 0})


db = Database(os.getenv('MONGO_URI'))
