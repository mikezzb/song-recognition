from pymongo import MongoClient

def get_db(uri, name):
    client = MongoClient(uri)
    return client[name]
