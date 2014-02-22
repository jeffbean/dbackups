# coding=utf-8
import logging
import datetime

import os
from abc import ABCMeta, abstractmethod
import tempfile


__author__ = 'jbean'
FORMAT = "%(asctime)s %(levelname)-6s line %(lineno)-4s %(message)s"
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger()


class RestoreDatabaseMismatchException(Exception):
    pass


class Database(object):
    __metaclass__ = ABCMeta

    def __init__(self, db_host, db_name, db_user, db_pass, db_port):
        self.db_name = db_name
        self.db_host = db_host
        self.db_user = db_user
        self.db_pass = db_pass
        self.db_port = db_port
        self.now_stamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        self._dump_file_name = '{}-{}-{}.dump'.format(self.db_host, self.db_name, self.now_stamp)

        self._dump_file = os.path.join(tempfile.gettempdir(), self.dump_file_name)

    @property
    def dump_file_name(self):
        return self._dump_file_name

    @dump_file_name.setter
    def dump_file_name(self, value):
        self._dump_file_name = value

    @property
    def dump_file(self):
        return self._dump_file

    @dump_file.setter
    def dump_file(self, path):
        if os.path.isdir(path):
            self._dump_file = path
        else:
            raise OSError()

    @abstractmethod
    def dump(self):
        pass

    @abstractmethod
    def restore(self, database_object):
        logger.debug('Checking if the object given is the same one as we need.')
        if not isinstance(database_object, self.__class__):
            raise RestoreDatabaseMismatchException(
                'The object to restore needs to be the same Database Object Type as the one being restored to.')
        logger.info('Trying to restore {} into {}'.format(self, database_object))

    @abstractmethod
    def create_empty_database(self, new_database_name):
        pass

    @abstractmethod
    def delete_local_db(self, database_name):
        pass

    def find_latest_dump(self):
        """
        returns the file path of the latest dump file from the same host and
        database.
        """
        dump_dir = os.path.dirname(self.dump_file_name)
        files = [os.path.join(dump_dir, f) for f in os.listdir(dump_dir)
                 if os.path.isfile(os.path.join(dump_dir, f)) and
                    f.startswith('{}-{}'.format(self.db_host, self.db_name))]
        latest_file = max(files, key=os.path.getmtime)
        return os.path.abspath(latest_file)

    def __unicode__(self):
        return 'H: {} N: {}'.format(self.db_host, self.db_name, self.dump_file)

    def __str__(self):
        return 'H: {} N: {}'.format(self.db_host, self.db_name, self.dump_file)
