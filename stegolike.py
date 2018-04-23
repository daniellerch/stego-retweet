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
        to_retweet=[]
        tw = textwrap.wrap(sys.argv[3], config.STEGOLIKE_CHARS_X_INTERACTION, \
                           drop_whitespace=False)
        for mm in tw:
            m = str_to_code(mm)
            to_retweet.append(data[m-1])

        print ','.join(to_retweet)

    elif sys.argv[2] == 'unhide':
        retweets = sys.argv[3].split(",")
        message=''
        for r in retweets:
            message += code_to_str(data_r[r]+1)
        print "message:", message

if __name__ == "__main__":
    main()






