#! /usr/bin/python
# coding: utf-8

import random
import logging

import requests

from socrates import hanzi 
from socrates.set import log, mongo

POST_URL = 'http://weilairiji.com/api/statuses/update.json' 

def diff_from_password(talk, pwd_str):
    pwd_base64 = pwd_str.lstrip('Basic').strip()
    pwd_with_mail = pwd_base64.decode('base64')
    pwd = pwd_with_mail[pwd_with_mail.find(':')+1:]
    assert pwd not in talk, hanzi.SENSITIVE

def diff_from_old(talk, old_hash):
    new_hash = hash(talk)
    assert new_hash!=old_hash, hanzi.REPEAT

def less_than_300(talk):
    if len(talk)>300:
        raise OverflowError

def slice_talk(talk):
    pass

def send_ok_ret(user):
    ret_state = user.get('ret', 1)
    return '' if ret_state is 0 else hanzi.SEND_OK 

def transmit(user, talk,touser=None):
    headers = {}
    headers['Authorization'] = user['xiezhua_id']

    data = {}
    data['status'] = talk.encode('GB18030')
    data['source'] = user['tail'].encode('GB18030')
    data['in_reply_to_status_id'] = ''
    data['status_type'] = 'talk'

    transmit_ret = requests.post(POST_URL, data=data, headers=headers)

    if transmit_ret.status_code in [404, 500, 503]:
        raise RuntimeWarning
    elif transmit_ret.status_code in [401, 403]:
        mongo.elfin.remove({'xiezhua_id':xiezhua_id})
        raise UserWarning
    elif transmit_ret.status_code is 200:
        return send_ok_ret(user)
    else:
        raise FutureWarning

def send(fromUser, talk):
    user = mongo.elfin.find_one({'wechat_id':fromUser})
    try:
        diff_from_password(talk, user['xiezhua_id'])
        diff_from_old(talk, user['hash'])
        less_than_300(talk)
    except AssertionError, e:
        logging.info(e)
        return e
    except OverflowError:
        slice_ret = map(lambda talk: transmit(user,talk), slice_talk(talk))
        reduce(sum, slice_ret)
    else:
        try:
            send_ok_ret = transmit(user, talk)
        except RuntimeWarning:
            return hanzi.ERR_SERVER
        except UserWarning:
            return hanzi.ERR_PSW
        except FutureWarning:
            return hanzi.ERR_UNKOWN
        else:
            mongo.elfin.update({'id':user['id']},{'$set':{'hash':hash(talk)}})
            return send_ok_ret
    finally:
        logging.info(user['id'] + ' : ' + talk)
