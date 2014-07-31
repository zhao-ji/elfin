#!/usr/bin/env python 
# coding:utf-8

import json

import requests

SIMI_URL = 'http://sandbox.api.simsimi.com/request.p'
def simi(talk):
    params = {}
    params['key'] = '7809eac7-d8df-494c-b430-98412e330a00'
    params['lc'] = 'ch'
    params['text'] = talk

    r = requests.get(url=SIMI_URL, params=params)
    respons = json.loads(r.text)
    return respons['response']
