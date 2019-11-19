import unittest

from tonggong.enum import IntEnum, StrEnum, enum


class EnumTestCase(unittest.TestCase):
    def test_unique(self):
        try:
            @enum.unique
            class Alphabet(IntEnum):
                A = 1
                B = 2
                C = 1
        except Exception as e:
            self.assertIsInstance(e, ValueError)

    def test_int_enum(self):
        class Alphabet(IntEnum):
            A = 1
            B = 2

        self.assertEqual(Alphabet.A, 1)

        a = Alphabet(1)
        self.assertEqual(a, Alphabet.A)
        self.assertNotEqual(a, Alphabet.B)

    def test_str_enum(self):
        class Alphabet(StrEnum):
            A = 'a'
            B = 'b'

        self.assertEqual(Alphabet.A, 'a')

        a = Alphabet('a')
        self.assertEqual(a, Alphabet.A)
        self.assertNotEqual(a, Alphabet.B)
