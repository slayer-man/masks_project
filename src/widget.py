from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(account_card: str) -> str:
    """Функция принимает в качестве аргумента строку, содержащую тип и номер карты или счета, и возвращает строку с замаскированным номером"""

    account_card_info = account_card.rsplit(' ', 1)

    if "Счет" in account_card:
        return f"{account_card_info[0]} {get_mask_account(account_card_info[1])}"

    else:
        return f"{account_card_info[0]} {get_mask_card_number(account_card_info[1])}"




def get_date(date_iso_8601: str) -> str:
    """Конвертирует дату из международного стандарта в обычный формат 'ДД.ММ.ГГГГ'"""

    formatted_date = datetime.strptime(date_iso_8601, "%Y-%m-%dT%H:%M:%S.%f")
    return formatted_date.strftime("%d.%m.%Y")
