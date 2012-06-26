#-*- coding: utf-8 -*-
"""
    main.py
    ~~~~~~~

    This module is run from the command line and triggers the start of
    the mail-client server

    :copyright: (c) 2012 by Mek
    :license: BSD, see LICENSE for more details.
"""

import web
from reloader import PeriodicReloader
from configs.config import SERVER
from configs.config import db

urls = ('/compose/?', 'view.index.Compose',
        '/emails/(.+)', 'view.index.Email',
        '/emails/?', 'view.index.Email',
        '/test/?', 'view.index.Test',
        '/logout/?', 'view.index.Logout',
        '/contacts/(.+)/?', 'view.index.Contacts',
        '/contacts/?', 'view.index.Contacts',
        '/', 'view.index.Index')

app = web.application(urls, globals(), autoreload=False)
application = app.wsgifunc()

# ======================
# Session Initialization
# ======================
def session_hook():
    web.ctx.session = {"session": session,
                       "render": render,
                       "slender": slender,
                       }

def initialize_session(app, storage_method):
    session = web.session.Session(app, storage_method, initializer=get_default_session)
    return session

def get_default_session(webpy_sess):
    # TODO: User really should be a class
    default_session = { 'logged': False,
                        'email': None,
                        'passwd': None,
                        'admin': False,
                        }
    webpy_sess.update(default_session)

app.add_processor(web.loadhook(session_hook))

storage_method = web.session.DiskStore(SERVER['APP_PATH'] + '/sessions')
#storage_method = web.session.DBStore(db, 'sessions')
session = initialize_session(app, storage_method)

# ==================
# Template Renderers
# ==================
globs = {'ctx': web.ctx,
         'session': session,
         'len': len,
         }

slender = web.template.render(SERVER['APP_PATH'] + '/templates/', globals=globs)
render  = web.template.render(SERVER['APP_PATH'] + '/templates/', base='layout', globals=globs)

if __name__ == "__main__":
    if SERVER['DEBUG_MODE']:
        PeriodicReloader()
    app.run()

