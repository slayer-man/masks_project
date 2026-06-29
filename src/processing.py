from datetime import datetime

from tests.tests_dict import my_list_dict


def filter_by_state(my_list_dict: list, state: str = "EXECUTED") -> list[str]:
    """Функция, которая принимает список словарей и опционально значение для ключа state (по умолчанию
    'EXECUTED'). Функция возвращает новый список словарей, содержащий только те словари, у которых ключ state
    соответствует указанному значению."""

    return [my_dict for my_dict in my_list_dict if my_dict.get("state") == state]


def sort_by_date(date_sort: list, reverse: bool = True) -> list:
    """Сортирует список словарей по дате в ключе 'date'."""

    def parse_date(date_str: str) -> datetime:
        """Преобразует строку даты в формате ISO в объект datetime."""

        return datetime.fromisoformat(date_str)

    # Сортируем список, используя ключ — преобразованную дату; сохраняем порядок по параметру reverse

    sorted_date = sorted(date_sort, key=lambda x: parse_date(x["date"]), reverse=reverse)

    return sorted_date


# Примеры использования и проверки функций


if __name__ == "__main__":

    print("По умолчанию (state='EXECUTED'):")

    result_executed = filter_by_state(my_list_dict)

    for item in result_executed:

        print(item)

    print("Сортировка по убыванию (reverse=True):")

    sorted_date = sort_by_date(result_executed, reverse=True)

    for item in sorted_date:

        print(item)
