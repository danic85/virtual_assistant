

import datetime, unittest
import os, sys, collections
from mock import Mock, call, patch
from freezegun import freeze_time

from lib.interaction import Interaction
from behaviours import general

class TestBehaviourMethods(unittest.TestCase):

    def test_behaviour_init(self):
        # self.assertEqual(type(general.General.routes), type(collections.OrderedDict()))
        g = general.General(db=None, config={}, dir='')  # Use general because Behaviour is abstract base class
        self.assertEqual(g.act, {})
        self.assertEqual(g.db, None)
        self.assertEqual(g.dir, '')
        self.assertEqual(g.files, g.dir + '/files')
        self.assertEqual(g.config, {})
        self.assertEqual(g.collection, '')
        self.assertEqual(g.match, None)
        self.assertEqual(g.execution_order, 1)
        self.assertEqual(g.logging, None)
        self.assertEqual(g.history, {})

    def test_behaviour_handle(self):
        g = general.General(db=None, config={}, dir='')  # Use general because Behaviour is abstract base class
        act = Interaction()
        g.logging = Mock()
        g.info = Mock(return_value=True)
        response = g.handle(act)
        self.assertEqual(response, None)
        act.command = {'text': 'time'}
        response = g.handle(act)
        self.assertNotEqual(response, None)

    @freeze_time("2017-01-01")
    def test_behaviour_set_history(self):
        g = general.General(db=None, config={}, dir='')  # Use general because Behaviour is abstract base class
        g.logging = Mock()
        g.info = Mock(return_value=True)
        g.set_history(1, {'msg': 'test'})
        expected = {1: {'msg': 'test', 'time': datetime.datetime.now()}}
        self.assertEqual(g.history, expected)

    @freeze_time("2017-01-01")
    def test_behaviour_get_recent_history(self):
        g = general.General(db=None, config={}, dir='')  # Use general because Behaviour is abstract base class
        g.logging = Mock()
        g.info = Mock(return_value=True)
        response = g.get_recent_history(1)
        self.assertEqual(response, None)  # If no history

        g.history = {1: {'msg': 'test', 'time': datetime.datetime.now() - datetime.timedelta(minutes=10)}}
        response = g.get_recent_history(1)
        self.assertEqual(response, None)  # If history expired

        expected = {'msg': 'test', 'time': datetime.datetime.now()}
        g.history = {1: expected}
        response = g.get_recent_history(1)
        self.assertEqual(response, expected)  # If history valid

if __name__ == '__main__':
    unittest.main()