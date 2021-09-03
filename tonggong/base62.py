import string


"""
简单实现的 Base62 编码转化

https://en.wikipedia.org/wiki/Base62
"""

_BASE_ALPH = tuple(string.ascii_uppercase + string.ascii_lowercase + string.digits)
_BASE_DICT = dict((c, v) for v, c in enumerate(_BASE_ALPH))
_BASE_LEN = len(_BASE_ALPH)


def encode(n: int) -> str:
    """数值转换编码"""
    if not n:
        return _BASE_ALPH[0]
    encoding = ""
    while n:
        n, remainder = divmod(n, _BASE_LEN)
        encoding = _BASE_ALPH[remainder] + encoding
    return encoding


def decode(s: str) -> int:
    """编码转换数值"""
    num = 0
    for char in s:
        if char not in _BASE_ALPH:
            raise Exception(f"string {char} not surport Base62 coding format")
        num = num * _BASE_LEN + _BASE_DICT[char]
    return num
