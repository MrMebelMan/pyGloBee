#!/usr/bin/env python3

from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))


setup(
    name='pyGloBee',

    version='1.0',

    description='Python3 package for GloBee payments API',
    long_description = """\
    This is a Python3 package that implements GloBee payments API
    """,

    url='https://github.com/MrMebelMan/pyGloBee',

    author='Vladyslav Burzakovskyy',
    author_email='burzakovskij@protonmail.com',

    license='MIT',

    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],

    packages=['globee', 'globee/resources'],

    install_requires=[],
)

