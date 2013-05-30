#-*- coding: utf-8 -*-

"""
    index.py [view]
    ~~~~~~~~
    Renders the view for the homepage.

    :copyright: (c) 2012 by Mek
    :license: BSD, see LICENSE for more details.
"""

import imaplib
from waltz import web, render, session
from api.v1.mail import Mailbox, Mailman, unescape_html

class Index:
    def GET(self):
        """Homepage which lists received emails / mailbox"""
        i = web.input(response="")
        if getattr(session(), 'passwd', None):            
            raise web.seeother('/emails?page=0&limit=10')
        raise web.seeother('/login')

class Email:
    def GET(self, uid=None):
        i = web.input(page=0, limit=10) 
        if getattr(session(), 'passwd', None):
            mail = Mailbox(session().email, session().passwd, session().imap)
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
            mail = Mailbox(session().email, session().passwd, session().imap)

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


