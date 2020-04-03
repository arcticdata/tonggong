import calendar
import datetime
import json


def padding_base64(base64_str: str) -> str:
    num = len(base64_str) % 4
    num = 4 - num if num else 0
    return base64_str + "=" * num


def json_dumps(
    obj, separators=(",", ":"), sort_keys=True, ensure_ascii=False, **kwargs
) -> str:
    return json.dumps(
        obj,
        separators=separators,
        sort_keys=sort_keys,
        ensure_ascii=ensure_ascii,
        **kwargs
    )


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
