import contextlib
import http
import unittest
from typing import Callable


class TestCaseMixin(unittest.TestCase):
    """
    增加一些便于测试的小方法的 Mixin

    Examples:

        from rest_framework.test import APITestCase

        class TestCase(APITestCase, TestCaseMixin):
            pass

        class ExampleTest(TestCase):

            def test_something(self):
                response = self.client.get(url)
                self.http_ok(response)

    For details, see <tests.test_unittest.FuncTestCaseAPITests>
    """

    def http_ok(self, response, status_code=http.HTTPStatus.OK, **kwargs):
        self.assertEqual(status_code, response.status_code, f"status code should be {status_code}")
        if kwargs:
            self.assert_same(response.data, **kwargs)
        return self

    def http_201(self, response, **kwargs):
        return self.http_ok(response, http.HTTPStatus.CREATED, **kwargs)

    def http_204(self, response, **kwargs):
        return self.http_ok(response, http.HTTPStatus.NO_CONTENT, **kwargs)

    def http_bad(self, response, **kwargs):
        return self.http_ok(response, http.HTTPStatus.BAD_REQUEST, **kwargs)

    def http_403(self, response, **kwargs):
        return self.http_ok(response, http.HTTPStatus.FORBIDDEN, **kwargs)

    def http_404(self, response, **kwargs):
        return self.http_ok(response, http.HTTPStatus.NOT_FOUND, **kwargs)

    def assert_increases(self, delta: int, func: Callable, name=""):
        """shortcuts to verify func change is equal to delta"""
        test_case = self

        class Detector(contextlib.AbstractContextManager):
            def __init__(self):
                self.previous = None

            def __enter__(self):
                self.previous = func()

            def __exit__(self, exc_type, exc_val, exc_tb):
                if not exc_val:
                    test_case.assertEqual(self.previous + delta, func(), f"{name} should change {delta}".strip())

        return Detector()

    def assert_model_increases(self, *models, **lookups):
        """shortcuts to verify value change"""
        stack = contextlib.ExitStack()
        for case in models:
            if isinstance(case, tuple):
                model, delta = case
            else:
                model, delta = case, 1
            stack.enter_context(self.assert_increases(delta, model.objects.filter(**lookups).count, model.__name__))
        return stack

    def assert_same(self, actual_data, **expects):
        """shortcuts to compare value (support nested dictionaries, lists and array length)"""

        def _get_key(_data, _key: str):
            """get the expanded value"""
            _value = _data
            for part in _key.split("__"):
                if part == "length":
                    _value = len(_value)
                elif part == "bool":
                    _value = bool(_value)
                elif part.startswith("_"):
                    try:
                        _value = _value[int(part[1:])]
                    except ValueError:
                        try:
                            _value = getattr(_value, part[1:])
                        except AttributeError:
                            _value = _value[part[1:]]
                else:
                    try:
                        _value = _value[int(part)]
                    except ValueError:
                        _value = _value[part]
            return _value

        for key, expect in expects.items():
            actual = _get_key(actual_data, key)
            try:
                self.assertEqual(
                    expect,
                    actual,
                    f"{key} value not match.\nExpect: {expect} ({type(expect)})\nActual: {actual} ({type(actual)})",
                )
            except Exception:
                print("\nAssertionError:")
                print(f"Actual: {actual_data}")
                print(f"Expect: {expects}")
                raise
        return self
