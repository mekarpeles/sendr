#-*- coding: utf-8 -*-
"""
    mail.py [model.v1]
    ~~~~~~~
    Contains all of the logic for retrieving and organizing emails

    :copyright: (c) 2012 by Mek
    :license: BSD, see LICENSE for more details.
"""

import imaplib
from stdlib.utils.util import objectify_email

RFC = {"imap.gmail.com": "822",
       "imap.mail.yahoo.com": "822"
       }

class Mail(object):

    def __init__(self, email, passwd, imap='imap.gmail.com'):
        self.imap = imap
        self.mail = imaplib.IMAP4_SSL(self.imap)
        self.email = email
        self.login(email, passwd)
        self.count = self.switch()[1]

    def __getstate__(self):
        return self.__dict__.copy()

    def login(self, email, passwd):
        self.mail.login(email, passwd)

    def folders(self):
        """list of "folders" aka labels in gmail."""
        return self.mail.list()

    def switch(self, box="inbox"):
        """connect to inbox"""
        status, count = self.mail.select("inbox")
        return status, count

    @property
    def uids(self):
        """Returns all the uids associated with a folder/box"""
        result, data = self.mail.uid('search', None, "ALL")
        uids = data[0].split()
        return uids

    def read(self, uid):
        result, data = self.mail.fetch(uid, "(RFC%s)" % RFC[self.imap])
        if not data == [None]:
            raw_email = data[0][1] # email body, raw text of email            
            email = objectify_email(raw_email)
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
            # no Tags were found
            return raw_body, None

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
                    email = objectify_email(raw_email)
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

