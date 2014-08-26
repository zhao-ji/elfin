#! /usr/bin/python
# coding: utf-8

import logging

import requests
from gevent import spawn, joinall

from socrates import hanzi 
from socrates.set import log
from scripts.simi import simi
from scripts.mongo_operate import update_user, del_user

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
        del_user(user)
        raise UserWarning
    elif transmit_ret.status_code is 200:
        return
    else:
        raise FutureWarning

def send(user, talk):
    try:
        diff_from_password(talk, user['xiezhua_id'])
        diff_from_old(talk, user['hash'])
        less_than_300(talk)
    except AssertionError, e:
        logging.info(e)
        return e
    except OverflowError:
        map(lambda talk: transmit(user,talk), slice_talk(talk))
        ret = hanzi.MULTITALK
        return ret
    else:
        try:
            if user['ret']:
                transmit(user, talk)
                ret = user['ret']
            else:
                task_simi = spawn(simi, talk)
                task_send = spawn(transmit, user, talk)
                joinall([task_simi, task_send])
                ret = task_simi.value
        except RuntimeWarning:
            return hanzi.ERR_SERVER
        except UserWarning:
            return hanzi.ERR_PSW
        except FutureWarning:
            return hanzi.ERR_UNKOWN
        else:
            return ret
    finally:
        update_user(id=user['id'], hash=hash(talk))
        logging.info(str(user['id']) + ' : ' + talk)
        logging.info(str(user['id']) + ' : ' + ret)
