import pytest
#from datetime import datetime
from src.processing import filter_by_state, sort_by_date  # Замени your_module_name на имя твоего модуля


my_list_dict = [
{"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
{"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
{"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
# добавь другие элементы здесь
]

#Тест для функции filter_by_state

@pytest.mark.parametrize("state, expected_count", [
("EXECUTED", 2),  # обнови ожидаемое количество в соответствии с твоими данными
("CANCELED", 1)   # обнови ожидаемое количество в соответствии с твоими данными
])


def test_filter_by_state(state, expected_count):
    filtered = filter_by_state(my_list_dict, state)
    assert len(filtered) == expected_count
    assert all(item['state'] == state for item in filtered)


#Тест для функции sort_by_date

@pytest.mark.parametrize("reverse, expected_first_date", [
(True, "2019-07-03T18:35:29.512364"),  # обнови ожидаемую первую дату
(False, "2018-06-30T02:08:58.425572")  # обнови ожидаемую первую дату
])


def test_sort_by_date(reverse, expected_first_date):
    sorted_list = sort_by_date(my_list_dict, reverse)
    assert sorted_list[0]['date'] == expected_first_date