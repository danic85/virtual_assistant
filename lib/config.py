from lib.db import Database
import sys

class Config(object):

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
        self.db = Database()

    def set(self, key, value):
        results = self.db.find_one('config', {'key': key})
        if results is not None:
            self.db.delete(results)

        self.db.insert('config', {'key': key, 'value': value})
        return 'Config set'

    def get(self, key):
        results = self.db.find_one('config', {'key': key})
        if results is None:
            raise ValueError(key + ' is not set in config')
            return None
        return results['value']

    def request(self, key):  # pragma: no cover
        if sys.version_info < (3, 0):
            value = raw_input("Enter value for config '" + key + "': ")
        else:
            value = input("Enter value for config '" + key + "': ")
        self.set(key, value)
        return value

    def get_or_request(self, key):
        try:
            value = self.get(key)
        except ValueError:
            value = self.request(key)
        return value
