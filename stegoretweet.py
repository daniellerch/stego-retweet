#!/usr/bin/python

import sys
import md5
import json
import time
import datetime
import numpy as np
from srt import config
from srt.twitter import load_data, hide, unhide


def main():

    if len(sys.argv) != 4:
        print "Usage: "
        print "   %s <db> <hide> <text>" % (sys.argv[0])
        print "   %s <db> <unhide> <ID string>" % (sys.argv[0])
        print 
        sys.exit(0)

    data = load_data(sys.argv[1])
    data_r = {v: k for k, v in data.items()}

    if sys.argv[2] == 'hide':
        print hide(sys.argv[3], data)

    elif sys.argv[2] == 'unhide':
        print unhide(sys.argv[3], data_r)

if __name__ == "__main__":
    main()






