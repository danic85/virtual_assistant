import unittest
from mock import Mock, call, patch
from lib.config import Config


class TestGeneralMethods(unittest.TestCase):
    def test_set_config(self):
        b = Config()
        b.db = Mock()
        b.db.insert = Mock(return_value=1234)

        self.assertEquals(b.set('configItem', 'value'), 'Config set: configItem = value')
        b.db.insert.assert_called_with('config', {'key': 'configItem', 'value': 'value'})


    def test_get_config(self):
        b = Config()
        b.db = Mock()
        b.db.find_one = Mock(return_value=None)
        try:
            self.assertEquals(b.get('something'), None)
        except ValueError as e:
            self.assertEqual(str(e), 'something is not set in config')

        b.db.find_one = Mock(return_value={'key': 'configItem', 'value': '1234'})
        self.assertEquals(b.get('something'), '1234')
