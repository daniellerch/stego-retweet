import logging
import textwrap
import tweepy
from srt import config
from srt.encoding import str_to_code, code_to_str

log = logging.getLogger(__name__)


def extract_words(text):
    """ Returns a list with all processed words in a text.

    Attributes:
        :text (str): Text to process all words.
    """

    log.debug('Extracting words from text.')
    text = text.lower()
    text = text.replace('#', '')
    words = text.split()
    result = []

    for w in words:
        if len(w) < 4:
            continue
        if '@' in w:
            continue
        if '/' in w:
            continue
        result.append(w)

    return result


def load_words(path):
    """ Returns a list with all words in file splitted by line.

    Attributes:
        :path (str):    Path to file with words to load.
    """

    log.debug(f'Loading words from file "{path}".')

    with open(path, 'r') as f:
        w = f.read().splitlines()
        return w
    return []


def hide(msg):
    """ Returns a list of tuples (base, R) for each msg chunk.

    Attributes:
        :msg (str): Message to hide.
    """

    log.debug(f'Hidding message "{msg}".')
    tw = textwrap.wrap(
        msg,
        config.CHARS_X_INTERACTION,
        drop_whitespace=False
    )

    interactions = []
    for chunk in tw:
        base, offset = str_to_code(chunk)
        log.debug(f'hide: [chunk: {chunk}, base: {base}, offset: {offset}]')
        interactions.append((base, 'R'))

    log.debug(f'interactions: {interactions}')

    return interactions


def unhide(seq_list):
    message = ''
    for base in seq_list:
        if base == -1:
            continue
        offset = 0
        message += code_to_str(base, offset)
    return message


def get_api():
    """ Returns Twitter API object. """

    auth = tweepy.OAuthHandler(
        config.TWITTER_CONSUMER_KEY,
        config.TWITTER_CONSUMER_SECRET
    )
    auth.set_access_token(
        config.TWITTER_TOKEN,
        config.TWITTER_TOKEN_SECRET
    )
    return tweepy.API(
        auth,
        wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True
    )


def send_message(seq_list, words, hashtag_list):
    """
    Attributes:
        :seq_list (lst):        List of tuples os sequence and actions.
        :words (lst):           List of words.
        :hashtag_list (lst):    List of hashtag given.
    """

    api = get_api()

    def interact(seq, hashtag):
        target = words[seq]
        if len(hashtag) > 0:
            target += ' #'+hashtag
        for t in tweepy.Cursor(
            api.search,
            q=target,
            include_entities=False,
            trim_user=True
        ).items():

            for w in extract_words(t.text):
                if w not in words:
                    log.debug('Not in list: {w}')
                    continue
                if w != words[seq]:
                    log.debug('Wrong tweet: {w}')
                    break

                try:
                    api.retweet(t.id)
                    print(f'Retweet: {t.id}, search: {target}')
                    return True
                except Exception as e:
                    log.debug('Already retweeted: {t.id}')
                    log.error(e)
                    continue
        return False

    for seq, actions in seq_list:
        for hashtag in hashtag_list:
            log.debug(f'hashtag: {hashtag}, seq: {seq}, actions: {actions}')
            if interact(int(seq), hashtag):
                break


def read_message(screen_name, words):
    api = get_api()

    interactions = []
    retweets = api.user_timeline(screen_name, count=10)

    for t in reversed(retweets):
        seq = -1
        for w in extract_words(t.text):
            if w in words:
                try:
                    seq = words.index(w)
                except ValueError:
                    pass
                break

        interactions.append(seq)

    return interactions
