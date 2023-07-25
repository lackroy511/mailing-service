import datetime
from client_management.models import Client

from mailing_management.models import Mailing, MailingSettings
from services.crontab_utils import add_cron_job, generate_cron_command, \
    remove_cron_job


SEND_EMAILS_SCRIPT_FILENAME = 'send_emails.py'


def format_periodicity_to_cron_schedule(time: datetime,
                                        raw_periodicity: str) -> str:
    """Форматирует шаблон расписания для crontab в виде 'M H * * *',
    вставляя реальное время.
    Args:
        time (datetime): Время
        raw_periodicity (str): Шаблон расписания.

    Returns:
        str: Форматированная строка расписания. '58 23 * * *'.
    """
    formatted_time = time.strftime('%M:%H')
    formatted_time = formatted_time.split(':')

    periodicity = raw_periodicity.replace('H', formatted_time[1])
    periodicity = periodicity.replace('M', formatted_time[0])

    return periodicity


def get_periodicity_display(raw_periodicity: str) -> str:
    """Получить человекопонятное расписание.
    Args:
        raw_periodicity (_type_): Шаблон расписания для crontab 'M H * * *'.

    Returns:
        str: Человекопонятное расписание, например: "Раз в день"
    """
    return dict(
        MailingSettings.MAILING_PERIODICITY_CHOICES).get(raw_periodicity)


def add_mailing_cron_job(mailing: Mailing,
                         mailing_settings: MailingSettings) -> None:
    """Добавить задачу crontab.
    Args:
        mailing (Mailing): Объект модели рассылки
        mailing_settings (MailingSettings): Объект модели настроек рассылки.
    """
    schedule = mailing_settings.mailing_periodicity
    subject = mailing.massage_subject
    massage = mailing.massage_text
    email_list = [client.email for client in Client.objects.all()]

    command = generate_cron_command(
        SEND_EMAILS_SCRIPT_FILENAME, subject, massage, email_list,
    )

    add_cron_job(schedule, command)


def remove_mailing_cron_job(self: Mailing = None, pk: int = None) -> None:
    """Удалить задачу crontab.
    Args:
        self (Mailing): Экземпляр модели рассылки.
        pk (int): ID задачи crontab.
    """
    if pk is None:
        pk = self.kwargs.get('pk')

    mailing = Mailing.objects.get(pk=pk)
    subject = mailing.massage_subject
    massage = mailing.massage_text
    email_list = [client.email for client in Client.objects.all()]

    command = generate_cron_command(
        SEND_EMAILS_SCRIPT_FILENAME, subject, massage, email_list,
    )
    remove_cron_job(command)
