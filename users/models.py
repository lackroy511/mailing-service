from django.db import models
from django.contrib.auth.models import AbstractUser

from mailing_management.models import NULLABLE


# Create your models here.


class User(AbstractUser):

    username = None
    email = models.EmailField(unique=True, verbose_name='email')
    avatar = models.ImageField(upload_to='users_avatar',
                               verbose_name='аватар', **NULLABLE)
    first_name = models.CharField(max_length=50,
                                  verbose_name='имя', **NULLABLE)
    last_name = models.CharField(max_length=50,
                                 verbose_name='фамилия', **NULLABLE)
    is_active = models.BooleanField(default=False, verbose_name='активирован')

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
