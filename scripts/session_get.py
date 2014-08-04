# coding: utf-8

import pickle

import requests

from scripts.mongo_operate import update_user 

def get_session(xiezhua_id):

    login_url = 'http://m.weilairiji.com/index.php?op=login'
    s = requests.Session()

    data = {}
    data['loginaccount'] = xiezhua_id[0]
    data['loginpass'] = xiezhua_id[1]
    data['action'] = 'login'

    r = s.post(login_url, data=data)
    session = pickle.dumps(s)
    update_user({'xiezhua_id':xiezhua_id},
                    session=session)
    return s
