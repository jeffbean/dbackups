#!/usr/bin/env python
# coding=utf-8
import ConfigParser
import argparse
import logging
import logging.config
import sys
import os
import tempfile

from fabric.api import local
from fabric.operations import prompt

from db.postgres import PostgresDatabase, WindowsPostgresDatabase
from db.mysql import MySQLDatabase


__author__ = 'jbean'

# change these as appropriate for your platform/environment :
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

parser = argparse.ArgumentParser()

parser.add_argument('--host', help='The host server running postgres for the Database .')
parser.add_argument('--port', help='The port server running postgres for the Database.')
parser.add_argument('--user', help='The user that has access to the DB.')
parser.add_argument('--password', help='The user password for performing the actions.')
parser.add_argument('--dump_dir', default=tempfile.gettempdir(), help='Directory to put the PG dump files locally.')

sub_parser = parser.add_subparsers(help='Service Actions', dest='command')

backup_parser = sub_parser.add_parser('backup', help='Helper functions for backing up a Postgres server')
backup_parser.add_argument('--upload_url', help='Target URL to upload the resulting backup.')

clone_parser = sub_parser.add_parser('clone', help='Clone a production DB into a development DB.')
clone_parser.add_argument('--dev_host', help='The host you want to publish the dumped database to.')
clone_parser.add_argument('--dev_port', help='The port to the DB going to be restored to.')
clone_parser.add_argument('--dev_user', help='The  user that can perform a restore.')
clone_parser.add_argument('--dev_password', help='The user password for performing the actions.')
clone_parser.add_argument('-l', default=False, action='store_true', help='If you want to use the latest local dump.')

parser.add_argument('database', help='The database name you want to clone.')


def upload_dump_to_ucp_hcp(file_to_upload, upload_url):
    logging.info('About to upload file: {}'.format(file_to_upload))
    local('curl -u ucpbackup:534hawks -k -T {} {}'.format(file_to_upload, upload_url))
    logging.info('Finished uploading file to {}.'.format(upload_url))


if __name__ == '__main__':
    if not os.path.isdir(os.path.join(BASE_DIR, 'logs')):
        os.mkdir(os.path.join(BASE_DIR, 'logs'))

    config_file = os.path.abspath(os.path.join(os.path.dirname(__file__), 'config', 'backup_database.ini'))
    if not os.path.isfile(config_file):
        print('Config File not found. {}'.format(config_file))
        sys.exit(1)

    logging_config = os.path.abspath(os.path.join(os.path.dirname(__file__), 'config', 'logging.ini'))
    logging.config.fileConfig(logging_config)

    args = parser.parse_args()

    config = ConfigParser.ConfigParser()
    config.read(config_file)

    logging.debug(config.sections())

    if sys.platform == 'win32':
        cmd = '[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Program Files (x86)\PostgreSQL\8.4\bin",  [System.EnvironmentVariableTarget]::User)'

    if not config.has_section(args.database):
        logging.info('DB not found in the config file. [{}]'.format(args.database))
        db_type = prompt('What type of Database are you working with: ', default='postgresql')
        if not args.host is None:
            db_host = prompt('What host is the DB on: ')
        else:
            db_host = args.host

        db_user = prompt('User for the DB connection: ')
        db_pass = prompt('Password for the DB connection: ')
        db_port = prompt('Port for the DB connection: ', default=5432, validate=int)
        db_name = args.database
    else:
        logging.info('Found the DB settings in the config file. Continuing.')
        db_type = config.get(args.database, 'db_type')
        db_host = config.get(args.database, 'db_host')
        db_user = config.get(args.database, 'db_user')
        db_pass = config.get(args.database, 'db_password')
        db_port = config.get(args.database, 'db_port')
        db_name = config.get(args.database, 'db_name')

    if db_type == 'postgresql':
        if sys.platform == 'win32':
            db = WindowsPostgresDatabase(db_host, db_name, db_user, db_pass, db_port)
        else:
            db = PostgresDatabase(db_host, db_name, db_user, db_pass, db_port)
    elif db_type == 'mysql':
        db = MySQLDatabase(db_host, db_name, db_user, db_pass, db_port)
    else:
        logging.error('Not a supported DB for this service: {}'.format(db_type))
        logging.info('Supported types are: {}'.format(config.get('DEFAULT', 'supported_db_types')))
        sys.exit(1)

    logging.debug(db)

    if args.command == 'backup':
        logging.info('Chose to backup {}'.format(db.db_host))
        logging.info('Dump file: [{}]'.format(db.dump_file_name))
        db.dump()
        logging.info('Dumping DB finished.')

        #upload_dump_to_ucp_hcp(latest_local_db_file, args.upload_url)

