from lib.db import Database


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

    def get(self, section, key):
        results = self.db.find_one('config', {'key': key})
        if results is None:
            return None
        return results['value']
