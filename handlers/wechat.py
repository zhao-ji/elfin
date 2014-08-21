#!/usr/bin/env python
# coding: utf-8

import os
import sys
import time
import logging
import xml.etree.ElementTree as ET

from gevent import spawn, joinall
import tornado.httpserver
import tornado.web

from socrates import hanzi
from socrates.set import mongo, log
from scripts.check_sig import check_sig
from scripts.mongo_operate import whether_login, del_user
from scripts.send_talk import send
from scripts.send_photo import upload_photo
from scripts.home import home
from scripts.simi import simi
from scripts.hot_word_get import hot_word
from scripts.timeline_get import open_line, time_line
from scripts.message_get import get_message_num

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir))

class wechat(tornado.web.RequestHandler):
    def get(self):
        signature = self.get_argument('signature')
        timestamp = self.get_argument('timestamp')
        nonce = self.get_argument('nonce')
        echostr = self.get_argument('echostr')
        if check_sig(signature, timestamp, nonce):
            self.write(echostr)

    def post(self):
        ret_render = lambda ret_str: self.render(
                     'text.xml', toUser=fromUser, 
                     time=time.time(), text=ret_str,
                     )
        xml = self.request.body
        xml = ET.fromstring(xml)
        fromUser = xml.find('FromUserName').text
        MsgType = xml.find('MsgType').text
        if MsgType == 'text':
            Text = xml.find('Content').text
            try:
                whether_login(fromUser) 
            except AssertionError:
                del_user(wechat_id=fromUser)
                Feedback = (hanzi.HELLO)%fromUser
                logging.info(Feedback)
                ret_render(Feedback)
            else:
                task_simi = spawn(simi, Text)
                task_send = spawn(send, fromUser, Text)
                joinall([task_simi, task_send])
                logging.info(Text)
                logging.info(task_simi.value)
                ret_render(task_send.value) if bool(task_send.value) else ret_render(task_simi.value)

        elif MsgType == 'image':
            picurl   = xml.find("PicUrl").text
            msgid   = xml.find("MediaId").text
            ret_render(upload_photo(fromUser, picurl, msgid))

        elif MsgType == 'event':
            event = xml.find("Event").text
            if event == 'subscribe':
                ret_render(hanzi.HELLO%fromUser)
            elif event == 'unsubscribe':
                del_user(wechat_id=fromUser)
            elif event == 'CLICK':
                key = xml.find("EventKey").text
                if key == 'help':
                    ret_render(hanzi.HELP)

                elif key in ['home1', 'home2', 'home3']:
                    try:
                        whether_login(fromUser) 
                    except AssertionError:
                        del_user(wechat_id=fromUser)
                        Feedback = hanzi.HELLO%fromUser
                        ret_render(Feedback)
                    else:
                        Feedback = home(fromUser, key)
                        ret_render(Feedback)
               
                elif key in ['tml1', 'tml2', 'tml3']:
                    time_lines = time_line(key, fromUser)
                    ret_render(time_lines)
                elif key in ['at_msg', 'private_msg']: 
                    message_num = get_message_num(key, fromUser)
                    ret_render(message_num)
                elif key == 'tail':
                    ret_render(hanzi.USET%fromUser)
                elif key == 'public_msg': 
                    open_lines = open_line()
                    ret_render(open_lines)
                elif key == 'recent_visitor': 
                    ret_render('hello')
                elif key == 'hot_words': 
                    hot_words = hot_word()
                    ret_render(hot_words)

