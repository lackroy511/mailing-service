#!/home/debian/.cache/pypoetry/virtualenvs/coursework-6-7n6ESyJz-py3.11/bin/python
# Путь до интерпретатора Python в виртуальном окружении.
import smtplib
import argparse
import os
import sys

# Абсолютный путь до файла скрипта, для того что бы работали импорты.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath('send_emails.py')))
sys.path.append(BASE_DIR)

from config.settings import EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, \
    EMAIL_HOST_PASSWORD


def parse_args() -> argparse.Namespace:
    """ Парсинг позиционных аргументов из cron задачи.
    Returns:
        argparse: Объект argparse с аргументами.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('subject', type=str)
    parser.add_argument('massage', type=str)
    parser.add_argument('email_list', type=str)

    args = parser.parse_args()

    return args


def send_emails(subject: str = 'ТЕСТОВОЕ СООБЩЕНИЕ',
                massage: str = 'Оно приходит, когда что-то не работает',
                email_list: str = 'lackroy511@gmail.com') -> None:
    """ Отправляет письма по списку адресов электронной почты.
    Args:
        subject (str): Тема письма
        massage (str): Текст письма
        email_list (str): Список адресов электронной почты, одной строкой,
                          разделенных символом пробела.
    """

    server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    server.connect(EMAIL_HOST, EMAIL_PORT)
    server.ehlo()
    server.starttls()
    server.ehlo()

    login = EMAIL_HOST_USER
    password = EMAIL_HOST_PASSWORD
    sender = EMAIL_HOST_USER
    server.login(login, password)

    # Формирование сообщения
    email = f'Subject: {subject}\n\n{massage}'

    # Русский не поддерживается, поэтому энкодим
    email = email.encode("UTF-8")

    # Разделение списка адресов по пробелам, если адресов в строке больше двух
    if email_list.count(' ') > 0:
        email_list = email_list.split(' ')

    if isinstance(email_list, list):
        for receiver in email_list:
            server.sendmail(sender, receiver, email)
    else:
        server.sendmail(sender, email_list, email)

    server.quit()


def main() -> None:

    args = parse_args()

    send_emails(subject=args.subject,
                massage=args.massage,
                email_list=args.email_list)


if __name__ == '__main__':
    main()
