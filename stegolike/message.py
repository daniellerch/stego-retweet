#!/usr/bin/python

import sys
import md5
import json
import time
import hashlib
import datetime
import numpy as np
from stegolike import config


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

def str_to_code(s):
    while len(s) % config.STEGOLIKE_CHARS_X_INTERACTION != 0:
        s += " "

    x = [config.STEGOLIKE_CHARSET.index(c) for c in s]
    y = [(b >> i) & 1 for b in x for i in reversed(range(config.STEGOLIKE_BITS_X_CHAR)) ]
    y_str = ''.join(str(a) for a in y)
    code = int(y_str, 2)
    base = int(code / config.STEGOLIKE_AVAILABLE_INTERACTIONS)
    offset = code - (base*3)
    return base, offset

def code_to_str(base, offset):
    code = base * config.STEGOLIKE_AVAILABLE_INTERACTIONS + offset
    bits=[int(x) for x in list("{0:012b}".format(code))]
    chars=''
    for i in range(0, len(bits), config.STEGOLIKE_BITS_X_CHAR):
        c_bits = bits[i:i+config.STEGOLIKE_BITS_X_CHAR]
        c_bits_str = ''.join(map(str, c_bits))
        chars += config.STEGOLIKE_CHARSET[(int(c_bits_str, 2))]
    return chars




