"""
简单实现的 Base62 编码转化

https://en.wikipedia.org/wiki/Base62
"""

import string

_ALPHABET = string.ascii_uppercase + string.ascii_lowercase + string.digits
_BASE_DICT = dict((c, v) for v, c in enumerate(_ALPHABET))


def encode(n: int) -> str:
    """数值转换编码"""
    if not n:
        return _ALPHABET[0]
    encoding = ""
    num = abs(n)
    while num:
        num, remainder = divmod(num, len(_ALPHABET))
        encoding = _ALPHABET[remainder] + encoding
    return encoding if n >= 0 else "-" + encoding


def decode(s: str) -> int:
    """编码转换数值"""
    num = 0
    flag = True
    if s[0] == "-":
        s = s[1:]
        flag = False
    for char in s:
        if char not in _ALPHABET:
            raise Exception(f"string {char} not surport Base62 coding format")
        num = num * len(_ALPHABET) + _BASE_DICT[char]
    return num if flag else -num
