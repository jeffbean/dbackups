# coding=utf-8
import os
import tempfile
from time import strptime
from unittest import TestCase
import time

from dbackups.util import cleanup_backups


__author__ = 'jbean'


def touch(fname, tmp_dir, times=None):
    fname = os.path.join(tmp_dir, fname)
    with open(fname, 'a'):
        os.utime(fname, times)


class TestCleanup(TestCase):
    test_db_host = 'foohost'
    test_db_name = 'foodb'
    test_tmp_dir = tempfile.gettempdir()

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

    def setUp(self):
        self.expected_delete_files = []
        for timestamp in self.leftover:
            self.expected_delete_files.append(
                os.path.join(self.test_tmp_dir, '{}-{}-{}'.format(self.test_db_host, self.test_db_name, timestamp)))

        for timestamp in self.long_list:
            filename = '{}-{}-{}'.format(self.test_db_host, self.test_db_name, timestamp)
            time_int = time.mktime(strptime(timestamp, '%Y-%m-%d-%H-%M-%S'))
            touch(filename, self.test_tmp_dir, (time_int, time_int))

    def tearDown(self):
        for timestamp in self.long_list:
            filename = os.path.join(self.test_tmp_dir,
                                    '{}-{}-{}'.format(self.test_db_host, self.test_db_name, timestamp))
            if os.path.isfile(filename):
                os.remove(filename)

    def test_find_five_files_for_delete(self):
        """
        Tests if the method for returning a list of files to remove is good.
        """
        list_of_files = cleanup_backups.find_files_for_delete(self.test_tmp_dir, self.test_db_host,
                                                              self.test_db_name)
        self.assertEquals(sorted(self.expected_delete_files), sorted(list_of_files))

    def test_delete_file_list(self):
        """
        Tests if the method to remove the files from the file system really removes the files.
        """
        list_of_files = cleanup_backups.find_files_for_delete(self.test_tmp_dir, self.test_db_host,
                                                              self.test_db_name)
        self.assertEquals(sorted(self.expected_delete_files), sorted(list_of_files))

        cleanup_backups.delete_file_list(list_of_files)

        for files in list_of_files:
            self.assertFalse(os.path.isfile(files), "Failed to remove the file.")