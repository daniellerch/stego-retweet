import os

TRACE_LEVEL = os.getenv('TRACE_LEVEL', 'INFO')
LOG_PATH = os.getenv('LOG_PATH', 'log')
LOG_MAX_MEGABYTES = int(os.getenv('LOG_MAX_BYTES', 5))
LOG_MAX_FILES = int(os.getenv('LOG_MAX_FILES', 3))
LOG_FORMATTER = '%(asctime)-15s [%(levelname)s] %(funcName)s() %(message)s'

CHARSET = "abcdefghijklmnopqrstuvwxyz0123456789 '.,:?!/-+=<>$_*()@#|%&[]{}^"
BITS_X_CHAR = 6
CHARS_X_INTERACTION = 2
AVAILABLE_INTERACTIONS = 1
NUM_MESSAGES = (len(CHARSET) ** CHARS_X_INTERACTION) / \
    AVAILABLE_INTERACTIONS + 1

TWITTER_CONSUMER_KEY = 'XXX'
TWITTER_CONSUMER_SECRET = 'XXX'
TWITTER_TOKEN = 'XXX'
TWITTER_TOKEN_SECRET = 'XXX'
