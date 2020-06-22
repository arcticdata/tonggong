import base64
import datetime
import logging
import unittest

from tonggong.util import (
    add_months,
    base64_decode,
    base64_encode,
    json_dumps,
    minus_months,
    padding_base64,
    prevent_django_request_warnings,
)


class UtilTestCase(unittest.TestCase):
    def test_base64_encode_and_decode(self):
        cases = [
            ("hello", "aGVsbG8"),
            ("any carnal pleas", "YW55IGNhcm5hbCBwbGVhcw"),
        ]
        for value, encode_value in cases:
            actual = base64_encode(value)
            self.assertEqual(encode_value, actual)
            actual = base64_decode(actual)
            self.assertEqual(value, actual)

    def test_padding_base64(self):
        # reference: https://en.wikipedia.org/wiki/Base64
        cases = [
            ("YW55IGNhcm5hbCBwbGVhcw", "YW55IGNhcm5hbCBwbGVhcw==", b"any carnal pleas"),
            ("YW55IGNhcm5hbCBwbGVhc3U", "YW55IGNhcm5hbCBwbGVhc3U=", b"any carnal pleasu"),
            ("YW55IGNhcm5hbCBwbGVhc3Vy", "YW55IGNhcm5hbCBwbGVhc3Vy", b"any carnal pleasur"),
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

    def test_add_months(self):
        cases = [
            (datetime.date(2020, 1, 1), 2, datetime.date(2020, 3, 1)),
            (datetime.date(2020, 1, 29), 1, datetime.date(2020, 2, 29)),
            (datetime.date(2019, 1, 29), 1, datetime.date(2019, 2, 28)),
            (datetime.date(2020, 1, 1), 13, datetime.date(2021, 2, 1)),
            (datetime.date(2015, 12, 31), 12, datetime.date(2016, 12, 31)),
        ]
        for origin_date, num, expected in cases:
            actual = add_months(origin_date, num)
            self.assertEqual(expected, actual)

    def test_minus_months(self):
        cases = [
            (datetime.date(2020, 1, 1), 2, datetime.date(2019, 11, 1)),
            (datetime.date(2020, 2, 2), 1, datetime.date(2020, 1, 2)),
            (datetime.date(2020, 3, 29), 1, datetime.date(2020, 2, 29)),
            (datetime.date(2019, 3, 29), 1, datetime.date(2019, 2, 28)),
            (datetime.date(2020, 1, 1), 13, datetime.date(2018, 12, 1)),
            (datetime.date(2015, 12, 31), 12, datetime.date(2014, 12, 31)),
        ]
        for origin_date, num, expected in cases:
            actual = minus_months(origin_date, num)
            self.assertEqual(expected, actual)

    @prevent_django_request_warnings
    def test_prevent_django_request_warnings(self):
        logger = logging.getLogger("django.request")
        self.assertEqual(logging.ERROR, logger.getEffectiveLevel())
