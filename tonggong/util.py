import base64
import calendar
import datetime
import json
import logging
import re
from typing import Union


def base64_encode(value: str) -> str:
    """对字符串进行 base64 编码， 去掉末尾的 ="""
    return base64.b64encode(value.encode("utf8"), altchars=b"+-").decode("utf8").rstrip("=")


def base64_decode(value: str) -> str:
    """对字符串进行 base64 解码"""
    return base64.b64decode(padding_base64(value), altchars=b"+-").decode("utf8")


def padding_base64(value: str) -> str:
    num = len(value) % 4
    num = 4 - num if num else 0
    return value + "=" * num


def json_dumps(obj, separators=(",", ":"), sort_keys=True, ensure_ascii=False, **kwargs) -> str:
    return json.dumps(obj, separators=separators, sort_keys=sort_keys, ensure_ascii=ensure_ascii, **kwargs)


def add_months(date: datetime.date, num: int) -> datetime.date:
    month = date.month - 1 + num
    year = date.year + month // 12
    month = month % 12 + 1
    day = min(date.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


def minus_months(date: datetime.date, num: int) -> datetime.date:
    year = date.year - num // 12
    if num % 12 >= date.month:
        year = year - 1
        month = date.month + 12 - num % 12
    else:
        month = date.month - num % 12
    day = min(date.day, calendar.monthrange(year, month)[1])
    return datetime.date(year=year, month=month, day=day)


def prevent_django_request_warnings(original_func):
    """
    add this decorator can prevent the django request class from throwing warnings.
    """

    def new_func(*args, **kwargs):
        # raise logging level to ERROR
        logger = logging.getLogger("django.request")
        previous_logging_level = logger.getEffectiveLevel()
        logger.setLevel(logging.ERROR)

        # trigger original function that would throw warning
        original_func(*args, **kwargs)

        # lower logging level back to previous
        logger.setLevel(previous_logging_level)

    return new_func


def is_int(num: Union[str, float]) -> bool:
    if isinstance(num, str):
        num = float(num)
    return abs(round(num) - num) <= 1e-7


_GEN_DELIMS_REGEX = re.compile(r"[\:\/\?\#\[\]\@]")
_SUB_DELIMS_REGEX = re.compile(r"[\!\$\&\'\(\)\*\+\,\;\=]")


def has_uri_reversed_character(s: str) -> bool:
    """Ref: https://tools.ietf.org/html/rfc3986#section-2.2"""
    return bool(_GEN_DELIMS_REGEX.search(s) or _SUB_DELIMS_REGEX.search(s))
