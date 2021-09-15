import re

from .errors import EmailError

# 手机号正则表达式
_REGEX_PHONE = re.compile(r"1\d{10}")
_GEN_DELIMS_REGEX = re.compile(r"[\:\/\?\#\[\]\@]")
_SUB_DELIMS_REGEX = re.compile(r"[\!\$\&\'\(\)\*\+\,\;\=]")


def is_phone(phone: str = None) -> bool:
    if not phone:
        return False
    return bool(_REGEX_PHONE.fullmatch(phone))


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


class EmailValidate(object):
    message = None
    code = None
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

    def __init__(self, message=None, code=None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        if not value or "@" not in value:
            raise EmailError(self.message)

        user_part, domain_part = value.rsplit("@", 1)

        if not self.user_regex.match(user_part):
            raise EmailError(self.message)

        if not self.validate_domain_part(domain_part):
            raise EmailError(self.message)

    def validate_domain_part(self, domain_part):
        if self.domain_regex.match(domain_part):
            return True
        return False
