#!/usr/bin/python

import re
import sys
import json
import time
import tweepy
import textwrap
import datetime
import logging
from srt import config
from srt.encoding import str_to_code, code_to_str

def extract_words(text):
    text = text.lower()
    text = text.replace('#', '')
    words = text.split()
    result = []
    for w in words:
        if len(w)<4:
            continue
        if '@' in w:
            continue
        if '/' in w:
            continue
        result.append(w)
    return result

def load_words(path):
    with open(path, 'r') as f:
        w = f.read().splitlines()
        return w
    return []

def find_tweets(seq_list, words):
    logging.basicConfig()
    auth = tweepy.OAuthHandler(config.TWITTER_CONSUMER_KEY, config.TWITTER_CONSUMER_SECRET)
    auth.set_access_token(config.TWITTER_KEY, config.TWITTER_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    
    def find(id_list):
        for t in tweepy.Cursor(api.search, q=words[seq], 
                               include_entities=False, trim_user=True).items():
            
            for w in extract_words(t.text):
                if w not in words:
                    # print "not in list:", w
                    continue
                if w!=words[seq]:
                    # print "wrong tweet:", w
                    break
                id_list.append((t.id, action))
                #print "save", w, ":", t.text
                print w
                return

    id_list = []
    for seq, action in seq_list:
        find(id_list)
        time.sleep(0.5) # minimize rate limits effects

    return id_list


def hide(path):
    tw = textwrap.wrap(path, config.CHARS_X_INTERACTION, \
                       drop_whitespace=False)
    interactions = []
    for mm in tw:
        base, offset = str_to_code(mm)
        print "hide:", base, offset
        if offset==0:
            interactions.append((base, 'R'))
        elif offset==1:
            interactions.append((base, 'L'))
        else:
            interactions.append((base, 'RL'))

    return interactions


def unhide(seq_list):
    message=''
    for base, actions in seq_list:
        if base == -1:
            continue
        #print "|", base, "|"
        #print "actions:", actions
        offset = 0
        if 'RL' in actions:
            offset = 2
        elif 'L' in actions:
            offset = 1

        print "unhide:", base, offset
        message += code_to_str(base, offset)
    return message


def send_message(id_list):

    auth = tweepy.OAuthHandler(config.TWITTER_CONSUMER_KEY, config.TWITTER_CONSUMER_SECRET)
    auth.set_access_token(config.TWITTER_KEY, config.TWITTER_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    for tid, actions in id_list:
        if 'RL' in actions:
            print "Retweet & Like:", tid
            api.retweet(tid)
            api.create_favorite(tid)
        elif 'L' in actions:
            print "Like:", tid
            api.create_favorite(tid)
        else:
            print "Retweet:", tid
            api.retweet(tid)

def read_message(screen_name, words):

    auth = tweepy.OAuthHandler(config.TWITTER_CONSUMER_KEY, config.TWITTER_CONSUMER_SECRET)
    auth.set_access_token(config.TWITTER_KEY, config.TWITTER_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    interactions = []
    tweets = api.user_timeline(screen_name, count=10)
    for t in reversed(tweets):
        seq = -1
        for w in extract_words(t.text):
            if w in words:
                try:
                    seq = words.index(w)
                except ValueError:
                    pass
                break

        if t.favorited and not t.retweeted:
            action = "L"
        elif t.retweeted and not t.favorited:
            action = "R"
        else:
            action = "RL"   
        interactions.append((seq, action))

    return interactions


