#!/usr/bin/env python
# coding: utf-8

import os
import sys
import time
import logging
import xml.etree.ElementTree as ET

from tornado.web import RequestHandler

from socrates import hanzi
from socrates.set import log
from scripts.mongo_operate import del_user, get_user_value

from scripts.check_sig import check_sig
from scripts.talk_send import send
from scripts.photo_send import upload_photo
from scripts.homeline_get import home
from scripts.hot_word_get import hot_word
from scripts.timeline_get import open_line, time_line
from scripts.message_get import get_message_num

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir))


class BaseHandler(RequestHandler):

    wechat_id = None
    user = None
    message_type = None
    content = None

    def initialize(self):
        xml = self.request.body
        xml = ET.fromstring(xml)
        self.wechat_id = xml.find('FromUserName').text

        ret = get_user_value(wechat_id=self.wechat_id)
        if ret:
            self.user = ret
        else:    
            self.wechat(hanzi.HELLO%self.wechat_id)
            return 
        
        self.message_type = xml.find('MsgType').text
        if self.message_type == 'text':
            self.content = xml.find('Content').text 
        elif self.message_type == 'image':
            self.content = xml.find("PicUrl").text
            self.media_id = xml.find("MediaId").text
        elif self.message_type == 'event':
            self.content = xml.find("Event").text
            if self.content == 'CLICK':
                self.eventkey = xml.find("EventKey").text
        logging.info(time.clock())

    def wechat(self, ret_str):
        logging.info(time.clock())
        self.render('text.xml', 
                    toUser=self.wechat_id, 
                    time=time.time(), 
                    text=ret_str)



class Wechat(BaseHandler):

    def get(self):
        signature = self.get_argument('signature')
        timestamp = self.get_argument('timestamp')
        nonce = self.get_argument('nonce')
        echostr = self.get_argument('echostr')
        if check_sig(signature, timestamp, nonce):
            self.write(echostr)


    def post(self):
        if self.message_type == 'text':
            self.wechat(send(self.user, self.content))

        elif self.message_type == 'image':
            self.wechat(upload_photo(self.user, self.content, 
                                     self.media_id,))

        elif self.message_type == 'event':
            if self.content == 'subscribe':
                self.wechat(hanzi.HELLO%self.wechat_id)
            elif self.content == 'unsubscribe':
                del_user(wechat_id=self.wechat_id)
            elif self.content == 'CLICK':
                if self.eventkey == 'help':
                    self.wechat(hanzi.HELP)

                elif self.eventkey in ['home1', 'home2', 'home3']:
                    Feedback = home(self.user, self.eventkey)
                    self.wechat(Feedback)
               
                elif self.eventkey in ['tml1', 'tml2', 'tml3']:
                    time_lines = time_line(self.eventkey, self.user)
                    self.wechat(time_lines)

                elif self.eventkey in ['at_msg', 'private_msg']: 
                    message_num = get_message_num(self.eventkey, self.user)
                    self.wechat(message_num)

                elif self.eventkey == 'tail':
                    self.wechat(hanzi.USET%self.wechat_id)

                elif self.eventkey == 'public_msg': 
                    open_lines = open_line()
                    self.wechat(open_lines)

                elif self.eventkey == 'recent_visitor': 
                    self.wechat('hello')

                elif self.eventkey == 'hot_words': 
                    hot_words = hot_word()
                    self.wechat(hot_words)
