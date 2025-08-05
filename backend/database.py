import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if MONGO_URI:
    client = MongoClient(MONGO_URI)
    db = client["constroiverse"]
else:
    class _FakeCollection(dict):
        def find_one(self, query):
            return next(
                (doc for doc in self.values() if all(doc.get(k) == v for k, v in query.items())),
                None,
            )

        def insert_one(self, doc):
            doc = dict(doc)
            doc["_id"] = len(self) + 1
            self[doc["_id"]] = doc

            class _Result:
                inserted_id = doc["_id"]

            return _Result()

        def delete_many(self, query):
            keys = [k for k, v in self.items() if all(v.get(k2) == v2 for k2, v2 in query.items())]
            for k in keys:
                del self[k]

    class _FakeDB:
        def __init__(self):
            self.users = _FakeCollection()

    db = _FakeDB()
