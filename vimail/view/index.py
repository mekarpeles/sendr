#-*- coding: utf-8 -*-
"""
    index.py [view]
    ~~~~~~~~

    Renders the view for the homepage.

    :copyright: (c) 2012 by Mek
    :license: BSD, see LICENSE for more details.
"""

import web

from model.v1.mail import Mail

render = lambda: web.ctx.session['render']

class Index:
    def GET(self):
        return render().index()

    def POST(self):
        i = web.input(email=None, passwd=None)
        m = Mail(i.email, i.passwd)        
        return render().ui(emails=m.newest(limit=10, offset=None))

