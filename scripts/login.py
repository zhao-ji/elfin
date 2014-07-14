# coding: utf-8

import json
import logging

import requests

from socrates import hanzi
from socrates.set import log

POST_URL = 'http://weilairiji.com/api/statuses/update.json'

class login:
    xieban = 0
    user_name = ''
    protected = 0

    def __init__(self, email=None, psw=None):
        bsc_str = 'Basic ' + (email+':'+psw).encode('base64')[:-1]
        __headers = {}
        __headers['Authorization'] = bsc_str

        __data = {}
        __data['status'] = hanzi.BIND_OK.decode('utf-8').encode('GB18030')
        __data['source'] = hanzi.DEVICE.decode('utf-8').encode('GB18030')
        __data['status_type'] = 'talk'

        self.bind_ret = requests.post(POST_URL, data=__data, headers=__headers)
        self.status_code = self.bind_ret.status_code
        self.xiezhua_id = bsc_str
        self.hash = 0
        self.ret = 1

    def analyses(self):
        ret_json = self.bind_ret.text.replace('=', ':')
        try:
            ret_list = json.loads(ret_json, encoding='GB18030')
        except Exception, e:
            logging.error(e)
        else:
            user_info = ret_list[0]['user']
            self.id = int(user_info['id'])
