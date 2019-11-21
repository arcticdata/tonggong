import hashlib


class Hash(object):
    @staticmethod
    def md5(value: str) -> str:
        return hashlib.md5(value.encode()).hexdigest()

    @staticmethod
    def sha1(value: str) -> str:
        return hashlib.sha1(value.encode()).hexdigest()

    @staticmethod
    def sha256(value: str) -> str:
        return hashlib.sha256(value.encode()).hexdigest()
