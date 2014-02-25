import logging
import logging.config
import os
import time

__author__ = 'jbean'

logging_config = os.path.abspath(os.path.join(os.path.dirname(__file__), 'config', 'logging.ini'))
logging.config.fileConfig(logging_config)


class DBBackupDaemon(object):
    def __init__(self):
        self.stop = False

    def stop_run(self):
        self.stop = True

    def run(self):
        if not self.stop:
            logging.info('some things are going on')
            time.sleep(2)
        else:
            logging.info('we are going to stop now')

    logging.info('testing the service here')


if __name__ == '__main__':
    service = DBBackupDaemon()
    service.run()
