from datetime import datetime
from src.widget import get_date

def check_date_format(date_string, date_format="%d.%m.%Y"):
    """
    Проверяет, корректна ли дата и соответствует ли она заданному формату.
    Возвращает True, если ошибок нет, и False, если они есть.
    """
    try:
        # Пытаемся распарсить строку в дату
        datetime.strptime(date_string, date_format)
        return True
    except ValueError:
        # Ловим ошибку, если формат неверный или дата не существует
        return False
