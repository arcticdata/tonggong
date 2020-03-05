import unittest

from tonggong.constant import DatabaseAdapter


class BunchTestCase(unittest.TestCase):
    def test_choices(self):
        for name, value in DatabaseAdapter.choices():
            self.assertTrue(isinstance(name, int))
            self.assertTrue(isinstance(value, str))
