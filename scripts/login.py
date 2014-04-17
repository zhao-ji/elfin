# coding: utf-8

import json
import logging

import requests

#from ..socrates import global_settings as config

POST_URL = 'http://weilairiji.com/api/statuses/update.json'

class login:
    xieban = 0
    user_name = ''
    protected = 0

    def __init__(self, email=None, psw=None):
        self.bsc_str = 'Basic ' + (email+':'+psw).encode('base64')[:-1]
        headers = {}
        headers['Authorization'] = self.bsc_str

        data = {}
        data['status'] = 'BINDOK'
        data['source'] = 'DEVICE'
        data['status_type'] = 'talk'

        self.bind_ret = requests.post(POST_URL, data=data, headers=headers)
        self.status_code = self.bind_ret.status_code

    def analyses(self):
        ret_json = self.bind_ret.content.replace('=', ':')[1:-1]
        try:
            ret_list = json.loads(ret_json, encoding='GB2312')
        except Exception, e:
            logging.error(e)
        else:
            user_info = ret_list['user']
            self.xieban = user_info['id']
            self.user_name = user_info['name']
            self.protected = 1 if user_info['protected'] == 'true' else 0
            self.photo_url = user_info['profile_image_url']
            self.description = user_info['description']
