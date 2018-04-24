#!/usr/bin/python

import sys
import md5
import json
import time
import textwrap
import datetime
import numpy as np
from stegolike import config
from stegolike.message import load_data, str_to_code, code_to_str


def main():

    if len(sys.argv) != 4:
        print "Usage: "
        print "   %s <db> <hide> <text>" % (sys.argv[0])
        print "   %s <db> <unhide> <tweet ids>" % (sys.argv[0])
        print 
        sys.exit(0)

    data = load_data(sys.argv[1])
    data_r = {v: k for k, v in data.items()}

    if sys.argv[2] == 'hide':
        to_like=[]
        tw = textwrap.wrap(sys.argv[3], config.STEGOLIKE_CHARS_X_INTERACTION, \
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

        print ','.join(interactions)

    elif sys.argv[2] == 'unhide':
        interactions = sys.argv[3].split(",")
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
        print "message:", message

if __name__ == "__main__":
    main()






