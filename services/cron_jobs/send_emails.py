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


def main() -> None:
    from mailing_management.models import Mailing
    from mailing_management.services import SEND_EMAILS_SCRIPT_FILENAME, \
        set_end_mailing_time_for_cron_command, set_pk_for_cron_command
    from config.settings import EMAIL_HOST_USER, TIME_ZONE
    from services.crontab_utils import generate_cron_command, remove_cron_job

    args = get_args()

    if args.pk is not None:
        mailing = Mailing.objects.get(pk=args.pk)
        mailing.mailingsettings.mailing_status = 'Отправляется'
        mailing.mailingsettings.save()

    send_mail(args.subject,
              args.massage,
              EMAIL_HOST_USER,
              args.email_list.split(' '))

    if args.pk is not None:
        mailing.mailingsettings.mailing_status = 'Завершена'
        mailing.mailingsettings.save()

    if args.end_mailing_time:

        end_mailing_time = mailing.mailingsettings.end_mailing_time

        tz = pytz.timezone(TIME_ZONE)
        if datetime.now(tz=tz) > end_mailing_time.astimezone(tz):

            command = generate_cron_command(
                SEND_EMAILS_SCRIPT_FILENAME, args.subject,
                args.massage, args.email_list.split(' '),
            )
            command = set_pk_for_cron_command(command, args.pk)
            command = set_end_mailing_time_for_cron_command(
                command, end_mailing_time.astimezone(tz),
            )

            mailing.mailingsettings.mailing_status = 'Устарела'
            mailing.mailingsettings.save()

            print(command)

            remove_cron_job(command)


if __name__ == '__main__':
    main()
