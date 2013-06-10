#-*- coding: utf-8 -*-

"""
    routes.email
    ~~~~~~~~~~~~

    Email routes for displaying inbox and reading + composing email

    :copyright: (c) 2012 by Mek
    :license: BSD, see LICENSE for more details.
"""

from waltz import web, session, render
from api.v1.mail import Mailman, Mailbox

class Read:
    def GET(self, uid=None):
        i = web.input(page=0, limit=10)
        if getattr(session(), 'passwd', None) and uid:
            mail = Mailbox()
            if uid:
                return render().email(uid, email=mail.read(uid))
        raise web.seeother('/')

class Inbox:
    def GET(self):
        i = web.input(page=0, limit=10)
        if getattr(session(), 'passwd', None):
            mail = Mailbox()
            page, limit = int(i.page), int(i.limit)
            offset = page * limit
            emails = mail.newest(limit=limit, offset=offset)
            return render().ui(emails=emails, page=page, limit=limit)
        raise web.seeother('/')

class Compose:
    def GET(self, uid=None):
        if getattr(session(), 'passwd', None):
            return render().compose()
        raise web.seeother('/')

    def POST(self):
        i = web.input(to="", cc="", bcc="", subject="", tags="", message="")
        if not getattr(session(), 'passwd', None):
            raise web.seeother('/')
        resp = "success"
        try:            
            if 'passwd' in session() and session().passwd:
                message = unescape_html("%s [%s]" % (i.message, i.tags) \
                                            if i.tags else i.message)
                mailman = Mailman(session()['email'], session()['passwd'])
                mailman.sendmail(sender=session().email, subject=i.subject,
                                 recipients=[i.to], msg=message, fmt="html")
            else:
                raise Exception("Email not sent, account credentials " \
                                    "could not be verified.")
        except Exception as e:
            return e
            resp = "failure"
        raise web.seeother(web.ctx.homedomain + '?response=' + resp)
