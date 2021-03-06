# coding=utf-8
import logging
import subprocess

__author__ = 'jbean'

logger = logging.getLogger(name='root')


class CommandError(Exception):
    pass


def assert_command(command):
    """
        Simple command runner with some logging around it.
        Assert means we raise an error when any error occurs.

    @param command:  The command to be run
    @type command: str
    @raise CommandError
    """
    logger.debug('Command given: {}'.format(command))
    child = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    (stdoutdata, stderrdata) = child.communicate()
    logger.debug('Out:  {}'.format(stdoutdata))
    logger.debug('Err:  {}'.format(stderrdata))
    if child.returncode:
        raise CommandError('Command failed with exit status {}'.format(child.returncode))
    logger.debug('Finished running command.')