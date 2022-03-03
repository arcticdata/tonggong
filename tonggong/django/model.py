class ModelMixin:
    """集合了一些 Model 的方法。collects some model helper methods.

    Examples::

        class User(models.Model, ModelMixin):
            name = models.CharField()
            age = models.IntegerField()
        User.increase(age=1)
        User.modify(name='kevin')
    """

    def modify(self, need_refresh=False, **fields):
        """只修改指定域。specify fields to update.

        Examples::

            user.modify(age=18)
        """
        for field, value in fields.items():
            if field not in self._meta.fields_map:
                raise ValueError(f"Invalid field name {field}")
            setattr(self, field, value)
        self.save(update_fields=list(fields.keys()))
        if need_refresh:
            self.refresh_from_db(fields=fields)

    def increase(self, **fields):
        """利用 F() 来修改指定域。increase fields value using F().

        Examples::

            user.increase(points=10)
        """
        from django.db import models

        fields = {field: models.F(field) + amount for field, amount in fields.items()}
        self.modify(need_refresh=True, **fields)
