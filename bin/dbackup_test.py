# coding=utf-8
__author__ = 'jbean'

from dbackups.db.postgres import *
from dbackups.db.mysql import *


def main():
    PostgresDatabase('asdf0', 'asdf', 'asdf', 'asdf')
    MySQLDatabase('asdf0', 'asdf', 'asdf', 'asdf', 1234)


if __name__ == '__main__':
    main()