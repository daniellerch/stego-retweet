#!/usr/bin/python

import sys
import json
import tweepy
from srt import config

if len(sys.argv)!=2:
    print "Usage:", sys.argv[0], "<tweet id>\n" 
    sys.exit(0)

tid = sys.argv[1]
auth = tweepy.OAuthHandler(config.TWITTER_CONSUMER_KEY, config.TWITTER_CONSUMER_SECRET)
auth.set_access_token(config.TWITTER_KEY, config.TWITTER_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
print json.dumps(api.get_status(tid)._json, indent=2)
 
