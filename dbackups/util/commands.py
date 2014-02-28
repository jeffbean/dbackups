import logging
import subprocess

__author__ = 'jbean'

logger = logging.getLogger()


class CommandError(Exception):
    pass


def assert_command(command):
    logger.debug('Command given: {}'.format(command))
    print(command)
    child = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    (stdoutdata, stderrdata) = child.communicate()
    logger.debug('Out:  {}'.format(stdoutdata))
    logger.debug('Err:  {}'.format(stderrdata))
    if child.returncode:
        raise CommandError('Command failed with exit status {}'.format(child.returncode))
    logger.debug('Finished running command.')