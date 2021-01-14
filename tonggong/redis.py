import signal
import time
import os

from redis import Redis
from redis.lock import Lock, LockError

from tonggong.hash import Hash

_COUNT = 400


def safe_delete_hash(conn: Redis, hash_key: str, count: int = None):
    if not conn.exists(hash_key):
        return
    new_key = f"gc:hash:{Hash.md5(hash_key)}"
    conn.rename(hash_key, new_key)
    cursor = 0
    count = count or _COUNT
    while True:
        cursor, fields = conn.hscan(new_key, cursor, count=count)
        if fields:
            conn.hdel(new_key, *fields)
        if not cursor:
            break
    conn.delete(new_key)


def safe_delete_list(conn: Redis, list_key: str):
    if not conn.exists(list_key):
        return
    new_key = f"gc:list:{Hash.md5(list_key)}"
    conn.rename(list_key, new_key)
    while conn.llen(new_key):
        conn.ltrim(new_key, 0, -99)
    conn.delete(new_key)


def safe_delete_set(conn: Redis, set_key: str, count: int = None):
    if not conn.exists(set_key):
        return
    new_key = f"gc:set:{Hash.md5(set_key)}"
    conn.rename(set_key, new_key)
    cursor = 0
    count = count or _COUNT
    while True:
        cursor, members = conn.sscan(new_key, cursor, count=count)
        if members:
            conn.srem(new_key, *members)
        if not cursor:
            break
    conn.delete(new_key)


def safe_delete_sorted_set(conn: Redis, sorted_set_key: str):
    if not conn.exists(sorted_set_key):
        return
    new_key = f"gc:zset:{Hash.md5(sorted_set_key)}"
    conn.rename(sorted_set_key, new_key)
    while conn.zcard(new_key):
        conn.zremrangebyrank(new_key, 0, 100)
    conn.delete(new_key)


class RedisLock(Lock):
    def __init__(
        self, conn: Redis, name: str, timeout=None, sleep=0.1, blocking=True, blocking_timeout=None, thread_local=True,
    ):
        super(RedisLock, self).__init__(
            conn,
            self.get_key_name(name),
            timeout=timeout,
            sleep=sleep,
            blocking=blocking,
            blocking_timeout=blocking_timeout,
            thread_local=thread_local,
        )
        self._acquired = False

    def __enter__(self):
        token = str(time.time())  # Set token to current time string
        self._acquired = self.acquire(token=token)
        # 保存原始信号处理器
        self.old_sigint = signal.signal(signal.SIGINT, self._handler)
        self.old_sigterm = signal.signal(signal.SIGTERM, self._handler)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            super(RedisLock, self).release()
            self._acquired = False
        except LockError:  # 可能锁已经自动失效释放，忽略 LockError
            pass

    def _handler(self, signum, frame):
        # 释放锁
        try:
            super(RedisLock, self).release()
            self._acquired = False
        except LockError:  # 可能锁已经自动失效释放，忽略 LockError
            pass
        # 还原信号处理器
        signal.signal(signal.SIGINT, self.old_sigint)
        signal.signal(signal.SIGTERM, self.old_sigterm)
        # 发送原始信号
        os.kill(os.getpid(), signum)

    @property
    def acquired(self) -> bool:
        return self._acquired

    @classmethod
    def get_key_name(cls, name: str) -> str:
        """ Get Redis lock key name """
        return f"redis-lock:{name}"
