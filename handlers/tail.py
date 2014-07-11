#!/usr/bin/env python
# coding: utf-8

import sys
import os.path

import tornado.web

from socrates import hanzi
from socrates.set import mongo
from scripts import send_talk

class tail(tornado.web.RequestHandler):
    def get(self, wechat_id):
        action = '/elfin/tail/' + wechat_id
        self.render('tail.html', action=action)
    def post(self, weixin_id):
        tail = self.get_argument('tail')
        if not tail:
            self.write(hanzi.NOT_NULL)
        send(weixin_id,tail=tail)
        user = mongo.elfin.find_one({'wechat_id':wechat_id})
        user['tail'] = tail
        try:
            send_talk.transmit(user, hanzi.CHANGE_TAIL%tail)
        except:
            self.write(hanzi.TAIL_ERR)
        else:
            mongo.elfin.update({'wechat_id':wechat_id},
                            {'$set':{'tail':tail}})
            self.write(hanzi.TAIL_OK)
        finally:
            logging.info('change tail : ' + user['id']\
                + ' ' + tail)
