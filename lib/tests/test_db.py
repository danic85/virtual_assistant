

import datetime, unittest
import os, sys
from mock import Mock, call, patch, MagicMock
import pymongo

from lib.db import Database

class TestDBMethods(unittest.TestCase):

    def test_insert(self):
        pass
        # with patch('pymongo.MongoClient') as mock_mongo:
        #     db = Database()
        #     mock_db = {'test': Mock()}
        #     mock_db['test'].insert_one = Mock()
        #     mock_mongo.mojo_db = mock_db
        #     db.insert('test', {'something': 'thing'})
        #     mock_db['test'].insert_one.assert_called_with({'something': 'asd'})

if __name__ == '__main__':
    unittest.main()
