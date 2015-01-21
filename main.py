#!/usr/bin/env python
# coding: utf-8
# version2.0 @Nightwish

import os.path

import tornado
import tornado.web
import tornado.ioloop
import tornado.httpserver

from handlers.wechat import Wechat
from handlers.bind import bind
from handlers.userset import userset

from tornado.options import define, options
define('port', default=3333, type=int)

template_path = os.path.join(os.path.dirname(__file__), 'templates')
static_path = os.path.join(os.path.dirname(__file__), 'static')

handlers = [ (r'/wechat', Wechat),
             (r'/bind/(.*)', bind),
             (r'/userset/(.*)', userset),
             (r'/static/(.*)', 
             tornado.web.StaticFileHandler,
             {'path': static_path}),
           ]

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=handlers,
                            template_path=template_path,)
    http_server = tornado.httpserver.HTTPServer(app, xheaders=True)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
