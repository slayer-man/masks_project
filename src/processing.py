from datetime import datetime


def filter_by_state(my_list_dict: list, state: str = "EXECUTED") -> list[str]:
    """Функция filter_by_state, которая принимает список словарей и опционально значение для ключа state (по умолчанию
    'EXECUTED'). Функция возвращает новый список словарей, содержащий только те словари, у которых ключ state
    соответствует указанному значению."""

    return [my_dict for my_dict in my_list_dict if my_dict.get("state") == state]


def sort_by_date(transactions: list, reverse: bool = True) -> list:
    """Сортирует список словарей по дате в ключе 'date'."""

    def parse_date(date_string: str) -> datetime:
        """Парсит строку даты в формате ISO в объект datetime."""

        return datetime.fromisoformat(date_string)

    # Сортируем список, используя ключ — преобразованную дату; сохраняем порядок по параметру reverse

    sorted_transactions = sorted(transactions, key=lambda x: parse_date(x["date"]), reverse=reverse)

    return sorted_transactions


# Примеры использования и проверки функций

if __name__ == "__main__":

# Тестовые данные

    test_data = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]

    print("По умолчанию (state='EXECUTED'):")

    result_executed = filter_by_state(test_data)

    for item in result_executed:

        print(item)

    print("Сортировка по убыванию (reverse=True):")

    sorted_desc = sort_by_date(result_executed, reverse=True)

    for item in sorted_desc:

        print(item)
