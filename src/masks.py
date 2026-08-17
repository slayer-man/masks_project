import logging
from typing import Union

logger = logging.getLogger("masks")
file_handler = logging.FileHandler("D:/Python/Projects/Masks_Project/logs/masks.log")
logger.setLevel(logging.DEBUG)
file_formater = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formater)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: Union[str]) -> Union[str]:
    """Функция заменяет часть строки на *  и через через 4 знака ставит пробел"""

    card_number = card_number.replace(" ", "")

    if len(str(card_number)) != 16:
        logger.error("Введен не верный номер карты: ")
        raise ValueError("Неверный номер карты")

    else:
        logger.debug("Замена части номера карты на *: ")
        card_mask = card_number[0:4] + " " + card_number[4:6] + "** **** " + card_number[12:]

    return card_mask


def get_mask_account(account: Union[str], number: int = 2) -> Union[str, int]:
    """Функция заменяет часть строки на *"""

    account = account.replace(" ", "")

    if len(account) != 20:
        logger.error("Введен не верный номер счета: ")
        raise ValueError("Неверный номер счета")

    else:
        logger.debug("Замена всех цифр кроме последних 4 на *: ")
        mask_account: str = "*" * number + account[-4:]

    return mask_account
