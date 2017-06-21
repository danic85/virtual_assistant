# from pymongo import MongoClient
import pymongo
import random


class Database(object):
    def __init__(self):
        client = pymongo.MongoClient()
        self.db = client.assistant_db

    def insert(self, collection_name, data_json):
        data_json['collection'] = collection_name  # this will mean we don't need to pass it explicitly to delete
        result = self.db[collection_name].insert_one(data_json)
        return result.inserted_id

    def update(self, collection_name, data_json):
        data_json['collection'] = collection_name  # this will mean we don't need to pass it explicitly to delete
        record_id = data_json.get('_id')
        data_json.pop('_id', None)
        return self.db[collection_name].update({'_id': record_id}, {'$set': data_json})

    def upsert(self, collection_name, data_json):
        data_json['collection'] = collection_name  # this will mean we don't need to pass it explicitly to delete
        record_id = data_json.get('_id')
        data_json.pop('_id', None)
        if not record_id:
            return self.insert(collection_name, data_json)
        return self.db[collection_name].update({'_id': record_id}, {'$set': data_json}, upsert=True)

    def find_random(self, collection_name, criteria={}):
        results = self.db[collection_name].find(criteria)
        return results.skip(random.randrange(0, results.count(), 1)).next()

    def find_one(self, collection_name, criteria={}):
        return self.db[collection_name].find_one(criteria)

    def find(self, collection_name, criteria={}, sort=[]):
        results = self.db[collection_name].find(criteria)
        if len(sort) > 0:
            return results.sort(sort)
        return results

    def delete(self, document):
        collection_name = document.get('collection')
        return self.db[collection_name].delete_one({'_id': document.get('_id')})
