import os
from crontab import CronTab

from config.settings import BASE_DIR, CRON_JOBS_DIR


def generate_cron_command(script_filename: str,
                          pk: str = None, *args: str | list) -> str:
    """Формирует команду для добавления/удаления задачи в crontab.
    Args:
        script_filename (str): Имя python скрипта.
        pk (str): pk объекта Mailing.
        *args (str): Позиционные аргументы, которые используются внутри скрипта

    Returns:
        str: Сформированная команда.
    """

    path_to_project = os.path.join(BASE_DIR, '')
    path_to_cron_jobs = CRON_JOBS_DIR

    command = f'PYTHONPATH={path_to_project} ' +\
        f'{path_to_project}{path_to_cron_jobs}{script_filename}'

    if args:
        for arg in args:
            if isinstance(arg, list):
                arg = list_to_string_with_spaces(arg)
            command += f' "{arg}"'

    if pk:
        command += f' --pk {pk}'

    return command


def list_to_string_with_spaces(list: list[str]) -> str:
    """Формирует строку из списка строк, разделяя их пробелами.
    Args:
        list (list): Список строк.

    Returns:
        str: Сформированная строка.
    """
    return ' '.join(list)


def add_cron_job(schedule: str, command: str) -> None:
    """Добавить задачу в crontab.
    Args:
        schedule (str): Расписание задачи в формате crontab.
        command (str): Сформированная команда.
    """
    cron = CronTab(user=True)

    job = cron.new(command=command)
    job.setall(schedule)

    cron.write()


def remove_cron_job(command: str) -> None:
    """Удалить задачу из crontab.
    Args:
        command (str): Строка команды.
    """
    cron = CronTab(user=True)

    jobs = cron.find_command(command)
    for job in jobs:
        cron.remove(job)

    cron.write()
