#!/usr/bin/env python
# coding: utf-8

import time
import logging

import tornado.web

from socrates import hanzi
from socrates.set import log
from scripts.send_talk import transmit
from scripts.mongo_operate import get_value, del_item, save_user

class userset(tornado.web.RequestHandler):
    def get(self, wechat_id):
        action = '/elfin/userset/' + wechat_id
        self.render('userset.html', info=hanzi.USERSET , time=time.ctime(), action=action)
    def post(self, wechat_id):
        tail = self.get_arguments('tail')
        ret = self.get_arguments('ret')
        user = get_value(wechat_id=wechat_id)
        if tail:
            user['tail'] = tail[0]
            try:
                transmit(user, 'Change tail to ' + tail[0])
            except:
                self.write(hanzi.TAIL_ERR)
            else:
                del_item(wechat_id=wechat_id)
                save_user(user)
                self.write(hanzi.TAIL_OK)
            finally:
                logging.info(str(user['id']) + ':' + user['tail'])
        elif ret:
            if ret[0]=='0':
                user['ret'] = 0
                del_item(wechat_id=wechat_id)
                save_user(user)
            elif ret[0]=='1':
                method = self.get_argument('method')
                user['ret'] = 1
                if method=='custom':
                    custom_ret = self.get_argument('custom_ret')
                    user['custom_ret'] = custom_ret
                else:
                    user.pop('custom_ret')
                del_item(wechat_id=wechat_id)
                save_user(user)
            self.write('ok')
