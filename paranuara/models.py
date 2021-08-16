import uuid
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from food.models import Vegetable, Fruit


# Create your models here.

class Company(models.Model):
    """
        Model for Company
    """
    index = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(_('name'), max_length=255, null=False, unique=True)

    class Meta:
        db_table = 'company'

    def __str__(self):
        return u'{0}'.format(self.name)


class People(models.Model):
    """
        Model for People
    """
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    )

    index = models.PositiveIntegerField(primary_key=True)
    company = models.ForeignKey(Company, related_name='peoples', null=True,
                                on_delete=models.SET_NULL)
    id = models.CharField(_('id'), max_length=255, null=False, unique=True)
    name = models.CharField(_('name'), max_length=255, null=False, unique=True)
    guid = models.UUIDField(_('guid'), default=uuid.uuid4, editable=False)
    has_died = models.BooleanField(_('has died'), default=False)
    balance = models.CharField(_('balance'), max_length=255, null=False)
    picture = models.URLField(_('picture'), max_length=255)
    age = models.PositiveSmallIntegerField(_('age'),
                                           validators=[MinValueValidator(0)])
    eyeColor = models.CharField(_('eye color'), max_length=50, null=False)
    gender = models.CharField(_('gender'), max_length=20,
                              choices=GENDER_CHOICES, default='Male')
    email = models.EmailField(_('email'), max_length=255, null=False,
                              unique=True)
    phone = models.CharField(_('phone'), max_length=20, null=False)
    # if required below address field can also be created as a reference of
    # another table Address containing st addr, state, city and zipcode
    address = models.CharField(_('address'), max_length=255, null=False)
    about = models.TextField(_('about'))
    registered = models.DateTimeField(_('registered'), null=False)
    greeting = models.TextField(_('greeting'))
    tags = ArrayField(
        models.CharField(max_length=20, blank=True)
    )
    friend = models.ManyToManyField('self', symmetrical=False, related_name='friends')
    vegetable = models.ManyToManyField(Vegetable, related_name='peoples')
    fruit = models.ManyToManyField(Fruit, related_name='peoples')

    class Meta:
        db_table = 'people'

    def __str__(self):
        return u'{0}'.format(self.name)
