import os
import signal
import time

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
        self,
        conn: Redis,
        name: str,
        timeout=None,
        sleep=0.1,
        blocking=True,
        blocking_timeout=None,
        thread_local=True,
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
        self._prev_sigint = None
        self._prev_sigterm = None

    def __enter__(self):
        token = str(time.time())  # Set token to current time string
        self._acquired = self.acquire(token=token)
        self._register_signal_handler()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
        self._restore_signal_handler()

    def _signal_handler(self, signum, frame):
        """信号处理函数，保证退出前释放锁"""
        self.release()
        self._restore_signal_handler()
        # 继续向外发送信号
        os.kill(os.getpid(), signum)

    @property
    def acquired(self) -> bool:
        return self._acquired

    @classmethod
    def get_key_name(cls, name: str) -> str:
        """Get Redis lock key name"""
        return f"redis-lock:{name}"

    def release(self):
        try:
            super(RedisLock, self).release()
        except LockError:  # 可能锁已经自动失效释放，忽略 LockError
            pass

    def _register_signal_handler(self):
        """接管信号处理函数"""
        self._prev_sigint = signal.signal(signal.SIGINT, self._signal_handler)
        self._prev_sigterm = signal.signal(signal.SIGTERM, self._signal_handler)

    def _restore_signal_handler(self):
        """还原信号处理函数"""
        if self._prev_sigint is not None:
            signal.signal(signal.SIGINT, self._prev_sigint)
        if self._prev_sigterm is not None:
            signal.signal(signal.SIGTERM, self._prev_sigterm)
