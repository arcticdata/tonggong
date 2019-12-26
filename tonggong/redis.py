from redis import Redis
from redis.lock import Lock, LockError


def safe_delete_hash(conn: Redis, hash_key: str):
    raise NotImplementedError


def safe_delete_list(conn: Redis, list_key: str):
    raise NotImplementedError


def safe_delete_set(conn: Redis, set_key: str):
    raise NotImplementedError


def safe_delete_sorted_set(conn: Redis, sorted_set_key: str):
    raise NotImplementedError


class RedisLock(Lock):
    def __init__(self, conn: Redis, name: str,
                 timeout=None, sleep=0.1, blocking=True, blocking_timeout=None, thread_local=True):
        name = 'redis-lock:{}'.format(name)
        super(RedisLock, self).__init__(
            conn, name,
            timeout=timeout, sleep=sleep,
            blocking=blocking, blocking_timeout=blocking_timeout, thread_local=thread_local)
        self._acquired = False

    def __enter__(self):
        self._acquired = self.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            super(RedisLock, self).release()
        except LockError:  # 可能锁已经自动失效释放，忽略 LockError
            pass

    @property
    def acquired(self) -> bool:
        return self._acquired
