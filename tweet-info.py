import json
import tweepy
import sys
from srt import config

if len(sys.argv) != 2:
    print(f'Usage: {sys.argv[0]} <tweet id>\n')
    sys.exit(0)

tid = sys.argv[1]
auth = tweepy.OAuthHandler(
    config.TWITTER_CONSUMER_KEY,
    config.TWITTER_CONSUMER_SECRET
)
auth.set_access_token(
    config.TWITTER_TOKEN,
    config.TWITTER_TOKEN_SECRET
)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

print(json.dumps(api.get_status(tid)._json, indent=2))
