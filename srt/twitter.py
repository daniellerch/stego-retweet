import logging
import textwrap
import tweepy
from srt import config
from srt.encoding import str_to_code, code_to_str

log = logging.getLogger(__name__)


def extract_words(tweet):
    """ Returns a list with all processed words in a tweet.

    Attributes:
        :tweet (str): Tweet text to process all words.
    """

    log.debug('Extracting words from tweet.')
    words = tweet.replace('#', '').lower().split()
    result = []

    for word in words:
        if len(word) < 4 or '@' in word or '/' in word:
            continue
        result.append(word)

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
    """ Try to retweet those tweets that have a series of characteristics.

    Attributes:
        :seq_list (lst):        List of tuples os sequence and actions.
        :words (lst):           List of words.
        :hashtag_list (lst):    List of hashtag given.
    """

    api = get_api()

    def interact(seq, hashtag):
        """ This function looking  for tweets  that contain  a specific target.
        Then, for every tweet found, it lists all its words and searches one by
        one if they are in the word list.  If it is in the list, if the word is
        the same as the target. If the word is not equal to the target, discard
        the tweet and search the next one. If on the contrary the word is equal
        to the target, proceed  to retweet.  Finally, if retweet  returns True,
        else returns False.

        Attributes:
            :seq (int):     Index to search word in list of words.
            :hashtag (str): Hashtag to include in tagert if is not empty.
        """

        target = words[seq]

        if len(hashtag) > 0:
            target += ' #' + hashtag

        log.debug(f'Looking for tweets that contain target "{target}".')
        input()

        for tweet in tweepy.Cursor(
            api.search,
            q=target,
            include_entities=False,
            trim_user=True
        ).items():

            log.debug(
                f'Tweet with id "{tweet.id}" founded with target "{target}"!'
            )
            input()

            for word in extract_words(tweet.text):
                log.debug(f'Check if word "{word}" is in list of words.')
                input()
                if word not in words:
                    log.debug(
                        f'Word "{word}" not in list of words, check next.'
                    )
                    input()
                    continue

                log.debug(f'Yeah! Word "{word}" in list of words!')
                input()
                log.debug(f'Check if word "{word}" is equal than target.')
                input()
                if word != target:
                    log.debug(
                        f'Oh fuck! Word "{word}" is not equal than target \
"{target}". Trying with another tweet.'
                    )
                    input()
                    break

                log.debug(
                    f'Yeah! Word "{word}" is equal than taget "{target}".'
                )
                log.debug('Trying to retweet.')
                input()
                try:
                    api.retweet(tweet.id)
                    out = f'Tweet with id "{tweet.id}" successfully retweeted!'
                    log.debug(out)
                    print(out)
                    input()
                    return True
                except Exception as e:
                    log.debug(f'Tweet with id "{tweet.id}" already retweeted.')
                    log.error(e)
                    continue

        log.debug(
            f'Tweet with target "{target}" not found, check next hashtag.'
        )
        input()
        return False

    for seq, actions in seq_list:
        for hashtag in hashtag_list:
            log.debug(
                f'hashtag: "{hashtag}", seq: "{seq}", actions: "{actions}"'
            )
            input()
            if interact(seq, hashtag):
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
