#-*- coding: utf-8 -*-

"""
    email.py [view]
    ~~~~~~~~
    Renders inbox view + renders email messages

    :copyright: (c) 2012 by Mek
    :license: BSD, see LICENSE for more details.
"""

from waltz import web, render, session
from api.v1.mail import Mailbox, Mailman, unescape_html

class Read:
    def GET(self, uid=None):
        i = web.input(page=0, limit=10)
        m = Mailbox()
        if uid:
            return render().email(uid, email=m.read(uid))
        raise web.notfound()

class Inbox:
    def GET(self):
        i = web.input(page=0, limit=10)
        m = Mailbox()
        if getattr(session(), 'passwd', None):
            page, limit = int(i.page), int(i.limit)
            offset = page * limit
            emails = m.newest(limit=limit, offset=offset)
            return render().ui(emails=emails, page=page, limit=limit)
        raise web.seeother('/login')

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
            if 'passwd' in session() and session().passwd:
                tags = [str('#%s' % tag.strip()) if tag[0] != '#' else str(tag.strip()) \
                            for tag in i.tags.split(',')]
                message = unescape_html("%s %s" % (i.message, tags) if tags else i.message)
                return message
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


