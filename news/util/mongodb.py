from typing import Optional

from pymongo import MongoClient

from news.util.configer import config


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

    def insert_many_new(
        self, coll_name: str, primary_key: str, documents: list[dict]
    ) -> int:
        """Insert many new documents to a collection"""
        coll = self._db[coll_name]
        count = 0
        for doc in documents:
            exists = list(coll.find({primary_key: doc[primary_key]}))
            if not exists:
                coll.insert_one(doc)
                count += 1

        return count

    def delete_one(self, coll_name: str, filter: Optional[dict] = None):
        coll = self._db[coll_name]
        return coll.delete_one(filter)

    def find(
        self, coll_name: str, filter: Optional[dict] = None, sorter: list = None
    ) -> list:
        coll = self._db[coll_name]
        results = coll.find(filter)
        if sorter is not None:
            results = results.sort(sorter)
        return list(results)

    def find_one(
        self, coll_name: str, filter: Optional[dict] = None, sorter: list = None
    ) -> dict:
        results = self.find(coll_name, filter, sorter)
        return results[0] if results else {}


mongo = MongoDB(
    config["mongodb_host"], config["mongodb_port"], config["mongodb_database"]
)
