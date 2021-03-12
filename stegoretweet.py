import argparse
import getpass
import hashlib
import logging
import os
import random

from logging.handlers import RotatingFileHandler
from srt import config
from srt.twitter import load_words, hide, unhide, send_message, read_message

log = logging.getLogger(__name__)


def config_logging():
    log_formatter = logging.Formatter(
        '%(asctime)-15s [%(levelname)s] %(funcName)s(%(lineno)d) %(message)s'
    )
    handler = RotatingFileHandler(
        f'{config.LOG_PATH}/stego-retweet.log',
        mode='a',
        maxBytes=config.LOG_MAX_MEGABYTES * 1024 * 1024,  # Megabytes
        backupCount=config.LOG_MAX_FILES,
        encoding=None,
        delay=0
    )
    handler.setFormatter(log_formatter)
    handler.setLevel(config.TRACE_LEVEL)

    log.addHandler(handler)
    log.setLevel(config.TRACE_LEVEL)


def get_args():
    parser = argparse.ArgumentParser(
        description='Stego-retweet is a tool for hiding messages in Twitter \
using retweets. With this tool you can hide two chars per retweet.'
    )

    parser.add_argument(
        '-m',
        '--mode',
        help='Mode of execution, to send or recieve messages.',
        choices=['send', 'recv']
    )

    parser.add_argument(
        '-s',
        '--secret',
        help='Secret to hide.'
    )

    parser.add_argument(
        '-ht',
        '--hashtags',
        help='List of hashtags.',
        type=str
    )

    parser.add_argument(
        '-a',
        '--account',
        help='Sender twitter account name, without @.',
        type=str
    )

    parser.add_argument(
        '-r',
        '--retweets',
        help='Number of recent retweets to search hidden information.',
        type=int
    )

    args = parser.parse_args()

    if args.mode == 'send' and args.account:
        parser.error('--account can only be set when --mode=recv.')
    if args.mode == 'send' and args.retweets:
        parser.error('--retweets can only be set when --mode=recv.')
    if args.mode == 'send' and not args.secret:
        parser.error('--secret it\'s mandatory when --mode=recv.')

    if args.mode == 'recv' and args.secret:
        parser.error('--secret can only be set when --mode=send.')
    if args.mode == 'recv' and args.hashtags:
        parser.error('--hashtags can only be set when --mode=send.')
    if args.mode == 'recv' and not args.account:
        parser.error('--account it\'s mandatory when --mode=recv.')
    if args.mode == 'recv' and not args.retweets:
        parser.error('--retweets it\'s mandatory when --mode=recv.')

    return args


def main():

    if not os.path.exists(config.LOG_PATH):
        os.makedirs(config.LOG_PATH)

    config_logging()

    args = get_args()
    words = load_words('db/words.txt')
    password = getpass.getpass().encode('utf-8')
    password_hex = hashlib.sha256(password).hexdigest()
    password_int = int(password_hex, 16)
    random.seed(password_int)
    random.shuffle(words)

    if args.mode == 'send':
        msg = args.secret
        hashtag_list = []
        if args.hashtags:
            hashtag_list = args.hashtags.split(',')
        hashtag_list += ['']
        seq_list = hide(msg.lower())
        send_message(seq_list, words, hashtag_list)

    if args.mode == 'recv':
        seq_list = read_message(args.account, words, args.retweets)
        print(unhide(seq_list))


if __name__ == '__main__':
    main()
