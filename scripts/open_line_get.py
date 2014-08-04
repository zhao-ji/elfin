# coding: utf-8

import re
import logging

import requests

from socrates.set import log

open_line_url = 'http://m.weilairiji.com/index.php?op=browse'

open_line_pattern = re.compile(ur".*uid=\d+'>(.+?)</a>(.+?)<span.*")

def open_line():
    r = requests.get(url=open_line_url)
    open_line_list = open_line_pattern.findall(r.text)
    to_unicode = lambda i: i.replace('&#x','\u').replace(';','').decode('unicode_escape')
    open_line_unicode = map(lambda j:map(to_unicode, j), open_line_list)
    logging.info(open_line_unicode)
    open_line_combine = '\n\n'.join(map(lambda k: ' '.join(k), open_line_unicode))
    return '\n\n'.join(open_line_combine)
