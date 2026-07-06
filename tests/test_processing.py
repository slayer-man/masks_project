from typing import Any

from src.processing import filter_by_state, sort_by_date


def test_filter_by_state(test_data: list) -> Any:
    """Тест для filter_by_state"""
    result = filter_by_state(test_data, state="EXECUTED")
    # assert len(result) == 2  # Должно быть 2 элемента с state='EXECUTED'
    assert all(item["state"] == "EXECUTED" for item in result)


def test_sort_by_date(test_data: list) -> Any:
    """Тест для sort_by_date"""
    result = sort_by_date(test_data, reverse=True)
    assert result[0]["date"] == "2023-05-01"  # Дата должна быть самой поздней
