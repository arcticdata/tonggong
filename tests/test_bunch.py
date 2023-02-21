import doctest
import sys
import unittest

from tonggong import bunch


class BunchTestCase(unittest.TestCase):
    @unittest.skipIf(sys.version_info.minor == 11, "error info different from py3.11")
    def test(self):
        returned = doctest.testmod(bunch)
        self.assertFalse(returned.failed)
