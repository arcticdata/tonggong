class BaseValidationError(Exception):
    def __init__(self, message=None, e_type=None, data=None):
        if not isinstance(message, str):
            message = f"{message}"
        self.message = message
        self.e_type = e_type
        self.data = data

    def __str__(self):
        return f"{self.e_type}: {self.message}"


class ParamError(BaseValidationError):
    def __init__(self, message=None):
        super(ParamError, self).__init__(message=message, e_type=ParamError)


class MinLengthError(BaseValidationError):
    def __init__(self, message=None):
        super(MinLengthError, self).__init__(message=message, e_type=MinLengthError)


class MaxLengthError(BaseValidationError):
    def __init__(self, message=None):
        super(MaxLengthError, self).__init__(message=message, e_type=MaxLengthError)


class NullError(BaseValidationError):
    def __init__(self, message=None):
        super(NullError, self).__init__(message=message, e_type=NullError)


class LengthError(BaseValidationError):
    def __init__(self, message=None):
        super(LengthError, self).__init__(message=message, e_type=LengthError)


class EmailError(BaseValidationError):
    def __init__(self, message=None):
        super(EmailError, self).__init__(message=message, e_type=EmailError)


class SchemaError(BaseValidationError):
    def __init__(self, message=None, data=None):
        super(SchemaError, self).__init__(message=message, e_type=SchemaError, data=data)
