import unittest

import tonggong.formatter


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
            actual = tonggong.formatter.remove_special_character(case)
            self.assertEqual(expected, actual)

    def test_isoweek(self):
        test_cases = [
            ((2019, 1), '2018-12-31'),
            ((2018, 1), '2018-01-01'),
        ]
        for case, expected in test_cases:
            actual = tonggong.formatter.Formatter.week(*case)
            self.assertEqual(expected, actual)
