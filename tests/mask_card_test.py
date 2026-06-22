from typing import Union

card_number = str(input("Введите номер карты:   "))


def get_mask_card_number(card_number: Union[str]) -> Union[str]:
    """Функция заменяет часть строки на *  и через через 4 знака ставит пробел"""

    if len(card_number) == 16:
        card_mask = card_number[0:4] + " " + card_number[4:6] + "** **** " + card_number[12:]

    else:
        print("Неверный номер карты")
        return card_number

    return card_mask


print("Номер карты:   ", get_mask_card_number(card_number))
