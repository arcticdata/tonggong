import dataclasses
import unittest

from tonggong.unittest import TestCaseMixin


@dataclasses.dataclass
class Data:
    num: int = 42
    name: str = "kristine"


@dataclasses.dataclass
class Response:
    status_code: int = 200
    data = {"message": "ok"}


class UnittestTestCase(TestCaseMixin, unittest.TestCase):
    def test_ok(self):
        functions = {
            200: self.http_ok,
            201: self.http_201,
            204: self.http_204,
            400: self.http_bad,
            403: self.http_403,
            404: self.http_404,
        }
        for code, func in functions.items():
            func(Response(code), message="ok")

    def test_assert_increases(self):
        value = 10
        with self.assert_increases(5, lambda: value):
            value += 5

        obj = Data()
        with self.assert_increases(5, lambda: obj.num):
            obj.num += 5

    def test_assert_same(self):
        data = {"key": "value"}
        self.assert_same(data, key="value")

        data = ["key", "value"]
        self.assert_same(data, _0="key", _1="value", length=2)

        data = {
            "nested": {
                "dict": {"key": "value"},
                "list": ["key", "value"],
                "object": Data(),
                "bool_false": None,
                "bool_true": "value",
            },
        }
        self.assert_same(
            data,
            nested__dict__key="value",
            nested__list__0="key",
            nested__list__1="value",
            nested__list__length=2,
            nested__object___name="kristine",
            nested__object___name__length=8,
            nested__bool_false__bool=False,
            nested__bool_true__bool=True,
        )
