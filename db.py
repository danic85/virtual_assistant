from pymongo import MongoClient


class Database(object):
    def __init__(self):
        client = MongoClient()
        self.db = client.mojo_db

    def insert(self, collection_name, data_json):
        data_json['collection'] = collection_name  # this will mean we don't need to pass it explicitly to delete
        result = self.db[collection_name].insert_one(data_json)
        return result.inserted_id

    def find(self, collection_name, criteria={}):
        return self.db[collection_name].find(criteria)

    def delete(self, document):
        collection_name = document.get('collection','properties')  # default to properties @todo remove when not needed
        return self.db[collection_name].delete_one(document)
