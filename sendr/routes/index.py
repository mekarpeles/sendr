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
from model.v1.mail import contextio
from stdlib.api.v1.mail import Mailer

render = lambda: web.ctx.session['render']
slender = lambda: web.ctx.session['slender']
session = lambda: web.ctx.session['session']

class Index:
    def GET(self):
        i = web.input(response="")
        if getattr(session(), 'passwd', None):            
            raise web.seeother('/emails?page=0&limit=10')
        raise web.seeother('/login')

class Email:
    def GET(self, uid=None):
        i = web.input(page=0, limit=10) 
        if getattr(session(), 'passwd', None):
            mail = Mail(session().email, session().passwd, session().imap)
            if uid:
                return render().email(uid, email=mail.read(uid))
            page, limit = int(i.page), int(i.limit)
            offset = page * limit
            emails = mail.newest(limit=limit, offset=offset)
            return render().ui(emails=emails, page=page, limit=limit)
        raise web.seeother('/')

class TagEmail:
    def GET(self, uid=None):
        if getattr(session(), 'passwd', None):
            mail = Mail(session().email, session().passwd, session().imap)

            # If multiple email ids were specified, load emails into array
            i = web.input(uid_list=uid)
            uid_list = i.uid_list.split(",")
            if uid_list != "":
                email_list = []
                for single_uid in uid_list:
                    email_list.append(mail.read(single_uid))
                return render().email(uid_list[0], email_list=email_list)
            inbox = render().ui(emails=mail.newest(limit=10, offset=None))
            return inbox
        raise web.seeother('/')

class Reply:
    def GET(self):
        pass

class Compose:
    def GET(self, uid=None):
        return render().compose()

    def POST(self):
        i = web.input(to="", cc="", bcc="", subject="", tags="", message="")
        resp = "success"
        try:            
            message = "%s [%s]" % (i.message, i.tags)
            mailman = Mailer()
            mailman.sendmail(sender=session().email, subject=i.subject,
                             recipients=[i.to], msg=message)
        except Exception as e:
            return e
            resp = "failure"
        raise web.seeother(web.ctx.homedomain + '?response=' + resp)

class Test:
    def GET(self):
        return contextio()

