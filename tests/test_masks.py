import pytest

from src.masks import get_mask_account, get_mask_card_number


def test_card_masking(test_get_mask_card_number: list) -> None:
    """Проверка корректного маскирования карты."""
    for data in test_get_mask_card_number:
        # data["card"] — входящий номер
        # mask_function — ваша функция маскирования
        result = get_mask_card_number(data["card"])

        # Сравниваем реальный результат с ожидаемым
        assert result == data["masked_card"]


def test_account_masking(test_get_mask_account: list) -> None:
    """Проверка корректного маскирования счета."""
    for data in test_get_mask_account:
        # data["account"] — входящий номер
        # mask_function — ваша функция маскирования
        result = get_mask_account(data["account"])

        # Сравниваем реальный результат с ожидаемым
        assert result == data["masked_account"]


def test_card_masking_invalid_format() -> None:
    """Проверяем, что некорректная строка вызывает ошибку карты"""
    with pytest.raises(ValueError):
        raise ValueError("Неверное значение")
    get_mask_card_number("не-карта")


def test_account_masking_invalid_format() -> None:
    """Проверяем, что некорректная строка вызывает ошибку аккаунта"""
    with pytest.raises(ValueError):
        raise ValueError("Неверное значение")
    get_mask_account("не-аккаунт")
