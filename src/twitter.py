"""
stego-retweet.
"""
import textwrap
import tweepy

from src import config, logger
from src.encoding import str_to_code, code_to_str

log = logger.get_logger(__name__)


def extract_words(tweet: str) -> list:
    """ Returns a list with all processed words in a tweet.
    :param tweet: Tweet text to process all words.
    """
    log.debug('Extracting words from tweet.')
    words = tweet.replace('#', '').lower().split()
    result = []

    for word in words:
        if len(word) < 4 or '@' in word or '/' in word:
            continue
        result.append(word)

    return result


def load_words(path: str) -> list:
    """ Returns a list with all words in file split by line.
    :param path: Path to file with words to load.
    """
    try:
        log.debug(f"Loading words from file '{path}'.")
        with open(path, 'r', encoding='UTF-8') as file:
            words = file.read().splitlines()
            return words
    except OSError:
        log.error(f"Could not open file '{path}'.")
        return []


def hide(msg: str) -> list:
    """ Returns a list of integers, one for each msg chunk.
    :param msg: Message to hide.
    """
    log.debug(f"Hidding message '{msg}'.")
    text_wrap = textwrap.wrap(msg, config.CHARS_X_INTERACTION, drop_whitespace=False)
    interactions = []

    for chunk in text_wrap:
        base, offset = str_to_code(chunk)
        log.debug(f'hide: [chunk: {chunk}, base: {base}, offset: {offset}]')
        interactions.append(base)

    log.debug(f'interactions: {interactions}')

    return interactions


def unhide(seq_list: list) -> str:
    """ It receives a list of indexes and uses each of these indexes to build a plain text message.
    :param seq_list: List of indexes.
    """
    log.info('Unhiding secret message.')

    message = ''
    for base in seq_list:
        if base == -1:
            continue
        message += code_to_str(base)

    return message


def get_api() -> tweepy.API:
    """ Returns Twitter API object. """
    auth = tweepy.OAuthHandler(config.TWITTER_CONSUMER_KEY, config.TWITTER_CONSUMER_SECRET)
    auth.set_access_token(config.TWITTER_TOKEN, config.TWITTER_TOKEN_SECRET)

    return tweepy.API(auth, wait_on_rate_limit=True)


def send_message(seq_list: list, words: list, hashtag_list: list) -> None:
    """ Try to retweet those tweets that have a series of characteristics.
    :para seq_list: List of integers.
    :para words: List of words.
    :para hashtag_list: List of hashtag given.
    """
    api = get_api()

    def interact(seq_index: int, hashtag_target: str) -> bool:
        """ This function looking for tweets that contain a specific target. Then, for every tweet found, it lists
        all its words and searches one by one if they are in the word list. If it is in the list, if the word is the
        same as the target. If the word is not equal to the target, discard the tweet and search the next one. If on the
        contrary the word is equal to the target, proceed to retweet. Finally, if retweet returns True, else returns
        False.
        :param seq_index: Index to search word in list of words.
        :param hashtag_target: Hashtag to include in tagert if is not empty.
        """

        target = words[seq_index]

        if len(hashtag_target) > 0:
            target += ' #' + hashtag_target

        log.debug(f"Looking for tweets that contain target '{target}'.")

        twitter_query_response = tweepy.Cursor(api.search_tweets, q=target, include_entities=False).items()

        for tweet in twitter_query_response:

            log.debug(f"Tweet with id '{tweet.id}' founded with target '{target}'!")

            for word in extract_words(tweet.text):
                log.debug(f"Checking if word '{word}' is in list of words.")

                if word not in words:
                    log.debug(f"Word '{word}' not in list of words, check next.")
                    continue

                log.debug(f"Yeah! Word '{word}' in list of words!")
                log.debug(f"Checking if word '{word}' is equal than target.")

                if word != target:
                    log.debug(f"Word '{word}' is not equal than target '{target}'. Trying with another tweet.")

                    break

                log.debug(f"Yeah! Word '{word}' is equal than taget '{target}'.")
                log.debug('Trying to retweet.')

                try:
                    api.retweet(tweet.id)
                    out = f"Tweet with id '{tweet.id}' containing the target '{target}' successfully retweeted!"
                    log.info(out)
                    print(out)

                    return True
                except Exception as err:
                    log.debug(f"Tweet with id '{tweet.id}' already retweeted.")
                    log.error(err)
                    continue

        log.debug(f"Tweet with target '{target}' not found, jump to next hashtag.")

        return False

    for seq in seq_list:
        for hashtag in hashtag_list:
            log.debug(f"hashtag: '{hashtag}', seq: '{seq}'.")

            if interact(seq, hashtag):
                break


def read_message(sender_twitter_user: str, words: list, count: int) -> list:
    """ This function searches the last 10 retweets for a specific user. Then for each retweet found, it lists all of
    your words and searches one by one if they are in the word list. If it's in the list, it stores the index of the
    word in a list. Finally, it returns the list of indexes.
    :param sender_twitter_user: Sender Twitter account name, without @.
    :param words: List of words.
    :param count: Number of recent retweets to search hidden information.
    """
    api = get_api()
    interactions = []

    log.debug(f"Looking for retweets in '{sender_twitter_user}' user timeline.")
    retweets = api.user_timeline(screen_name=sender_twitter_user, count=count)

    for tweet in reversed(retweets):
        seq = -1
        word = ''
        for word in extract_words(tweet.text):
            log.debug(f"Check if word '{word}' is in list of words.")

            if word in words:
                try:
                    seq = words.index(word)
                except ValueError:
                    pass

                log.debug(f"Yeah! Word '{word}' in list of words!")

                break
        log.debug(f"Appending seq '{seq}' from word '{word}' to list of interactions.")

        interactions.append(seq)

    log.debug(f'interactions: {interactions}')

    return interactions
