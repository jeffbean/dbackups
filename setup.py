# coding=utf-8
from setuptools import setup, find_packages

__author__ = 'jbean'

setup(
    name='dbackups',
    version='1.0',
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    author='Jeffrey Bean',
    author_email='jeff.bean@hds.com',
    url='hds.com',
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