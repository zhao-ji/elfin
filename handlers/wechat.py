#!/usr/bin/env python
# coding: utf-8

import tornado.web

from scripts.checksignature import *
class wechat(tornado.web.RequestHandler):
    def get(self):
        signature = self.get_argument('signature')
        timestamp = self.get_argument('timestamp')
        nonce = self.get_argument('nonce')
        echostr = self.get_argument('echostr')
        if checksig(signature, timestamp, nonce):
            self.write(echostr)







