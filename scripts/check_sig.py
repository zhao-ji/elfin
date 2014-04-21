#!/usr/bin/env python
# coding: utf-8

import hashlib

TOKEN = 'elfin'

def check_sig(signature=None, timestamp=None, nonce=None):
    if all([signature, timestamp, nonce]):
        tmp_list = [timestamp, nonce, TOKEN]
        tmp_list.sort()
        tmp_str = ''.join(tmp_list)
        sha1_str = hashlib.sha1(tmp_str).hexdigest()
        return 1 if signature == sha1_str else 0
    return 0
