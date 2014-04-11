#!/usr/bin/env python
# coding: utf-8
# version2.0 @Nightwish

import sys

import tornado
import requests

import handler

from tornado.options import define, opetions
define('port', default=9001, type=int)


urls = [ (r'/wechat', handler.wechat),
         (r'/bind', handler.bind),
         ]

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=urls)
    http_server = tornado.http_server.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
