# coding: utf-8

import json

import requests

from mongo_operate import get_value
home_url = "http://weilairiji.com/api/statuses/user_timeline.json"
home_dict = {'home1':1
             'home2':2
             'home3':3}

def home(wechat_id, key):
    user = get_value('wechat_id', 'id')

    head = {}
    head['Authorization'] = user['wechat_id']

    data = {}
    data['id'] = user['id']
    data['page'] = home_dict[key]

    r = requests.get(home_url, data=data, head=head)
    assert r.status_code==200

    home_original = json.loads(r.replace('=',':'),\
                        encoding='GB18030')
    ret = reduce(sum, map(\\
     lambda item: item['text']+item['time']+'\n',\
                home_original))
    return ret
