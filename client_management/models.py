from django.db import models

from mailing_management.models import NULLABLE

# Create your models here.


class Client(models.Model):
    """
    Представление клиента в базе данных.
    """
    email = models.EmailField(max_length=100, verbose_name='почта')
    first_name = models.CharField(max_length=250, verbose_name='имя', **NULLABLE)
    last_name = models.CharField(max_length=250, verbose_name='фамилия', **NULLABLE)
    surname = models.CharField(max_length=250, verbose_name='отчество', **NULLABLE)
    comment = models.TextField(verbose_name='комментарий', **NULLABLE)

    def __str__(self) -> str:
        return f'ФИО: {self.last_name} {self.first_name}' + \
            f'{self.surname}, email: {self.email}'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = "клиенты"
        ordering = ('first_name', 'last_name', 'surname')
