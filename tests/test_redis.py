import unittest

import redis

from tonggong.generator import Generator
from tonggong.redis import *


class RedisTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.conn = redis.Redis(host='localhost', port=6379, db=0)

    def test_safe_delete_hash(self):
        key = Generator.uuid4()
        mapping = {'{}'.format(i): i for i in range(10000)}
        self.conn.hmset(key, mapping)
        self.assertEqual(self.conn.hlen(key), 10000)
        safe_delete_hash(self.conn, key)
        self.assertFalse(self.conn.exists(key))
        self.assertFalse(self.conn.exists('gc:hash:{}'.format(Hash.md5(key))))

    def test_safe_delete_list(self):
        key = Generator.uuid4()
        self.conn.lpush(key, *range(10000))
        self.assertEqual(self.conn.llen(key), 10000)
        safe_delete_list(self.conn, key)
        self.assertFalse(self.conn.exists(key))
        self.assertFalse(self.conn.exists('gc:list:{}'.format(Hash.md5(key))))

    def test_safe_delete_set(self):
        key = Generator.uuid4()
        self.conn.sadd(key, *range(10000))
        self.assertEqual(self.conn.scard(key), 10000)
        safe_delete_set(self.conn, key)
        self.assertFalse(self.conn.exists(key))
        self.assertFalse(self.conn.exists('gc:set:{}'.format(Hash.md5(key))))

    def test_safe_delete_sorted_set(self):
        key = Generator.uuid4()
        mapping = {i: '{}'.format(i) for i in range(10000)}
        self.conn.zadd(key, mapping)
        self.assertEqual(self.conn.zcard(key), 10000)
        safe_delete_sorted_set(self.conn, key)
        self.assertFalse(self.conn.exists(key))
        self.assertFalse(self.conn.exists('gc:zset:{}'.format(Hash.md5(key))))
