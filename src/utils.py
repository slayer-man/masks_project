# utils.py

import json
from typing import List, Dict


def load_transactions() -> List[Dict]:
    """
    Читает data/operations.json.
    Возвращает [] если файл не найден, пуст или содержит ошибки.
    """
    try:
        with open("data/operations.json") as f:
            return json.load(f)
    except Exception:
        # Ловим всё: FileNotFoundError, JSONDecodeError, PermissionError
        return []