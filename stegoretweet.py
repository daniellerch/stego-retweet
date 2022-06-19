"""
stego-retweet.
"""
import argparse
import getpass
import hashlib
import random

from src import logger
from src.twitter import load_words, hide, unhide, send_message, read_message

log = logger.get_logger(__name__)


def get_args() -> tuple:
    """
    Function to parse program arguments.
    """
    parser = argparse.ArgumentParser(
        description='Stego-retweet is a tool for hiding messages in Twitter using retweets. With this tool you can \
hide two chars per retweet.'
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

    return args, parser


def main() -> None:
    """
    Main function.
    """
    log.info('Starting program.')

    args, parser = get_args()

    if args.mode in {'send', 'recv'}:
        words = load_words('db/words.txt')
        password = getpass.getpass().encode('utf-8')
        password_hex = hashlib.sha256(password).hexdigest()
        password_int = int(password_hex, 16)
        random.seed(password_int)
        random.shuffle(words)

        if args.mode == 'send':
            msg = args.secret
            hashtag_list = args.hashtags.split(',') + [''] if args.hashtags else ['']
            seq_list = hide(msg.lower())
            send_message(seq_list, words, hashtag_list)

        elif args.mode == 'recv':
            seq_list = read_message(args.account, words, args.retweets)
            print(unhide(seq_list))
    else:
        parser.error('Please, provide some arguments')

    log.info('Finishing program.')


if __name__ == '__main__':
    main()
