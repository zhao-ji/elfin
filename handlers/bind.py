#!/usr/bin/env python
# coding: utf-8

import time

import tornado.web

from scripts.login import login
from socrates import hanzi
from socrates.set import mongo

class bind(tornado.web.RequestHandler):
    def get(self, wechat_id):
        action = '/elfin/bind/' + wechat_id
        self.render('login.html', time=time.ctime(), action=action)
    def post(self, wechat_id):
        email = self.get_argument('email')
        psw = self.get_argument('psw')
        if not all([email, psw]):
            action = '/elfin/bind/' + wechat_id
            self.render('login.html', info=hanzi.NOT_ALL, action=action)
            return
        _login = login(email=email, psw=psw)
        _login.analyses()
        if _login.status_code == 200:
            self.write(hanzi.BIND_OK)
            mongo.authenticate('elfin', 'sljfZ5weyil')
            elfin = {}
            elfin['wechat_id'] = wechat_id
            elfin['xiezhua_id'] = _login.xiezhua_id
            elfin['id'] = _login.id
            elfin['tail'] = hanzi.DEVICE
            elfin['hash'] = _login.hash
            elfin['ret'] = _login.ret
            mongo.elfin.remove({'id':elfin['id']})
            mongo.elfin.insert(elfin)

        elif _login.status_code == 401:
            action = '/elfin/bind/' + wechat_id
            self.render('login.html', info=hanzi.ERR_PSW, action=action)
        elif _login.status_code in [404,500]:
            self.write(hanzi.ERR_SERVER)
        else:
            self.write(hanzi.ERR_UNKOWN)
