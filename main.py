#!/usr/bin/env python
# coding: utf-8
# version2.0 @Nightwish

import os.path

import tornado
import tornado.web
import tornado.ioloop
import tornado.httpserver

from handlers.wechat import wechat
from handlers.bind import *
from handlers.tail import *

from socrates.set import mongo

from tornado.options import define, options
define('port', default=9001, type=int)

template_path = os.path.join(os.path.dirname(__file__), 'templates')
static_path = os.path.join(os.path.dirname(__file__), 'static')

handlers = [ (r'/wechat', wechat),
             (r'/bind/(.*)', bind),
             (r'/tail/(.*)', tail),
             (r'/static/(.*)', 
             tornado.web.StaticFileHandler,
             {'path': static_path}),
           ]

if __name__ == '__main__':
    mongo.authenticate('elfin', 'sljfZ5weyil')
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=handlers,
                            template_path=template_path,)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
