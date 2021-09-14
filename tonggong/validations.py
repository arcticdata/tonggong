# -*- coding: utf-8 -*-
"""
-------------------------------------------------
Project Name: tonggong
File Name: validations.py
Author: xyb
Create Date: 2021/9/13 上午11:35
-------------------------------------------------
"""

import datetime
import decimal
import ipaddress
import json
import re
from typing import List, Union


class BaseError(Exception):
    def __init__(self, message=None, e_type=None, data=None):
        if not isinstance(message, str):
            message = f"{message}"
        self.message = message
        self.e_type = e_type
        self.data = data

    def __str__(self):
        return f"{self.e_type}: {self.message}"


class ParamError(BaseError):
    def __init__(self, message=None):
        super(ParamError, self).__init__(message=message, e_type=ParamError)


class MinLengthError(BaseError):
    def __init__(self, message=None):
        super(MinLengthError, self).__init__(message=message, e_type=MinLengthError)


class MaxLengthError(BaseError):
    def __init__(self, message=None):
        super(MaxLengthError, self).__init__(message=message, e_type=MaxLengthError)


class NullError(BaseError):
    def __init__(self, message=None):
        super(NullError, self).__init__(message=message, e_type=NullError)


class LengthError(BaseError):
    def __init__(self, message=None):
        super(LengthError, self).__init__(message=message, e_type=LengthError)


class EmailError(BaseError):
    def __init__(self, message=None):
        super(EmailError, self).__init__(message=message, e_type=EmailError)


class SchemaError(BaseError):
    def __init__(self, message=None, data=None):
        super(SchemaError, self).__init__(message=message, e_type=SchemaError, data=data)


# -------------------- 自定义异常 ----------------------------------------------


def validate_ipv4_address(value):
    try:
        ipaddress.IPv4Address(value)
    except ValueError:
        raise EmailError("invalid IPv4 address.")
    else:
        # Leading zeros are forbidden to avoid ambiguity with the octal
        # notation. This restriction is included in Python 3.9.5+.
        # TODO: Remove when dropping support for PY39.
        if any(octet != "0" and octet[0] == "0" for octet in value.split(".")):
            raise EmailError("invalid IPv4 address.")


def is_valid_ipv6_address(ip_str):
    """
    Return whether or not the `ip_str` string is a valid IPv6 address.
    """
    try:
        ipaddress.IPv6Address(ip_str)
    except ValueError:
        return False
    return True


def validate_ipv6_address(value):
    if not is_valid_ipv6_address(value):
        raise EmailError("invalid IPv6 address.")


def validate_ipv46_address(value):
    try:
        validate_ipv4_address(value)
    except Exception:
        try:
            validate_ipv6_address(value)
        except Exception:
            raise EmailError("invalid IPv4 or IPv6 address.")


class EmailValidate(object):
    message = "Enter a valid email address."
    code = "invalid"
    user_regex = re.compile(
        r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*\Z"  # dot-atom
        r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"\Z)',  # quoted-string
        re.IGNORECASE,
    )
    domain_regex = re.compile(
        # max length for domain name labels is 63 characters per RFC 1034
        r"((?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+)(?:[A-Z0-9-]{2,63}(?<!-))\Z",
        re.IGNORECASE,
    )
    literal_regex = re.compile(
        # literal form, ipv4 or ipv6 address (SMTP 4.1.3)
        r"\[([A-f0-9:.]+)\]\Z",
        re.IGNORECASE,
    )
    domain_allowlist = ["localhost"]

    def __init__(self, message=None, code=None, allowlist=None, *, whitelist=None):
        if whitelist is not None:
            allowlist = whitelist
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code
        if allowlist is not None:
            self.domain_allowlist = allowlist

    def __call__(self, value):
        if not value or "@" not in value:
            raise EmailError(self.message)

        user_part, domain_part = value.rsplit("@", 1)

        if not self.user_regex.match(user_part):
            raise EmailError(self.message)

        if domain_part not in self.domain_allowlist and not self.validate_domain_part(domain_part):
            # Try for possible IDN domain-part
            try:
                domain_part = domain_part.encode("idna").decode("ascii")
            except UnicodeError:
                pass
            else:
                if self.validate_domain_part(domain_part):
                    return
            raise EmailError(self.message)

    def __eq__(self, other):
        return (
            isinstance(other, EmailValidate)
            and (self.domain_allowlist == other.domain_allowlist)
            and (self.message == other.message)
            and (self.code == other.code)
        )

    def validate_domain_part(self, domain_part):
        if self.domain_regex.match(domain_part):
            return True

        literal_match = self.literal_regex.match(domain_part)
        if literal_match:
            ip_address = literal_match[1]
            # noinspection PyBroadException
            try:
                validate_ipv46_address(ip_address)
                return True
            except Exception:
                pass
        return False


# -------------------- 邮箱验证 ------------------------------------------------


# 手机号正则表达式
REGEX_PHONE = re.compile(r"1\d{10}")
_GEN_DELIMS_REGEX = re.compile(r"[\:\/\?\#\[\]\@]")
_SUB_DELIMS_REGEX = re.compile(r"[\!\$\&\'\(\)\*\+\,\;\=]")


def is_phone(phone: str = None) -> bool:
    if not phone:
        return False
    return bool(REGEX_PHONE.fullmatch(phone))


def is_email(email: str = None) -> bool:
    if not email:
        return False
    email_validator = EmailValidate()
    result = True
    try:
        email_validator(email)
    except EmailError:
        result = False
    return result


def has_uri_reversed_character(s: str) -> bool:
    """Ref: https://tools.ietf.org/html/rfc3986#section-2.2"""
    return bool(_GEN_DELIMS_REGEX.search(s) or _SUB_DELIMS_REGEX.search(s))


class Validator(object):
    accept_type = None

    def validate(self, value, field_name):
        try:
            data = self.accept_type(value) if value is not None else None
        except (ValueError, decimal.InvalidOperation):
            raise ParamError(f"{field_name}参数不正确")
        return data


class Validation(object):
    def __init__(self, validators: Union[Validator, List[Validator]], field_name: str, optional: bool = False):
        self.validators = validators if isinstance(validators, list) else [validators]
        self.field_name = field_name
        self.optional = optional


class FloatValidator(Validator):
    """浮点数数据类型验证器"""

    accept_type = float


class IntValidator(Validator):
    """整型数据类型验证器"""

    accept_type = int

    def __init__(self, min_value: int = None, max_value: int = None, allow_null: bool = False):
        self.min_value = min_value
        self.max_value = max_value
        self.allow_null = allow_null

    def validate(self, value, field_name):
        if value is None:
            if self.allow_null:
                return None
            raise NullError(f"{field_name}不能为空")
        # 调用父类的validate方法
        data = super().validate(value, field_name)
        if self.min_value is not None and data < self.min_value:
            raise MinLengthError(f"{field_name}最小值为{self.min_value}")
        elif self.max_value is not None and data > self.max_value:
            raise MaxLengthError(f"{field_name}最大值为{self.max_value}")
        return data


class DictValidator(Validator):
    """字典数据类型验证器"""

    accept_type = dict

    def validate(self, value, field_name):
        if isinstance(value, self.accept_type):
            return value
        try:
            data = dict(json.loads(value)) if value is not None else None
        except Exception:
            raise ParamError(f"{field_name}参数不正确")
        return data


class DecimalValidator(Validator):
    accept_type = decimal.Decimal

    def __init__(self, default=None, decimal_places=2, rounding=decimal.ROUND_HALF_UP):
        self.default = default
        self.decimal_places = decimal_places
        self.rounding = rounding

    def validate(self, value, field_name):
        if value is None and self.default is not None:
            value = self.default
        elif value is None:
            raise NullError(f"{field_name}不能为空")
        value = super().validate(value, field_name)
        quantize = f".{'0' * (self.decimal_places - 1)}1"
        return decimal.Decimal(value).quantize(decimal.Decimal(quantize), rounding=self.rounding)


class StrValidator(Validator):
    accept_type = str

    def __init__(
        self,
        length=None,
        min_length=None,
        max_length=None,
        allow_null=False,
        allow_reversed_characters=True,
        strip: bool = True,
    ):
        self.length = length
        self.min_length = min_length
        self.max_length = max_length
        self.allow_null = allow_null
        self.strip = strip
        self.allow_reversed_characters = allow_reversed_characters

    def validate(self, value, field_name):
        if value is None:
            if self.allow_null:
                return None
            raise NullError(f"{field_name}不能为空")
        data = super().validate(value, field_name)
        if not self.allow_reversed_characters and has_uri_reversed_character(data):
            raise ParamError(f"{field_name}不允许包含URI保留字符")
        if self.length and len(data) != self.length:
            raise LengthError(f"{field_name}长度必须为{self.length}")
        if self.min_length and len(data) < self.min_length:
            raise MinLengthError(f"{field_name}长度不能小于{self.min_length}")
        if self.max_length and len(data) > self.max_length:
            raise MaxLengthError(f"{field_name}长度不能超过{self.max_length}")
        return data


class UUIDValidator(StrValidator):
    """UUID验证"""

    accept_type = str

    def __init__(self, allow_null: bool = False):
        super(UUIDValidator, self).__init__(length=32, allow_null=allow_null)


class BoolValidator(Validator):
    """ "GET 方法无法使用此验证器验证"""

    accept_type = bool


class EmailValidator(Validator):
    """邮箱验证"""

    accept_type = str

    def __init__(self, allow_null: bool = False):
        self.allow_null = allow_null

    def validate(self, value, field_name):
        # 长度为0的认为是None
        if value is None or not len(value.strip()):
            if self.allow_null:
                return None
            raise NullError(f"{field_name}不能为空")
        if not is_email(value):
            raise EmailError(f"{field_name}邮箱格式不正确")
        return value


class SchemaValidator(Validator):
    def __init__(self, schema):
        if isinstance(schema, dict):
            self.schema = schema
        else:
            raise ValueError("schema should be a dictionary")

    def validate(self, value, field_name):
        data = {}
        for field, validation in self.schema.items():
            if isinstance(validation, Validation):
                _required = not validation.optional
                _field_name = validation.field_name
                if _required and field not in value:
                    error_msg = f"{_field_name}未传递"
                    if field_name is not None:
                        error_msg = f"{_field_name}中{error_msg}"
                    raise SchemaError(error_msg, data={"field": field})
                if field in value:
                    success = False
                    for validator in validation.validators:
                        try:
                            data[field] = validator.validate(value[field], _field_name)
                            success = True
                            break
                        except BaseError as e:
                            if len(validation.validators) == 1:
                                raise e
                            continue
                    if not success:
                        raise SchemaError(f"{_field_name}参数错误", data={"field": field})
        return value


class PhoneValidator(StrValidator):
    def __init__(self, allow_null: bool = False):
        super(PhoneValidator, self).__init__(length=11, allow_null=allow_null)

    def validate(self, value, field_name):
        # 长度为0的字符串认为是None
        if value is None or not len(value.strip()):
            if self.allow_null:
                return None
        data = super().validate(value, field_name)
        if data and not is_phone(data):
            raise ParamError("手机号格式不正确")
        return data


class UsernameValidator(StrValidator):
    def __init__(self, allow_null=False):
        super(UsernameValidator, self).__init__(max_length=50, allow_null=allow_null)

    def validate(self, value, field_name):
        try:
            data = super().validate(value, field_name)
            if data is not None and ("@" in data or data.isdigit()):
                raise ParamError()
        except ParamError:
            raise ParamError(f"{field_name}用户名格式不正确, 应为数字和字母组合, 不能包含@特殊符号")
        return data


class DateValidator(Validator):
    def validate(self, value, field_name):
        try:
            data = datetime.datetime.strptime(value, "%Y-%m-%d").date()
        except (ValueError, decimal.InvalidOperation):
            raise ParamError(f"{field_name}日期格式不正确")
        return data


class DatetimeValidator(Validator):
    def validate(self, value, field_name):
        try:
            data = datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        except (ValueError, decimal.InvalidOperation):
            raise ParamError(f"{field_name}时间格式不正确")
        return data


class EnumValidator(Validator):
    def __init__(self, enum_type, accept_type, allow_null: bool = False):
        self.enum_type = enum_type
        self.accept_type = accept_type
        self.allow_null = allow_null

    def validate(self, value, field_name):
        try:
            data = self.enum_type(self.accept_type(value)).value if (not self.allow_null or value) else None
        except Exception:
            raise ParamError(f"{field_name}参数不正确")
        return data


class ListValidator(Validator):
    def __init__(self, validator, max_length: int = None, allow_null: bool = False, strict: bool = False):
        self.validator = validator
        self.max_length = max_length
        self.allow_null = allow_null
        self.strict = strict

    def validate(self, value, field_name):
        try:
            if value is None:
                if self.allow_null:
                    return None
                else:
                    raise NullError(f"{field_name}参数不允许为空")
            data = []
            if not value:
                return data
            if not isinstance(value, List):
                if self.strict:
                    raise ParamError(f"{field_name}参数必须为列表类型")
                if value is None:
                    raise NullError(f"{field_name}参数不允许为空")
                value = value.split(",")
            if self.max_length and len(value) > self.max_length:
                raise MaxLengthError(f"{field_name}参数长度最大为{self.max_length}")
            for d in value:
                _d = self.validator.validate(d, field_name)
                data.append(_d)
        except Exception as e:
            # if not isinstance(e, ParamError):
            #     e = ParamError(f"{field_name}参数不正确")
            raise e
        return data


# ----------------------- 上面是验证器 -------------------------------------------

QUESTION_VALIDATORS = [
    ListValidator(DictValidator(), strict=True),
    ListValidator(StrValidator(), strict=True),
    StrValidator(),
]
