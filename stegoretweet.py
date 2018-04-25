#!/usr/bin/python

import sys
import md5
import json
import time
import datetime
import numpy as np
from srt import config
from srt.twitter import load_data, hide, unhide, send_message, read_message


def main():

    if len(sys.argv) != 4:
        print "Usage: "
        print "   %s <db> <send> <text>" % (sys.argv[0])
        print "   %s <db> <recv> <user>" % (sys.argv[0])
        print 
        sys.exit(0)

    data = load_data(sys.argv[1])
    data_r = {v: k for k, v in data.items()}

    if sys.argv[2] == 'send':
        id_string = hide(sys.argv[3], data)
        send_message(id_string)

    elif sys.argv[2] == 'recv':
        seq_string = read_message(sys.argv[3])
        print unhide(seq_string)

if __name__ == "__main__":
    main()






