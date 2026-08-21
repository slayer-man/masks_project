import pytest
from logs import *

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("1234567890123456", "1234 56** **** 3456"),
        ("1234 5678 9012 3456", "1234 56** **** 3456"),
    ],
)
def test_card_masking(card_number, expected):
    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize(
    "account, expected",
    [
        ("12345678901234567890", "**7890"),
        ("1234 5678 9012 3456 7890", "**7890"),
    ],
)
def test_account_masking(account, expected):
    assert get_mask_account(account) == expected


def test_card_masking_invalid_format() -> None:
    """Проверяем, что некорректная строка вызывает ошибку карты"""
    with pytest.raises(ValueError, match="Неверный номер карты"):
        get_mask_card_number("не-карта")


def test_account_masking_invalid_format() -> None:
    """Проверяем, что некорректная строка вызывает ошибку аккаунта"""
    with pytest.raises(ValueError, match="Неверный номер счета"):
        get_mask_account("не-аккаунт")
