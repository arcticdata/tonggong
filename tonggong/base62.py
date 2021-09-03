"""
简单实现的 Base62 编码转化

https://en.wikipedia.org/wiki/Base62
"""

BASE_ALPH = tuple("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
BASE_DICT = dict((c, v) for v, c in enumerate(BASE_ALPH))
BASE_LEN = len(BASE_ALPH)


def encode(n: int) -> str:
    """数值转换编码"""
    if not n:
        return BASE_ALPH[0]
    encoding = ""
    while n:
        n, remainder = divmod(n, BASE_LEN)
        encoding = BASE_ALPH[remainder] + encoding
    return encoding


def decode(s: str) -> int:
    """编码转换数值"""
    num = 0
    for char in s:
        if char not in BASE_ALPH:
            print(f"该字符{char}不符合Base62编码格式")
            return -1
        num = num * BASE_LEN + BASE_DICT[char]
    return num


for i in range(100):
    print(i, decode(encode(i)), encode(i))
