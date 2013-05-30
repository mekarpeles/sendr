#-*- coding: utf-8 -*-

"""
    sendr
    ~~~~~

    Setup
    `````

    $ pip install -e .
"""

import os
from distutils.core import setup

setup(
    name='sendr',
    version='0.0.11',
    url='http://github.com/mekarpeles/sendr',
    author='mek',
    author_email='michael.karpeles@gmail.com',
    packages=[
        'sendr',
        'sendr/test',
        'sendr/model',
        'sendr/model/v1',
        'sendr/subapps'
        ],
    platforms='any',
    license='LICENSE',
    install_requires=[
        'waltz >= 0.1.7',
        'lepl >= 5.1.3',
    ],
    description="Sendr semantic email client",
    long_description=open(os.path.join(os.path.dirname(__file__),
                                       'README.md')).read(),
)
