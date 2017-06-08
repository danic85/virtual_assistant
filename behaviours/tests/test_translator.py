import datetime, unittest
import os, sys
from mock import Mock, call, patch
from lib import feeds
import re
from behaviours import translator
import json

class TestTranslatorMethods(unittest.TestCase):

    def test_translate(self):
        path = os.path.dirname(os.path.realpath(__file__)) + '/testdata/translator_get_language_code.json'
        with open(path) as data_file:
            data = json.load(data_file)

        translate = {"to": "es", "translationText": "Esto Es un prueba", "from": "en", "text": "this is a test"}
        feeds.get_json = Mock()
        feeds.get_json.side_effect = [data, translate]

        b = translator.Translator(db=None, config={}, dir='')
        key, value = next(iter(b.routes.items()))
        b.match = re.search(key, 'translate this is a test to spanish', re.IGNORECASE)
        self.assertEqual(b.translate(), "Esto Es un prueba")

    def test_translate_back(self):
        path = os.path.dirname(os.path.realpath(__file__)) + '/testdata/translator_get_language_code.json'
        with open(path) as data_file:
            data = json.load(data_file)

        translate = {"to": "en", "translationText": "This is a test", "from": "es", "text": "Esto Es un prueba"}
        feeds.get_json = Mock()
        feeds.get_json.side_effect = [data, translate]

        b = translator.Translator(db=None, config={}, dir='')
        key, value = next(iter(b.routes.items()))
        b.match = re.search(key, 'translate Esto Es un prueba from spanish', re.IGNORECASE)
        self.assertEqual(b.translate(), "This is a test")

    def test_translate_no_language(self):
        path = os.path.dirname(os.path.realpath(__file__)) + '/testdata/translator_get_language_code.json'
        with open(path) as data_file:
            data = json.load(data_file)

        # this should not be needed, as it will not hit it
        translate = {"to": "", "translationText": "Esto Es un prueba", "from": "en", "text": "this is a test"}

        feeds.get_json = Mock()
        feeds.get_json.side_effect = [data, translate]

        b = translator.Translator(db=None, config={}, dir='')
        key, value = next(iter(b.routes.items()))
        b.match = re.search(key, 'translate this is a test to Unknown', re.IGNORECASE)
        self.assertEqual(b.translate(), "I can't translate to Unknown")
