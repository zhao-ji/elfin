#! /usr/bin/python 
# coding: utf-8

from socrates.set import mongo

def whether_login(wechat_id):
    query = {'wechat_id':wechat_id}
    count = mongo.elfin.find(query).count()
    if count>1:
        logging.error('wechat_id : ' + \
          wechat_id + 'more than 1 record')
    return 'yes' if count==1 else 'no'
