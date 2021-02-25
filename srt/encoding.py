from srt import config


def str_to_code(s):
    """ Given a  string, it  returns a  tuple with  the base  and  a previously
    calculated offset.

    Attributes:
        :s (string): String to code.
    """

    while len(s) % config.CHARS_X_INTERACTION != 0:
        s += ' '

    x = [config.CHARSET.index(c) for c in s]
    y = [bin(n)[2:].zfill(config.BITS_X_CHAR) for n in x]
    y_str = ''.join(y)
    code = int(y_str, 2)
    base = code / config.AVAILABLE_INTERACTIONS
    offset = code - (base * config.AVAILABLE_INTERACTIONS)

    return base, offset


def code_to_str(base, offset):
    code = base * config.AVAILABLE_INTERACTIONS + offset
    bits = [int(x) for x in list("{0:012b}".format(code))]
    chars = ''
    for i in range(0, len(bits), config.BITS_X_CHAR):
        c_bits = bits[i:i+config.BITS_X_CHAR]
        c_bits_str = ''.join(map(str, c_bits))
        chars += config.CHARSET[(int(c_bits_str, 2))]
    return chars
