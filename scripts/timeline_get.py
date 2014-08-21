# coding: utf-8

import pickle
import logging

import requests

from scripts.timeline_operate import timeline
from scripts.session_get import get_session
from scripts.mongo_operate import get_user_value
from socrates.set import open_line_url, time_line_url, log

def open_line():
    open_line_ret = requests.get(url=open_line_url)
    return timeline(open_line_ret.content)

def time_line(key, wechat_id):
    session_dict = get_user_value('session', wechat_id=wechat_id)
    if session_dict.get('session',''):
        session = session_dict['session']
        session = pickle.loads(session)
    else:
        user = get_user_value(wechat_id=wechat_id)
        session = get_session(user['xiezhua_id'])
    tml_dict = {'tml1':1, 'tml2':2, 'tml3':3,}
    time_line_ret = session.get(url=time_line_url.format(tml_dict[key]))
    return timeline(time_line_ret.content)
