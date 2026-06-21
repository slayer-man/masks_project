import re
from datetime import datetime


def mask_account_card(account_card: str) -> tuple:
    """Функция отделения текста от цифр"""

    if "Счет" in account_card:
        account_number = re.findall(r"\d+", account_card)
        account_text = re.findall(r"[a-zA-Zа-яА-ЯёЁ]+", account_card)
        account_str = " ".join(account_number)
        account_text_str = " ".join(account_text)
        return account_text_str, account_str

    else:
        card_numbers = re.findall(r"\d+", account_card)
        card_text = re.findall(r"[a-zA-Zа-яА-ЯёЁ]+", account_card)
        card_number_str = " ".join(card_numbers)
        card_text_str = " ".join(card_text)
        return card_text_str, card_number_str


def get_date(date_string: str) -> str:
    """Преобразует строку даты из ISO формата в формат ДД.ММ.ГГГГ."""
    # Шаблон %Y-%m-%dT%H:%M:%S.%f соответствует вашему формату "2024-03-11T02:26:18.671407"
    date_obj = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%f")

    # Форматируем объект datetime в нужный вид "11.03.2024"
    return date_obj.strftime("%d.%m.%Y")
