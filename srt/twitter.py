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


def send_message(seq_list, words, hashtag_list):
    logging.basicConfig()
    auth = tweepy.OAuthHandler(config.TWITTER_CONSUMER_KEY, config.TWITTER_CONSUMER_SECRET)
    auth.set_access_token(config.TWITTER_KEY, config.TWITTER_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    def interact(seq, hashtag):
        target = words[seq]
        if len(hashtag)>0:
            target += ' #'+hashtag
        for t in tweepy.Cursor(api.search, q=target, 
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
                        api.retweet(t.id)
                        api.create_favorite(t.id)
                        print "Retweet & Like:", t.id, ", search:", target
                    else:
                        api.retweet(t.id)
                        print "Retweet:", t.id, ", search:", target
                    return True
                except Exception,e:
                    #print "already retweeted:", t.id
                    #print str(e)
                    continue
        return False

    for seq, actions in seq_list:
        print seq
        for hashtag in hashtag_list:
            print "using hashtag:", hashtag
            if interact(seq, hashtag):
                break


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


