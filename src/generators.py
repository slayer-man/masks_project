from typing import Any, Dict, Generator, Iterator, List

from data.data_dict_generators import transactions


# 1. Генератор банковских карт
def card_number_generator(start_val: int, end_val: int) -> Generator[str, None, None]:
    """Генератор номеров карт с начальным значением start и конечным значением end"""
    for current_num in range(start_val, end_val + 1):
        card_number = f"{current_num:016d}"
        card_num = " ".join([card_number[i: i + 4] for i in range(0, len(card_number), 4)])
        yield card_num


# 2. Функция фильтр
def filter_by_currency(transactions: List[Dict[str, Any]], currency: str) -> Iterator[Dict[str, Any]]:
    """Функция фильтрующая словарь с транзакциями по currency"""
    for x in transactions:
        if (
            "operationAmount" in x
            and "currency" in x["operationAmount"]
            and x["operationAmount"]["currency"].get("code") == currency
        ):
            yield x


# 3. Генератор транзакций
def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """Генератор выводящий данные из словаря транзакций по 'description'."""
    for t in transactions:
        if "description" in t:
            yield t["description"]


# === ВСЕ ПРИНТЫ И ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ ПЕРЕНОСИМ СЮДА ===
if __name__ == "__main__":
    print("--- Тест генератора карт ---")
    start = 1
    end = 5
    card = card_number_generator(start, end)
    for _ in range(end + 1 - start):
        print(next(card))

    print("\n--- Тест фильтра валюты ---")
    usd_transactions = filter_by_currency(transactions, "USD")
    try:
        for _ in range(3):
            print(next(usd_transactions))
    except StopIteration:
        pass

    print("\n--- Тест описания транзакций ---")
    descriptions = transaction_descriptions(transactions)
    try:
        for _ in range(5):
            print(next(descriptions))
    except StopIteration:
        pass
