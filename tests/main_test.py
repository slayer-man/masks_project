#from tests.widget_test import *


card_number = str(input("Введите номер банковской карты:   "))

account = str(input("Введите номер банковского счета:   "))


print("Номер банковской карты:   ", get_mask_card_number(card_number))

print("Номер банковского счета:   ", get_mask_account(account))
