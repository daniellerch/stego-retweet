#!/usr/bin/python

import json
import time
import hashlib
import textwrap
from stegolike import config
from stegolike.encoding import str_to_code, code_to_str

def load_data(path):
    with open(path) as f:
        json_list = f.readlines()
    data={}
    for i, j in enumerate(json_list):
        tweet=json.loads(j)

        hx = hashlib.md5(tweet["text"].encode('utf-8')).hexdigest()
        seq = int(hx, 16) % config.STEGOLIKE_NUM_MESSAGES
        #seq = int(tweet["date"]) % config.STEGOLIKE_NUM_MESSAGES

        data[seq] = tweet["id"]
    return data

def hide(path, data):
    tw = textwrap.wrap(path, config.STEGOLIKE_CHARS_X_INTERACTION, \
                       drop_whitespace=False)
    interactions = []
    for mm in tw:
        base, offset = str_to_code(mm)
        if offset==0:
            interactions.append(str(data[base])+':R')
        elif offset==1:
            interactions.append(str(data[base])+':L')
        else:
            interactions.append(str(data[base])+':RL')

    return ','.join(interactions)


def unhide(path, data_r):
    interactions = path.split(",")
    message=''
    for r in interactions:
        msg_id, actions = r.split(':')
        base = data_r[msg_id]
        offset = 0
        if 'L' in actions:
            offset = 1
        if 'RL' in actions:
            offset = 2

        message += code_to_str(base, offset)
    return message


