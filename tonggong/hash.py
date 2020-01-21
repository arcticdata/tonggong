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

    @staticmethod
    def file_md5(_path: str) -> str:
        """ 计算文件的 md5 值 """
        hash_md5 = hashlib.md5()
        with open(_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
