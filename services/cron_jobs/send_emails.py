#!/home/debian/.cache/pypoetry/virtualenvs/coursework-6-7n6ESyJz-py3.11/bin/python
# Путь до интерпретатора Python в виртуальном окружении.
import argparse
import os
import sys
import django
from django.core.mail import send_mail

BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath('send_emails.py'))))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from mailing_management.models import Mailing
from config.settings import EMAIL_HOST_USER


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

    args = parser.parse_args()

    return args


def main() -> None:
    args = get_args()

    if args.pk is not None:
        mailing = Mailing.objects.get(pk=args.pk)
        mailing.mailingsettings.mailing_status = 'отправляется'
        mailing.mailingsettings.save()

    send_mail(args.subject,
              args.massage,
              EMAIL_HOST_USER,
              args.email_list.split(' '))

    if args.pk is not None:
        mailing.mailingsettings.mailing_status = 'завершена'
        mailing.mailingsettings.save()


if __name__ == '__main__':
    main()
