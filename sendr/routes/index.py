#-*- coding: utf-8 -*-

"""
    index.py [view]
    ~~~~~~~~
    Renders the view for the homepage.

    :copyright: (c) 2012 by Mek
    :license: BSD, see LICENSE for more details.
"""

from waltz import web, render, session

class Index:
    def GET(self):
        """Homepage which lists received emails / mailbox"""
        i = web.input(response="")
        if getattr(session(), 'passwd', None):            
            raise web.seeother('/emails?page=0&limit=10')
        raise web.seeother('/login')
