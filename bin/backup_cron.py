#!/usr/bin/env python
# coding=utf-8
import ConfigParser
import logging
import logging.config
import os
from pprint import pprint
import sys

from src.util.tools import get_database_object, upload_dump_to_ucp_hcp


__author__ = 'jbean'

logging_config = os.path.abspath(os.path.join(os.path.dirname(__file__), '../config', 'logging.ini'))
logging.config.fileConfig(logging_config)

if __name__ == '__main__':
    config_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '../config', 'backup_database.ini'))
    if not os.path.isfile(config_file):
        print('Config File not found. {}'.format(config_file))
        sys.exit(1)

    logging_config = os.path.abspath(os.path.join(os.path.dirname(__file__), '../config', 'logging.ini'))
    logging.config.fileConfig(logging_config)

    config = ConfigParser.ConfigParser()
    config.read(config_file)

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

    pprint(map_of_db_objects)
    for db_section, db_obj in map_of_db_objects.iteritems():
        db_obj.dump()
        upload_dump_to_ucp_hcp(db_obj.dump_file,
                               config.get(db_section, 'upload_url'),
                               config.get(db_section, 'upload_user'),
                               config.get(db_section, 'upload_pass'),
                               verify_request=False)
