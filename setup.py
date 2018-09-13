#!/usr/bin/env python3
# coding: UTF-8

import os

from setuptools import setup, Command

root = os.path.abspath('.')
current_dir = os.path.dirname(__file__)


def read_file(file_name):
    with open(os.path.join(current_dir, file_name), 'r') as file:
        return file.read()

README = read_file('README.rst')
VERSION = read_file('VERSION')


class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info ./eggs')

test_deps = [
    'coverage',
    'pytest',
    'pytest-runner',
    'pytest-cov'
]

extras = {
    'test': test_deps,
}

setup(
    name                    = 'estnin',
    version                 = VERSION,
    url                     = 'https://github.com/antirais/estnin',
    py_modules              = ['estnin'],
    license                 = 'MIT',
    include_package_data    = True,
    author                  = 'Anti Räis',
    author_email            = 'antirais@gmail.com',
    description             = 'library for handling Estonian national identity numbers',
    long_description        = README,
    test_suite              = 'tests',
    tests_require           = test_deps,
    extras                  = {'test': test_deps},
    classifiers             = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    cmdclass = {
        'clean': CleanCommand,
    },
)
