import pytest

from data.data_dict_generators import short_data, transactions, transactions_cur
from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


def test_transaction_descriptions_diff_length_data() -> None:
    """Проверка функции, что корректно обрабатывает списки различной длины"""

    # Проверка работы функции с пустым списком.
    empty_data: list = []
    descriptions = list(transaction_descriptions(empty_data))
    assert len(descriptions) == 0

    # Проверка работы функции с коротким списком (одна транзакция).
    descriptions = transaction_descriptions(short_data)
    assert next(descriptions) == "Перевод со счета на счет"

    # Проверка работы функции с длинным списком (транзакций в модуле data_dict_generators.py).
    descriptions = list(transaction_descriptions(transactions))
    assert len(descriptions) == 5


@pytest.mark.parametrize(
    "start, end, expected",
    [
        (1, 1, "0000 0000 0000 0001"),
        (2, 2, "0000 0000 0000 0002"),
        (12, 12, "0000 0000 0000 0012"),
    ],
)
def test_card_number_generator(start: int, end: int, expected: str) -> None:
    card_gen = card_number_generator(start, end)
    assert next(card_gen) == expected


# Тест валюты generators.py
@pytest.mark.parametrize(
    "currency, expected_count",
    [
        ("USD", 2),
        ("EUR", 1),
        ("RUB", 0),
    ]
)
def test_filter_by_currency(currency: str, expected_count: str) -> None:
    """Тест валюты generators.py"""
    result = list(filter_by_currency(transactions_cur, currency))
    assert len(result) == expected_count


def test_filter_by_currency_no_transactions() -> None:
    transactions = [
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
        },
    ]
    generator = filter_by_currency(transactions, "EUR")  # Предположим, что 'EUR' нет в списке
    with pytest.raises(StopIteration):
        next(generator)


def test_filter_by_currency_(transactions: dict) -> None:
    generator = filter_by_currency(transactions, "USD")
    assert next(generator)["operationAmount"]["currency"]["code"] == "USD"


def test_filter_by_currency_empty_list() -> None:
    generator = filter_by_currency([], "USD")
    with pytest.raises(StopIteration):
        next(generator)
