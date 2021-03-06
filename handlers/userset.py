#!/usr/bin/env python
# coding: utf-8

import time
import logging

import tornado.web

from socrates import hanzi
from socrates.set import log
from scripts.talk_send import transmit
from scripts.mongo_operate import get_user_value, del_user, save_user

class userset(tornado.web.RequestHandler):
    def get(self, wechat_id):
        action = '/elfin/userset/' + wechat_id
        self.render('userset.html', info=hanzi.USERSET , time=time.ctime(), action=action)
    def post(self, wechat_id):
        tail = self.get_arguments('tail')
        ret = self.get_arguments('ret')
        user = get_user_value(wechat_id=wechat_id)
        if tail:
            user['tail'] = tail[0]
            try:
                transmit(user, hanzi.CHANGE_TAIL.decode('utf-8').format(tail[0]))
            except:
                self.write(hanzi.TAIL_ERR)
            else:
                del_user(wechat_id=wechat_id)
                save_user(user)
                self.render('return.html', info=hanzi.TAIL_OK, time=time.ctime())
            finally:
                logging.info(str(user['id']) + ':' + user['tail'])
        elif ret:
            if ret[0]=='0':
                user['ret'] = ''
                del_user(wechat_id=wechat_id)
                save_user(user)
            elif ret[0]=='1':
                custom = self.get_argument('custom')
                user['ret'] = custom
                del_user(wechat_id=wechat_id)
                save_user(user)
            self.render('return.html', info=hanzi.RET_OK, time=time.ctime())
