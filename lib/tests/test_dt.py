

import datetime, unittest
from mock import Mock, call, patch, MagicMock
import lib.dt
from freezegun import freeze_time

class TestDateTimeMethods(unittest.TestCase):

    @freeze_time("2017-06-07 07:00")
    def test_period_from_datetime(self):
        self.assertEqual(lib.dt.period_from_datetime(datetime.datetime.now() + datetime.timedelta(days=-1)),
                         'a Tuesday morning')
        self.assertEquals(lib.dt.period_from_datetime(datetime.datetime.now()), 'this morning')
        self.assertEqual(lib.dt.period_from_datetime(datetime.datetime.now() + datetime.timedelta(days=1)), 'Thursday morning')
        self.assertEqual(lib.dt.period_from_datetime(datetime.datetime.now() + datetime.timedelta(days=2)),
                         'Friday morning')
        self.assertEqual(lib.dt.period_from_datetime(datetime.datetime.now() + datetime.timedelta(days=3)),
                         'Saturday morning')
        self.assertEqual(lib.dt.period_from_datetime(datetime.datetime.now() + datetime.timedelta(days=4)),
                         'Sunday morning')
        self.assertEqual(lib.dt.period_from_datetime(datetime.datetime.now() + datetime.timedelta(days=5)),
                         'Monday morning')
        self.assertEqual(lib.dt.period_from_datetime(datetime.datetime.now() + datetime.timedelta(days=6)),
                         'Tuesday morning')
        self.assertEqual(lib.dt.period_from_datetime(datetime.datetime.now() + datetime.timedelta(days=7)),
                         'next Wednesday morning')
        self.assertEqual(lib.dt.period_from_datetime(datetime.datetime.now() + datetime.timedelta(days=8)),
                         'next Thursday morning')
        self.assertEqual(lib.dt.period_from_datetime(datetime.datetime.now() + datetime.timedelta(days=9)),
                         'next Friday morning')
        self.assertEqual(lib.dt.period_from_datetime(datetime.datetime.now() + datetime.timedelta(days=10)),
                         'next Saturday morning')
        self.assertEqual(lib.dt.period_from_datetime(datetime.datetime.now() + datetime.timedelta(days=11)),
                         'next Sunday morning')
        self.assertEqual(lib.dt.period_from_datetime(datetime.datetime.now() + datetime.timedelta(days=12)),
                         'next Monday morning')
        self.assertEqual(lib.dt.period_from_datetime(datetime.datetime.now() + datetime.timedelta(days=13)),
                         'next Tuesday morning')
        self.assertEqual(lib.dt.period_from_datetime(datetime.datetime.now() + datetime.timedelta(days=14)),
                         'a Wednesday morning')

        # hours
        for i in range(0, 6):
            self.assertEqual(lib.dt.period_from_datetime(datetime.datetime(2017, 6, 7, i, 0)),
                             'early this morning')
            self.assertEqual(lib.dt.period_from_datetime(datetime.datetime(2017, 6, 8, i, 0)),
                             'Thursday early morning')

        for i in range(7, 12):
            self.assertEqual(lib.dt.period_from_datetime(datetime.datetime(2017, 6, 7, i, 0)), 'this morning')
            self.assertEqual(lib.dt.period_from_datetime(datetime.datetime(2017, 6, 8, i, 0)),
                             'Thursday morning')

        for i in range(13, 15):
            self.assertEqual(lib.dt.period_from_datetime(datetime.datetime(2017, 6, 7, i, 0)), 'this midday')  # @todo 'this midday'???
            self.assertEqual(lib.dt.period_from_datetime(datetime.datetime(2017, 6, 8, i, 0)),
                             'Thursday midday')

        for i in range(16, 18):
            self.assertEqual(lib.dt.period_from_datetime(datetime.datetime(2017, 6, 7, i, 0)), 'this afternoon')
            self.assertEqual(lib.dt.period_from_datetime(datetime.datetime(2017, 6, 8, i, 0)),
                             'Thursday afternoon')

        for i in range(19, 21):
            self.assertEqual(lib.dt.period_from_datetime(datetime.datetime(2017, 6, 7, i, 0)), 'this evening')
            self.assertEqual(lib.dt.period_from_datetime(datetime.datetime(2017, 6, 8, i, 0)),
                             'Thursday evening')

        for i in range(22, 24):
            self.assertEqual(lib.dt.period_from_datetime(datetime.datetime(2017, 6, 7, i, 0)), 'tonight')
            self.assertEqual(lib.dt.period_from_datetime(datetime.datetime(2017, 6, 8, i, 0)),
                             'Thursday night')

if __name__ == '__main__':
    unittest.main()
