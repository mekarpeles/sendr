
#-*- coding: utf-8 -*-

"""
    test_routes
    ~~~~~~~~~~~

    Test that waltz application runs correctly and that sendr routes
    load as expected.

    :copyright: (c) 2012 by Mek
    :license: BSD, see LICENSE for more details.
"""

import unittest
from paste.fixture import TestApp as Sendr
from nose.tools import *
from main import app

class TestIndex(unittest.TestCase):

    def test_index(self):
        middleware = []
        sendr = Sendr(app.wsgifunc(*middleware))
        r = sendr.get('/')
        self.assertTrue(r.status == 303, "Expected 303 Response, " \
                            "(redir to /login) instead got: %s" % r.status)

class TestAuth(unittest.TestCase):

    def test_login(self):
        middleware = []
        sendr = Sendr(app.wsgifunc(*middleware))
        r = sendr.get('/login')
        self.assertTrue(r.status == 200, "Expected 200 Response, " \
                            "instead got: %s" % r.status)
        r.mustcontain('Welcome!')

    def test_logout(self):
        middleware = []
        sendr = Sendr(app.wsgifunc(*middleware))
        r = sendr.get('/logout')
        self.assertTrue(r.status == 303, "Expected 303 Response, " \
                            "(redir from /logout to /) " \
                            "instead got: %s" % r.status)
        self.assertTrue(r.normal_body == "", "No content expected at /, " \
                            "instead got: %s" % r.normal_body)
