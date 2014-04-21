#!/usr/bin/env python
# coding: utf-8

import tornado.web

from socrates import hanzi
from socrates.set import mongo

class tail(tornado.web.RequestHandler):
    def get(self, wechat_id):
        action = '/elfin/tail/' + wechat_id
        self.render('login.html', action=action)
    def post(self, weixin_id):
        tail = self.get_argument('tail')
        if not tail:
            self.write(hanzi.NOT_NULL)
        send(weixin_id,tail=tail)
        mongo.elfin.update({'wechat_id':wechat_id},
                            {'$set':{'tail':tail}})
        self.write(hanzi.TAIL_OK)
