# coding=utf-8
import sys

import os
import requests
from requests.auth import HTTPBasicAuth

from dbackups.db.mysql import MySQLDatabase
from dbackups.db.postgres import PostgresDatabase


__author__ = 'jbean'

import logging

class NotSupportedDBTypeException(Exception):
    """
    This Exception is to allow the program to give feedback you are trying to connect to an unsupported DB
    """
    pass


def get_database_object(db_type_string, host, name, user, password, port):
    """
        This method allows an easy way to obtain the correct DB class you are going to be connecting to.

    @param db_type_string: The string database identifier so the code can return the correct Class object
    @type db_type_string: str
    @param host: The Host string for the DB connection parameters
    @type host: str
    @param name: The name of the database
    @type name: str
    @param user: The connection user for doing the dump.
    @type user: str
    @param password: the password connection parameter
    @type password: str
    @param port: port of the connection
    @type port: int
    """
    log = logging.getLogger()
    log.debug('Determining what Class to use for this environment and configuration')
    if db_type_string == 'postgresql':
        if sys.platform == 'win32':
            return NotImplementedError
            #TODO: support Windows as a place to run FROM
            #return WindowsPostgresDatabase(host, name, user, password, port)
        else:
            return PostgresDatabase(host, name, user, password, port)
    elif db_type_string == 'mysql':
        if sys.platform == 'win32':
            return NotImplementedError
            #TODO: support Windows as a place to run FROM
            #return WindowsMySQLDatabase(host, name, user, password, port)
        else:
            return MySQLDatabase(host, name, user, password, port)
    else:
        raise NotSupportedDBTypeException('Not a supported DB for this service: {}'.format(db_type_string))


def upload_http_put(file_to_upload, upload_url, user=None, password=None, verify_request=True):
    """
        This method today has to have authentication but can be expanded to upload to multiple protocols and
        situations.

    @param file_to_upload: The path to the file for upload. has be able to read
    @type file_to_upload: str
    @param upload_url: The http url to do the put to.
    @type upload_url: str
    @param user: Basic HTTP Auth username
    @type user: str
    @param password: Basic HTTP Auth password
    @type password: str
    @param verify_request: If you want to skip the request certificate verification step.
    @type verify_request: bool
    """
    logging.info('About to upload file: {}'.format(file_to_upload))
    logging.debug('Upload url: {}'.format(upload_url))
    logging.debug('Upload Credentials -> User: {} Password: {}'.format(user, password))
    with open(file_to_upload) as file_obj:
        r = requests.put('{}/{}'.format(upload_url, os.path.basename(file_to_upload)),
                         data=file_obj,
                         auth=HTTPBasicAuth(user, password),
                         verify=verify_request)

    logging.debug('Request URL: {}'.format(r.url))
    r.raise_for_status()
    logging.info('Finished uploading file to {}.'.format(r.url))