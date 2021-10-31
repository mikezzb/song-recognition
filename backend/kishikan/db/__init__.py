from pymongo import MongoClient

def get_db(uri, name):
    client = MongoClient(uri)
    return client[name]

class Database():
    def __init__(self, uri, name):
        client = MongoClient(uri)
        self.db = client[name]  # Collection
        self.fingerprints = self.db["fingerprints"]
        self.songs = self.db["songs"]

    def insert_fingerprints(self, fp, hash):
        self.fingerprints.insert_many([{
            "fingerprint": item[0],  # Fingerprint Hash
            "hash": hash,
            "offset": int(item[1]),  # type cast np.int64 to normal int
        } for item in fp])

    def insert_song(self, hash, info={}):
        info["_id"] = hash
        self.songs.insert(info)

    def get_song_hashes(self):
        songs = list(self.songs.aggregate([
            {"$group": {
                "_id": "$_id"
            }}
        ]))
        return [song["_id"] for song in songs]
