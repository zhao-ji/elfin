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
        signature = self.request.body_arguments.get('signature')
        xml = self.request.body
        xml = ET.fromstring(xml)
        fromUser = xml.find('FromUserName').text
        MsgType = xml.find('MsgType').text
        if MsgType == 'text':
            Time = time.time()
            Text = xml.find('Content').text+str(signature) +str(self.request.arguments)
            self.render('text.xml', toUser=fromUser,
                    time=Time, text=Text)





