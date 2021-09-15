class BaseValidationError(Exception):
    def __init__(self, message=None, data=None):
        if not isinstance(message, str):
            message = f"{message}"
        self.message = message
        self.data = data

    def __repr__(self):
        return f"{type(self)}: {self.message}"


class ParamError(BaseValidationError):
    """参数错误异常类型"""


class MinLengthError(BaseValidationError):
    """小于最小长度异常类型"""


class MaxLengthError(BaseValidationError):
    """超出最大长度异常类型"""


class NullError(BaseValidationError):
    """参数为空异常类型"""


class LengthError(BaseValidationError):
    """长度不符合异常类型"""


class EmailError(BaseValidationError):
    """邮箱格式错误异常类型"""


class SchemaError(BaseValidationError):
    """schema错误异常类型"""
