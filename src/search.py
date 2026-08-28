import re
from collections import Counter
from typing import Dict, List


def process_bank_search(data: List[dict], search: str) -> List[dict]:
    """Фильтрует список банковских операций по заданной строке поиска в поле 'description'."""
    if not isinstance(data, list) or not search:
        return []

    pattern = re.compile(re.escape(search), re.IGNORECASE)
    result = []

    for item in data:
        if not isinstance(item, dict):
            continue
        description = item.get("description", "")
        if description and pattern.search(description):
            result.append(item)

    return result


def count_operations_by_category(data: List[dict], categories: List[str]) -> Dict[str, int]:
    """Подсчитывает количество банковских операций для каждой категории."""
    if not isinstance(data, list) or not isinstance(categories, list):
        return {}

    all_descriptions = [
        str(item.get("description", "")).strip().lower()
        for item in data
        if isinstance(item, dict) and item.get("description")
    ]

    descriptions_counter = Counter(all_descriptions)
    result = {}

    for category in categories:
        category_lower = category.strip().lower()
        result[category] = descriptions_counter.get(category_lower, 0)

    return result
