import getpass
import hashlib
import logging
import os
import random
import sys
from srt import config
from srt.twitter import load_words, hide, unhide, send_message, read_message

log = logging.getLogger(__name__)


def main():
    if not os.path.exists(config.LOG_PATH):
        os.makedirs(config.LOG_PATH)

    logging.basicConfig(
        filename=f'{config.LOG_PATH}/stego-retweet.log',
        level=logging.getLevelName(config.TRACE_LEVEL),
        format='%(asctime)-15s  [%(levelname)s] %(message)s'
    )

    if len(sys.argv) < 3:
        print('Usage:')
        print(f'\t{sys.argv[0]} <send> <text>')
        print(f'\t{sys.argv[0]} <send> <text> <hashtag1,hahstag2,hashtagN>')
        print(f'\t{sys.argv[0]} <recv> <user>')
        sys.exit(1)

    words = load_words('db/words.txt')
    password = getpass.getpass().encode('utf-8')
    password_hex = hashlib.sha256(password).hexdigest()
    password_int = int(password_hex, 16)
    random.seed(password_int)
    random.shuffle(words)

    if sys.argv[1] == 'send':
        msg = sys.argv[2]
        hashtag_list = []
        if len(sys.argv) == 4:
            hashtag_list = sys.argv[3].split(',')
        hashtag_list += ['']
        seq_list = hide(msg.lower())
        send_message(seq_list, words, hashtag_list)

    elif sys.argv[1] == 'recv':
        sender_twitter_user = sys.argv[2]
        count = sys.argv[3]
        seq_list = read_message(sender_twitter_user, words, count)
        print(unhide(seq_list))


if __name__ == '__main__':
    main()
