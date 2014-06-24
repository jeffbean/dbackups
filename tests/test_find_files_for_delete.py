# coding=utf-8
import os
from unittest import TestCase

from dbackups.util import cleanup_backups


__author__ = 'jbean'


def touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)


class TestCleanup(TestCase):
    long_list = ['/tmp/mcp-tts-01-tts-2014-04-10-14-37-00.dump',
                 '/tmp/mcp-tts-01-tts-2014-04-10-14-36-55.dump',
                 '/tmp/mcp-tts-01-tts-2014-04-10-14-36-51.dump',
                 '/tmp/mcp-tts-01-tts-2014-04-10-14-36-46.dump',
                 '/tmp/mcp-tts-01-tts-2014-04-10-14-36-42.dump',
                 '/tmp/mcp-tts-01-tts-2014-04-10-14-36-37.dump',
                 '/tmp/mcp-tts-01-tts-2014-04-10-14-36-31.dump']

    good_list = ['/tmp/mcp-tts-01-tts-2014-04-10-14-37-00.dump',
                 '/tmp/mcp-tts-01-tts-2014-04-10-14-36-55.dump',
                 '/tmp/mcp-tts-01-tts-2014-04-10-14-36-51.dump',
                 '/tmp/mcp-tts-01-tts-2014-04-10-14-36-46.dump',
                 '/tmp/mcp-tts-01-tts-2014-04-10-14-36-42.dump']

    leftover = ['/tmp/mcp-tts-01-tts-2014-04-10-14-36-37.dump',
                '/tmp/mcp-tts-01-tts-2014-04-10-14-36-31.dump']

    test_db_host = 'mcp-tts-01'
    test_db_name = 'tts'

    def setUp(self):
        for filename in self.long_list:
            touch(filename)

    def tearDown(self):
        for filename in self.long_list:
            os.remove(filename)

    def test_find_five_files_for_delete(self):
        list_of_files = cleanup_backups.find_files_for_delete('/tmp', self.test_db_host, self.test_db_name)
        print(list_of_files)
        self.assertEquals(sorted(self.leftover), sorted(list_of_files))

    def test_delete_file_list(self):
        self.fail()