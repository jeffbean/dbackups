#!/usr/bin/env python
# coding=utf-8
import ConfigParser
import argparse
import logging
import logging.config
from pprint import pprint
import sys
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
clone_parser.add_argument('dev_host', default='localhost', help='The host you want to publish the dumped database '
                                                                  'to.')
clone_parser.add_argument('dev_port', help='The port to the DB going to be restored to.')
clone_parser.add_argument('dev_user', help='The  user that can perform a restore.')
clone_parser.add_argument('--dev_pass', default='', help='The user password for performing the actions.')
clone_parser.add_argument('-l', dest='latest_local', default=False, action='store_true',
                          help='If you want to use the latest local dump.')

parser.add_argument('database', help='The database name you want to clone.')


def main():
    home_dir = os.path.expanduser('~')
    program_dir = os.path.abspath(os.path.join(home_dir, '.dbackups'))
    db_config_file = os.path.join(program_dir, 'databases.ini')

    if not os.path.isdir(os.path.join(BASE_DIR, '../logs')):
        os.mkdir(os.path.join(BASE_DIR, '../logs'))

    if not os.path.isfile(db_config_file):
        print('Config File not found. {}'.format(db_config_file))
        sys.exit(1)

    #logging_config = resource_filename(__name__, '../config/logging.ini')
    #logging.config.fileConfig(logging_config)

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-6s line %(lineno)-4s %(message)s')

    args = parser.parse_args()
    pprint(args)
    config = ConfigParser.ConfigParser()
    config.read(db_config_file)

    logging.debug(config.sections())

    if not config.has_section(args.database):
        logging.info('DB alias not found in the config file {} -> [{}]'.format(db_config_file, args.database))
        sys.exit(1)
    else:
        logging.info('Found the DB settings in the config file. Continuing.')
        db_type = config.get(args.database, 'db_type')
        db_host = config.get(args.database, 'db_host')
        db_user = config.get(args.database, 'db_user')
        db_pass = config.get(args.database, 'db_pass')
        db_port = config.get(args.database, 'db_port')
        db_name = config.get(args.database, 'db_name')

    db_object = get_database_object(db_type, db_host, db_name, db_user, db_pass, db_port)
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
        print('what.')
        logging.info('Going to clone_to from one DB to another.')
        dev_db = get_database_object(db_type, args.dev_host, '{}-dev'.format(db_name), args.dev_user, args.dev_pass,
                                     args.dev_port)
        db_object.clone_to(dev_db, args.latest_local)


if __name__ == '__main__':
    main()