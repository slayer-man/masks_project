import csv
import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List
import pandas as pd

# === НАСТРОЙКА ЛОГИРОВАНИЯ ===
logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)

# Динамически вычисляем путь к папке logs в корне проекта
BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

log_file_path = os.path.join(LOG_DIR, "utils.log")

# Добавлена кодировка utf-8 для предотвращения ошибок отображения кириллицы в Windows
file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
file_formater = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(file_formater)
logger.addHandler(file_handler)


def load_transactions() -> List[Dict]:
    """Читает data/operations.json.

    Возвращает [] если файл не найден, пуст или содержит ошибки.
    """
    try:
        logger.debug("Открытие файла operations.json")
        with open("data/operations.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            logger.info("Файл operations.json успешно прочитан")
            return data if isinstance(data, list) else []
    except Exception as e:
        logger.error(
            "Ошибка: Нет файла, Не правильный формат файла operations.json"
            f" или ошибка времени выполнения: {e}"
        )
        return []


def load_csv_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Загружает список транзакций из CSV-файла и приводит к единой структуре."""
    logger.debug(f"Попытка открытия CSV-файла по пути: {file_path}")

    if not os.path.exists(file_path):
        logger.warning(f"CSV-файл не найден по пути: {file_path}")
        return []

    transactions = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=";")
            for row in reader:
                tx = {
                    "id": row.get("id"),
                    "state": row.get("state"),
                    "date": row.get("date"),
                    "description": row.get("description"),
                    "from": row.get("from"),
                    "to": row.get("to"),
                    "operationAmount": {
                        "amount": row.get("amount"),
                        "currency": {
                            "name": row.get("currency_name"),
                            "code": row.get("currency_code"),
                        },
                    },
                }
                transactions.append(tx)
        logger.info(
            f"CSV-файл успешно прочитан. Загружено транзакций: {len(transactions)}"
        )
    except Exception as e:
        logger.error(f"Не удалось прочитать CSV-файл: {e}")
        return []

    return transactions


def load_xlsx_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Загружает список транзакций из файла Excel (.xlsx) и приводит к единой структуре."""
    logger.debug(f"Попытка открытия XLSX-файла по пути: {file_path}")

    if not os.path.exists(file_path):
        logger.warning(f"XLSX-файл не найден по пути: {file_path}")
        return []

    transactions = []
    try:
        df = pd.read_excel(file_path)
        df = df.fillna("")

        for _, row in df.iterrows():
            tx = {
                "id": str(row.get("id", "")),
                "state": str(row.get("state", "")),
                "date": str(row.get("date", "")),
                "description": str(row.get("description", "")),
                "from": str(row.get("from", "")),
                "to": str(row.get("to", "")),
                "operationAmount": {
                    "amount": str(row.get("amount", "")),
                    "currency": {
                        "name": str(row.get("currency_name", "")),
                        "code": str(row.get("currency_code", "")),
                    },
                },
            }
            transactions.append(tx)
        logger.info(
            f"XLSX-файл успешно прочитан. Загружено транзакций: {len(transactions)}"
        )
    except Exception as e:
        logger.error(f"Не удалось прочитать XLSX-файл: {e}")
        return []

    return transactions
