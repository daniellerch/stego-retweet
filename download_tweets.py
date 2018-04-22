#!/usr/bin/python

import os
import sys
import json
import re
import time
import datetime
import cookielib
import urllib
import urllib2
from pyquery import PyQuery


n_tweets = 65535
#n_tweets = 1000

def update_progress(progress):
    sys.stdout.write('\r{0:.2f}%: {1} of {2}'.format(100*float(progress)/n_tweets, progress, n_tweets))
    sys.stdout.flush()

def download(search_string, dateMax, tweets_path):
    cookieJar = cookielib.CookieJar() 
    url = "https://twitter.com/i/search/timeline?f=tweets&q=%s&src=typd&max_position=%s"

    timeMax = int(time.mktime(datetime.datetime.strptime(dateMax, "%Y-%m-%d").timetuple()))


    cnt = 0
    refreshCursor = 0
    while cnt < n_tweets:
        current_url = url % (search_string.replace(' ', '%20')+'%20until%3A'+dateMax, refreshCursor)

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

            if dateSec > timeMax+86400:
                print "--> ignore", dateSec, timeMax
                continue

            cnt +=1

            d = {}
            d["id"] = id
            d["username"] = usernameTweet
            d["text"] = txt
            d["retweets"] = retweets
            d["favorites"] = favorites
            d["date"] = dateSec
            d["link"] = permalink

            update_progress(cnt)
            with open(tweets_path, 'a+') as f:
                f.write(json.dumps(d)+'\n')

            if cnt >= n_tweets-1:
                return


def main():

    if len(sys.argv) != 4:
        print "Usage: "
        print "   %s <search string> <max date: Y-m-d> <tweets file>" % (sys.argv[0])
        print ""
        print "Example:"
        print "   %s '#crypto' '2018-01-01' 'tweets.db'" % (sys.argv[0])
        print 
        sys.exit(0)

    if os.path.isfile(sys.argv[3]):
        os.remove(sys.argv[3])
    download(sys.argv[1], sys.argv[2], sys.argv[3])

if __name__ == "__main__":
    main()


