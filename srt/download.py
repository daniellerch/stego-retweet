#!/usr/bin/python

import os
import sys
import json
import re
import time
import tweepy
import datetime
import logging
from srt import config



n_tweets = config.NUM_MESSAGES 

def update_progress(progress, cnt, n_tweets):
    sys.stdout.write('\r{0:.2f}%: {1} of {2} (total: {3})'.format(100*float(progress)/n_tweets, progress, n_tweets, cnt))
    sys.stdout.flush()

def get_tweets(search_string, tweets_path):
    logging.basicConfig()
    seq_dict = {}
    seq_count = 0

    auth = tweepy.OAuthHandler(config.TWITTER_CONSUMER_KEY, config.TWITTER_CONSUMER_SECRET)
    auth.set_access_token(config.TWITTER_KEY, config.TWITTER_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    cnt = 0
    while True:
        for t in tweepy.Cursor(api.search, q=search_string, include_entities=False, trim_user=True).items():

            seq = int(time.mktime(t.created_at.timetuple())) % config.NUM_MESSAGES 
            if seq not in seq_dict:
                seq_dict[seq]=True
                seq_count += 1
                with open(tweets_path, 'a+') as f:
                    f.write('{"seq":'+str(seq)+', "id":'+t.id_str+'}\n')

            update_progress(seq_count, cnt, config.NUM_MESSAGES)

            if seq_count >= config.NUM_MESSAGES:
                return

            time.sleep(0.5)
            cnt += 1

        print "retry!"


