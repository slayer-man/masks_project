from typing import Union

#card_number = str()


def get_mask_card_number(card_number: Union[str]) -> Union[str]:
    """Функция заменяет часть строки на *  и через через 4 знака ставит пробел"""

    card_number = card_number.replace(" ", "")

    if len(card_number) == 16:
        card_mask = card_number[0:4] + " " + card_number[4:6] + "** **** " + card_number[12:]

    else:
        return "Не верно введен номер банковской карты", card_number

    return card_mask


#account = str()


def get_mask_account(account: Union[str], number: int = 2) -> Union[str, int]:
    """Функция заменяет часть строки на *"""

    if len(account) != 20:
        return "Не верно введен номер банковского счета:   ", account

    else:
        mask_account: str = "*" * number + account[-4:]

    return mask_account
