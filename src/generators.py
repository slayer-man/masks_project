import itertools
from typing import Any

from data.data_dict_generators import transactions


# Генератор банковских карт
def card_number_generator(prefix: str, length: int = 16) -> Any:
    """Генератор номеров карт. prefix - первые цифры в виде строки length - общая длина номера карты"""
    zeros_count = length - len(prefix)
    # Задаем начальное значение последних цифр (.count())
    for counter in itertools.count(1):
        counter_str = f"{counter:0{zeros_count}d}"
        card_number = "".join(prefix + counter_str)
        card_num = " ".join([card_number[i : i + 4] for i in range(0, len(card_number), 4)])
        yield card_num


# Создаем генератор номеров, всего 16 цифр (prefix - задает начальные цифры(до 14 цифр))
card = card_number_generator(prefix="", length=16)
# Вывод n - номеров.
for _ in range(5):
    print(next(card))


# Функция фильтр
def filter_by_currency(transactions: dict, currency: str) -> Any:
    """Функция фильтрующяя по currency"""

    for x in transactions:
        if x["operationAmount"]["currency"]["code"] == currency:

            yield x


usd_transactions = filter_by_currency(transactions, "USD")
for _ in range(3):
    print(next(usd_transactions))


# Генератор транзакций
def transaction_descriptions(transactions: list[dict[str, object]]) -> Any:
    """Генератор выводящий данные по 'description'."""
    for i, t in enumerate(transactions):
        transactions_name = t["description"]
        yield transactions_name


descriptions = transaction_descriptions(transactions)
for _ in range(5):
    print(next(descriptions))
