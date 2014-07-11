#! /usr/bin/python
# coding: utf-8

import requests

from socrates import hanzi 
from socrates.set import mongo

POST_URL = 'http://weilairiji.com/api/statuses/update.json' 

def transmit(xiezhua_id, talk, tail, touser=None):
    headers = {}
    headers['Authorization'] = xiezhua_id

    data = {}
    data['status'] = talk.decode('utf-8').encode('GB18030')
    data['source'] = tail.decode('utf-8').encode('GB18030')
    data['in_reply_to_status_id'] = ''
    data['status_type'] = 'talk'

    transmit_ret = requests.post(POST_URL, data=data, headers=headers)
    return transmit_ret.status_code

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
        transmit_code = transmit(user['xiezhua_id'], talk, user['tail'])
        return hanzi.talk_ret_code_dict[transmit_code]
    finally:
        logging(user['id'] + ' : ' + talk)
