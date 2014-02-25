# coding=utf-8
from db.database import Database

__author__ = 'jbean'


class MySQLDatabase(Database):
    def create_empty_database(self, new_database_name):
        Database.create_empty_database(new_database_name)

    def delete_local_db(self, database_name):
        Database.delete_local_db(database_name)

    def dump(self):
        Database.dump()

    def restore(self, database_object):
        Database.restore(database_object)

