#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
    main.py
    ~~~~~~~

    This module is run from the command line and triggers the start of
    the mail-client server

    :copyright: (c) 2012 by Mek
    :license: BSD, see LICENSE for more details.
"""

import waltz
from configs.config import SERVER

urls = ('/compose/?', 'routes.email.Compose',
        '/emails/(.+)', 'routes.email.Read',
        '/emails/?', 'routes.email.Inbox',
        '/login/?', 'routes.auth.Login',
        '/logout/?', 'routes.auth.Logout',
        '/', 'routes.index.Index')

# Default values for new client sessions
session_defaults = {'logged': False,
                    'email': None,
                    'passwd': None,
                    'admin': False,
                    }

# Make the following variable and methods available for use within the
# html templates)
env = {'ctx': waltz.web.ctx,
       'session': waltz.session,
       'len': len,
       }

app = waltz.setup.dancefloor(urls, globals(), sessions=session_defaults, env=env,
                             debug=SERVER['DEBUG_MODE'])

if __name__ == "__main__":
    app.run()

