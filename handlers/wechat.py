#!/usr/bin/env python
# coding: utf-8

import os
import sys
import time
import logging
import xml.etree.ElementTree as ET

import tornado.httpserver
import tornado.web

from socrates import hanzi
from socrates.set import mongo
from scripts.check_sig import *

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
        signature = self.get_body_arguments('signature')
        timestamp = self.get_body_arguments('timestamp')
        nonce = self.get_body_arguments('nonce')
        #if not check_sig(signature, timestamp, nonce):
            #return 
        ret_render = lambda ret_str: self.render('text.xml',
                                                toUser=fromUser,
                                                time=time.time(),
                                                text=ret_str
                                                )
        xml = self.request.body
        xml = ET.fromstring(xml)
        fromUser = xml.find('FromUserName').text
        MsgType = xml.find('MsgType').text
        if MsgType == 'text':
            Text = xml.find('Content').text
            Feedback = send(fromUser, Text)
            ret_render(Feedback)

        elif MsgType == 'image':
            pass

        elif MsgType == 'event':
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
                    ret_render('hello')
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

