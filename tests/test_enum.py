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

        self.assertEqual(1, Alphabet.A)

        a = Alphabet(1)
        self.assertEqual(a, Alphabet.A)
        self.assertNotEqual(a, Alphabet.B)
        self.assertEqual('1', format(Alphabet.A))
        self.assertEqual('1', '{}'.format(Alphabet.A))

    def test_str_enum(self):
        class Alphabet(StrEnum):
            A = 'a'
            B = 'b'

        self.assertEqual('a', Alphabet.A)

        a = Alphabet('a')
        self.assertEqual(a, Alphabet.A)
        self.assertNotEqual(a, Alphabet.B)
        self.assertEqual('a', format(Alphabet.A))
        self.assertEqual('a', '{}'.format(Alphabet.A))

    def test_choices(self):
        class Alphabet(StrEnum):
            A = 'a'
            B = 'b'

        expected = [
            ('a', 'a'),
            ('b', 'b'),
        ]
        self.assertEqual(expected, Alphabet.choices())

        expected = ['a', 'b']
        self.assertEqual(expected, Alphabet.choice_values())
