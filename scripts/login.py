# coding: utf-8

import json
import pickle
import logging

import requests

from socrates import hanzi
from socrates.set import log
from scripts import session_get

POST_URL = 'http://weilairiji.com/api/statuses/update.json'

class login:
    xieban = 0
    user_name = ''
    protected = 0
    id = 0

    def __init__(self, email=None, psw=None):
        __data = {}
        __data['status'] = hanzi.BIND_OK.decode('utf-8').encode('GB18030')
        __data['source'] = hanzi.DEVICE.decode('utf-8').encode('GB18030')
        __data['status_type'] = 'talk'

        self.bind_ret = requests.post(POST_URL, data=__data, auth=(email, psw))
        self.status_code = self.bind_ret.status_code
        self.xiezhua_id = [email, psw]
        self.hash = 0
        self.ret = ''

    def analyses(self):
        ret_json = self.bind_ret.text.replace('=', ':')
        try:
            ret_list = json.loads(ret_json, encoding='GB18030')
        except Exception, e:
            logging.error(e)
        else:
            user_info = ret_list[0]['user']
            self.id = int(user_info['id'])
            self.session = pickle.dumps(session_get.get_session(self.xiezhua_id))
