from django.contrib.postgres.fields import CICharField
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Vegetable(models.Model):
    """
        Model for Vegetable
    """
    name = CICharField(_('name'), max_length=255, null=False, unique=True)

    class Meta:
        db_table = 'vegetable'

    def __str__(self):
        return u'{0}'.format(self.name)


class Fruit(models.Model):
    """
        Model for Fruit
    """
    name = CICharField(_('name'), max_length=255, null=False, unique=True)

    class Meta:
        db_table = 'fruit'

    def __str__(self):
        return u'{0}'.format(self.name)
