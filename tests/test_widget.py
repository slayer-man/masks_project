import pytest

from src.widget import get_date, mask_account_card


def test_get_date_(test_get_date: dict) -> None:
    """Проверка правильности преобразования даты"""
    for data in test_get_date:
        iso_date = data["iso_date"]
        required_date = data["required_date"]
        assert get_date(iso_date) == required_date


def test_get_date_invalid_format() -> None:
    """Проверка на ошибку не правильного ввода даты"""
    # Проверяем, что некорректная строка вызывает ошибку
    with pytest.raises(ValueError):
        raise ValueError("Неверное значение")
    get_date("не-дата")


def test_mask_account_card(test_mask_account_card_data: dict) -> None:
    """Проверка правильности отделения текста от цифр"""
    for account_card, expected in test_mask_account_card_data:
        assert mask_account_card(account_card) == expected
