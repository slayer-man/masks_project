import itertools
from typing import Any

from data.data_dict_generators import transactions


# Генератор банковских карт
def card_number_generator(start_val: int, end_val: int, prefix: str, length: int = 16) -> Any:
    """Генератор номеров карт. prefix - первые цифры в виде строки length - общая длина номера карты"""

    # Перебор диапазона от начального до конечного значения
    for current_num in range(start_val, end_val + 1):

        # Вычисляем сколько случайных цифр нужно дописать, чтобы достичь длины карты
        num_to_fill = length - len(prefix)

        for counter in itertools.count(start_val):
            counter_str = f"{counter:0{num_to_fill}d}"
            card_number = "".join(prefix + counter_str)
            card_num = " ".join([card_number[i : i + 4] for i in range(0, len(card_number), 4)])
            yield card_num


# --- Пример использования ---
if __name__ == "__main__":
    start = 1  # Начальное значение диапазона
    end = 5  # Конечное значение диапазона

    card = card_number_generator(start, end, prefix="0", length=16)

    for _ in range(end + 1 - start):
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
