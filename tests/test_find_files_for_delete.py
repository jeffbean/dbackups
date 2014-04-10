# coding=utf-8
from unittest import TestCase

__author__ = 'jbean'


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

    def test_find_files_for_delete(self):
        self.fail()

    def test_delete_file_list(self):
        self.fail()