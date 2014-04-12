#!/usr/bin/env python
# coding: utf-8

import tornado.web

class wechat(tornado.web.RequestHandler):
    def get(self):
        self.write('hello world !')







