#! /usr/bin/python 
# coding: utf-8

from socrates.set import mongo

def whether_login(wechat_id):
    query = {'wechat_id':wechat_id}
    count = mongo.elfin.find(query).count()
    assert count==1

def del_item(**query):
    mongo.elfin.remove(query)

def get_value(*keys, **query):
    if keys:
        user = mongo.elfin.find_one(query,
           {i:1 for i in keys})
    else:
        user = mongo.elfin.find_one(query)

    return user
