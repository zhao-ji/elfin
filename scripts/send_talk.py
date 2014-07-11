#! /usr/bin/python
# coding: utf-8

import random

import requests

from socrates import hanzi 
from socrates.set import mongo

POST_URL = 'http://weilairiji.com/api/statuses/update.json' 

def diff_from_password(talk, pwd_str):
    pwd_base64 = pwd_str.lstrip('Basic').strip()
    pwd_with_mail = pwd_base64.decode('base64')
    pwd = pwd_with_mail[pwd_with_mail.find(':')+1:]
    if pwd in talk:
        raise SensitiveError

def diff_from_old(talk, old_hash):
    new_hash = hash(talk)
    if new_hash == old_hash:
        raise RepeatError

def send_ok_ret(user):
    ret_state = user.get('ret', 1)
    return None if int(ret_state) is 0 else random.choice(hanzi.RET_OK)

def transmit(user, talk,touser=None):
    headers = {}
    headers['Authorization'] = user['xiezhua_id']

    data = {}
    data['status'] = talk.decode('utf-8').encode('GB18030')
    data['source'] = user['tail'].decode('utf-8').encode('GB18030')
    data['in_reply_to_status_id'] = ''
    data['status_type'] = 'talk'

    transmit_ret = requests.post(POST_URL, data=data, headers=headers)

    if transmit_ret.status_code in ['404', '500', '503']:
        raise ServerError
    elif transmit_ret.status_code in ['401', '403']:
        mongo.elfin.remove({'xiezhua_id':xiezhua_id})
        raise VerifyError
    elif transmit_ret.status_code=='200':
        send_ok_ret(user)
    else:
        raise UnkownError

def send(fromUser, talk):
    user = mongo.elfin.find_one({'wechat_id':fromUser})
    try:
        diff_from_password(talk, user['xiezhua_id'])
        diff_from_old(talk, user['hash'])
        less_than_250(talk)
    except SensitiveError:
        return hanzi.sensitive
    except RepeatError:
        return hanzi.repeat
    except OverLengthError:
        slice_ret = map(lambda talk: send(fromUser,talk), slice_talk(talk))
        reduce(sum, slice_ret)
    else:
        try:
            send_ok_ret = transmit(user, talk)
        except ServerError:
            return hanzi.ERR_SERVER
        except VerifyError:
            return hanzi.ERR_PSW
        except UnkownError:
            return hanzi.ERR_UNKOWN
        else:
            return send_ok_ret
    finally:
        logging(user['id'] + ' : ' + talk)
