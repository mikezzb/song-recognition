from collections import defaultdict
from typing import Dict, List, Tuple
import numpy as np
from pymongo import MongoClient

from kishikan.configs import DATA_CONFIGS, QUERY_BATCH_SIZE
from kishikan.types import Fingerprint

class Database:
    def __init__(self, uri: str, name: str) -> None:
        client = MongoClient(uri)
        self.db = client[name]  # Collection
        self.fingerprints = self.db["fingerprints"]
        self.songs = self.db["songs"]
        self.metadata = client[DATA_CONFIGS["METADATA_DB_NAME"]]['metadata']
        # Create index for fingerprint hash to speed up matching
        self.fingerprints.create_index("fp_hash")

    def insert_fingerprints(self, fps: List[Fingerprint], song_id: str):
        self.fingerprints.insert_many([{
            "fp_hash": fp_hash,  # Fingerprint Hash
            "song_id": song_id,
            "offset": int(offset),  # type cast np.int64 to normal int
        } for fp_hash, offset in fps])

    def insert_song(self, id: str, num_fps: int, title: str, meta: dict):
        song = {
            "_id": id,
            "num_fingerprints": num_fps
        }
        if not meta:
            song["title"] = title
        self.songs.insert(song)
        if meta:
            meta["_id"] = id
            self.metadata.insert(meta)

    def get_song_hashes(self) -> List[str]:
        songs = list(self.songs.aggregate([
            {
                "$group": {
                    "_id": "$_id"
                }
            }
        ]))
        return [song["_id"] for song in songs]

    def get_song(self, id, meta) -> dict:
        return (self.metadata if meta else self.songs).find_one({"_id": id}, {"extra": 0})

    def get_songs(self, ids: np.ndarray) -> dict:
        return self.metadata.find({"_id": {"$in": ids}}, {"extra": 0})

    def match_fingerprints(self, fps: List[Fingerprint]) -> Tuple[list, Dict[str, Dict[str, int]]]:
        hash_offset_map = defaultdict(list)
        for fp_hash, offset in fps:
            hash_offset_map[fp_hash].append(offset)
        hashes = list(hash_offset_map.keys())
        songs_matches = defaultdict(lambda: {
            "matches": 0,
            "offsets": defaultdict(lambda: 0),
        })
        for i in range(0, len(hashes), QUERY_BATCH_SIZE):
            items = list(self.fingerprints.find({
                "fp_hash": {
                    "$in": hashes[i:i + QUERY_BATCH_SIZE]
                }
            }))
            for fp in items:
                fp_song = songs_matches[fp["song_id"]]
                for offset in hash_offset_map[fp["fp_hash"]]:
                    match_offset = fp["offset"] - offset
                    fp_song["offsets"][match_offset] += 1
                    fp_song["matches"] += 1
        return songs_matches
