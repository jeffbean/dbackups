# coding=utf-8
import logging
import os

from fabric.operations import local

from db.database import Database


__author__ = 'jbean'


class PostgresDatabase(Database):
    def restore(self, database_object):
        """
        restores the dump file to the dev postgres server
        :param database_object:
        """
        Database.restore(self, database_object)
        cmd = '/usr/bin/pg_restore --host {h} --port {p} --username ' \
              '"{u}" --dbname "{db}" --no-password  --verbose ' \
              '"{dump_file}"'.format(h=database_object.db_host, p=database_object.db_port, u=database_object.db_user,
                                     db=database_object.db_name, dump_file=database_object.dump_file)
        local(cmd)

    def create_empty_database(self, new_database_name):
        Database.create_empty_database(new_database_name)

    def delete_local_db(self, database_name):
        """
        locally drop the database that you will be restoring to
        """
        Database.delete_local_db(database_name)
        cmd = 'dropdb --host {h} -p {p} -U {u} {db} --if-exists'.format(
            h=self.db_host, p=self.db_port, u=self.db_user, db=database_name)
        local(cmd)

    def dump(self):
        """
        /usr/bin/pg_dump -h db1 -U postgres jiradb2 -f $BKROOT.$SUF -F c --oids
        >>$LOGFILE 2>&1
        """
        logging.info('Dumping database to file: [{}]'.format(self.dump_file))
        cmd = '/usr/bin/pg_dump -h {host} -p {port} -U {user} {dbname} -f {file} ' \
              '-F c --oids --verbose'.format(host=self.db_host, port=self.db_port,
                                             user=self.db_user, dbname=self.db_name, file=self.dump_file)

        local(cmd)

    def create_pg_pass_file(self):
        """
        Creates the pgpass file in your home dir for re-use and no password
        prompts

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
        """

        """
        logging.info('Dumping database to file: [{}]'.format(self.dump_file))
        cmd = 'pg_dump.exe -h {host} -p {port} -U {user} -f {file} ' \
              '-F c --oids --verbose {dbname}'.format(host=self.db_host, port=self.db_port,
                                                      user=self.db_user, dbname=self.db_name, file=self.dump_file)

        local(cmd)

    def delete_local_db(self, database_name):
        pass

    def restore(self, database_object):
        pass

    def create_empty_database(self, new_database_name):
        pass
