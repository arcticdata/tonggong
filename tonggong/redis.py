from redis import Redis
from redis.lock import Lock, LockError


def safe_delete_hash(conn: Redis, hash_key: str):
    # rename the key
    new_key = 'nk:{}'.format(hash_key)
    conn.rename(hash_key, new_key)
    cursor = 0
    while True:
        cursor, fields = conn.hscan(new_key, cursor, count=100)
        if fields:
            conn.hdel(new_key, *fields)
        if not cursor:
            break


def safe_delete_list(conn: Redis, list_key: str):
    # rename the key
    new_key = 'nk:{}'.format(list_key)
    conn.rename(list_key, new_key)
    while conn.llen(new_key):
        conn.ltrim(new_key, 0, -99)


def safe_delete_set(conn: Redis, set_key: str):
    # rename the key
    new_key = 'nk:{}'.format(set_key)
    conn.rename(set_key, new_key)
    cursor = 0
    while True:
        cursor, members = conn.sscan(new_key, cursor, count=100)
        if members:
            conn.srem(new_key, *members)
        if not cursor:
            break


def safe_delete_sorted_set(conn: Redis, sorted_set_key: str):
    # rename the key
    new_key = 'nk:{}'.format(sorted_set_key)
    conn.rename(sorted_set_key, new_key)
    while conn.zcard(new_key):
        conn.zremrangebyrank(new_key, 0, 100)


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
