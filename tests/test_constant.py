import unittest

from tonggong.constant import TimeUnit, TimeUnitAbbr


class BunchTestCase(unittest.TestCase):
    _time_unit_map = [
        (8, "s"),
        (1, "m"),
        (2, "h"),
        (3, "d"),
        (4, "w"),
        (5, "M"),
        (6, "Q"),
        (7, "y"),
    ]

    def test_choices(self):
        for name, value in TimeUnit.choices():
            self.assertTrue(isinstance(name, int))
            self.assertTrue(isinstance(value, int))

    def test_time_unit(self):
        for value, expected in self._time_unit_map:
            actual = TimeUnit(value).abbr
            self.assertEqual(TimeUnitAbbr(expected), actual)

    def test_time_unit_abbr(self):
        for expected, value in self._time_unit_map:
            actual = TimeUnitAbbr(value).time_unit
            self.assertEqual(TimeUnit(expected), actual)
