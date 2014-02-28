#!/usr/bin/env python
# coding=utf-8

__author__ = 'jbean'

import ConfigParser
import logging
import logging.config
import sys

import os
from pkg_resources import resource_filename

from dbackups.util.tools import get_database_object, upload_http_put


def main():
    home_dir = os.path.expanduser('~')
    program_dir = os.path.abspath(os.path.join(home_dir, '.dbackups'))
    db_config_file = os.path.join(program_dir, 'databases.ini')

    log_dir = os.path.join(program_dir, 'logs')
    if not os.path.isdir(log_dir):
        os.mkdir(log_dir)

    logging_config = resource_filename(__name__, '../config/logging.ini')
    logging.config.fileConfig(logging_config)

    if not os.path.isdir(program_dir):
        os.mkdir(program_dir)

    if not os.path.isfile(db_config_file):
        print('Config File not found. {}'.format(db_config_file))
        sys.exit(1)

    config = ConfigParser.ConfigParser()
    config.read(db_config_file)

    map_of_db_objects = {}

    for db_alias in config.sections():
        if config.getboolean(db_alias, 'enabled'):
            db = get_database_object(config.get(db_alias, 'db_type'),
                                     config.get(db_alias, 'db_host'),
                                     config.get(db_alias, 'db_name'),
                                     config.get(db_alias, 'db_user'),
                                     config.get(db_alias, 'db_pass'),
                                     config.get(db_alias, 'db_port'))
            map_of_db_objects[db_alias] = db

    for db_section, db_obj in map_of_db_objects.iteritems():
        db_obj.dump()
        upload_http_put(db_obj.dump_file,
                        config.get(db_section, 'upload_url'),
                        config.get(db_section, 'upload_user'),
                        config.get(db_section, 'upload_pass'),
                        verify_request=False)


if __name__ == '__main__':
    main()