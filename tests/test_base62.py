import doctest
import unittest

from tonggong import bunch


class BunchTestCase(unittest.TestCase):
    def test(self):
        returned = doctest.testmod(bunch)
        self.assertFalse(returned.failed)
