# coding=utf-8
import base64
import hashlib
import logging
import os
import sys

import requests
from requests.auth import AuthBase, HTTPBasicAuth

from src.db.mysql import MySQLDatabase
from src.postgres import WindowsPostgresDatabase, PostgresDatabase


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


class HTTPHCPAuth(AuthBase):
    """Attaches HTTP Basic Authentication to the given Request object."""

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def _hcp_auth_str(self):
        """Returns a Basic HCP Auth string."""
        auth_user = base64.b64encode(self.username)
        auth_pass = hashlib.md5(self.password)
        return 'HCP {}:{}'.format(auth_user, auth_pass.hexdigest())

    def __call__(self, r):
        r.headers['Authorization'] = self._hcp_auth_str()
        return r


def upload_dump_to_ucp_hcp(file_to_upload, upload_url, user, password, verify_request=True):
    logging.info('About to upload file: {}'.format(file_to_upload))
    #local('curl -u {user}:{passwd} -k -T {file} {url}'.format(file=file_to_upload, url=upload_url, user=user,
    #                                                              passwd=password))
    logging.info('Upload url: {}'.format(upload_url))
    logging.info('Upload Credentials -> User: {} Password: {}'.format(user, password))
    r = requests.put('{}/{}'.format(upload_url, os.path.basename(file_to_upload)),
                     data=file_to_upload,
                     auth=HTTPBasicAuth(user, password),
                     verify=verify_request)
    logging.debug('Request URL: {}'.format(r.url))
    r.raise_for_status()
    logging.info('Finished uploading file to {}.'.format(r.url))