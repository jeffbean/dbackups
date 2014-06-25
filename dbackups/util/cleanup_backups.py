# coding=utf-8
import logging
import os
from pprint import pformat

__author__ = 'jbean'


def find_files_for_delete(base_directory, db_host, db_name, number_to_keep=5):
    """

    @param base_directory: The path to list out the files to find dump files in
    @type base_directory: str
    @param db_host: The name of the host that matches
    @type db_host:str
    @param db_name:
    @type db_name: str
    @return: A list of directories that we can remove to save space.
    @rtype: list
    """
    dump_dir = os.path.abspath(base_directory)
    starts_with_string = '{}-{}'.format(db_host, db_name)
    files = [os.path.join(dump_dir, f) for f in os.listdir(dump_dir)
             if os.path.isfile(os.path.join(dump_dir, f)) and
                f.startswith(starts_with_string)]
    sorted_files = sorted(files, key=os.path.getctime, reverse=True)
    if sorted_files:
        logging.debug('Found list of dumps that match the database.')
        logging.debug(pformat(sorted_files))
    else:
        logging.warning(
            'No files were found in dir: {} that start with [{}]'.format(base_directory, starts_with_string))
    return sorted_files[number_to_keep:]


def delete_file_list(file_list):
    for file_f in file_list:
        os.remove(file_f)