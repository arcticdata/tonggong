import datetime
from typing import Union


_special_characters = """!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~！？｡＂＃＄％＆＇（）＊＋－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏·° \t\n\r\v\f"""
_translator = str.maketrans('', '', _special_characters)


def remove_special_character(_str: str) -> str:
    """ 过滤掉字符串中的特殊字符 """
    return _str.translate(_translator)


class Formatter(object):
    @classmethod
    def money(cls, value) -> str:
        if value is None:
            return '-'
        from tonggong.converter import Converter
        value = Converter.get_decimal(value)
        _base = '({})' if value < 0 else '{}'
        value = abs(value)
        if value > 100000000:
            return '{}亿元'.format(_base.format(Converter.get_decimal(value / 100000000)))
        if value > 10000:
            return '{}万元'.format(_base.format(Converter.get_int(value / 10000)))
        return '{}元'.format(_base.format(value))

    @classmethod
    def text(cls, value) -> str:
        return str(value)

    @classmethod
    def int(cls, value) -> str:
        return str(int(value))

    @classmethod
    def date(cls, value: Union[str, datetime.date, datetime.datetime]) -> str:
        if isinstance(value, str):
            value = datetime.datetime.strptime(value, '%Y-%m-%d')
        return value.strftime('%Y-%m-%d')

    @classmethod
    def month(cls, _year, _month) -> str:
        return '{}年{}月'.format(_year, _month)

    @classmethod
    def week(cls, _year, _week) -> str:
        value = '{}-{}-1'.format(_year, _week)
        _monday = datetime.datetime.strptime(value, '%Y-%W-%w')
        return Formatter.date(_monday)

    @classmethod
    def quarter(cls, _year, _quarter) -> str:
        return '{}年{}季度'.format(_year, _quarter)

    @classmethod
    def year(cls, _year) -> str:
        return '{}年'.format(_year)

    @classmethod
    def format_number_to_chinese_display(cls, number: float) -> str:
        """ 数字的中文展示 """
        _num = 100000000
        if not number % 100 and 10000 <= number < _num:
            return '{}万'.format(number / 10000)
        if not number % 100000 and number >= _num:
            return '{}亿'.format(number / _num)
        return str(number)


class YAxisFormatter(Formatter):
    @classmethod
    def money(cls, value, gap=0) -> str:
        return cls._number(value, gap)

    @classmethod
    def int(cls, value, gap=0) -> str:
        return cls._number(value, gap)

    @classmethod
    def decimal(cls, value, gap=0) -> str:
        return cls._number(value, gap)

    @classmethod
    def float(cls, value, gap=0) -> str:
        return cls._number(value, gap)

    @classmethod
    def percent(cls, value) -> str:
        if isinstance(value, str):
            if not value.endswith('%'):
                value = str(float(value) * 100) + '%'
            return value
        else:
            return str(value * 100) + '%'

    @classmethod
    def text(cls, value) -> str:
        if isinstance(value, (list, tuple, set)):
            value = ','.join(map(str, value))
        return str(value)

    @classmethod
    def _number(cls, value, gap=0) -> str:
        unit = ''
        flag = 1
        point = 0
        if gap > 100000000:
            unit = '亿'
            flag = 100000000
        elif gap > 10000:
            flag = 10000
            unit = '万'
        if 0 < gap <= 5 or 10000 < gap <= 50000 or 100000000 < gap <= 500000000:
            point = 2
        value = ('%.{}f'.format(point)) % (value / flag)
        return value + unit


class XAxisFormatter(Formatter):
    @classmethod
    def text(cls, value) -> str:
        if isinstance(value, (list, tuple, set)):
            value = ','.join(map(str, value))
        return str(value)
