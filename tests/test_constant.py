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

    def test_get_abbreviation(self):
        test_cases = [
            (TimeUnit.MINUTES, 'i'),
            (TimeUnit.HOURS, 'h'),
            (TimeUnit.DAYS, 'd'),
            (TimeUnit.WEEKS, 'w'),
            (TimeUnit.MONTHS, 'm'),
            (TimeUnit.QUARTERS, 'q'),
            (TimeUnit.YEARS, 'y')
        ]
        for unit, expected in test_cases:
            actual = TimeUnit.get_abbreviation(unit)
            self.assertEqual(expected, actual)
