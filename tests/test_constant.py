import unittest

from tonggong.constant import DatabaseAdapter, TimeUnit


class BunchTestCase(unittest.TestCase):
    def test_choices(self):
        for name, value in DatabaseAdapter.choices():
            self.assertTrue(isinstance(name, int))
            self.assertTrue(isinstance(value, str))

        for name, value in TimeUnit.choices():
            self.assertTrue(isinstance(name, int))
            self.assertTrue(isinstance(value, int))

    def test_time_unit(self):
        test_cases = [
            (1, 'i'),
            (2, 'h'),
            (3, 'd'),
            (4, 'w'),
            (5, 'm'),
            (6, 'q'),
            (7, 'y')
        ]
        for value, expected in test_cases:
            actual = TimeUnit(value).abbreviation
            self.assertEqual(expected, actual)
