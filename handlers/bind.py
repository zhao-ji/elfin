#!/usr/bin/env python
# coding: utf-8

import redis
import tornado.web

from scripts.login import login
from socrates import hanzi
from socrates import config

class bind(tornado.web.RequestHandler):
    def get(self):
        self.render('login.html', info=hanzi.NOTIFY)
    def post(self, weixin_id):
        email = self.get_argument('email')
        psw = self.get_argument('password')
        login = login(email=email, psw=psw)
        if login.status_code == 200:
            self.write(hanzi.BIND_OK)

        elif login.status_code == 401:
            self.render('login.html', info=hanzi.ERR_PSW)
        else:
            self.write(hanzi.UNKOWN_ERR)
