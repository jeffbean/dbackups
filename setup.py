# coding=utf-8
import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages

__author__ = 'jbean'

setup(
    name='dbackups',
    version='0.5.2',
    description='A simple python application that makes database backups a little easier.',
    url='https://pypi.python.org/pypi/dbackups',
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    author='Jeffrey Bean',
    author_email='jrb3330@gmail.com',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'dbackupscron = bin.backup_cron:main',
        ],
    },
    exclude_package_data={'': ['.gitignore']},
    install_requires=open('requirements.txt').read(),
    setup_requires=open('setup_requirements.txt').read(),
    zip_safe=False,
)