#-*- coding: utf-8 -*-
"""
    main.py
    ~~~~~~~

    This module is run from the command line and triggers the start of
    the mail-client server

    :copyright: (c) 2012 by Mek
    :license: BSD, see LICENSE for more details.
"""

from waltz import web, setup
from configs.config import SERVER
from configs.config import db

urls = ('/compose/?', 'routes.index.Compose',
        '/emails/(.+)', 'routes.index.Email',
        '/emails/?', 'routes.index.Email',
        '/login/?', 'routes.auth.Login',
        '/logout/?', 'routes.auth.Logout',
        '/contacts/(.+)/?', 'routes.index.Contacts',
        '/contacts/?', 'routes.index.Contacts',
        '/tagemail/?', 'routes.index.TagEmail',
        '/tagemail/(.+)', 'routes.index.TagEmail',
        '/', 'routes.index.Index')

app = setup.dancefloor(urls, globals())
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


default_session = { 'logged': False,
                    'email': None,
                    'passwd': None,
                    'admin': False,
                    }
app.add_processor(web.loadhook(session_hook))

storage_method = web.session.DiskStore(SERVER['APP_PATH'] + '/sessions')
#storage_method = web.session.DBStore(db, 'sessions')
session = web.session.Session(app, storage_method, initializer=default_session)

# ==================
# Template Renderers
# ==================
globs = {'ctx': web.ctx,
         'session': session,
         'len': len,
         }

slender = web.template.render(SERVER['APP_PATH'] + '/templates/',
                              globals=globs)
render  = web.template.render(SERVER['APP_PATH'] + '/templates/',
                              base='layout', globals=globs)

if __name__ == "__main__":
    app.run()

