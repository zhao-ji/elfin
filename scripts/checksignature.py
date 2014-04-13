#!/usr/bin/env python
# coding: utf-8

import hashlib

TOKEN = 'xiezhua'

def checksig(signature=None, timestamp=None,
            nonce=None):
    if all(signature, timestamp, nonce):
        tmp_list = [timestamp, nonce, TOKEN]
        tmp_list.sort()
        tmp_str = ''.join(tmp_list)
        sha1_str = hashlib.sha1()
        sha1_str.update(tmp_str)
        sha1_sig = sha1_str.hexdigest()
        return 1 if signature == sha1_sig else 0
    else:
        return 0
