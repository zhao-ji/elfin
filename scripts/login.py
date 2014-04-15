# coding: utf-8

import json
import logging

import requests

#from ..socrates import global_settings as config

POST_URL = 'http://weilairiji.com/api/statuses/update.json'

class login:
    def __init__(self, email=None, psw=None):
        self.headers = {}
        self.xieban = 0
        self.user_name = ''
        self.protected = False

        self.email = email
        self.psw = psw
        bsc_str = 'Basic ' + (email+':'+psw).encode('base64')[:-1]
        self.headers['Authorization'] = bsc_str

        data = {}
        data['status'] = 'BINDOK'
        data['source'] = 'DEVICE'
        data['status_type'] = 'talk'

        self.bind_ret = requests.post(POST_URL, data=data,
                                       headers=self.headers)
        self.status_code = self.bind_ret.status_code

    def analyses(self):
        ret_json = self.bind_ret.content.replace('=', ':')
        try:
            ret_list = json.dumps(ret_json, encoding='GB2312')
            print type(ret_list[0])
            print len(ret_list)
            print type(ret_list)
        except Exception, e:
            print e
            #logging.error(e)
        else:
            user_info = ret_list[0]['user']
            self.xieban = int(user_info['id'])
            self.user_name = user_info['name']
            self.protected = True if user_info['protected'] == 'True' else False

