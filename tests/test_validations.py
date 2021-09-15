import datetime
import decimal
import unittest
from enum import Enum

from tonggong.validations.errors import (
    BaseValidationError,
    LengthError,
    MaxLengthError,
    MinLengthError,
    NullError,
    ParamError,
    SchemaError
)
from tonggong.validations.utils import *
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
    UUIDValidator,
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
            ((1, 5, True), (None, "test_field_1"), None),
            ((), (1, "test_field_2"), 1),
            ((), ("1", "test_field_3"), 1),
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
            ({"allow_reversed_characters": True}, (r"\@", "test_field_6"), r"\@"),
            ({"length": 5}, ("abc", "wrong_field_1"), LengthError),
            ({"min_length": 3, "max_length": 5}, ("ab", "wrong_field_2"), MinLengthError),
            ({"min_length": 3, "max_length": 5}, ("abcdefg", "wrong_field_3"), MaxLengthError),
            ({"allow_null": False}, (None, "wrong_field_4"), NullError),
            ({"allow_reversed_characters": False}, (r"\@", "wrong_field_5"), ParamError),
        ]

        for args, case, expected in test_cases:
            try:
                actual = StrValidator(**args).validate(*case)
                self.assertEqual(expected, actual)
            except Exception as e:
                self.assertTrue(isinstance(e, expected))

class UUIDValidatorTestCase(unittest.TestCase):
    def test_validate(self):
        test_cases = [
            ((), ("421237d8161011ec999e0a80ff2603de", "test_field_1"), "421237d8161011ec999e0a80ff2603de"),
            ((True,), (None, "test_field_2"), None),
            ((), (None, "wrong_field_1"), NullError),
            ((), ("abcedfasfaw", "wrong_field_2"), LengthError),
        ]

        for args, case, expected in test_cases:
            try:
                actual = UUIDValidator(*args).validate(*case)
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
            ((), ("21312412xxxxxx", "wrong_field_4"), EmailError),
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

        colorEnum = Enum("ColorEnum", {"red": 1, "green": 2, "blue": 3, "yellow": 4, "pink": 5, "cyan": 6})

        test_cases = [
            ((colorEnum, int), (1, "test_field_1"), 1),
            ((colorEnum, int), ("a", "wrong_field_1"), ParamError),
        ]

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
            ((IntValidator(), 10), ([], "test_field_4"), []),
            ((IntValidator(), 10, True), (None, "test_field_5"), None),
            ((IntValidator(), 3), ([1, 2, 3, 4, 5], "wrong_field_1"), MaxLengthError),
            ((StrValidator(), 10, False, True), ("1,2,3,4", "wrong_field_2"), ParamError),
            ((StrValidator(), 10, False, True), ("1,2,3,4", "wrong_field_2"), ParamError),
            ((IntValidator(), 10), (None, "test_field_3"), NullError),
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
                ({"key1": "abc", "key2": "value2", "key3": "123"}, "wrong_test_1"),
                LengthError,
            ),
            ("abc", ({"key1": "value1"}), ParamError),
            ({"key1": Validation(IntValidator(), "wrong_field_4")}, ({"key2": 1}, "wrong_test_2"), SchemaError),
            ({"key1": Validation(IntValidator(), "wrong_field_5")}, ({"key2": 1}),
             SchemaError),
            ({"key1": Validation(IntValidator(), "wrong_field_6")}, ({"key1": "a"}, "wrong_test_4"), ParamError)
        ]

        for args, case, expected in test_cases:
            try:
                actual = SchemaValidator(args).validate(*case)
                self.assertEqual(expected, actual)
            except Exception as e:
                self.assertTrue(isinstance(e, expected))


class ErrorsModuleTestCase(unittest.TestCase):
    def test_BaseValidationError(self):
        test_cases = [
            (("this is wrong", {"data": "data"}), ("this is wrong", {"data": "data"})),
            (({"key1": "value1"}, {"data": "data"}), ("{'key1': 'value1'}", {"data": "data"})),
        ]

        for case, expected in test_cases:
            b = BaseValidationError(*case)
            self.assertEqual((b.message, b.data), expected)

    def test_repr(self):
        test_cases = [
            (
                BaseValidationError("error").__repr__(),
                "<class 'tonggong.validations.errors.BaseValidationError'>: error",
            ),
            (BaseValidationError().__repr__(), "<class 'tonggong.validations.errors.BaseValidationError'>: None"),
        ]

        for case, expected in test_cases:
            self.assertEqual(case, expected)


class UtilsTestCase(unittest.TestCase):
    def test_EmailValidate(self):
        test_cases = [((), (None, None)), (("message", "code"), ("message", "code"))]

        for case, expected in test_cases:
            e = EmailValidate(*case)
            self.assertEqual((e.message, e.code), expected)

    def test_is_phone(self):
        test_cases = [(None, False), ("12345678911", True)]

        for case, expected in test_cases:
            self.assertEqual(is_phone(case), expected)

    def test_is_email(self):
        test_cases = [(None, False), ("123456789@outlook.com", True)]

        for case, expected in test_cases:
            self.assertEqual(is_email(case), expected)

    def test_has_uri_reversed_character(self):
        test_cases = [(r"\@", True), ("abcfgh", False)]

        for case, expected in test_cases:
            self.assertEqual(has_uri_reversed_character(case), expected)
