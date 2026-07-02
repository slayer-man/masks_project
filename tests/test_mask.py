import pytest
import re
from src.masks import get_mask_card_number, get_mask_account


def test_valid_16_digit_card():
    """Проверка стандартной 16-значной карты."""
    original = "1234567890123456"
    masked = get_mask_card_number(original)

    assert masked == "123456******3456"
    assert len(masked) == 16


def test_card_with_spaces():
    """Проверка удаления пробелов и маскирования."""
    original = "1234 5678 9012 3456"
    masked = get_mask_card_number(original)

    assert masked == "123456******3456"


def test_short_card_error():
    """Проверка обработки слишком коротких номеров."""
    with pytest.raises(ValueError, match="Некорректный номер карты"):
        get_mask_card_number("1234567")


def test_all_cards_in_logs():
    """Проверка поиска и маскирования номеров карт в тексте (поиск утечек)."""
    log_text = "Пользователь ввел карту 5555551111223333 для оплаты."

    # Ищем скрытые шаблоны
    found_cards = re.findall(r"\d{6}\d{6}\d{4}", log_text)

    # В идеале в логах не должно быть не замаскированных карт
    assert len(found_cards) == 0, "Обнаружен открытый номер карты в тексте!"





@pytest.mark.parametrize(
    "card_input, expected_output",
    [
        ("7000792289636363", "7000 79** **** 6363"),
        ("1234567812345678", "1234 56** **** 5678"),
    ],
)
def test_mask_card_number_success(card_input, expected_output):
    """Проверка корректного маскирования карты."""
    assert get_mask_card_number(card_input) == expected_output


def test_mask_account_number_success():
    """Проверка корректного маскирования счета."""
    account_number = "12345678901234567890"
    assert get_mask_account(account_number) == "**7890"


@pytest.mark.parametrize(
    "invalid_input",
    [
        "123",  # короткая
        "12345678123456789",  # длинная
        "abcd567812345678",  # буквы
        "",  # пустая строка
    ],
)
def test_mask_card_number_exceptions(invalid_input):
    """Проверка выброса ошибок при неверном номере карты."""
    with pytest.raises(ValueError, match="Некорректный номер карты"):
        get_mask_card_number(invalid_input)


@pytest.mark.parametrize(
    "invalid_input",
    [
        "1234567890123456789",  # 19 цифр
        "abcd",  # буквы
        "",  # пустая строка
    ],
)
def test_mask_account_number_exceptions(invalid_input):
    """Проверка выброса ошибок при неверном номере счета."""
    with pytest.raises(ValueError, match="Некорректный номер счета"):
        get_mask_account(invalid_input)
