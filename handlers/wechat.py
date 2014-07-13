#!/usr/bin/env python
# coding: utf-8

import os
import sys
import time
import xml.etree.ElementTree as ET

import tornado.httpserver
import tornado.web

from socrates import hanzi
from socrates.set import mongo
from scripts.check_sig import check_sig
from scripts.mongo_operate import whether_login, del_item
from scripts.send_talk import send
from scripts.home import home

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
        ret_render = lambda ret_str: self.render('text.xml',
                                            toUser=fromUser,
                                           time=time.time(),
                                               text=ret_str,
                                                )
        xml = self.request.body
        xml = ET.fromstring(xml)
        fromUser = xml.find('FromUserName').text
        MsgType = xml.find('MsgType').text
        if MsgType is 'text':
            Text = xml.find('Content').text
            try:
                whether_login(fromUser) 
            except AssertionError:
                del_item(wechat_id=fromUser)
                Feedback = hanzi.HELLO%fromUser
            else:
                Feedback = send(fromUser, Text)
            finally:
                ret_render(Feedback)

        elif MsgType is 'image':
            pass

        elif MsgType is 'event':
            event = xml.find("Event").text
            if event == 'subscribe':
                ret_render(hanzi.HELLO%fromUser)
            elif event == 'unsubscribe':
                pass
            elif event == 'CLICK':
                key = xml.find("EventKey").text
                if key == 'help':
                    ret_render(hanzi.HELP)

                elif key in ['home1', 'home2', 'home3']:
                    try:
                        whether_login(fromUser) 
                    except AssertionError:
                        del_item(wechat_id=fromUser)
                        Feedback = hanzi.HELLO%fromUser
                    else:
                        Feedback = home(fromUser, key)
                    finally:
                        ret_render(Feedback)
               
                elif key in ['tml1', 'tml2', 'tml3']:
                    ret_render('hello')
                elif key in ['at_msg', 'pri_msg']: 
                    ret_render('hello')
                elif key == 'tail':
                    ret_render(hanzi.TAIL%fromUser)
                elif key == 'open_msg': 
                    ret_render('hello')
                elif key == 'resent_visitor': 
                    ret_render('hello')
                elif key == 'hot_word': 
                    ret_render('hello')

