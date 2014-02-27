# coding=utf-8
from setuptools import setup, find_packages

__author__ = 'jbean'

setup(
    name='dbackups',
    version='1.0',
    packages=find_packages(),
    requires=open('requirements.txt').read()
)