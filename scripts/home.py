# coding: utf-8

import json
import logging

import requests

from scripts.mongo_operate import get_value
from socrates.set import log

home_url = "http://weilairiji.com/api/statuses/user_timeline.json"
home_dict = {'home1':1,
             'home2':2,
             'home3':3}

def home(wechat_id, key):
    user = get_value('id', 'xiezhua_id', wechat_id=wechat_id)

    headers = {}
    headers['Authorization'] = user['xiezhua_id']

    data = {}
    data['id'] = user['id']
    data['page'] = home_dict[key]

    r = requests.get(home_url, params=data, headers=headers)
    assert r.status_code==200
    
    home_original = json.loads(r.text.replace('=',':'), encoding='GB18030')
    ret = '\n\n'.join(map(\
     lambda item: item['text'], home_original))
    return ret
