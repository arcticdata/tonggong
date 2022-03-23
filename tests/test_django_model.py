import unittest

from tonggong.django.model import ModelMixin


class Meta:
    def get_field(self, field: str):
        from django.core.exceptions import FieldDoesNotExist

        if field not in {"key": "key", "name": "name"}:
            raise FieldDoesNotExist("not exist")
        return field


class User(ModelMixin):
    def __init__(self):
        self.update_fields = None
        self.fields = None
        self._meta = Meta()

    def save(self, update_fields):
        self.update_fields = update_fields

    def refresh_from_db(self, fields):
        self.fields = fields


class DjangoModelTest(unittest.TestCase):
    def test_modify(self):
        user = User()
        user.modify(key="value", name="unknown")
        self.assertIsNone(user.fields)
        self.assertEqual(user.update_fields, ["key", "name"])

    def test_modify_fail(self):
        with self.assertRaises(ValueError):
            User().modify(gender="male")
