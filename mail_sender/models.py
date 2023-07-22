from django.db import models

# Create your models here.

NULLABLE = {'null': True, 'blank': True}


class Client(models.Model):
    """
    Представление клиента в базе данных.
    """
    email = models.CharField(max_length=100, verbose_name='почта')
    first_name = models.CharField(max_length=250, verbose_name='имя')
    last_name = models.CharField(max_length=250, verbose_name='фамилия')
    surname = models.CharField(max_length=250, verbose_name='отчество')
    comment = models.TextField(verbose_name='комментарий', **NULLABLE)

    def __str__(self) -> str:
        return f'ФИО: {self.last_name} {self.first_name} {self.surname}, email: {self.email}'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = "клиенты"
        ordering = ('first_name', 'last_name', 'surname', )


class Mailing(models.Model):
    """
    Представление сообщения в базе данных.
    """
    massage_subject = models.CharField(max_length=250, verbose_name='тема сообщения')
    massage_text = models.TextField(verbose_name='текст сообщения')

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
        ('M H */1 * *', 'Раз в день'),
        ('M H * * 1', 'Раз в неделю'),
        ('M H * */1 *', 'Раз в месяц'),
    )
    
    mailing_time = models.TimeField(auto_now=False, auto_now_add=False, verbose_name='время рассылки')
    mailing_periodicity = models.CharField(max_length=40, verbose_name='периодичность', choices=MAILING_PERIODICITY_CHOICES)
    mailing_status = models.CharField(max_length=10, verbose_name='cтатус', default='Создана')

    mailing = models.ForeignKey(
        Mailing, on_delete=models.CASCADE, verbose_name='рассылка')

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

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='рассылка')

    def __str__(self) -> str:
        return f'Дата попытки: {self.last_try_date}, Статус: {self.try_status}, Ответ сервера: {self.server_response}'

    class Meta:
        verbose_name = 'Логи'
        verbose_name_plural = 'Логи'
        ordering = ('last_try_date', )
