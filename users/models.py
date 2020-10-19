from django.contrib.auth.models import AbstractUser
from django.db import models

from common.models import TimestampModel
from users import roles
from .managers import UserManager


class Permission(TimestampModel):
    codename = models.CharField(max_length=255, primary_key=True, unique=True)

    class Meta:
        ordering = ('codename',)

    def __str__(self):
        return self.codename


class Role(TimestampModel):
    codename = models.CharField(max_length=255, primary_key=True, unique=True)
    ru_name = models.CharField(max_length=255, blank=True, null=True)
    permissions = models.ManyToManyField(Permission)

    class Meta:
        ordering = ('codename',)

    def __str__(self):
        return self.codename


class User(AbstractUser, TimestampModel):
    first_name = models.CharField(max_length=255, verbose_name='First Name')
    last_name = models.CharField(max_length=255, verbose_name='Last Name')
    email = models.EmailField(verbose_name='Email', unique=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, default=roles.ADMINISTRATOR['codename'])

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return "{first_name} {last_name}".format(first_name=self.first_name, last_name=self.last_name)
