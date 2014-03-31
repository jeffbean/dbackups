#!/usr/bin/env python
# coding=utf-8
import argparse
import logging
import logging.config
from pprint import pprint
import tempfile
import os

from pkg_resources import resource_filename

from dbackups.util.tools import get_database_object, upload_http_put


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
backup_parser.add_argument('--upload_url', default=None, help='Target URL to upload the resulting backup.')

clone_parser = sub_parser.add_parser('clone', help='Clone a production DB into a development DB.')
clone_parser.add_argument('--dev_host', default='localhost', help='The host you want to publish the dumped database '
                                                                  'to.')
clone_parser.add_argument('--dev_name', help='The name of the DB for the clone_to.')
clone_parser.add_argument('--dev_port', help='The port to the DB going to be restored to.')
clone_parser.add_argument('--dev_user', help='The  user that can perform a restore.')
clone_parser.add_argument('--dev_password', help='The user password for performing the actions.')
clone_parser.add_argument('-l', dest='latest_local', default=False, action='store_true',
                          help='If you want to use the latest local dump.')

parser.add_argument('database', help='The database name you want to clone_to.')
parser.add_argument('type', help='The DB type.')

def main():
    if not os.path.isdir(os.path.join(BASE_DIR, '../logs')):
        os.mkdir(os.path.join(BASE_DIR, '../logs'))

    logging_config = resource_filename(__name__, '../config/logging.ini')
    logging.config.fileConfig(logging_config)

    args = parser.parse_args()
    pprint(args)
    db_object = get_database_object(args.type, args.host, args.name, args.user, args.password, args.port)
    logging.debug('DB object created: {}'.format(db_object))

    if args.command == 'backup':
        logging.info('Chose to backup {}'.format(db_object.db_host))
        logging.info('Dump file: [{}]'.format(db_object.dump_file_name))
        db_object.dump()
        logging.info('Dumping DB finished.')
        if args.upload_url:
            print('Uploading to the desired URL: {}'.format(args.upload_url))
            upload_http_put(db_object.dump_file, args.upload_url)

    if args.command == 'clone':
        logging.info('Going to clone_to from one DB to another.')
        dev_db = get_database_object(args.db_type, args.dev_host, args.dev_name, args.dev_user, args.dev_password,
                                     args.dev_port)
        db_object.clone_to(dev_db, args.latest_local)


if __name__ == '__main__':
    main()