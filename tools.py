# coding=utf-8
import logging
import sys

from fabric.operations import local

from db.mysql import MySQLDatabase
from db.postgres import WindowsPostgresDatabase, PostgresDatabase


__author__ = 'jbean'


class NotSupportedDBTypeException(Exception):
    pass


def get_database_object(db_type_string, host, name, user, password, port):
    if db_type_string == 'postgresql':
        if sys.platform == 'win32':
            return WindowsPostgresDatabase(host, name, user, password, port)
        else:
            return PostgresDatabase(host, name, user, password, port)
    elif db_type_string == 'mysql':
        return MySQLDatabase(host, name, user, password, port)
    else:
        raise NotSupportedDBTypeException('Not a supported DB for this service: {}'.format(db_type_string))


def upload_dump_to_ucp_hcp(file_to_upload, upload_url, user, password):
    logging.info('About to upload file: {}'.format(file_to_upload))
    local('curl -u {user}:{passwd} -k -T {file} {url}'.format(file=file_to_upload, url=upload_url, user=user,
                                                              passwd=password))
    logging.info('Finished uploading file to {}.'.format(upload_url))