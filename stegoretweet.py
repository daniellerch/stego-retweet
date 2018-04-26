#!/usr/bin/python

import sys
import md5
import json
import time
import datetime
import numpy as np
from srt import config
from srt.twitter import load_words, hide, unhide, send_message, read_message


def main():

    if len(sys.argv) < 3:
        print "Usage: "
        print "   %s <send> <text>" % (sys.argv[0])
        print "   %s <send> <text> <hashtag1,hahstag2,hashtagN>" % (sys.argv[0])
        print "   %s <recv> <user>" % (sys.argv[0])
        print 
        sys.exit(0)

    words = load_words("db/words.txt")
    if sys.argv[1] == 'send':
        hashtag_list = []
        if len(sys.argv)==4:
            hashtag_list = sys.argv[3].split(',')
        hashtag_list += [""]
        seq_list = hide(sys.argv[2].lower())
        send_message(seq_list, words, hashtag_list)

    elif sys.argv[1] == 'recv':
        seq_list = read_message(sys.argv[2], words)
        print unhide(seq_list)

if __name__ == "__main__":
    main()






