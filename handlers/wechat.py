#!/usr/bin/env python
# coding: utf-8

import time
import xml.etree.ElementTree as ET

import tornado.web

from scripts.checksignature import *

class wechat(tornado.web.RequestHandler):
    def get(self):
        signature = self.get_argument('signature')
        timestamp = self.get_argument('timestamp')
        nonce = self.get_argument('nonce')
        echostr = self.get_argument('echostr')
        if checksig(signature, timestamp, nonce):
            self.write(echostr)

    def post(self):
        #signature = self.get_body_arguments('signature')
        #timestamp = self.request.arguments['timestamp']
        #nonce = self.request.arguments['nonce']
        #ret = checksig(signature, timestamp, nonce)
        #signature = self.request.body_arguments.get('signature')
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
            jjjj

        elif MsgType == 'event':
            event = xml.find("Event").text
            if event == 'subscribe':
                ret_render(hanzi.hello + fromUser)
            elif event == 'help':
                ret_render(hanzi.help)
            elif event in ['home_one', 'home_two', 'home_three']
                pass
            elif event in ['at_msg', 'pri_msg']: 
                ret_render()
            elif event == 'open_msg': 
                ret_render()
            elif event in ['tml_one', 'tml_two', 'tml_three']
                ret_render()
            elif event == 'resent_visitor': 
                ret_render()
            elif event == 'hot_word': 
                ret_render()
            elif event == 'unsubscribe':
                pass

