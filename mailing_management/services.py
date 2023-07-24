import os
from crontab import CronTab

from config.settings import BASE_DIR, CRON_JOBS_DIR


def generate_cron_command(script_filename: str, *args: str) -> str:
    """Формирует команду для добавления/удаления задачи в crontab.
    Args:
        script_filename (str): Имя python скрипта.
        *args (str): Аргументы для скрипта.

    Returns:
        str: Сформированная команда.
    """

    path_to_project = os.path.join(BASE_DIR, '')
    path_to_cron_jobs = CRON_JOBS_DIR

    command = f'PYTHONPATH={path_to_project} ' +\
        f'{path_to_project}{path_to_cron_jobs}{script_filename}'

    for arg in args:
        command += f' "{arg}"'

    return command


def list_to_string(list: list[str]) -> str:
    """Формирует строку из списка строк, разделяя их пробелами.
    Args:
        list (list): Список строк.

    Returns:
        str: Сформированная строка.
    """
    return ' '.join(list)


def add_cron_job(schedule, command):

    cron = CronTab(user=True)

    job = cron.new(command=command)
    job.setall(schedule)

    cron.write()


def remove_cron_job():
    pass
