from typing import Union


def get_mask_card_number(card_number: Union[str]) -> Union[str]:
    """Функция заменяет часть строки на *  и через через 4 знака ставит пробел"""

    card_number = card_number.replace(" ", "")

    if len(str(card_number)) == 16:
        card_mask = card_number[0:4] + " " + card_number[4:6] + "** **** " + card_number[12:]

    else:
        try:
            raise ValueError(card_number)

        except ValueError:
            # Ловим ошибку и продолжаем дальше
            print("Не верно введен номер банковской карты:  ")
            pass

        return card_number

    return card_mask


def get_mask_account(account: Union[str], number: int = 2) -> Union[str, int]:
    """Функция заменяет часть строки на *"""

    account = account.replace(" ", "")

    if len(account) != 20:
        try:
            raise ValueError(account)

        except ValueError:
            # Ловим ошибку и продолжаем дальше
            print("Не верно введен номер банковского счета:  ")
            pass

        return account

    else:
        mask_account: str = "*" * number + account[-4:]

    return mask_account
