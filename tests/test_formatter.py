# -*- coding: utf-8 -*-
import unittest

import tonggong.formatter


class FormatterTestCase(unittest.TestCase):
    def test_remove_special_character(self):
        test_cases = [
            (' hello world！', 'helloworld'),
            ('Adding To...', 'AddingTo'),
        ]
        for case, expected in test_cases:
            actual = tonggong.formatter.remove_special_character(case)
            self.assertEqual(expected, actual)
