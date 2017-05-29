from pymongo import MongoClient


class Database(object):
    def __init__(self):
        client = MongoClient()
        self.db = client.mojo_db

    def insert(self, collection_name, data_json):
        result = self.db[collection_name].insert_one(data_json)
        return result.inserted_id

    def find(self, collection_name, criteria={}):
        result = self.db[collection_name].find(criteria)
        return result

    def delete(self, collection_name, document):
        self.db[collection_name].delete_one(document)