#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from setuptools import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
changelog = open('CHANGELOG.rst').read().replace('.. :changelog:', '')

try:
    from pip.req import parse_requirements
except ImportError:
    print('pip is required in order to install this package')
    sys.exit(1)

install_reqs = parse_requirements('requirements.txt')
reqs = [str(ir.req) for ir in install_reqs]

config = {
    'name': 'testdoubles',
    'version': '0.1.0',
    'description': 'testdoubles is a library that provides testdoubles.',
    'long_description': readme + '\n\n' + changelog,
    'author': 'Omer Katz',
    'author_email': 'omer.drow@gmail.com',
    'url': 'https://github.com/testsuite/testdoubles',
    'packages': [
        'testdoubles',
    ],
    'package_dir': {'testdoubles': 'testdoubles'},
    'include_package_data': True,
    'install_requires': reqs,
    'setup_requires': ['setuptools'],
    'test_suite': 'nose2.collector.collector',
    'license': 'BSD3',
    'zip_safe': False,
    'keywords': 'testdoubles',
    'classifiers': [
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Topic :: Software Development',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
}

setup(
    **config
)