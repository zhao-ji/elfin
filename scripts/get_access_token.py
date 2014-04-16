#!/usr/bin/env python
# coding: utf-8

import time
import pickle
import logging

import requests

GRANT_TYPE = 'client_credential'
APPID = 'wx16b6a22daa10d5c1'
SECRET = '37e8ff0ffbe0cfa1589787cb42ab3b54'
URL = 'https://api.weixin.qq.com/cgi-bin/token'
ACCESS_TOKEN = ''

def get_access_token():
    params = {'grant_type':GRANT_TYPE,
              'appid':APPID,
              'secret':SECRET}
    r = requests.get(URL, params=params)
    if r.status_code == 200:
        json_dict = r.json()
        access_token = json_dict['access_token']
        global ACCESS_TOKEN
        ACCESS_TOKEN = pickle.dumps(access_token)
        logging.info('access_token:' + access_token)
    else:
        logging.error(r.status_code)

if __name__ == '__main__':
    while 1:
        get_access_token()
        time.sleep(3600)
