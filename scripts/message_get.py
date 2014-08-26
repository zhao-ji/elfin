# coding: utf-8

import re
import pickle

import requests

from socrates import hanzi
from scripts.session_get import get_session

message_url = 'http://m.weilairiji.com/index.php'
at_pattern = re.compile(ur".*atreplies'>(.+?)</a>.*")
private_message_pattern = re.compile(ur".*privatemsg'>(.+?)</a>.*")

def get_message_num(message_type, user):
    if user.get('session', ''):
        session = user['session']
        session = pickle.loads(session)
    else:
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
