import base64
import unittest

from tonggong.util import json_dumps, padding_base64


class UtilTestCase(unittest.TestCase):
    def test_padding_base64(self):
        # reference: https://en.wikipedia.org/wiki/Base64
        cases = [
            ("YW55IGNhcm5hbCBwbGVhcw", "YW55IGNhcm5hbCBwbGVhcw==", b"any carnal pleas"),
            (
                "YW55IGNhcm5hbCBwbGVhc3U",
                "YW55IGNhcm5hbCBwbGVhc3U=",
                b"any carnal pleasu",
            ),
            (
                "YW55IGNhcm5hbCBwbGVhc3Vy",
                "YW55IGNhcm5hbCBwbGVhc3Vy",
                b"any carnal pleasur",
            ),
        ]
        for encoded, encoded_with_padding, decoded in cases:
            actual = padding_base64(encoded)
            self.assertEqual(encoded_with_padding, actual)
            actual = base64.b64decode(actual)
            self.assertEqual(decoded, actual)

    def test_json_dumps(self):
        cases = [
            (66, "66"),
            ([1, 2], "[1,2]"),
            ({1: 1}, '{"1":1}'),
            ({"a": "a"}, '{"a":"a"}'),
        ]
        for _obj, expected in cases:
            actual = json_dumps(_obj)
            self.assertEqual(actual, expected)
