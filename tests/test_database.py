# coding=utf-8
import os
import tempfile
from unittest import TestCase
from mock import patch

from dbackups.db.database import Database


__author__ = 'jbean'


class TestDatabaseClass(Database):
    def restore(self, database_object, latest_file):
        pass

    def dump(self):
        pass

    def create_empty_database(self, new_database_name):
        pass

    def drop_db(self):
        pass


class TestDatabase(TestCase, TestDatabaseClass):
    test_db_host = 'foo-host'
    test_db_name = 'bar-db'
    test_db_user = 'testuser1'
    test_db_password = 'testuserpass'
    test_db_port = 1324

    def setUp(self):
        self.tempfile_gettempdir = tempfile.gettempdir()

        self.db_obj = TestDatabaseClass(self.test_db_host, self.test_db_name, self.test_db_user, self.test_db_password,
                                        self.test_db_port)
        self.db_obj_2 = TestDatabaseClass(self.test_db_host, self.test_db_name, self.test_db_user,
                                          self.test_db_password,
                                          self.test_db_port)

    def test_dump_file_name(self):
        self.assertEqual(self.db_obj.dump_file_name, '{}-{}-{}.dump'.format(self.test_db_host,
                                                                            self.test_db_name,
                                                                            self.db_obj.now_stamp))

    def test_dump_file(self):
        self.assertEqual(self.db_obj.dump_file, os.path.join(self.tempfile_gettempdir, self.db_obj.dump_file_name))
        self.assertRaises(OSError, setattr, self.db_obj, 'dump_file', '/fooadfa')

    @patch('TestDatabaseClass')
    def test_clone_to(self, mock_class):
        self.db_obj.clone_to(mock_class)


    def test_find_latest_dump(self):
        self.fail()