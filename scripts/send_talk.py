#! /usr/bin/python
# coding: utf-8

import random
import logging

import requests

from socrates import hanzi 
from socrates.set import log, mongo
from scripts import simi

POST_URL = 'http://weilairiji.com/api/statuses/update.json' 

def diff_from_password(talk, pwd_list):
    assert pwd_list[1] not in talk, hanzi.SENSITIVE

def diff_from_old(talk, old_hash):
    new_hash = hash(talk)
    assert new_hash!=old_hash, hanzi.REPEAT

def less_than_300(talk):
    if len(talk)>300:
        raise OverflowError

def slice_talk(talk):
    talk_list = [talk[i:i + 295] for i in range(0, len(talk), 295)]
    return map(lambda string: u'【' + str(1 + talk_list.index(string)) + u'】' + string, talk_list)

def send_ok_ret(user, talk):
    ret_state = user.get('ret')
    if ret_state is 0:return ''
    return user.get('custom_ret', simi.simi(talk))

def transmit(user, talk,touser=None):
    data = {}
    data['status'] = talk.encode('GB18030')
    data['source'] = user['tail'].encode('GB18030')
    data['in_reply_to_status_id'] = ''
    data['status_type'] = 'talk'

    transmit_ret = requests.post(POST_URL, data=data, auth=tuple(user['xiezhua_id']))

    if transmit_ret.status_code in [404, 500, 503]:
        raise RuntimeWarning
    elif transmit_ret.status_code in [401, 403]:
        mongo.elfin.remove(user)
        raise UserWarning
    elif transmit_ret.status_code is 200:
        return send_ok_ret(user, talk)
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
        return reduce(lambda x, y: x + '\n' + y, slice_ret)
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
        logging.info(str(user['id']) + ' : ' + talk)
