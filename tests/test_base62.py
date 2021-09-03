import unittest

from tonggong import base62


class Base62TestCase(unittest.TestCase):
    def test(self):
        cases = [
            (0, "A"),
            (1, "B"),
            (2, "C"),
            (123, "B9"),
            (62, 'BA'),
            (234484, '9AA'),
            (-99, '-Bl'),
            (-73, '-BL')
        ]
        for num, value in cases:
            self.assertEqual(num, base62.decode(value))
            self.assertEqual(value, base62.encode(num))
