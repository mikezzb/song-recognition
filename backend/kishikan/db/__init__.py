from collections import defaultdict
import sys
from typing import Dict, List, Tuple
from pymongo import MongoClient

from kishikan.configs import QUERY_BATCH_SIZE
from kishikan.types import Fingerprint

class Database:
    def __init__(self, uri: str, name: str) -> None:
        client = MongoClient(uri)
        self.db = client[name]  # Collection
        self.fingerprints = self.db["fingerprints"]
        self.songs = self.db["songs"]
        # Create index for fingerprint hash to speed up matching
        self.fingerprints.create_index("fp_hash")

    def insert_fingerprints(self, fps: List[Fingerprint], song_id: str):
        self.fingerprints.insert_many([{
            "fp_hash": fp_hash,  # Fingerprint Hash
            "song_id": song_id,
            "offset": int(offset),  # type cast np.int64 to normal int
        } for fp_hash, offset in fps])

    def insert_song(self, id: str, meta: dict = {}):
        meta["_id"] = id
        self.songs.insert(meta)

    def get_song_hashes(self) -> List[str]:
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

    def match_fingerprints(self, fps: List[Fingerprint]) -> Tuple[list, Dict[str, Dict[str, int]]]:
        hash_offset_map = defaultdict(list)
        for fp_hash, offset in fps:
            hash_offset_map[fp_hash].append(offset)
        hashes = list(hash_offset_map.keys())
        songs_matches = defaultdict(lambda: {
            "matches": 0,
            "offsets": defaultdict(lambda: 0),
            "max_offset": 0,
            "min_offset": 0
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
                    if match_offset < fp_song["min_offset"]:
                        fp_song["min_offset"] = match_offset
                    if match_offset > fp_song["max_offset"]:
                        fp_song["max_offset"] = match_offset
                    fp_song["offsets"][match_offset] += 1
                    fp_song["matches"] += 1
        return songs_matches
