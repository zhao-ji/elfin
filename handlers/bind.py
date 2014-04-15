#!/usr/bin/env python
# coding: utf-8

import tornado.web

class bind(tornado.web.RequestHandler):
    def get(self):
        self.render('login.html')
    def post(self):
        email = self.get_argument('email')
        psw = self.get_argument('password')
        self.write('\n'.join([email,psw]))
