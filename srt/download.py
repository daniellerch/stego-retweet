#!/usr/bin/python

import os
import sys
import json
import re
import time
import hashlib
import datetime
import cookielib
import urllib
import urllib2
from pyquery import PyQuery
from srt import config

n_tweets = config.NUM_MESSAGES 

def update_progress(progress, cnt):
    sys.stdout.write('\r{0:.2f}%: {1} of {2} (total: {3})'.format(100*float(progress)/n_tweets, progress, n_tweets, cnt))
    sys.stdout.flush()

def get_tweets(search_string, tweets_path):

    seq_dict = {}
    seq_count = 0

    cookieJar = cookielib.CookieJar() 
    url = "https://twitter.com/i/search/timeline?f=tweets&q=%s&src=typd&max_position=%s"

    cnt = 0
    refreshCursor = 0
    while seq_count < n_tweets:

        try:
            current_url = url % (search_string, refreshCursor)

            headers = [
                ('Host', "twitter.com"),
                ('User-Agent', "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"),
                ('Accept', "application/json, text/javascript, */*; q=0.01"),
                ('Accept-Language', "de,en-US;q=0.7,en;q=0.3"),
                ('X-Requested-With', "XMLHttpRequest"),
                ('Referer', current_url),
                ('Connection', "keep-alive")
            ]

            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar)) 
            opener.addheaders = headers

            response = opener.open(current_url) 
            jsonResponse = response.read()
            dataJson = json.loads(jsonResponse)


            last_refreshCursor = refreshCursor
            refreshCursor = dataJson['min_position']  
            if refreshCursor==last_refreshCursor:
                break;
            

            scrapedTweets = PyQuery(dataJson['items_html'])
            scrapedTweets.remove('div.withheld-tweet')
            tweets = scrapedTweets('div.js-stream-tweet')

            if len(tweets)==0:
                break


            for tweetHTML in tweets:
                tweetPQ = PyQuery(tweetHTML)

                usernameTweet = tweetPQ("span:first.username.u-dir b").text()
                txt = re.sub(r"\s+", " ", tweetPQ("p.js-tweet-text").text().replace('# ', '#').replace('@ ', '@'))
                retweets = int(tweetPQ("span.ProfileTweet-action--retweet span.ProfileTweet-actionCount").attr("data-tweet-stat-count").replace(",", ""))
                favorites = int(tweetPQ("span.ProfileTweet-action--favorite span.ProfileTweet-actionCount").attr("data-tweet-stat-count").replace(",", ""))
                dateSec = int(tweetPQ("small.time span.js-short-timestamp").attr("data-time"))
                id = tweetPQ.attr("data-tweet-id")
                permalink = tweetPQ.attr("data-permalink-path")

                cnt +=1

                d = {}
                d["id"] = id
                d["username"] = usernameTweet
                d["text"] = txt
                d["retweets"] = retweets
                d["favorites"] = favorites
                d["date"] = dateSec
                d["link"] = permalink

                hx = hashlib.md5(txt.encode('utf-8')).hexdigest()
                seq = int(hx, 16)%n_tweets
                #seq = dateSec % n_tweets
                if seq not in seq_dict:
                    seq_dict[seq]=True
                    seq_count += 1
                    with open(tweets_path, 'a+') as f:
                        f.write(json.dumps(d)+'\n')

                update_progress(seq_count, cnt)
         
                if seq_count >= n_tweets-1:
                    return

        except KeyboardInterrupt:
            sys.exit(0)
        except:
            refreshCursor=0
            print "\nerror! retry\n"
            time.sleep(10)
            continue

