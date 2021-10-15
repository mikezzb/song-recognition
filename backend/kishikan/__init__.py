from kishikan.db.mongodb import get_db

class Kishikan:
    def __init__(self, db_uri, db_name="kishikan"):
        self.db = get_db(db_uri, db_name)
