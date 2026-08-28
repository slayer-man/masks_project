import pytest
from src.search import process_bank_search, count_operations_by_category


# ==========================================
# Тесты для process_bank_search (re)
# ==========================================

def test_process_bank_search_success():
    """Тест успешного поиска подстроки в описании транзакции."""
    data = [
        {"id": 1, "description": "Перевод организации"},
        {"id": 2, "description": "Открытие вклада"},
        {"id": 3, "description": "Перевод со счета"}
    ]

    # Ищем слово "перевод" в любом регистре
    result = process_bank_search(data, "перевод")
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["id"] == 3


def test_process_bank_search_empty_or_invalid():
    """Тест обработки пустых входящих данных."""
    assert process_bank_search([], "Перевод") == []
    assert process_bank_search([{"description": "Тест"}], "") == []
    assert process_bank_search("не список", "Перевод") == []


def test_process_bank_search_no_match():
    """Тест ситуации, когда совпадений не найдено."""
    data = [{"description": "Открытие вклада"}]
    assert process_bank_search(data, "Покупка") == []


# ==========================================
# Тесты для count_operations_by_category (Counter)
# ==========================================

def test_count_operations_by_category_success():
    """Тест успешного подсчета количества операций по категориям."""
    data = [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
        {"description": "Перевод организации"},
        {"description": "Покупка продуктов"}
    ]
    categories = ["Перевод организации", "Открытие вклада", "Перевод со счета"]

    result = count_operations_by_category(data, categories)

    # Проверяем точечный подсчет
    assert result["Перевод организации"] == 2
    assert result["Открытие вклада"] == 1
    # Категории не было в данных — должен быть 0
    assert result["Перевод со счета"] == 0


def test_count_operations_by_category_empty():
    """Тест передачи некорректных типов данных в счетчик."""
    # Если данные пустые, функция вернет словарь с нулями для каждой категории
    assert count_operations_by_category([], ["Категория"]) == {"Категория": 0}

    # А вот если передать не список в аргументы, сработает защита и вернется строго {}
    assert count_operations_by_category([{"description": "Тест"}], "не список") == {}
