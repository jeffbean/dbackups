# coding=utf-8
import os
import tempfile
from time import strptime
from unittest import TestCase
import time

from dbackups.util import cleanup_backups


__author__ = 'jbean'


def touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)


class TestCleanup(TestCase):
    long_list = ['2014-04-10-14-37-00',
                 '2014-04-10-14-36-55',
                 '2014-04-10-14-36-51',
                 '2014-04-10-14-36-46',
                 '2014-04-10-14-36-42',
                 '2014-04-10-14-36-37',
                 '2014-04-10-14-36-31']

    good_list = ['2014-04-10-14-37-00',
                 '2014-04-10-14-36-55',
                 '2014-04-10-14-36-51',
                 '2014-04-10-14-36-46',
                 '2014-04-10-14-36-42']

    leftover = ['2014-04-10-14-36-37',
                '2014-04-10-14-36-31']

    test_db_host = 'mcp-tts-01'
    test_db_name = 'tts'

    def setUp(self):
        for timestamp in self.long_list:
            filename = '{}-{}-{}.dump'.format(self.test_db_host, self.test_db_name, timestamp)
            time_int = time.mktime(strptime(timestamp, '%Y-%m-%d-%H-%M-%S'))
            touch(filename, (time_int, time_int))

    def tearDown(self):
        for filename in self.long_list:
            if os.path.isfile(filename):
                os.remove(filename)

    def test_find_five_files_for_delete(self):
        list_of_files = cleanup_backups.find_files_for_delete(tempfile.gettempdir(), self.test_db_host,
                                                              self.test_db_name)
        print(list_of_files)
        self.assertEquals(sorted(self.leftover), sorted(list_of_files))

    def test_delete_file_list(self):
        self.fail()