import datetime
import decimal
import unittest
from enum import Enum

from tonggong.validations.error import EmailError, LengthError, MaxLengthError, MinLengthError, NullError, ParamError
from tonggong.validations.validators import (
    DateValidator,
    DatetimeValidator,
    DecimalValidator,
    DictValidator,
    EmailValidator,
    EnumValidator,
    IntValidator,
    ListValidator,
    PhoneValidator,
    SchemaValidator,
    StrValidator,
    UsernameValidator,
    Validation,
    Validator,
)


class ValidatorTestCase(unittest.TestCase):
    def test_validate(self):
        test_cases = [((None, "test_field_name"), None)]

        for case, expected in test_cases:
            actual = Validator().validate(*case)
            self.assertEqual(expected, actual)


class IntValidatorTestCase(unittest.TestCase):
    def test_validate(self):
        test_cases = [
            ((), (1, "test_field_1"), 1),
            ((), ("1", "test_field_2"), 1),
            ((1, 5, False), (3, "test_field_3"), 3),
            ((5, 9, False), (3, "wrong_field_2"), MinLengthError),
            ((5, 9, False), (12, "wrong_field_3"), MaxLengthError),
            ((1, 5, False), (None, "wrong_field_4"), NullError),
        ]
        for args, case, expected in test_cases:
            try:
                actual = IntValidator(*args).validate(*case)
                self.assertEqual(expected, actual)
            except Exception as e:
                self.assertTrue(isinstance(e, expected))


class DictValidatorTestCase(unittest.TestCase):
    def test_validate(self):
        test_cases = [
            (({"key1": "value1"}, "test_field_1"), {"key1": "value1"}),
            (('{"key2": "value2"}', "test_field_2"), {"key2": "value2"}),
            (({"key1", "key2"}, "wrong_field_1"), ParamError),
            (("'key1', 'key2", "wrong_field_2"), ParamError),
        ]

        for case, expected in test_cases:
            try:
                actual = DictValidator().validate(*case)
                self.assertEqual(expected, actual)
            except Exception as e:
                self.assertTrue(isinstance(e, expected))


class DecimalValidatorTestCase(unittest.TestCase):
    def test_validate(self):
        test_cases = [
            ((None, 2, decimal.ROUND_HALF_UP), ("1.23456", "test_field_1"), decimal.Decimal("1.23")),
            ((None, 4, decimal.ROUND_DOWN), ("1.23456", "test_field_2"), decimal.Decimal("1.2345")),
            ((None, 4, decimal.ROUND_HALF_UP), ("1.23456", "test_field_3"), decimal.Decimal("1.2346")),
            (("1.23456", 4, decimal.ROUND_HALF_DOWN), (None, "test_field_4"), decimal.Decimal("1.2346")),
            ((None, 2, decimal.ROUND_HALF_UP), (None, "wrong_field_1"), NullError),
            ((None, 2, decimal.ROUND_HALF_UP), ("aaa", "wrong_field_2"), ParamError),
        ]

        for args, case, expected in test_cases:
            try:
                actual = DecimalValidator(*args).validate(*case)
                self.assertEqual(expected, actual)
            except Exception as e:
                self.assertTrue(isinstance(e, expected))


class StrValidatorTestCase(unittest.TestCase):
    def test_validate(self):
        test_cases = [
            ({}, ("abc", "test_field_1"), "abc"),
            ({"length": 5}, ("abcde", "test_field_2"), "abcde"),
            ({"min_length": 2, "max_length": 4}, ("abc", "test_field_3"), "abc"),
            ({"allow_null": True}, (None, "test_field_4"), None),
            ({"length": 5, "strip": False}, (" abc ", "test_field_5"), " abc "),
            ({"length": 5}, ("abc", "wrong_field_1"), LengthError),
            ({"min_length": 3, "max_length": 5}, ("ab", "wrong_field_2"), MinLengthError),
            ({"min_length": 3, "max_length": 5}, ("abcdefg", "wrong_field_3"), MaxLengthError),
            ({"allow_null": False}, (None, "wrong_field_4"), NullError),
        ]

        for args, case, expected in test_cases:
            try:
                actual = StrValidator(**args).validate(*case)
                self.assertEqual(expected, actual)
            except Exception as e:
                self.assertTrue(isinstance(e, expected))


class EmailValidatorTestCase(unittest.TestCase):
    def test_validator(self):
        test_cases = [
            ((True,), (None, "test_field_1"), None),
            ((), ("xxx12345@outlook.com", "test_field_2"), "xxx12345@outlook.com"),
            ((), (None, "wrong_field_1"), NullError),
            ((), ("xxx193242@@outlook.com", "wrong_field_2"), EmailError),
            ((), ("xxxxx@23423423@.com", "wrong_field_3"), EmailError),
        ]

        for args, case, expected in test_cases:
            try:
                actual = EmailValidator(*args).validate(*case)
                self.assertEqual(expected, actual)
            except Exception as e:
                self.assertTrue(isinstance(e, expected))


class PhoneValidatorTestCase(unittest.TestCase):
    def test_validate(self):
        test_cases = [
            ((True,), ("", "test_field_1"), None),
            ((), ("12345678911", "test_field_2"), "12345678911"),
            ((), ("", "wrong_field_1"), LengthError),
            ((), ("92312341231", "wrong_field_2"), ParamError),
            ((), ("1232424", "wrong_field_3"), LengthError),
        ]

        for args, case, expected in test_cases:
            try:
                actual = PhoneValidator(*args).validate(*case)
                self.assertEqual(expected, actual)
            except Exception as e:
                self.assertTrue(isinstance(e, expected))


class UsernameValidatorTestCase(unittest.TestCase):
    def test_validate(self):
        test_cases = [
            ((True,), (None, "test_field_1"), None),
            ((), ("username", "test_field_2"), "username"),
            ((), (None, "wrong_field_1"), NullError),
            ((), ("0" * 51, "wrong_field_2"), MaxLengthError),
            ((), ("321312", "wrong_field_3"), ParamError),
            ((), ("w214@qwe", "wrong_field_4"), ParamError),
        ]

        for args, case, expected in test_cases:
            try:
                actual = UsernameValidator(*args).validate(*case)
                self.assertEqual(expected, actual)
            except Exception as e:
                self.assertTrue(isinstance(e, expected))


class DateValidatorTestCase(unittest.TestCase):
    def test_validate(self):
        test_cases = [
            (("2021-09-14", "test_field_1"), datetime.datetime.strptime("2021-09-14", "%Y-%m-%d").date()),
            (("2001-12-31", "test_field_2"), datetime.datetime.strptime("2001-12-31", "%Y-%m-%d").date()),
            (("2020/01/31", "wrong_field_1"), ParamError),
            (("20201312", "wrong_field_2"), ParamError),
        ]

        for case, expected in test_cases:
            try:
                actual = DateValidator().validate(*case)
                self.assertEqual(expected, actual)
            except Exception as e:
                self.assertTrue(isinstance(e, expected))


class DatetimeValidatorTestCase(unittest.TestCase):
    def test_validate(self):
        test_cases = [
            (
                ("2021-09-14 00:00:00", "test_field_1"),
                datetime.datetime.strptime("2021-09-14 00:00:00", "%Y-%m-%d %H:%M:%S"),
            ),
            (
                ("2001-12-31 23:59:59", "test_field_2"),
                datetime.datetime.strptime("2001-12-31 23:59:59", "%Y-%m-%d %H:%M:%S"),
            ),
            (("2020/01/31 10:20:00", "wrong_field_1"), ParamError),
            (("20201312 22:34:00", "wrong_field_2"), ParamError),
        ]

        for case, expected in test_cases:
            try:
                actual = DatetimeValidator().validate(*case)
                self.assertEqual(expected, actual)
            except Exception as e:
                self.assertTrue(isinstance(e, expected))


class EnumValidatorTestCase(unittest.TestCase):
    def test_validate(self):
        class Color(Enum):
            red = 1
            green = 2
            blue = 3
            yellow = 4
            pink = 5
            cyan = 6

        test_cases = [((Color, int), (1, "test_field_1"), 1), ((Color, int), ("a", "wrong_field_1"), ParamError)]

        for args, case, expected in test_cases:
            try:
                actual = EnumValidator(*args).validate(*case)
                self.assertEqual(actual, expected)
            except Exception as e:
                self.assertTrue(isinstance(e, expected))


class ListValidatorTestCase(unittest.TestCase):
    def test_validate(self):
        test_cases = [
            ((IntValidator(), 10), ([1, 2, 3, 4], "test_field_1"), [1, 2, 3, 4]),
            ((StrValidator(), 10), (["1", "2", "3"], "test_field_2"), ["1", "2", "3"]),
            ((StrValidator(), 10), ("1,2,3,4,5", "test_field_3"), ["1", "2", "3", "4", "5"]),
            ((IntValidator(), 3), ([1, 2, 3, 4, 5], "wrong_field_1"), MaxLengthError),
            ((StrValidator(), 10, False, True), ("1,2,3,4", "wrong_field_2"), ParamError),
        ]

        for args, case, expected in test_cases:
            try:
                actual = ListValidator(*args).validate(*case)
                self.assertEqual(expected, actual)
            except Exception as e:
                self.assertTrue(isinstance(e, expected))


class SchemaValidatorTestCase(unittest.TestCase):
    def test_validate(self):
        test_cases = [
            (
                {
                    "key1": Validation(StrValidator(length=6), "test_field_1"),
                    "key2": Validation(StrValidator(), "test_field_2"),
                    "key3": Validation(IntValidator(), "test_field_3", optional=True),
                },
                ({"key1": "value1", "key2": "value2", "key3": 1}, "test"),
                {"key1": "value1", "key2": "value2", "key3": 1},
            ),
            (
                {
                    "key1": Validation(StrValidator(length=6), "wrong_field_1"),
                    "key2": Validation(StrValidator(), "wrong_field_2"),
                    "key3": Validation(IntValidator(), "wrong_field_3"),
                },
                ({"key1": "abc", "key2": "value2", "key3": "123"}, "wrong_test"),
                LengthError,
            ),
        ]

        for args, case, expected in test_cases:
            try:
                actual = SchemaValidator(args).validate(*case)
                self.assertEqual(expected, actual)
            except Exception as e:
                self.assertTrue(isinstance(e, expected))
