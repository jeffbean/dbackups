#!/usr/bin/env python
# coding=utf-8
__author__ = 'jbean'

import ConfigParser
import logging
import logging.config
import sys

import os


from pkg_resources import resource_filename

if not os.path.isdir('../logs'):
    os.mkdir('../logs')

logging_config = resource_filename(__name__, '../config/logging.ini')
logging.config.fileConfig(logging_config)

from dbackups.src.util.tools import get_database_object, upload_http_put


def main():
    db_config_file = os.path.abspath(os.path.join('/etc/dbackups/databases.ini'))

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