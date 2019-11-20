import unittest

from tonggong.generator import Generator


class GeneratorTestCase(unittest.TestCase):
    def test_uuid4(self):
        actual = Generator.uuid4()
        self.assertIsInstance(actual, str)
        self.assertEqual(32, len(actual))

    def test_pincode(self):
        pincode = Generator.pincode()
        self.assertIsInstance(pincode, str)
        self.assertTrue(pincode.isdigit())
        self.assertEqual(6, len(pincode))

        for length in range(1, 10):
            pincode = Generator.pincode(length=length)
            self.assertIsInstance(pincode, str)
            self.assertTrue(pincode.isdigit())
            self.assertEqual(length, len(pincode))

    def test_phone(self):
        phone = Generator.phone()
        self.assertIsInstance(phone, str)
        self.assertTrue(phone.isdigit())
        self.assertEqual(11, len(phone))
