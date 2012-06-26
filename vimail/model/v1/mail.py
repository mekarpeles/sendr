#-*- coding: utf-8 -*-
"""
    mail.py [model.v1]
    ~~~~~~~
    Contains all of the logic for retrieving and organizing emails

    :copyright: (c) 2012 by Mek
    :license: BSD, see LICENSE for more details.
"""

import imaplib
from mightymail_stdlib.utils.util import objectify_email

class Mail(object):

    def __init__(self, email, passwd):
        self.mail = imaplib.IMAP4_SSL('imap.gmail.com')        
        self.email = email
        self.login(email, passwd)
        self.switch()

    def __getstate__(self):
        return self.__dict__.copy()

    def login(self, email, passwd):
        self.mail.login(email, passwd)

    def folders(self):
        """list of "folders" aka labels in gmail."""
        return self.mail.list()

    def switch(self, box="inbox"):
        self.mail.select("inbox") # connect to inbox.        

    @property
    def uids(self):
        """Returns all the uids associated with a folder/box"""
        result, data = self.mail.uid('search', None, "ALL")
        uids = data[0].split()
        return uids

    def read(self, uid):
        result, data = self.mail.fetch(uid, "(RFC822)")
        if not data == [None]:
            raw_email = data[0][1] # email body, raw text of email            
            email = objectify_email(raw_email)
            email['Content'] = self.email_body(email)
            email['Uid'] = uid
            return email

    def newest(self, limit=25, offset=0):
        """fetch email body (RFC822) for a set of uids based on
        the current box, the limit, and the offset"""
        results = []
        uids = self.paginate(self.uids[::-1], limit, offset)
        for ii, uid in enumerate(uids):
            result, data = self.mail.fetch(uid, "(RFC822)")
            if not data == [None]:
                raw_email = data[0][1] # email body, raw text of email
                email = objectify_email(raw_email)
                email['Content'] = self.email_body(email)
                results.append({"uid": uid,
                                "index": ii,
                                "email": email,
                               })
            if len(results) == limit:
                return results                
        return results

    @classmethod
    def paginate(cls, uids, limit, offset):
        if offset:
            if offset > len(uids):
                return []
            return uids[offset:]
        return uids
        #if not limit or limit > len(uids):
        #    return uids
        #return uids[:limit]

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
