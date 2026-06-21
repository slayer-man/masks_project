from widget_test import mask_account_card
from mask_test import get_mask_card_number, get_mask_account

card = str(input("Введите свой банковский аккаунт или номер карты: "))

if "Счет" in card:
    text_part, number_part = mask_account_card(card)
    masked_account = get_mask_account(number_part)
    print(text_part, masked_account)
else:
    text_part, number_part = mask_account_card(card)
    masked_card_number = get_mask_card_number(number_part)
    print(text_part, masked_card_number)
