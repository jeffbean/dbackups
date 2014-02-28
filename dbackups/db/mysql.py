# coding=utf-8
import logging

from dbackups.db.database import Database
from dbackups.util.commands import assert_command


__author__ = 'jbean'

logger = logging.getLogger()


class MySQLDatabase(Database):
    def __init__(self, db_host, db_name, db_user, db_pass, db_port=3306):
        Database.__init__(self, db_host, db_name, db_user, db_pass, db_port)

    def create_empty_database(self, new_database_name):
        raise NotImplementedError

    def dump(self):
        """
            /usr/bin/pg_dump -h db1 -U postgres jiradb2 -f $BKROOT.$SUF -F c --oids
            >>$LOGFILE 2>&1
            """
        args = ''
        logger.info('Dumping database to file: [{}]'.format(self.dump_file))
        if self.db_pass:
            args += '-p{}'.format(self.db_pass)
        cmd = '/usr/bin/mysqldump -h {host} -P {port} -u {user} {args} {dbname} > {file}'.format(
            host=self.db_host, port=self.db_port,
            args=args, user=self.db_user,
            dbname=self.db_name, file=self.dump_file)

        assert_command(cmd)

    def clone(self, another_database_object):
        raise NotImplementedError

    def restore(self, database_object):
        raise NotImplementedError

    def drop_db(self):
        raise NotImplementedError


class WindowsMySQLDatabase(MySQLDatabase):
    def clone(self, another_database_object):
        raise NotImplementedError

    def create_empty_database(self, new_database_name):
        raise NotImplementedError

    def drop_db(self):
        raise NotImplementedError

    def dump(self):
        raise NotImplementedError

    def restore(self, database_object):
        raise NotImplementedError