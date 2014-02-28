# coding=utf-8
import logging
import sys
import os

import requests
from requests.auth import HTTPBasicAuth

from dbackups.db.mysql import MySQLDatabase, WindowsMySQLDatabase
from dbackups.db.postgres import WindowsPostgresDatabase, PostgresDatabase


__author__ = 'jbean'

logger = logging.getLogger()


class NotSupportedDBTypeException(Exception):
    pass


def get_database_object(db_type_string, host, name, user, password, port):
    if db_type_string == 'postgresql':
        if sys.platform == 'win32':
            return WindowsPostgresDatabase(host, name, user, password, port)
        else:
            return PostgresDatabase(host, name, user, password, port)
    elif db_type_string == 'mysql':
        if sys.platform == 'win32':
            return WindowsMySQLDatabase(host, name, user, password, port)
        else:
            return MySQLDatabase(host, name, user, password, port)
    else:
        raise NotSupportedDBTypeException('Not a supported DB for this service: {}'.format(db_type_string))


def upload_http_put(file_to_upload, upload_url, user, password, verify_request=True):
    logger.info('About to upload file: {}'.format(file_to_upload))
    logger.debug('Upload url: {}'.format(upload_url))
    logger.debug('Upload Credentials -> User: {} Password: {}'.format(user, password))

    with open(file_to_upload) as file_obj:
        r = requests.put('{}/{}'.format(upload_url, os.path.basename(file_to_upload)),
                         data=file_obj.read(),
                         auth=HTTPBasicAuth(user, password),
                         verify=verify_request)

    logger.debug('Request URL: {}'.format(r.url))
    r.raise_for_status()
    logger.info('Finished uploading file to {}.'.format(r.url))