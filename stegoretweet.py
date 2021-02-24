import getpass
import hashlib
import random
import sys
from srt.twitter import load_words, hide, unhide, send_message, read_message


def main():

    if len(sys.argv) < 3:
        print('Usage:')
        print(f'\t{sys.argv[0]} <send> <text>')
        print(f'\t{sys.argv[0]} <send> <text> <hashtag1,hahstag2,hashtagN>')
        print(f'\t{sys.argv[0]} <recv> <user>')
        sys.exit(0)

    words = load_words('db/words.txt')
    pw = getpass.getpass().encode('utf-8')
    hx = hashlib.sha256(pw).hexdigest()
    s = int(hx, 16)
    random.seed(s)
    random.shuffle(words)

    if sys.argv[1] == 'send':
        hashtag_list = []
        if len(sys.argv) == 4:
            hashtag_list = sys.argv[3].split(',')
        hashtag_list += ['']
        seq_list = hide(sys.argv[2].lower())
        send_message(seq_list, words, hashtag_list)

    elif sys.argv[1] == 'recv':
        seq_list = read_message(sys.argv[2], words)
        print(unhide(seq_list))


if __name__ == '__main__':
    main()
