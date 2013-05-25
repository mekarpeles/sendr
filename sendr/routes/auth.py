#-*- coding: utf-8 -*-

"""
    auth.py [view]
    ~~~~~~~
    Handles views for user authentication including login,
    registration, and logout

    :copyright: (c) 2012 by Mek
    :license: BSD, see LICENSE for more details.
"""

from waltz import web, render, slender, session
from model.v1.mail import Mail

class Login:
    def GET(self):
        # XXX Force https
        return slender().login()

    def POST(self):
        i = web.input(email=None, passwd=None, imap="imap.gmail.com")
        session().email = i.email
        session().passwd = i.passwd
        session().imap = i.imap
        if getattr(session(), 'passwd', None):            
            raise web.seeother('/emails?page=0&limit=10')
        raise web.seeother('/login')

class Logout:
    def GET(self):
        try:
            del session().email
            del session().passwd
        except:
            pass
        session().kill()
        raise web.seeother('/')
