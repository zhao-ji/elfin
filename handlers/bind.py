#!/usr/bin/env python
# coding: utf-8

import time

from tornado.web import RequestHandler

from scripts.login import login
from socrates import hanzi
from scripts.mongo_operate import save_user, del_user

class bind(RequestHandler):
    def get(self, wechat_id):
        action = '/elfin/bind/' + wechat_id
        self.render('bind.html', info=hanzi.BIND, time=time.ctime(), action=action)
    def post(self, wechat_id):
        email = self.get_argument('email')
        psw = self.get_argument('psw')
        action = '/elfin/bind/' + wechat_id
        if not all([email, psw]):
            self.render('base.html', info=hanzi.NOT_ALL, time=time.ctime(), action=action)
            return
        _login = login(email=email, psw=psw)
        _login.analyses()
        if _login.status_code == 200:
            elfin = {}
            elfin['wechat_id'] = wechat_id
            elfin['xiezhua_id'] = _login.xiezhua_id
            elfin['id'] = _login.id
            elfin['tail'] = hanzi.DEVICE
            elfin['hash'] = _login.hash
            elfin['ret'] = _login.ret
            try:
                elfin['session'] = _login.session
            except:
                pass
            del_user(wechat_id=wechat_id)
            save_user(elfin)
            self.write(hanzi.BIND_OK)

        elif _login.status_code == 401:
            action = '/elfin/bind/' + wechat_id
            self.render('bind.html', info=hanzi.ERR_PSW, time=time.ctime(), action=action)
        elif _login.status_code in [404,500, 503]:
            self.write(hanzi.ERR_SERVER)
        else:
            self.write(hanzi.ERR_UNKOWN)
