from src.masks import get_mask_account, get_mask_card_number
from src.processing import filter_by_state, sort_by_date
from src.widget import get_date, mask_account_card
from tests.tests_dict import my_list_dict

card = str(input("Введите свой банковский аккаунт или номер карты: ")).capitalize()
date_string = str(input("Введите дату:  "))

if "Счет" in card:
    text_part, number_part = mask_account_card(card)
    masked_account = get_mask_account(number_part)
    print(text_part, masked_account)
else:
    text_part, number_part = mask_account_card(card)
    masked_card_number = get_mask_card_number(number_part)
    print(text_part, masked_card_number)

print(get_date(date_string))


# Проверка модуля processing.py

if __name__ == "__main__":

    print("По умолчанию (state='EXECUTED'):")

    result_executed = filter_by_state(my_list_dict)

    for item in result_executed:

        print(item)

    print("Сортировка по убыванию (reverse=True):")

    sorted_date = sort_by_date(result_executed, reverse=True)

    for item in sorted_date:

        print(item)
