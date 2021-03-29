from srt import config


def str_to_code(s):
    """ Given a  string, it  returns a  tuple with  the base  and  a previously
    calculated offset.

    Attributes:
        :s (str): String to code.
    """

    while len(s) % config.CHARS_X_INTERACTION != 0:
        s += ' '

    x = [config.CHARSET.index(c) for c in s]
    y = [bin(n)[2:].zfill(config.BITS_X_CHAR) for n in x]
    y_str = ''.join(y)
    code = int(y_str, 2)
    base = code / config.AVAILABLE_INTERACTIONS
    offset = code - (base * config.AVAILABLE_INTERACTIONS)

    return int(base), int(offset)


def code_to_str(base):
    """ Given a base number, converts it to bits and divides it into two parts.
    From each part  obtains its value as integer  and its equivalent character.
    Finally it returns two characters, one for each BITS_X_CHAR bits.

    Attributes:
        :base (int): Integer to convert to bits.
    """

    code = base * config.AVAILABLE_INTERACTIONS
    len_bits = config.BITS_X_CHAR * 2
    bits = [int(b) for b in bin(code)[2:].zfill(len_bits)]
    bits_str = ''.join(str(bit) for bit in bits)
    char1 = int(bits_str[:config.BITS_X_CHAR], 2)
    char2 = int(bits_str[config.BITS_X_CHAR:], 2)

    return f'{config.CHARSET[char1]}{config.CHARSET[char2]}'
