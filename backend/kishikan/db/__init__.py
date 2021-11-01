import sys
from collections import defaultdict
from typing import List
from pymongo import MongoClient

from kishikan.configs import QUERY_BATCH_SIZE
from kishikan.types import Fingerprint

class Database:
    def __init__(self, uri: str, name: str):
        client = MongoClient(uri)
        self.db = client[name]  # Collection
        self.fingerprints = self.db["fingerprints"]
        self.songs = self.db["songs"]

    def insert_fingerprints(self, fps: List[Fingerprint], hash: str):
        self.fingerprints.insert_many([{
            "fingerprint": fp_hash,  # Fingerprint Hash
            "hash": hash,
            "offset": int(offset),  # type cast np.int64 to normal int
        } for fp_hash, offset in fps])

    def insert_song(self, hash: str, meta: dict = {}):
        meta["_id"] = hash
        self.songs.insert(meta)

    def get_song_hashes(self):
        songs = list(self.songs.aggregate([
            {
                "$group": {
                    "_id": "$_id"
                }
            }
        ]))
        return [song["_id"] for song in songs]

    def get_song(self, id) -> dict:
        return self.songs.find_one({"_id": id})

    def match_fingerprints(self, fps: List[Fingerprint]):
        hash_offset_map = defaultdict(list)
        for fp_hash, offset in fps:
            hash_offset_map[fp_hash].append(offset)
        hashes = list(hash_offset_map.keys())
        songs_matches = defaultdict(lambda: {
            "matches": 0,
            "offset": sys.maxsize
        })
        for i in range(0, len(hashes), QUERY_BATCH_SIZE):
            items = list(self.fingerprints.find({
                "fingerprint": {
                    "$in": hashes[i:i + QUERY_BATCH_SIZE]
                }
            }))
            for fp in items:
                songs_matches[fp["hash"]]["matches"] += 1
                for offset in hash_offset_map[fp["fingerprint"]]:
                    match_offset = fp["offset"] - offset
                    # If the match offset is earlier, use this as song offset
                    if match_offset < songs_matches[fp["hash"]]["offset"]:
                        songs_matches[fp["hash"]]["offset"] = match_offset
        return songs_matches
