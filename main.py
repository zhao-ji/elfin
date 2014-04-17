#!/usr/bin/env python
# coding: utf-8
# version2.0 @Nightwish

import os.path
import sys

import tornado
import tornado.web
import tornado.ioloop
import tornado.httpserver

import requests

from handlers.wechat import *
from handlers.bind import *

from tornado.options import define, options
define('port', default=9001, type=int)


handlers = [ (r'/wechat', wechat),
             (r'/bind/(\w+)', bind),
             (r'/tail', tail),
           ]
template_path = os.path.join(os.path.dirname(__file__), 'templates')

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=handlers, template_path=template_path)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
