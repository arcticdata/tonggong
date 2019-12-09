import datetime
import decimal
import unittest

from tonggong.formatter import Formatter, YAxisFormatter, remove_special_character


class FormatterTestCase(unittest.TestCase):
    def test_remove_special_character(self):
        test_cases = [
            (' hello world！', 'helloworld'),
            ('Adding To...', 'AddingTo'),
            ('(你好)', '你好'),
            ('（你好）', '你好'),
            ('%%abc', 'abc'),
            ('!#$%^&()~??}}{{++><abc', 'abc'),
            ('        ', ''),
        ]
        for case, expected in test_cases:
            actual = remove_special_character(case)
            self.assertEqual(expected, actual)

    def test_isoweek(self):
        test_cases = [
            ((2019, 1), '2018-12-31'),
            ((2018, 1), '2018-01-01'),
        ]
        for case, expected in test_cases:
            actual = Formatter.week(*case)
            self.assertEqual(expected, actual)

    def test_money(self):
        test_cases = [
            ('1000', '1000.00元'),
            ('100000', '10万元'),
            ('1034500000', '10.35亿元'),
            ('100.345', '100.34元'),
            ('54321', '5万元'),
            ('55951', '6万元'),
        ]
        for case, expected in test_cases:
            actual = Formatter.money(case)
            self.assertEqual(expected, actual)

    def test_text(self):
        test_cases = [
            (None, 'None'),
            (0, '0'),
            (1.1, '1.1'),
            ({1, 2}, '1,2'),
            ({2, 1}, '1,2'),
            ([2, 1], '2,1'),
            ((2, 1), '2,1'),
            (('hello', 'world'), 'hello,world'),
            (['hello', 'world'], 'hello,world'),
            ({'hello', 'world'}, 'hello,world'),
            ({None, None}, 'None'),
        ]
        for case, expected in test_cases:
            actual = Formatter.text(case)
            self.assertEqual(expected, actual)

    def test_int(self):
        test_cases = [
            (1, '1'),
            (1.4, '1'),
            (1.5, '1'),
            (-10.345, '-10'),
        ]
        for case, expected in test_cases:
            actual = Formatter.int(case)
            self.assertEqual(expected, actual)

    def test_date(self):
        test_cases = [
            ('2018-08-08', '2018-08-08'),
            (datetime.date(2018, 8, 8), '2018-08-08'),
            (datetime.datetime(2018, 8, 8), '2018-08-08'),
        ]
        for case, expected in test_cases:
            actual = Formatter.date(case)
            self.assertEqual(expected, actual)

    def test_month(self):
        test_cases = [
            ((2018, 8), '2018年8月'),
            (('2018', '1'), '2018年1月'),
            (('2018', '01'), '2018年01月'),
        ]
        for case, expected in test_cases:
            actual = Formatter.month(*case)
            self.assertEqual(expected, actual)

    def test_week(self):
        test_cases = [
            ((2018, 1), '2018-01-01'),
            ((2018, 2), '2018-01-08'),
            ((2019, 1), '2018-12-31'),
        ]
        for case, expected in test_cases:
            actual = Formatter.week(*case)
            self.assertEqual(expected, actual)

    def test_quarter(self):
        test_cases = [
            ((2018, 1), '2018年1季度'),
            (('2018', '1'), '2018年1季度'),
            (('猪', '1'), '猪年1季度'),
        ]
        for case, expected in test_cases:
            actual = Formatter.quarter(*case)
            self.assertEqual(expected, actual)

    def test_year(self):
        test_cases = [
            (2018, '2018年'),
            ('2018', '2018年'),
            ('猪', '猪年')
        ]
        for case, expected in test_cases:
            actual = Formatter.year(case)
            self.assertEqual(expected, actual)

    def test_chinese_number(self):
        test_cases = [
            (1000000, '100.0万'),
            (100000000, '1.0亿'),
            (123000, '12.3万'),
            (123123, '123123'),
        ]
        for case, expected in test_cases:
            actual = Formatter.chinese_number(case)
            self.assertEqual(expected, actual)


class YAxisFormatterTestCase(unittest.TestCase):
    def test_money(self):
        test_cases = [
            ((3.355, 4), '3.35'),
            ((55000, 50000), '5.50万'),
            ((1100000000, 400000000), '11.00亿'),
            ((1100000000, 30000), '110000.00万'),
        ]
        for case, expected in test_cases:
            actual = YAxisFormatter.money(*case)
            self.assertEqual(expected, actual)

    def test_int(self):
        test_cases = [
            ((3, 4), '3.00'),
            ((55000, 50000), '5.50万'),
            ((1100000000, 400000000), '11.00亿'),
            ((1100000000, 30000), '110000.00万'),
        ]
        for case, expected in test_cases:
            actual = YAxisFormatter.int(*case)
            self.assertEqual(expected, actual)

    def test_decimal(self):
        test_cases = [
            ((decimal.Decimal('3.355'), 4), '3.36'),
            ((decimal.Decimal('55000'), 50000), '5.50万'),
            ((decimal.Decimal('1100000000'), 400000000), '11.00亿'),
            ((decimal.Decimal('1100000000'), 30000), '110000.00万'),
        ]
        for case, expected in test_cases:
            actual = YAxisFormatter.decimal(*case)
            self.assertEqual(expected, actual)

    def test_float(self):
        test_cases = [
            ((3.357, 4), '3.36'),
            ((55000.11, 50000), '5.50万'),
            ((1100000000.55, 400000000), '11.00亿'),
            ((1100000000.66, 30000), '110000.00万'),
        ]
        for case, expected in test_cases:
            actual = YAxisFormatter.float(*case)
            self.assertEqual(expected, actual)

    def test_percent(self):
        test_cases = [
            (('0.23',), '23.0%'),
            ((0.23,), '23.0%'),
            (('0.999',), '99.9%'),
            (('0.991234',), '99.12%'),
            ((0.991234,), '99.12%'),
            (('95.4%',), '95.4%'),
            (('0.99123456789', 3), '99.123%'),
            ((0.99123456789, 3), '99.123%'),
        ]
        for case, expected in test_cases:
            actual = YAxisFormatter.percentage(*case)
            self.assertEqual(expected, actual)
