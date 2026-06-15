from tests.test import *
from tests.mask_test import get_mask_account, get_mask_card_number


card_number = str(input("Введите номер банковской карты:   ").lower())

account = str(input("Введите номер банковского счета:   ").lower())

if __name__ == "__main__":

    print(words, card_number)

    #print("Номер банковской карты:   ", get_mask_card_number(card_number).upper())

    #print("Номер банковского счета:   ", get_mask_account(mask_account).capitalize())

