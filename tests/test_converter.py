import datetime
import decimal
import unittest

from tonggong.converter import Converter


class ConverterTestCase(unittest.TestCase):
    def test_get_date(self):
        test_cases = [
            ('20180808', '%Y%m%d', datetime.date(2018, 8, 8)),
            ('2018-08-08', '%Y-%m-%d', datetime.date(2018, 8, 8)),
            ('2018-2-1', '%Y-%W-%w', datetime.date(2018, 1, 8)),
            ('2018-11', '%Y-%m', datetime.date(2018, 11, 1)),
            ('2018', '%Y', datetime.date(2018, 1, 1)),
        ]
        for case, _format, expected in test_cases:
            actual = Converter.get_date(case, _format)
            self.assertEqual(expected, actual)

    def test_get_int(self):
        test_cases = [
            (None, None),
            ('0', 0),
            ('0.1', 0),
            ('100.345', 100),
            ('1000.99', 1001),
            (1000.99, 1001),
            ('-1000.99', -1001),
            (-1000.99, -1001),
            (1000.6, 1001),
        ]
        for case, expected in test_cases:
            actual = Converter.get_int(case)
            self.assertEqual(expected, actual)

    def test_get_str(self):
        test_cases = [
            (None, None),
            ('', ''),
            ('\n\t', ''),
            ('hello world!', 'hello world!'),
            (-123456, '-123456'),
            ('   hello', 'hello')
        ]
        for case, expected in test_cases:
            actual = Converter.get_str(case)
            self.assertEqual(expected, actual)

    def test_get_float(self):
        test_cases = [
            (None, None),
            (0, 0),
            ('-0', 0),
            ('-100', -100),
            ('100-', -100),
            ('100.345', 100.345),
            ('100.346', 100.346),
            ('100.55555555', 100.55555555),
        ]
        for case, expected in test_cases:
            actual = Converter.get_float(case)
            self.assertEqual(expected, actual)

    def test_get_decimal(self):
        test_cases = [
            (None, None),
            (0, 0),
            ('100.3', decimal.Decimal('100.30')),
            (100.3, decimal.Decimal('100.30')),
            ('100.345', decimal.Decimal('100.34')),
            (100.345, decimal.Decimal('100.34')),
            ('100.355', decimal.Decimal('100.36')),
            (100.355, decimal.Decimal('100.36')),
            (100.5, decimal.Decimal('100.5')),
        ]
        for case, expected in test_cases:
            actual = Converter.get_decimal(case)
            self.assertEqual(expected, actual)

    def test_get_latitude_or_longitude(self):
        test_cases = [
            (None, None),
            (0, 0),
            (100.3, decimal.Decimal('100.30000000')),
            (100.345, decimal.Decimal('100.34500000')),
            (100.355, decimal.Decimal('100.35500000')),
            (100.123456789, decimal.Decimal('100.12345679')),
            ('100.123456789', decimal.Decimal('100.12345679')),
        ]
        for case, expected in test_cases:
            actual = Converter.get_latitude_or_longitude(case)
            self.assertEqual(expected, actual)
