#!/usr/bin/python


import sys
import json
import re
import datetime
import cookielib
import urllib
import urllib2


from pyquery import PyQuery


cookieJar = cookielib.CookieJar() 
url = "https://twitter.com/i/search/timeline?f=tweets&q=%s&src=typd&max_position=%s"

n_tweets = 65535
n_tweets = 70000
cnt = 0
refreshCursor = 0
#for i in range(10):
while cnt <= n_tweets:
    current_url = url % ('saturday', refreshCursor)

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
        print json.dumps(d)

           
