import time
import unittest

import redis

from tonggong.generator import Generator
from tonggong.hash import Hash
from tonggong.redis import (
    RedisLock,
    safe_delete_hash,
    safe_delete_list,
    safe_delete_set,
    safe_delete_sorted_set,
)


class RedisTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.conn = redis.Redis()

    def test_safe_delete_hash(self):
        key = Generator.uuid4()
        mapping = {format(i): i for i in range(10000)}
        self.conn.hset(key, mapping=mapping)
        self.assertEqual(self.conn.hlen(key), 10000)
        safe_delete_hash(self.conn, key)
        self.assertFalse(self.conn.exists(key))
        self.assertFalse(self.conn.exists("gc:hash:{}".format(Hash.md5(key))))

    def test_safe_delete_list(self):
        key = Generator.uuid4()
        self.conn.lpush(key, *range(10000))
        self.assertEqual(self.conn.llen(key), 10000)
        safe_delete_list(self.conn, key)
        self.assertFalse(self.conn.exists(key))
        self.assertFalse(self.conn.exists("gc:list:{}".format(Hash.md5(key))))

    def test_safe_delete_set(self):
        key = Generator.uuid4()
        self.conn.sadd(key, *range(10000))
        self.assertEqual(self.conn.scard(key), 10000)
        safe_delete_set(self.conn, key)
        self.assertFalse(self.conn.exists(key))
        self.assertFalse(self.conn.exists("gc:set:{}".format(Hash.md5(key))))

    def test_safe_delete_sorted_set(self):
        key = Generator.uuid4()
        mapping = {i: "{}".format(i) for i in range(10000)}
        self.conn.zadd(key, mapping)
        self.assertEqual(self.conn.zcard(key), 10000)
        safe_delete_sorted_set(self.conn, key)
        self.assertFalse(self.conn.exists(key))
        self.assertFalse(self.conn.exists("gc:zset:{}".format(Hash.md5(key))))

    def test_redis_lock(self):
        lock_key = Generator.uuid4()

        # test non blocking
        with RedisLock(self.conn, lock_key) as one:
            self.assertTrue(one.acquired)
            with RedisLock(self.conn, lock_key, blocking=False) as two:
                self.assertFalse(two.acquired)

        # test timeout
        with RedisLock(self.conn, lock_key, timeout=1) as one:
            self.assertTrue(one.acquired)
            time.sleep(1.00001)
            with RedisLock(self.conn, lock_key, blocking=False) as two:
                self.assertTrue(two.acquired)
