import logging
import os
from pathlib import Path

# === НАСТРОЙКА ЛОГИРОВАНИЯ ===
logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)

# Динамически вычисляем путь к папке логов в корне проекта
BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

log_file_path = os.path.join(LOG_DIR, "masks.log")

# ИСПРАВЛЕНИЕ: Добавлен параметр encoding="utf-8" для красивого отображения русского текста
file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
file_formater = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(file_formater)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Заменяет часть строки номера карты на * и разделяет пробелами по 4 знака."""
    card_number = str(card_number).replace(" ", "")

    if len(card_number) != 16:
        logger.error(f"Введен неверный номер карты: {card_number}")
        raise ValueError("Неверный номер карты")

    logger.debug("Успешная замена части номера карты на *")
    card_mask = (
        card_number[0:4]
        + " "
        + card_number[4:6]
        + "** **** "
        + card_number[12:]
    )
    return card_mask


def get_mask_account(account: str, number: int = 2) -> str:
    """Заменяет все цифры счета, кроме последних 4, на *."""
    account = str(account).replace(" ", "")

    if len(account) != 20:
        logger.error(f"Введен неверный номер счета: {account}")
        raise ValueError("Неверный номер счета")

    logger.debug("Успешная замена цифр счета кроме последних 4 на *")
    mask_account = "*" * number + account[-4:]
    return mask_account
