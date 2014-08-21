# coding: utf-8

import logging
import pickle

import requests

from socrates import hanzi
from socrates.set import log
from scripts.mongo_operate import update_user, get_user_value
from scripts.session_get import get_session

def get_photo_stream(pic_url, msgid):
    headers = {}
    headers['User-Agent']      = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:22.0) Gecko/20100101 Firefox/22.0'
    headers['Accept']          = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    headers['Accept-Language'] = 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3'
    headers['Accept-Encoding'] = 'gzip, deflate'
    headers['Connection']      = 'keep-alive'

    r=requests.get(pic_url, headers=headers)

    filename = '/home/nightwish/elfin/picture/' + msgid + '.jpg'
    f = open(filename, 'w')
    f.write(r.content)
    f.close()
    return open(filename, 'rb')


def upload_photo(wechat_id, pic_url, pic_id):
    user = get_user_value(wechat_id=wechat_id)
    #session = get_session(user['xiezhua_id'])
    photo = get_photo_stream(pic_url, pic_id)

    upload_photo_url = 'http://m.weilairiji.com/index.php?op=sendphoto&tsid='
    data = {}
    data['phototitle'] = (hanzi.WECHATPIC.decode('utf-8') + pic_id).encode('GB18030')
    data['action'] = 'upload'

    files = {}
    files['photo'] = ('1.jpg', photo, 'image/jpeg')

    if user.has_key('session'):
        session = pickle.loads(user.get('session'))
    else:
        session = get_session(user.get('xiezhua_id'))
    r = session.post(upload_photo_url, data=data, files=files)
    if r.status_code==200:
        update_user({'xiezhua_id':user.get('xiezhua_id')}, hash=hash(photo))
        return hanzi.SEND_OK 
    else:
        return hanzi.SEND_FAIL
