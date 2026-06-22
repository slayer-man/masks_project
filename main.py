from src.masks import get_mask_account, get_mask_card_number
from src.widget import mask_account_card, get_date

card = str(input("Введите свой банковский аккаунт или номер карты: "))
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
