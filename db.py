# from pymongo import MongoClient
import pymongo


class Database(object):
    def __init__(self):
        client = pymongo.MongoClient()
        self.db = client.mojo_db

    def insert(self, collection_name, data_json):
        data_json['collection'] = collection_name  # this will mean we don't need to pass it explicitly to delete
        result = self.db[collection_name].insert_one(data_json)
        return result.inserted_id

    def find(self, collection_name, criteria={}, sort=[]):
        results = self.db[collection_name].find(criteria)
        if len(sort) > 0:
            return results.sort(sort)
        return results

    def delete(self, document):
        collection_name = document.get('collection','properties')  # default to properties @todo remove when not needed
        return self.db[collection_name].delete_one(document)
