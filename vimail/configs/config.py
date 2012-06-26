#-*- coding: utf-8 -*-
"""
    config.py
    ~~~~~~~~~

    This module is the middle man for handling/consolidating
    configurations for the Dungeons project.

    :copyright: (c) 2012 by Mek
    :license: BSD, see LICENSE for more details.
"""

import web
import io
import os
import ConfigParser


config = ConfigParser.ConfigParser()

# *.cfg are unversioned files which, if don't exist, have default
# *_default.cfg fils containing default values

# SERVER variables
if os.path.isfile('configs/server.cfg'):
    config.read('configs/server.cfg')
else:
    config.read('configs/server_default.cfg')
SERVER = {'DEBUG_MODE': bool(config.get("server", "debug")),
          'APP_PATH': os.getcwd() 
          }

# DB variables
if os.path.isfile('configs/db.cfg'):
    config.read('configs/db.cfg')
    USER = config.get("mysql", "user")
    HOST = config.get("mysql", "host")    
    PASSWD = config.get("mysql", "passwd")
    DB = config.get("mysql", "db")
    db = web.database(host=HOST, dbn="mysql", db=DB,
                      user=USER, pw=PASSWD)
else:
    db = None

if os.path.isfile('configs/oauth2.cfg'):
    config.read('configs/oauth2.cfg')
    FB_TOKEN_KEY = config.get("fb", "TOKEN_KEY")
    FB_TOKEN_SECRET = config.get("fb", "TOKEN_SECRET")



