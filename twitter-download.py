#!/usr/bin/python

import os
import sys
from stegolike.download import get_tweets


def main():

    if len(sys.argv) != 3:
        print "Usage: "
        print "   %s <search string> <tweets file>" % (sys.argv[0])
        print ""
        print "Example:"
        print "   %s 'crypto' tweets.db" % (sys.argv[0])
        print 
        sys.exit(0)

    if os.path.isfile(sys.argv[2]):
        os.remove(sys.argv[2])
    get_tweets(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    main()


