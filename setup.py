#-*- coding: utf-8 -*-

"""
    sendr
    ~~~~~

    Setup
    `````

    $ pip install -e .
"""

from distutils.core import setup

setup(
    name='sendr',
    version='0.0.1',
    url='http://github.com/mekarpeles/sendr',
    author='mek',
    author_email='michael.karpeles@gmail.com',
    packages=[
        'sendr',
        'test'
        ],
    platforms='any',
    license='LICENSE',
    install_requires=[
        'waltz >= 0.1.64',
        'lepl >= 5.1.3',
    ],
    description="Sendr semantic email client",
    long_description=open('README.md').read(),
)