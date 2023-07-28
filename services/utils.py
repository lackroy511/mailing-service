from datetime import datetime


def datetime_to_string(dt: datetime):
    """Формирует строку из даты и времени.
    Args:
        dt (datetime): Дата и время.

    Returns:
        str: Сформированная строка.
    """
    
    
    
    return dt.strftime('%Y-%m-%d %H:%M:%S')


def list_to_string_with_spaces(list: list[str]) -> str:
    """Формирует строку из списка строк, разделяя их пробелами.
    Args:
        list (list): Список строк.

    Returns:
        str: Сформированная строка.
    """
    return ' '.join(list)
