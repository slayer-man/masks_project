from data.data_dict_generators import short_data, transactions
from src.generators import transaction_descriptions


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
