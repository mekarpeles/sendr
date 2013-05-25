#-*- coding: utf-8 -*-
"""
    config.py
    ~~~~~~~~~

    This module is the middle man for handling/consolidating
    configurations for the Sendr mail client.

    :copyright: (c) 2012 by Mek
    :license: BSD, see LICENSE for more details.
"""

import io
import os
import ConfigParser
import types
from waltz import web

path = os.path.dirname(__file__)

def makeconf(cfg):
    """Makes a config parser instance provided an unversioned (user
    specified) <file>.cfg. If no such .cfg exists, makeconf will
    attempt to load a fallback .cfg with defaults: <file>_default.cfg
    files containing default values
    """

    def getdef(self, section, option, default_value):
        """injectable method for config parsers which allows 'getattr'
        like behavior (i.e. default values in case config keys don't exist)
        """
        try:
            return self.get(section, option)
        except:
            return default_value

    config = ConfigParser.ConfigParser()
    if not os.path.isfile(cfg):
        cfg_ = cfg
        cfg = '_default'.join(os.path.splitext(cfg))
        if not os.path.isfile(cfg):
            raise IOError("[Errno 2] No such file or directory '%s'" \
                              "and no default/fallback: '%s'" % (cfg_, cfg))
    config.read(cfg)
    config.getdef = types.MethodType(getdef, config)
    return config

def server():
    config_srv = makeconf("%s/server.cfg" % path)
    server = {'DEBUG_MODE': bool(config_srv.getdef("server", "debug", True)),
              'APP_PATH': os.getcwd()
              }
    return server

def database():
    config_db = makeconf('%s/db.cfg' % path)
    user = config_db.getdef("dbms", "user", "ubuntu")
    host = config_db.getdef("dbms", "host", "localhost")
    port = config_db.getdef("dbms", "port", 3306)
    passwd = config_db.getdef("dbms", "passwd", "")
    dbn = config_db.getdef("dbms", "dbn", "mysql")
    db = config_db.getdef("dbms", "db", "sendr")
    try:
        return web.database(host=host, dbn="mysql", db=db,
                            user=user, pw=passwd)
    except:
        return None

SERVER = server()
db = database()
