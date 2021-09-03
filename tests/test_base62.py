import unittest

from tonggong import base62


class Base62TestCase(unittest.TestCase):
    def test(self):
        cases = [
            (0, "A"),
        ]
        for num, value in cases:
            self.assertEqual(num, base62.decode(value))
            self.assertEqual(value, base62.encode(num))
