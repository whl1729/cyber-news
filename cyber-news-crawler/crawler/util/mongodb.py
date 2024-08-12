from crawler.util.configer import config
from pymongo import MongoClient


class MongoDB:
    def __init__(self, host: str, port: int, db: str):
        self._client = MongoClient(f"mongodb://{host}:{port}/")
        self._db = self._client[db]

    def insert_one(self, coll_name: str, document: dict):
        """Insert a document to a collection"""
        coll = self._db[coll_name]
        return coll.insert_one(document)

    def insert_many(self, coll_name: str, documents: list[dict]):
        """Insert many documents to a collection"""
        coll = self._db[coll_name]
        return coll.insert_many(documents)

    def delete_one(self, coll_name: str, query: dict):
        coll = self._db[coll_name]
        return coll.delete_one(query)

    def find(self, coll_name: str, query: dict) -> list:
        coll = self._db[coll_name]
        return list(coll.find(query))


mongo = MongoDB(
    config["mongodb_host"], config["mongodb_port"], config["mongodb_database"]
)
