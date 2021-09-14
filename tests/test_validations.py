# -*- coding: utf-8 -*-
"""
-------------------------------------------------
Project Name: tonggong
File Name: test_validations.py
Author: xyb
Create Date: 2021/9/13 下午4:59
-------------------------------------------------
"""

import decimal
import datetime
import unittest

from tonggong.validations import (
    Validator,
    IntValidator,
    DictValidator,
    DecimalValidator,
    StrValidator,
    EmailValidator,
    SchemaValidator,
    PhoneValidator,
    UsernameValidator,
    DateValidator,
    DatetimeValidator,
    EnumValidator,
    ListValidator,
    Validation,
)

from tonggong.validations import (
    BaseError,
    ParamError,
    MinLengthError,
    MaxLengthError,
    NullError,
    LengthError,
    EmailError,
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
        ]
        for s_param, case, expected in test_cases:
            actual = IntValidator(*s_param).validate(*case)
            self.assertEqual(expected, actual)

        wrong_cases = [
            ((5, 9, False), (3, "wrong_field_2"), MinLengthError),
            ((5, 9, False), (12, "wrong_field_3"), MaxLengthError),
            ((1, 5, False), (None, "wrong_field_4"), NullError),
        ]
        for s_param, case, wrong_type in wrong_cases:
            # noinspection PyBroadException
            try:
                IntValidator(*s_param).validate(*case)
            except Exception as e:
                self.assertEqual(e.e_type, wrong_type)


class DictValidatorTestCase(unittest.TestCase):
    def test_validate(self):
        test_cases = [
            (({"key1": "value1"}, "test_field_1"), {"key1": "value1"}),
            (('{"key2": "value2"}', "test_field_2"), {"key2": "value2"}),
        ]

        for case, expected in test_cases:
            actual = DictValidator().validate(*case)
            self.assertEqual(expected, actual)

        wrong_cases = [
            (({"key1", "key2"}, "wrong_field_1"), ParamError),
            (("'key1', 'key2", "wrong_field_2"), ParamError),
        ]

        for case, wrong_type in wrong_cases:
            try:
                DictValidator().validate(*case)
            except Exception as e:
                self.assertEqual(e.e_type, wrong_type)


class DecimalValidatorTestCase(unittest.TestCase):
    def test_validate(self):
        test_cases = [
            ((None, 2, decimal.ROUND_HALF_UP), ("1.23456", "test_field_1"), decimal.Decimal("1.23")),
            ((None, 4, decimal.ROUND_DOWN), ("1.23456", "test_field_2"), decimal.Decimal("1.2345")),
            ((None, 4, decimal.ROUND_HALF_UP), ("1.23456", "test_field_3"), decimal.Decimal("1.2346")),
            (("1.23456", 4, decimal.ROUND_HALF_DOWN), (None, "test_field_4"), decimal.Decimal("1.2346")),
        ]

        for s_param, case, expected in test_cases:
            actual = DecimalValidator(*s_param).validate(*case)
            self.assertEqual(expected, actual)

        wrong_cases = [
            ((None, 2, decimal.ROUND_HALF_UP), (None, "wrong_field_1"), NullError),
            ((None, 2, decimal.ROUND_HALF_UP), ("aaa", "wrong_field_2"), ParamError),
        ]

        for s_param, case, wrong_type in wrong_cases:
            try:
                DecimalValidator(*s_param).validate(*case)
            except Exception as e:
                self.assertEqual(e.e_type, wrong_type)


class StrValidatorTestCase(unittest.TestCase):
    def test_validate(self):
        test_cases = [
            ({}, ("abc", "test_field_1"), "abc"),
            ({"length": 5}, ("abcde", "test_field_2"), "abcde"),
            ({"min_length": 2, "max_length": 4}, ("abc", "test_field_3"), "abc"),
            ({"allow_null": True}, (None, "test_field_4"), None),
            ({"length": 5, "strip": False}, (" abc ", "test_field_5"), " abc "),
        ]

        for s_param, case, expected in test_cases:
            actual = StrValidator(**s_param).validate(*case)
            self.assertEqual(expected, actual)

        wrong_cases = [
            ({"length": 5}, ("abc", "wrong_field_1"), LengthError),
            ({"min_length": 3, "max_length": 5}, ("ab", "wrong_field_2"), MinLengthError),
            ({"min_length": 3, "max_length": 5}, ("abcdefg", "wrong_field_3"), MaxLengthError),
            ({"allow_null": False}, (None, "wrong_field_4"), NullError),
        ]

        for s_param, case, wrong_type in wrong_cases:
            try:
                StrValidator(**s_param).validate(*case)
            except Exception as e:
                self.assertEqual(e.e_type, wrong_type)


class EmailValidatorTestCase(unittest.TestCase):
    def test_validator(self):
        test_cases = [
            ((True,), (None, "test_field_1"), None),
            ((), ("xxx12345@outlook.com", "test_field_2"), "xxx12345@outlook.com"),
        ]

        for s_param, case, expected in test_cases:
            actual = EmailValidator(*s_param).validate(*case)
            self.assertEqual(expected, actual)

        wrong_cases = [
            ((), (None, "wrong_field_1"), NullError),
            ((), ("xxx193242@@outlook.com", "wrong_field_2"), EmailError),
            ((), ("xxxxx@23423423@.com", "wrong_field_3"), EmailError),
        ]

        for s_param, case, wrong_type in wrong_cases:
            try:
                EmailValidator(*s_param).validate(*case)
            except Exception as e:
                self.assertEqual(e.e_type, wrong_type)


class PhoneValidatorTestCase(unittest.TestCase):
    def test_validate(self):
        test_cases = [((True,), ("", "test_field_1"), None), ((), ("12345678911", "test_field_2"), "12345678911")]

        for s_param, case, expected in test_cases:
            actual = PhoneValidator(*s_param).validate(*case)
            self.assertEqual(expected, actual)

        wrong_cases = [
            ((), ("", "wrong_field_1"), LengthError),
            ((), ("92312341231", "wrong_field_2"), ParamError),
            ((), ("1232424", "wrong_field_3"), LengthError),
        ]

        for s_param, case, wrong_type in wrong_cases:
            try:
                PhoneValidator(*s_param).validate(*case)
            except Exception as e:
                self.assertEqual(e.e_type, wrong_type)


class UsernameValidatorTestCase(unittest.TestCase):
    def test_validate(self):
        test_cases = [((True,), (None, "test_field_1"), None), ((), ("username", "test_field_2"), "username")]

        for s_param, case, expected in test_cases:
            actual = UsernameValidator(*s_param).validate(*case)
            self.assertEqual(expected, actual)

        wrong_cases = [
            ((), (None, "wrong_field_1"), NullError),
            ((), ("0" * 51, "wrong_field_2"), MaxLengthError),
            ((), ("321312", "wrong_field_3"), ParamError),
            ((), ("w214@qwe", "wrong_field_4"), ParamError),
        ]

        for s_param, case, wrong_type in wrong_cases:
            try:
                UsernameValidator(*s_param).validate(*case)
            except Exception as e:
                self.assertEqual(e.e_type, wrong_type)


class DateValidatorTestCase(unittest.TestCase):
    def test_validate(self):
        test_cases = [
            (("2021-09-14", "test_field_1"), datetime.datetime.strptime("2021-09-14", "%Y-%m-%d").date()),
            (("2001-12-31", "test_field_2"), datetime.datetime.strptime("2001-12-31", "%Y-%m-%d").date()),
        ]

        for case, expected in test_cases:
            actual = DateValidator().validate(*case)
            self.assertEqual(expected, actual)

        wrong_cases = [(("2020/01/31", "wrong_field_1"), ParamError), (("20201312", "wrong_field_2"), ParamError)]

        for case, wrong_type in wrong_cases:
            try:
                DateValidator().validate(*case)
            except Exception as e:
                self.assertEqual(e.e_type, wrong_type)


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
        ]

        for case, expected in test_cases:
            actual = DatetimeValidator().validate(*case)
            self.assertEqual(expected, actual)

        wrong_cases = [
            (("2020/01/31 10:20:00", "wrong_field_1"), ParamError),
            (("20201312 22:34:00", "wrong_field_2"), ParamError),
        ]

        for case, wrong_type in wrong_cases:
            try:
                DatetimeValidator().validate(*case)
            except Exception as e:
                self.assertEqual(e.e_type, wrong_type)


class EnumValidatorTestCase(unittest.TestCase):
    def test_validate(self):
        pass


class ListValidatorTestCase(unittest.TestCase):
    def test_validate(self):
        test_cases = [
            ((IntValidator(), 10), ([1, 2, 3, 4], "test_field_1"), [1, 2, 3, 4]),
            ((StrValidator(), 10), (["1", "2", "3"], "test_field_2"), ["1", "2", "3"]),
            ((StrValidator(), 10), ("1,2,3,4,5", "test_field_3"), ["1", "2", "3", "4", "5"]),
        ]

        for s_param, case, expected in test_cases:
            actual = ListValidator(*s_param).validate(*case)
            self.assertEqual(expected, actual)

        wrong_cases = [
            ((IntValidator(), 3), ([1, 2, 3, 4, 5], "wrong_field_1"), MaxLengthError),
            ((StrValidator(), 10, False, True), ("1,2,3,4", "wrong_field_2"), ParamError),
        ]

        for s_param, case, wrong_type in wrong_cases:
            try:
                ListValidator(*s_param).validate(*case)
            except Exception as e:
                self.assertEqual(e.e_type, wrong_type)


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
            )
        ]

        for s_param, case, expected in test_cases:
            actual = SchemaValidator(s_param).validate(*case)
            self.assertEqual(expected, actual)

        wrong_cases = [
            (
                {
                    "key1": Validation(StrValidator(length=6), "wrong_field_1"),
                    "key2": Validation(StrValidator(), "wrong_field_2"),
                    "key3": Validation(IntValidator(), "wrong_field_3"),
                },
                ({"key1": "abc", "key2": "value2", "key3": "123"}, "wrong_test"),
                LengthError,
            )
        ]

        for s_param, case, wrong_type in wrong_cases:
            try:
                SchemaValidator(s_param).validate(*case)
            except Exception as e:
                self.assertEqual(e.e_type, wrong_type)
