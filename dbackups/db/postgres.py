# coding=utf-8
import logging

import os

from dbackups.db.database import Database
from dbackups.util.commands import assert_command


__author__ = 'jbean'


class PostgresDatabase(Database):
    """
    A postgres database object representation for backups.
    """
    def __init__(self, db_host, db_name, db_user, db_pass, db_port=5432):
        Database.__init__(self, db_host, db_name, db_user, db_pass, db_port)

    def restore(self, database_object, latest_file=False):
        """
        Restores the dump file from another database objects dump file.
        This can be the same database with a different DB name.

        @param database_object A postgres database object that has a dump file.
        @type database_object PostgresDatabase
        """
        Database.restore(self, database_object, latest_file)
        if latest_file:
            self.dump_file = self.find_latest_dump()
        logging.info('Restoring {} to database {}'.format(database_object.dump_file, database_object.db_name))
        cmd = '/usr/bin/pg_restore --host {h} --port {p} --username ' \
              '"{u}" --dbname "{db}" --no-password ' \
              '"{dump_file}"'.format(h=database_object.db_host, p=database_object.db_port, u=database_object.db_user,
                                     db=database_object.db_name, dump_file=self.dump_file)
        assert_command(cmd)

    def create_empty_database(self, new_database_name):
        Database.create_empty_database(self, new_database_name)
        cmd = 'createdb -U {} {}'.format('postgres', new_database_name)
        assert_command(cmd)

    def drop_db(self):
        """
        BEWARE DATA WILL GO BYE BYE

        drop the database. This is meant for the clone feature that is coming. (you cant clone into a DB that already
        exists.)
        """
        Database.drop_db(self)
        cmd = 'dropdb --host {h} -p {p} -U {u} {db} --if-exists'.format(
            h=self.db_host, p=self.db_port, u=self.db_user, db=self.db_name)
        assert_command(cmd)

    def dump(self):
        """
        Implementation of postgresql dump command.

        /usr/bin/pg_dump -h <host> -U <user>  -f <filename> <database_name> -F c --oids
        """
        logging.info('Dumping database to file: [{}]'.format(self.dump_file))
        cmd = '/usr/bin/pg_dump -h {host} -p {port} -U {user} {dbname} -f {file} ' \
              '-F c --oids'.format(host=self.db_host, port=self.db_port,
                                   user=self.db_user, dbname=self.db_name, file=self.dump_file)

        assert_command(cmd)

    def create_pg_pass_file(self):
        """
        Creates the pgpass file in your home dir for re-use and no password prompts

        http://www.postgresql.org/docs/8.1/static/libpq-pgpass.html
        """
        logging.info('Writing a pgpass file for connections to the PGDB.')
        pg_line = '{}:{}:{}:{}:{}'.format(self.db_host, self.db_port, self.db_name, self.db_user, self.db_pass)
        logging.debug(pg_line)
        pg_pass_file = os.path.normpath(os.path.join(os.getenv('HOME'), '.pgpass'))

        with open(pg_pass_file, 'w') as pass_file:
            pass_file.write(pg_line)

        logging.debug('Chmod-ing the file to 600 as per postgres docs.')
        os.chmod(pg_pass_file, 0600)


class WindowsPostgresDatabase(Database):
    def dump(self):
        #TODO: Finish implementing the Windows Dump exe path issue. (In docs for now)
        logging.info('Dumping database to file: [{}]'.format(self.dump_file))
        cmd = 'pg_dump.exe -h {host} -p {port} -U {user} -f {file} ' \
              '-F c --oids --verbose {dbname}'.format(host=self.db_host, port=self.db_port,
                                                      user=self.db_user, dbname=self.db_name, file=self.dump_file)

        assert_command(cmd)

    def drop_db(self):
        raise NotImplementedError

    def restore(self, database_object, latest_file=False):
        raise NotImplementedError

    def create_empty_database(self, new_database_name):
        raise NotImplementedError
