import pytest
from src.masks import get_mask_card_number, get_mask_account


@pytest.mark.parametrize(
    "card_number, expected_output",
    [
        ("7000792289636363", "7000 79** **** 6363"),
        ("1234567812345678", "1234 56** **** 5678"),
        ("1234 5678 9012 3456", "1234 56** **** 3456"),
        #("Visa Platinum 8990922113665229", "Visa Platinum 8990 92** **** 5229"),
    ],
)
def test_get_mask_card_number(card_number, expected_output):
    """Проверка корректного маскирования карты."""
    assert get_mask_card_number(card_number) == expected_output


def test_get_mask_account_success():
    """Проверка корректного маскирования счета."""
    account_number = "12345678901234567890"
    assert get_mask_account(account_number) == "**7890"


def test_get_mask_account_with_spaces():
    """Проверка корректного маскирования счета."""
    account_number = "1234 5678 9012 3456 7890"
    assert get_mask_account(account_number) == "**7890"
