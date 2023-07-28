#!/home/debian/.cache/pypoetry/virtualenvs/coursework-6-7n6ESyJz-py3.11/bin/python
import argparse
import os
import sys
import django
import pytz
from datetime import datetime
from django.core.mail import send_mail

BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath('send_emails.py'))))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from mailing_management.models import Mailing, MailingLogs
from mailing_management.services import SEND_EMAILS_SCRIPT_FILENAME, \
    set_end_mailing_time_for_cron_command, set_pk_for_cron_command
from config.settings import EMAIL_HOST_USER, TIME_ZONE
from services.crontab_utils import generate_cron_command, remove_cron_job


def main() -> None:

    args = get_args()

    mailing = set_status_sent(args, Mailing)
    send_mail_with_logging(args, mailing)
    set_status_completed(args, mailing)

    corn_is_deleted = auto_delete_cron_job(args, mailing)
    if corn_is_deleted:
        set_status_deprecated(mailing)


def get_args() -> argparse.Namespace:
    """ Парсинг позиционных аргументов из cron задачи.
    Returns:
        argparse: Объект argparse с аргументами.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('subject', type=str)
    parser.add_argument('massage', type=str)
    parser.add_argument('email_list', type=str)
    parser.add_argument('--pk', type=int)
    parser.add_argument('--end_mailing_time', type=str)

    args = parser.parse_args()

    return args


def set_status_sent(args: argparse, mailing: Mailing) -> Mailing:
    """ Устанавливает статус отправки сообщений.
    Args:
        args (argparse): Объект argparse с аргументами.
        mailing (object): Объект Mailing.
    Returns:
        Mailing: Объект Mailing.
    """
    if args.pk is not None:
        mailing = Mailing.objects.get(pk=args.pk)
        mailing.mailingsettings.mailing_status = 'Отправляется'
        mailing.mailingsettings.save()

    return mailing


def set_status_completed(args: argparse, mailing: Mailing) -> None:
    """ Устанавливает статус завершения отправки сообщений.
    Args:
        args (argparse): Объект argparse с аргументами.
        mailing (object): Объект Mailing.
    """
    if args.pk is not None:
        mailing.mailingsettings.mailing_status = 'Завершена'
        mailing.mailingsettings.save()


def set_status_deprecated(mailing):
    """ Устанавливает статус завершения отправки сообщений.
    Args:
        mailing (object): Объект Mailing.
    """
    mailing.mailingsettings.mailing_status = 'Отключена'
    mailing.mailingsettings.save()


def send_mail_with_logging(args, mailing: Mailing) -> None:
    """ Отправляет письмо с логами.
    Args:
        args (argparse): Объект argparse с аргументами.
        mailing (object): Объект Mailing.
    """
    try:
        send_mail(args.subject,
                  args.massage,
                  EMAIL_HOST_USER,
                  args.email_list.split(' '))
        if args.pk:
            create_success_log(mailing)
    except Exception as e:
        if args.pk:
            create_error_log(mailing, str(e))


def create_success_log(mailing: Mailing) -> None:
    """Сделать запись в логе успешной отправки сообщений.
    Args:
        mailing (Mailing): Объект Mailing.
    """
    log = MailingLogs.objects.create(
        try_status='Успешно отправлено.', mailing=mailing)
    log.save()


def create_error_log(mailing: Mailing, exception: str) -> None:
    """Сделать запись в логе успешной отправки сообщений.
    Args:
        mailing (Mailing): Объект Mailing.
        e (str): Ошибка.
    """
    log = MailingLogs.objects.create(
        try_status='Ошибка отправки сообщений.',
        server_response=f"Отправка сообщений завершена с ошибкой:{str(exception)}",
        mailing=mailing,
    )
    log.save()


def auto_delete_cron_job(args: argparse, mailing: Mailing) -> bool or None:
    """Удаление cron задачи отправки сообщений по указанному времени.
    Args:
        args (argparse): Объект argparse с аргументами.
        mailing (Mailing): Объект Mailing.
    """
    if args.end_mailing_time:

        end_mailing_time = mailing.mailingsettings.end_mailing_time

        tz = pytz.timezone(TIME_ZONE)
        if datetime.now(tz=tz) > end_mailing_time.astimezone(tz):

            command = generate_cron_command_for_delete(args,
                                                       end_mailing_time, tz)
            remove_cron_job(command)

            return True


def generate_cron_command_for_delete(
        args: argparse, end_mailing_time: datetime, tz: pytz) -> str:
    """Сгенерировать команду для удаления задачи cron.
    Args:
        args (argparse): Объект argparse с аргументами.
        end_mailing_time (datetime): Время окончания отправки сообщений.
        tz (pytz): Объект pytz с временной зоной

    Returns:
        str: _description_
    """
    command = generate_cron_command(
        SEND_EMAILS_SCRIPT_FILENAME, args.subject,
        args.massage, args.email_list.split(' '),
    )
    command = set_pk_for_cron_command(command, args.pk)
    command = set_end_mailing_time_for_cron_command(
        command, end_mailing_time.astimezone(tz),
    )

    return command


if __name__ == '__main__':
    main()
