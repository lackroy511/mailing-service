from django.db import models

from users.models import User
# Create your models here.

NULLABLE = {'null': True, 'blank': True}


class Mailing(models.Model):
    """
    Представление сообщения в базе данных.
    """
    massage_subject = models.CharField(
        max_length=250, verbose_name='тема сообщения',
    )
    massage_text = models.TextField(verbose_name='текст сообщения')

    user = models.ForeignKey(
        User, verbose_name='пользователь', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'Тема сообщения: {self.massage_subject}'

    class Meta:
        verbose_name = 'Сообщение для рассылки'
        verbose_name_plural = 'Сообщения для рассылки'


class MailingSettings(models.Model):
    """
    Представление настроек рассылки в базе данных.
    """

    MAILING_PERIODICITY_CHOICES = (
        ('M H * * *', 'Раз в день'),
        ('M H * * 1', 'Раз в неделю'),
        ('M H 1 * *', 'Раз в месяц'),
    )

    MAILING_STATUS_CHOICES = (
        ('создана', 'Создана'),
        ('отправляется', 'Отправляется'),
        ('завершена', 'Завершена'),
        ('устарела', 'Устарела'),
    )

    mailing_time = models.TimeField(
        auto_now=False, auto_now_add=False, verbose_name='время рассылки',
    )
    end_mailing_time = models.DateTimeField(
        auto_now=False, auto_now_add=False,
        verbose_name='дата и время окончания рассылки',
    )
    mailing_periodicity = models.CharField(
        max_length=40, verbose_name='периодичность в формате crontab',
        choices=MAILING_PERIODICITY_CHOICES,
    )
    mailing_periodicity_display = models.CharField(
        max_length=40, verbose_name='периодичность', **NULLABLE,
    )
    mailing_status = models.CharField(
        max_length=20, verbose_name='cтатус', default='Создана',
        choices=MAILING_STATUS_CHOICES,
    )
    mailing_is_active = models.BooleanField(
        default=True, verbose_name='Рассылка активна',
    )
    mailing = models.OneToOneField(
        Mailing, verbose_name='рассылка', on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return f'Время: {self.mailing_time}, \
                 Периодичность: {self.mailing_periodicity}, \
                 Статус: {self.mailing_status}'

    class Meta:
        verbose_name = 'Настройки рассылки'
        verbose_name_plural = "Настройки рассылок"
        ordering = ('mailing_status', )


class MailingLogs(models.Model):
    """
    Представление логов рассылки в базе данных.
    """

    last_try_date = models.DateTimeField(
        auto_now_add=True, verbose_name='дата и время попытки')
    try_status = models.CharField(
        max_length=250, verbose_name='статус попытки')
    server_response = models.CharField(
        max_length=250, verbose_name='ответ сервера', **NULLABLE)

    user = models.ForeignKey(
        User, verbose_name='пользователь', on_delete=models.CASCADE)

    mailing = models.ForeignKey(
        Mailing, on_delete=models.CASCADE, verbose_name='рассылка')

    class Meta:
        verbose_name = 'Логи'
        verbose_name_plural = 'Логи'
        ordering = ('last_try_date', )

    def __str__(self) -> str:
        return f'Дата попытки: {self.last_try_date},' + \
               f'Статус: {self.try_status},' + \
               f'Ответ сервера: {self.server_response}'
