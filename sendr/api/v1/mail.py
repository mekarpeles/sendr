#-*- coding: utf-8 -*-
"""
    mail.py [model.v1]
    ~~~~~~~

    Contains logic for retrieving, organizing, and sending emails.

    :copyright: (c) 2012 by Mek
    :license: BSD, see LICENSE for more details.
"""

import imaplib
import smtplib
import requests
import xml.sax.saxutils as saxutils
from email.mime.multipart import MIMEMultipart
from email.MIMEText import MIMEText
from email import Encoders, message_from_string
from waltz import session
from configs.config import MAIL_API

RFC = {"imap.gmail.com": "822",
       "imap.mail.yahoo.com": "822"
       }

def unescape_html(x):
    return saxutils.unescape(x)

class Server(object):
    def __init__(self, email, passwd, imap='imap.gmail.com'):
        self.imap = imap
        self.mail = imaplib.IMAP4_SSL(self.imap)
        self.email = email
        self.login(email, passwd)
        self.count = self.switch()[1]

    def __getstate__(self):
        return self.__dict__.copy()

    @classmethod
    def objectify_email(cls, raw_email):
        """Turns email raw string into an email object"""
        return message_from_string(raw_email)

    def login(self, email, passwd):
        self.mail.login(email, passwd)

    def folders(self):
        """list "folders" aka labels in gmail."""
        return self.mail.list()

    def switch(self, box="inbox"):
        """Switch mailboxes, e.g. connect to inbox"""
        status, count = self.mail.select("inbox")
        return status, count

    def _uids(self, uids="ALL", limit=10):
        """Returns all the mail uids (unique identifiers) associated
        with a folder/box"""
        result, data = self.mail.uid('search', None, uids)[:limit]
        uids = data[0].split()
        return uids

    @property
    def uids(self):
        return self._uids()

    def read(self, uid):
        """
        """
        result, data = self.mail.fetch(uid, "(RFC%s)" % RFC[self.imap])
        if not data == [None]:
            raw_email = data[0][1] # email body, raw text of email            
            email = self.objectify_email(raw_email)
            email['Uid'] = uid
            email['Content'], email['Tags'] = \
                self.parse_email_body(self.email_body(email))
            return email

    def parse_email_body(self, raw_body):
        """Separate body and tag, and return two values:
        1. the updated body (with tags removed), and
        2. a list of updated body with parsed tags.

        Tags are represented at the end of the email (after all content and
        signatures), and are delimiated using square brackets.
        e.g.: [#tag1 #tag2 #tag3] => [ "tag1", "tag2", "tag3" ]
        e.g.: [#multiple word tag #tag2] => [ "multiple word tag", "tag2" ]
        """

        try:
            # Reverse split, seeking tag header
            parsed_body = raw_body.rsplit("[#", 1)
        except:
            return []

        if len(parsed_body) == 1:
            print "foo"
            # no Tags were found
            return raw_body, []

        # Remove trailing square bracket, if present
        tag_string = parsed_body[-1]
        # Removing trailing square bracket
        tag_string = tag_string.split("]", 1)[0]
        tag_list = tag_string.split(" #")

        return parsed_body[0], tag_list

    def newest(self, limit=25, offset=0):
        """fetch email body (RFC???) for a set of uids based on
        the current box, the limit, and the offset"""
        results = []
        for ii, uid in enumerate(self.uids[::-1]):
            result, data = self.mail.fetch(uid, "(RFC%s)" % RFC[self.imap])
            if not data == [None]:
                if offset:
                    offset-=1
                else:
                    raw_email = data[0][1] # email body, raw text of email
                    email = self.objectify_email(raw_email)
                    email['Content'] = self.email_body(email)
                    results.append({"uid": uid,
                                    "index": ii,
                                    "email": email,
                                    })
                    if limit and len(results) == limit:
                        return results
        return results

    @classmethod
    def email_body(cls, email_message_instance):
        """note that if you want to get text content (body) and the
        email contains multiple payloads (plaintext/ html), you must
        parse each message separately.  use something like the
        following: (taken from a stackoverflow post)
        """
        maintype = email_message_instance.get_content_maintype()
        if maintype == 'multipart':
            for part in email_message_instance.get_payload():
                if part.get_content_maintype() == 'text':
                    return part.get_payload()
        elif maintype == 'text':
            return email_message_instance.get_payload()

class Mailbox(Server):
    def __init__(self):
        super(Mailbox, self).__init__(session().email, session().passwd, session().imap)

class Mailman(object):
    """Send mail via smtp (default gmail) or mailgun
    usage:
    >>> from api.v1.mail import Mailer
    >>> mailman = Mailer('mekarpeles@gmail.com', '********')
    >>> mailman.sendmail(mailman.email, recipients=['michael.karpeles@gmail.com'],
    ...                  subject='foobarbaz', msg='<b>test</b>', fmt="html")
    {}
    """

    def __init__(self, email, passwd, host='smtp.gmail.com', port=587):
        self.email = email
        self.server = smtplib.SMTP(host, port)
        self.server.ehlo()
        self.server.starttls()
        self.server.ehlo()
        self.server.login(email, passwd)

    def sendmail(self, sender, recipients='', subject="", msg="",
                 fmt="", method="smtp"):
        func = getattr(self, method, method)
        return func(sender, recipients, subject=subject, msg=msg, fmt=fmt)

    def smtp(self, sender, recipients='', subject="", msg="",
             fmt="", attatchment=None):
        mail = MIMEText() if not fmt else MIMEMultipart('alternative')
        mail['From'] = sender
        mail['To'] = ', '.join(recipients)
        mail['Subject'] = subject
        if not fmt:
            mail.attach(MIMEText(msg, 'plain'))
        else:
            mail.attach(MIMEText(msg, 'html'))
        return self.server.sendmail(sender, recipients, mail.as_string())

    @classmethod
    def mailgun(cls, sender, recipients='', subject="", msg="", fmt="text"):
        """
        >>> from sendr_stdlib.api.v1.mail import Mailer;
        >>> r = Mailer.mailgun("email@org.com", subject="",
        ...                    recipients=["recipient@org.com"],
        ...                    msg="<p><strong>Salutations!</strong>" \
        ...                        "What's going on?</p>",
        ...                    fmt="html")
        >>> r.text
        u'{\n  "message": "Queued. Thank you.",\n
        "id": "<20120328062856.20096.24811@org.com>"\n}'        
        """
        r = requests.\
                 post((MAIL_API['url'] + MAIL_API['domain'] + "/messages"),
                      auth=("api", MAIL_API['key']),
                      data={"from": sender,
                            "to": recipients,
                            "subject": subject,
                            format: msg
                            }
                      )
        return r
