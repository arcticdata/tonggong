import random
import uuid


class Generator(object):
    """随机数据生成器"""

    @staticmethod
    def uuid4() -> str:
        return uuid.uuid4().hex

    @staticmethod
    def pincode(length: int = 6) -> str:
        max_int = 10 ** length - 1
        return "{:0{length}d}".format(random.randint(1, max_int), length=length)

    @staticmethod
    def phone() -> str:
        return "1{:010d}".format(random.randint(1, 9999999999))
