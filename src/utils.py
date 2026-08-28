import csv
import json
import logging
import os
from typing import Any, Dict, List

import pandas as pd

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


def load_csv_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Загружает список транзакций из CSV-файла и приводит к единой структуре."""
    if not os.path.exists(file_path):
        return []

    transactions = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            # Используем DictReader, чтобы каждая строчка стала словарем {заголовок: значение}
            reader = csv.DictReader(f, delimiter=";")  # Если разделитель запятая, замените на ','
            for row in reader:
                # Превращаем плоскую структуру CSV во вложенную, как в JSON
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
    except Exception as e:
        print(f"[ОШИБКА CSV] Не удалось прочитать файл: {e}")
        return []

    return transactions


def load_xlsx_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Загружает список транзакций из файла Excel (.xlsx) и приводит к единой структуре."""
    if not os.path.exists(file_path):
        return []

    transactions = []
    try:
        # Читаем таблицу с помощью pandas
        df = pd.read_excel(file_path)
        # Заменяем пустые ячейки (NaN) на пустые строки для безопасности
        df = df.fillna("")

        # Перебираем строки таблицы
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
    except Exception as e:
        print(f"[ОШИБКА EXCEL] Не удалось прочитать файл: {e}")
        return []

    return transactions
