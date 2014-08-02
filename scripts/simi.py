#!/usr/bin/env python 
# coding:utf-8

import json

import requests

SIMI_URL = 'http://api.simsimi.com/request.p'
def simi(talk):
    params = {}
    params['key'] = 'b031132b-28ab-4769-b560-96ebddf70c1e'
    params['lc'] = 'ch'
    params['text'] = talk

    r = requests.get(url=SIMI_URL, params=params)
    respons = json.loads(r.text)
    return respons['response']
