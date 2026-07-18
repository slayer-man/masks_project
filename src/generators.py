from typing import Any, Dict, Generator, Iterator, List

from data.data_dict_generators import transactions


# Генератор банковских карт
def card_number_generator(start_val: int, end_val: int) -> Generator[str, None, None]:
    """Генератор номеров карт. prefix - первые цифры в виде строки length - общая длина номера карты"""

    # Перебор диапазона от начального до конечного значения
    for current_num in range(start_val, end_val + 1):
        card_number = f"{current_num:016d}"
        card_num = " ".join([card_number[i:i + 4] for i in range(0, len(card_number), 4)])
        yield card_num


# --- Пример использования ---
if __name__ == "__main__":
    start = 1  # Начальное значение диапазона
    end = 5  # Конечное значение диапазона

    card = card_number_generator(start, end)

    for _ in range(end + 1 - start):
        print(next(card))


# Функция фильтр
def filter_by_currency(transactions: List[Dict[str, Any]], currency: str) -> Iterator[Dict[str, Any]]:
    """Функция фильтрующяя по currency"""

    for x in transactions:
        if x["operationAmount"]["currency"]["code"] == currency:

            yield x


usd_transactions = filter_by_currency(transactions, "USD")
for _ in range(3):
    print(next(usd_transactions))


# Генератор транзакций
def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """Генератор выводящий данные по 'description'."""
    for i, t in enumerate(transactions):
        transactions_name = t["description"]
        yield transactions_name


descriptions = transaction_descriptions(transactions)
for _ in range(5):
    print(next(descriptions))
