import pytest

from src.masks import get_mask_card_number


@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("1234567890123456", "1234 56 3456"),
        ("1234 5678 9012 3456", "1234 56 3456"),
    ],
)
def test_card_masking(card_number: str, expected: str) -> None:
    assert get_mask_card_number(card_number) == expected


@pytest.fixture
def test_get_mask_card_number() -> list:
    """Фикстура с тестовыми данными для маскирования карты. Для модуля masks.py"""
    return [
        {"card": "1234567890123456", "masked_card": "1234 56** **** 3456"},
        {"card": "1234 5678 9012 3456", "masked_card": "1234 56** **** 3456"},
    ]


@pytest.fixture
def test_get_mask_account() -> list:
    """Фикстура с тестовыми данными для маскирования счета. Для модуля masks.py"""
    return [
        {"account": "12345678901234567890", "masked_account": "**7890"},
        {"account": "1234 5678 9012 3456 7890", "masked_account": "**7890"},
    ]


@pytest.fixture
def test_get_date() -> list:
    """Фикстура с тестовыми данными для перевода даты из ISO в dd.mm.yyyy. Для модуля widget.py"""
    return [
        {
            "iso_date": "2024-03-11T02:26:18.671407",  # Базовый ISO
            "required_date": "11.03.2024",
        },
        {
            "iso_date": "2026-07-03",
            "required_date": "03.07.2026",
        },
        {
            "iso_date": "2026-07-03T12:30:00",  # ISO с временем
            "required_date": "03.07.2026",
        },
        {
            "iso_date": "2026-01-01T00:00:00Z",  # ISO с UTC
            "required_date": "01.01.2026",
        },
    ]


@pytest.fixture
def test_mask_account_card_data() -> list:
    """Фикстура с тестовыми данными для mask_account_card."""
    return [
        ("Счет 12345678901234567890", ("Счет", "12345678901234567890")),
        ("Visa 1234 5678 9012 3456", ("Visa", "1234 5678 9012 3456")),
        ("1234 5678 9012 3456 Maestro", ("Maestro", "1234 5678 9012 3456")),
        ("Здесь нет цифр", ("Здесь нет цифр", "")),
    ]


@pytest.fixture
def test_data() -> list:
    return [
        {"date": "2023-02-01", "state": "EXECUTED"},
        {"date": "2023-05-01", "state": "CANCELED"},
        {"date": "2023-01-01", "state": "EXECUTED"},
    ]


# Фикстура для транзакций
@pytest.fixture
def transactions():
    return [
        {
            "id": 970157810,
            "date": "2018-06-08T10:3:58.027767",
            "operationAmount": {
                "amount": "150",
                "currency": {
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Счет - 63475662387234505765",
            "to": "Счет 8175128657841941437"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        }
    ]

@pytest.fixture
def sample_transactions():
    return [
        {"id": 1, "operationAmount": {"amount": "100", "currency": {"code": "USD"}}},
        {"id": 2, "operationAmount": {"amount": "500", "currency": {"code": "RUB"}}},
        {"id": 3, "operationAmount": {"amount": "10"}},
        {"id": 4, "operationAmount": {"amount": None, "currency": {"code": "EUR"}}}
    ]
