import re
from datetime import datetime

# Переносим форматы внутрь функций или делаем их скрытыми (PEP 8)
_DATE_FORMATS = ["%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"]


def mask_account_card(account_card: str) -> tuple[str, str]:
    """Отделяет текстовое название карты или счета от числового номера.

    Гарантирует корректное разделение, даже если в названии есть пробелы.
    """
    # Очищаем строку от лишних пробелов по краям
    account_card = account_card.strip()

    # Регулярное выражение ищет группу цифр в самом конце строки (допускаются пробелы внутри номера)
    match = re.search(r"^(.*?)\s*([\d\s]+)$", account_card)

    if match:
        text_part = match.group(1).strip()
        # Удаляем пробелы из самого номера, чтобы вернуть чистую строку цифр
        number_part = match.group(2).replace(" ", "")
        return text_part, number_part

    # Если структура неожиданная, возвращаем как есть
    return account_card, ""


def get_date(date_string: str) -> str:
    """Преобразует строку даты из формата ISO (или похожих) в формат

    'dd.mm.yyyy'.
    """
    if not date_string or not isinstance(date_string, str):
        return "Некорректная дата"

    # Убираем символ Z (Zulu time) для совместимости
    clean_date = date_string.replace("Z", "")

    for fmt in _DATE_FORMATS:
        try:
            date_obj = datetime.strptime(clean_date, fmt)
            return date_obj.strftime("%d.%m.%Y")
        except ValueError:
            continue

    # Вместо print возвращаем строку-оповещение, чтобы main.py мог корректно её отобразить
    return f"Неверный формат даты ({date_string})"
