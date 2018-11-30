#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Install the "polevault" package and CLI command.'''


from __future__ import print_function, division

from setuptools import setup, find_packages


VERSION = '0.1.0'

setup(
    name='fonts2css',
    version=VERSION,
    author='Paulo Lopes',
    author_email='palopes@cisco.com',
    url='https://paulopes.github.io/fonts2css',
    description='Encrypts and decrypts credentials',
    long_description='''\
Encrypts and decrypts credentials, stores them
in a .ini, .conf, .json, .yml, or .yaml file,
and can decrypt them into Hashicorp's Vault.
''',
    packages=find_packages(exclude=[
        "*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'fonts2css = fonts2css:main',
        ]
    },
)
