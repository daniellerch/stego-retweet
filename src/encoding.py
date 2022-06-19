"""
stego-retweet.
"""
from random import randint

from src import config


def str_to_code(string: str) -> tuple:
    """ Given a string, it returns a tuple with the base and a previously calculated offset.
    :param string: String to code.
    """
    while len(string) % config.CHARS_X_INTERACTION != 0:
        string += ' '

    char = [config.CHARSET.index(c) for c in string]
    bin_char = [bin(n)[2:].zfill(config.BITS_X_CHAR) for n in char]
    str_char = ''.join(bin_char)
    code = int(str_char, 2)
    base = code / config.AVAILABLE_INTERACTIONS
    offset = code - (base * config.AVAILABLE_INTERACTIONS)

    return int(base), int(offset)


def get_char(index: int) -> str:
    """ Given an index, returns one char from CHARSET. If index is out of range returns a char with random index.
    :param index: CHARSET index to get one char.
    """
    try:
        return config.CHARSET[index]
    except IndexError:
        return config.CHARSET[randint(0, len(config.CHARSET) - 1)]


def code_to_str(base: int) -> str:
    """ Given a base number, converts it to bits and divides it into two parts. From each part obtains its value as
    integer and its equivalent character. Finally, it returns two characters, one for each BITS_X_CHAR bits.
    :param base: Integer to convert to bits.
    """
    code = base * config.AVAILABLE_INTERACTIONS
    len_bits = config.BITS_X_CHAR * 2
    bits = [int(b) for b in bin(code)[2:].zfill(len_bits)]
    bits_str = ''.join(str(bit) for bit in bits)
    char1_index = int(bits_str[:config.BITS_X_CHAR], 2)
    char2_index = int(bits_str[config.BITS_X_CHAR:], 2)
    char1 = get_char(char1_index)
    char2 = get_char(char2_index)

    return f'{char1}{char2}'
