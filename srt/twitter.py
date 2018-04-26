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

def find_tweet(seq, words):
    logging.basicConfig()
    auth = tweepy.OAuthHandler(config.TWITTER_CONSUMER_KEY, config.TWITTER_CONSUMER_SECRET)
    auth.set_access_token(config.TWITTER_KEY, config.TWITTER_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    
    for t in tweepy.Cursor(api.search, q=words[seq], 
                           include_entities=False, trim_user=True).items():
        
        for w in extract_words(t.text):
            if w not in words:
                # print "not in list:", w
                continue
            if w!=words[seq]:
                # print "wrong tweet:", w
                break
            return t.id

    print "tweet not found:", 
    sys.exit(0)



def hide(path):
    tw = textwrap.wrap(path, config.CHARS_X_INTERACTION, \
                       drop_whitespace=False)
    interactions = []
    for mm in tw:
        base, offset = str_to_code(mm)
        #print "hide:", base, offset
        if offset==0:
            interactions.append((base, 'R'))
        else:
            interactions.append((base, 'RL'))

    return interactions


def unhide(seq_list):
    message=''
    for base, actions in seq_list:
        if base == -1:
            continue
        offset = 0
        if 'RL' in actions:
            offset = 1

        #print "unhide:", base, offset
        message += code_to_str(base, offset)
    return message


def send_message(seq_list, words):
    auth = tweepy.OAuthHandler(config.TWITTER_CONSUMER_KEY, config.TWITTER_CONSUMER_SECRET)
    auth.set_access_token(config.TWITTER_KEY, config.TWITTER_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    def interact(seq):
        target_word = words[seq]
        print "target:", target_word
        for t in tweepy.Cursor(api.search, q=target_word, 
                               include_entities=False, trim_user=True).items():
            
            for w in extract_words(t.text):
                if w not in words:
                    # print "not in list:", w
                    continue
                if w!=words[seq]:
                    # print "wrong tweet:", w
                    break

                try:
                    if 'RL' in actions:
                        print "Retweet & Like:", t.id
                        api.retweet(t.id)
                        api.create_favorite(t.id)
                    else:
                        print "Retweet:", t.id
                        api.retweet(t.id)
                    return
                except Exception,e:
                    print "already retweeted:", t.id
                    print str(e)
                    continue

    for seq, actions in seq_list:
        interact(seq)


def read_message(screen_name, words):

    auth = tweepy.OAuthHandler(config.TWITTER_CONSUMER_KEY, config.TWITTER_CONSUMER_SECRET)
    auth.set_access_token(config.TWITTER_KEY, config.TWITTER_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    interactions = []
    retweets = api.user_timeline(screen_name, count=10)
    favorites = api.favorites(screen_name, count=10)

    for t in reversed(retweets+favorites):
        seq = -1
        for w in extract_words(t.text):
            if w in words:
                try:
                    seq = words.index(w)
                except ValueError:
                    pass
                break

        if t.retweeted and not t.favorited:
            action = "R"
        else:
            action = "RL"   
        interactions.append((seq, action))

    return interactions


