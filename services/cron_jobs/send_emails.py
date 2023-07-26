#!/home/debian/.cache/pypoetry/virtualenvs/coursework-6-7n6ESyJz-py3.11/bin/python
# Путь до интерпретатора Python в виртуальном окружении.
import argparse
import os
import sys
import django
from django.core.mail import send_mail

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath('send_emails.py'))))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from config.settings import EMAIL_HOST_USER
from mailing_management.models import Mailing


def parse_args() -> argparse.Namespace:
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


def send_emails(subject: str,
                massage: str,
                sender: str,
                email_list: str) -> None:
    """ Отправляет письма по списку адресов электронной почты.
    Args:
        subject (str): Тема письма
        massage (str): Текст письма
        email_list (str): Список адресов электронной почты, одной строкой,
                          разделенных символом пробела.
    """
    email_list = email_list.split(' ')
    send_mail(subject, massage, sender, email_list)


def main() -> None:
    args = parse_args()

    mailing = Mailing.objects.get(pk=args.pk)

    mailing.mailingsettings.mailing_status = 'отправляется'
    mailing.mailingsettings.save()
    send_emails(subject=args.subject,
                massage=args.massage,
                sender=EMAIL_HOST_USER,
                email_list=args.email_list)
    mailing.mailingsettings.mailing_status = 'завершена'
    mailing.mailingsettings.save()


if __name__ == '__main__':
    main()
