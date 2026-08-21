import json
import logging
from typing import Dict, List

logger = logging.getLogger("utils")
file_handler = logging.FileHandler("D:/Python/Projects/Masks_Project/logs/utils.log")
logger.setLevel(logging.DEBUG)
file_formater = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formater)
logger.addHandler(file_handler)


def load_transactions() -> List[Dict]:
    """
    Читает data/operations.json.
    Возвращает [] если файл не найден, пуст или содержит ошибки.
    """
    try:
        logger.debug("Открытие файла operations.json")
        with open("data/operations.json") as f:
            return json.load(f)
    except Exception:
        logger.error("Ошибка: Нет файла, Не правильный формат файла operations.json " "или ошибка времени выполнения")
        # Ловим всё: FileNotFoundError, JSONDecodeError, PermissionError
        return []
