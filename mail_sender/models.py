from django.db import models

# Create your models here.

NULLABLE = {'null': True, 'blank': True}


class Client(models.Model):
    """
    Представление клиента в базе данных.
    """
    email = models.CharField(max_length=100, verbose_name='почта')
    full_name = models.CharField(max_length=250, verbose_name='ФИО')
    comment = models.TextField(verbose_name='комментарий', **NULLABLE)

    def __str__(self) -> str:
        return f'ФИО: {self.full_name}, email: {self.email}'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = "клиенты"
        ordering = ('full_name', )


class MassageToSend(models.Model):
    """
    Представление сообщения в базе данных.
    """
    massage_subject = models.CharField(max_length=250, verbose_name='тема сообщения')
    massage_text = models.TextField(verbose_name='текст сообщения')
    
    mailing_settings = models.ForeignKey("MailingSettings", verbose_name="id настроек", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'Тема сообщения: {self.massage_subject}'

    class Meta:
        verbose_name = 'Сообщение для рассылки'
        verbose_name_plural = 'Сообщения для рассылки'


class MailingSettings(models.Model):
    """
    Представление настроек рассылки в базе данных.
    """
    mailing_time = models.CharField(max_length=100, verbose_name='время')
    mailing_periodicity = models.CharField(max_length=10, verbose_name='периодичность')
    mailing_status = models.CharField(max_length=10, verbose_name='cтатус')

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

    last_try_date = models.DateTimeField(auto_now=True, verbose_name='дата и время попытки')
    try_status = models.CharField(max_length=10, verbose_name='статус попытки')
    server_response = models.CharField(max_length=250, verbose_name='ответ сервера')
   
    client = models.ForeignKey("Client", verbose_name="id клиента", on_delete=models.DO_NOTHING)
    massage_to_send = models.ForeignKey("MassageToSend", verbose_name="id сообщения", on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return f'Дата попытки: {self.last_try_date}, Статус: {self.try_status}, Ответ сервера: {self.server_response}'

    class Meta:
        verbose_name = 'Логи'
        verbose_name_plural = 'Логи'
        ordering = ('last_try_date', )
