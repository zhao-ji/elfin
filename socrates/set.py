# coding: utf-8

import logging

log = logging.basicConfig(filename='log/run.log',
                    filemode='a',
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO
                    )


'''  [1] list   timeline of each user
     [2] list   recent visiters of each user
     [3] string @, private message
     [4] list   public message, hot words
     [5] string access_token
'''

REDIS = {'HOST':'localhost','PORT':6379}

'''  elfin-user-info
     {  wechat_id : string ,
        xieban    : string ,
        xiezhua_id: string ,
        name      : string ,
        protected : bool   ,
     }
'''

import pymongo

mongo = pymongo.MongoClient(host='localhost', port=27017)['elfin']
