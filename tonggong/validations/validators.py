import datetime
import decimal
import json
from typing import List, Union

from .errors import *
from .utils import has_uri_reversed_character, is_email, is_phone


class Validator(object):
    accept_type = None

    def validate(self, value: any, field_name: str):
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

    def validate(self, value: int, field_name: str):
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

    def validate(self, value: Union[str, dict], field_name: str):
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

    def validate(self, value, field_name: str):
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

    def validate(self, value: str, field_name: str):
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

    def validate(self, value: str, field_name: str):
        # 长度为0的认为是None
        if value is None or not len(value.strip()):
            if self.allow_null:
                return None
            raise NullError(f"{field_name}不能为空")
        if not is_email(value):
            raise EmailError(f"{field_name}邮箱格式不正确")
        return value


class SchemaValidator(Validator):
    def __init__(self, schema: dict):
        if isinstance(schema, dict):
            self.schema = schema
        else:
            raise ParamError("schema should be a dictionary")

    def validate(self, value: dict, field_name: str = None):
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
                        except BaseValidationError as e:
                            if len(validation.validators) == 1:
                                raise e
                            continue
                    if not success:
                        raise SchemaError(f"{_field_name}参数错误", data={"field": field})
        return value


class PhoneValidator(StrValidator):
    def __init__(self, allow_null: bool = False):
        super(PhoneValidator, self).__init__(length=11, allow_null=allow_null)

    def validate(self, value: str, field_name: str):
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

    def validate(self, value: str, field_name: str):
        try:
            data = super().validate(value, field_name)
            if data is not None and ("@" in data or data.isdigit()):
                raise ParamError(f"{field_name}用户名格式不正确, 应为数字和字母组合, 不能包含@特殊符号")
        except ParamError as e:
            raise e
        return data


class DateValidator(Validator):
    def validate(self, value: str, field_name: str):
        try:
            data = datetime.datetime.strptime(value, "%Y-%m-%d").date()
        except (ValueError, decimal.InvalidOperation):
            raise ParamError(f"{field_name}日期格式不正确")
        return data


class DatetimeValidator(Validator):
    def validate(self, value: str, field_name: str):
        try:
            data = datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        except (ValueError, decimal.InvalidOperation):
            raise ParamError(f"{field_name}时间格式不正确")
        return data


class EnumValidator(Validator):
    def __init__(self, enum_type: any, accept_type: any, allow_null: bool = False):
        self.enum_type = enum_type
        self.accept_type = accept_type
        self.allow_null = allow_null

    def validate(self, value: any, field_name: str):
        try:
            data = self.enum_type(self.accept_type(value)).value if (not self.allow_null or value) else None
        except Exception:
            raise ParamError(f"{field_name}参数不正确")
        return data


class ListValidator(Validator):
    def __init__(self, validator: Validator, max_length: int = None, allow_null: bool = False, strict: bool = False):
        self.validator = validator
        self.max_length = max_length
        self.allow_null = allow_null
        self.strict = strict

    def validate(self, value: Union[List, str], field_name: str):
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
                value = value.split(",")
            if self.max_length and len(value) > self.max_length:
                raise MaxLengthError(f"{field_name}参数长度最大为{self.max_length}")
            for d in value:
                _d = self.validator.validate(d, field_name)
                data.append(_d)
        except Exception as e:
            raise e
        return data
