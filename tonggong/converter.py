import datetime
import decimal
from typing import Union


class Converter(object):
    """ 将字符串转换成对用的 Python 类型 """

    @classmethod
    def get_date(cls, value: str, str_format="%Y-%m-%d") -> datetime.date:
        return datetime.datetime.strptime(value.strip(), str_format).date()

    @classmethod
    def get_int(cls, value) -> Union[int, None]:
        value = cls.get_float(value)
        return round(value) if value is not None else None

    @classmethod
    def get_str(cls, value) -> Union[str, None]:
        if value is None:
            return None
        return str(value).strip()

    @classmethod
    def get_float(cls, value) -> Union[float, None]:
        if value is None:
            return None
        if not isinstance(value, str):
            value = cls.get_str(value)
        value = value.strip()
        if value.endswith("-"):  # For SAP
            value = "-{}".format(value[:-1])
        if not value:
            return None
        return float(value)

    @classmethod
    def get_decimal(cls, value, decimal_places=2, rounding=decimal.ROUND_HALF_UP) -> Union[decimal.Decimal, None]:
        value = cls.get_float(value)
        if value is None:
            return None
        quantize = ".{}1".format("0" * (decimal_places - 1))
        return decimal.Decimal(value).quantize(decimal.Decimal(quantize), rounding=rounding)

    @classmethod
    def get_latitude_or_longitude(cls, value) -> Union[decimal.Decimal, None]:
        return cls.get_decimal(value, decimal_places=8)
