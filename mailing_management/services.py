from datetime import datetime
from django import forms
import pytz

from django.core.paginator import Paginator
from django.core.mail import send_mail

from client_management.models import Client
from mailing_management.models import Mailing, MailingSettings
from services.crontab_utils import add_cron_job, generate_cron_command, \
    remove_cron_job

from config.settings import EMAIL_HOST_USER, TIME_ZONE

SEND_EMAILS_SCRIPT_FILENAME = 'send_emails.py'


def get_page_obj_for_mailing(self) -> Paginator:
    """Создает объект страницы.
    Returns:
        Paginator: объект страницы.
    """
    mailing_list = Mailing.objects.filter(user=self.request.user)
    paginator = Paginator(mailing_list, 5)
    page_number = self.request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj


def add_mailing_cron_job(self, mailing: Mailing,
                         mailing_settings: MailingSettings) -> None:
    """Добавить задачу crontab.
    Args:
        mailing (Mailing): Объект модели рассылки
        mailing_settings (MailingSettings): Объект модели настроек рассылки.
    """
    schedule = mailing_settings.mailing_periodicity
    subject = mailing.massage_subject
    massage = mailing.massage_text
    email_list = [client.email for client in Client.objects.filter(
        user=self.request.user)]

    command = generate_cron_command(
        SEND_EMAILS_SCRIPT_FILENAME, mailing.pk, subject, massage, email_list,
    )

    add_cron_job(schedule, command)


def remove_mailing_cron_job(self=None, pk: int = None, request=None) -> None:
    """Удалить задачу crontab.
    Args:
        self: Текущий объект.
        pk (int): ID задачи crontab.
        request: Объект запроса.
    """
    if pk is None:
        pk = self.kwargs.get('pk')

    mailing = Mailing.objects.get(pk=pk)
    subject = mailing.massage_subject
    massage = mailing.massage_text

    if request:
        email_list = [client.email for client in Client.objects.filter(
            user=request.user)]
    else:
        email_list = [client.email for client in Client.objects.filter(
            user=self.request.user)]

    print(email_list)

    command = generate_cron_command(
        SEND_EMAILS_SCRIPT_FILENAME, pk, subject, massage, email_list,
    )

    remove_cron_job(command)


def save_mailing_settings_periodicity(
    mailing_settings: MailingSettings,
) -> None:
    """Сохранить настройки расписания для рассылки.
    Args:
        mailing_settings (MailingSettings): Настройки рассылки.
    """
    time_of_mailing = mailing_settings.mailing_time
    raw_periodicity = mailing_settings.mailing_periodicity

    mailing_settings.mailing_periodicity = \
        format_periodicity_to_cron_schedule(time_of_mailing,
                                            raw_periodicity)

    mailing_settings.mailing_periodicity_display = \
        get_periodicity_display(raw_periodicity)

    mailing_settings.save()


def upd_mailing_settings_periodicity(mailing_settings: Mailing,
                                     settings_form: forms) -> None:
    """Обновить настройки расписания для рассылки.
    Args:
        mailing (Mailing): Объект модели настроек рассылки.
        settings_form (Form): Форма для модели.
    """

    time_of_mailing = settings_form.cleaned_data['mailing_time']
    raw_periodicity = settings_form.cleaned_data['mailing_periodicity']

    mailing_settings.mailing_time = time_of_mailing
    mailing_settings.mailing_periodicity = \
        format_periodicity_to_cron_schedule(time_of_mailing,
                                            raw_periodicity)
    mailing_settings.mailing_periodicity_display = \
        get_periodicity_display(raw_periodicity)

    mailing_settings.save()


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


def start_mailing(self,
                  mailing: Mailing,
                  mailing_settings: MailingSettings,
                  email_list: list) -> None:

    timezone = pytz.timezone(TIME_ZONE)
    time_now = datetime.now(tz=timezone).time()

    if time_now > mailing_settings.mailing_time:
        send_mail(mailing.massage_subject, mailing.massage_text,
                  EMAIL_HOST_USER, email_list)
