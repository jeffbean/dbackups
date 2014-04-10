# coding=utf-8
import os
import tempfile
from unittest import TestCase

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
    def setUp(self):
        self.db_obj = TestDatabaseClass('host-test', 'test_name', 'test_user', 'test_password', 1234)

    def test_dump_file_name(self):
        self.assertEqual(self.db_obj.dump_file_name, '{}-{}-{}.dump'.format(self.db_obj.db_host,
                                                                            self.db_obj.db_name,
                                                                            self.db_obj.now_stamp))

    def test_dump_file(self):
        self.assertEqual(self.db_obj.dump_file, os.path.join(tempfile.gettempdir(), self.db_obj.dump_file_name))
        self.assertRaises(OSError, setattr, self.db_obj, 'dump_file', '/fooadfa')

    def test_dump(self):
        self.fail()

    def test_restore(self):
        self.fail()

    def test_create_empty_database(self):
        self.fail()

    def test_drop_db(self): 
        self.fail()

    def test_clone_to(self):
        self.fail()

    def test_find_latest_dump(self):
        self.fail()