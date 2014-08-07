# coding: utf-8

import re
import pickle
import logging

import requests

from socrates.set import log
from socrates import hanzi
from scripts.session_get import get_session
from scripts.mongo_operate import get_user_value

message_url = 'http://m.weilairiji.com/index.php'
at_pattern = re.compile(ur".*atreplies'>(.+?)</a>.*")
private_message_pattern = re.compile(ur".*privatemsg'>(.+?)</a>.*")

def get_message_num(message_type, wechat_id):
    session_dict = get_user_value('session', wechat_id=wechat_id)
    if session_dict:
        session = session_dict['session']
        session = pickle.loads(session)
    else:
        user = get_user_value(wechat_id=wechat_id)
        session = get_session(user['wechat_id'])
    r = session.get(url=message_url)
    if message_type == 'at_msg':
        message_init = at_pattern.findall(r.text)
        message_num = message_init[0][-1]
        message = hanzi.AT_MESSAGE.format(message_num)
    elif message_type == 'private_msg':
        message_init = private_message_pattern.findall(r.text)
        message_num = message_init[0][-1]
        logging.info('num:'+str(message_num))
        message = hanzi.PRIVATE_MESSAGE.format(message_num)
    return message
