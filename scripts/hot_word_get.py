# coding: utf-8

import re
import pickle
import logging
from urllib import urlencode

import requests

from socrates.set import log
from scripts.mongo_operate import get_user_value

hot_word_url = 'http://m.weilairiji.com/index.php?op=search&{}'

hot_word_wrap = '<a href="http://m.weilairiji.com/index.php?op=search&{}">{}</a>'

hot_word_pattern = re.compile(ur'style="padding:5px"\s>(.+?)</a>')

def hot_word():
    session = pickle.loads(get_user_value('session', id=47637).get('session'))
    r = session.get(url=hot_word_url.format(urlencode({'s':'90for'})))
    hot_word_list = hot_word_pattern.findall(r.text)
    to_unicode = lambda i: i.replace('&#x','\u').replace(';','').decode('unicode_escape')
    hot_word_unicode = map(to_unicode, hot_word_list)
    to_href = lambda i: hot_word_wrap.format(urlencode({'s':i.encode('gbk')}), i.encode('utf8'))
    hot_word_href = map(to_href, hot_word_unicode)
    return '\n\n'.join(hot_word_href)

