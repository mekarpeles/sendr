#-*- coding: utf-8 -*-
"""
    index.py [view]
    ~~~~~~~~

    Renders the view for the homepage.
    :copyright: (c) 2012 by Mek
    :license: BSD, see LICENSE for more details.
"""

import web
import imaplib
from model.v1.mail import Mail
from mightymail_stdlib.api.v1.mail import Mailer

render = lambda: web.ctx.session['render']
slender = lambda: web.ctx.session['slender']
session = lambda: web.ctx.session['session']

class Index:
    def GET(self):
        i = web.input(response="")
        if getattr(session(), 'passwd', None):            
            raise web.seeother('/emails')
        return slender().login()

    def POST(self):
        i = web.input(email=None, passwd=None)
        session().email = i.email
        session().passwd = i.passwd
        mail = Mail(session().email, session().passwd)
        return render().ui(emails=mail.newest(limit=10, offset=None))

class Email:
    def GET(self, uid=None):
        if getattr(session(), 'passwd', None):
            mail = Mail(session().email, session().passwd)
            if uid:
                return render().email(uid, email=mail.read(uid))
            return render().ui(emails=mail.newest(limit=10, offset=None))        
        raise web.seeother('/')

class Reply:
    def GET(self):
        pass

class Compose:
    def GET(self, uid=None):
        return render().compose()

    def POST(self):
        i = web.input(to="", cc="", bcc="",
                      subject="", message="")
        resp = "success"
        return i.to, session().email, i.bcc, i.cc, i.subject, i.message
        try:
            mailman = Mailer()
            mailman.sendmail(sender=session().email, subject=i.subject,
                             recipients=[i.to], msg=i.message)
        except Exception as e:
            return e
            resp = "failure"
            
        raise web.seeother(web.ctx.homedomain + '?response=' + resp)

class Logout:
    def GET(self):
        del session().email
        del session().passwd
        session().start()
        session().kill()
        raise web.seeother('/')

class Test:
    def GET(self):
        return render().test()
