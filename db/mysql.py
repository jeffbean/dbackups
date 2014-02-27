# coding=utf-8
import logging

from fabric.operations import local

from db.database import Database


__author__ = 'jbean'

logger = logging.getLogger()


class MySQLDatabase(Database):
    def create_empty_database(self, new_database_name):
        pass

    def dump(self):
        """
            /usr/bin/pg_dump -h db1 -U postgres jiradb2 -f $BKROOT.$SUF -F c --oids
            >>$LOGFILE 2>&1
            """
        logger.info('Dumping database to file: [{}]'.format(self.dump_file))
        cmd = '/usr/bin/mysqldump -h {host} -P {port} -u {user} -p{passwd} {dbname} > {file}'.format(
            host=self.db_host, port=self.db_port,
            passwd=self.db_pass, user=self.db_user,
            dbname=self.db_name, file=self.dump_file)

        local(cmd)

    def clone(self, another_database_object):
        pass

    def restore(self, database_object):
        pass

    def drop_db(self):
        pass