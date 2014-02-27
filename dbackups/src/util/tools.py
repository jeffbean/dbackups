# coding=utf-8
import logging
import sys

import os
import requests
from requests.auth import HTTPBasicAuth

from dbackups.src.db.mysql import MySQLDatabase
from src.db.postgres import WindowsPostgresDatabase, PostgresDatabase


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


def upload_http_put(file_to_upload, upload_url, user, password, verify_request=True):
    logging.info('About to upload file: {}'.format(file_to_upload))
    logging.debug('Upload url: {}'.format(upload_url))
    logging.debug('Upload Credentials -> User: {} Password: {}'.format(user, password))
    r = requests.put('{}/{}'.format(upload_url, os.path.basename(file_to_upload)),
                     data=file_to_upload,
                     auth=HTTPBasicAuth(user, password),
                     verify=verify_request)
    logging.debug('Request URL: {}'.format(r.url))
    r.raise_for_status()
    logging.info('Finished uploading file to {}.'.format(r.url))