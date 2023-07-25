import datetime

from mailing_management.models import MailingSettings


SCRIPT_FILENAME = 'send_emails.py'


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
