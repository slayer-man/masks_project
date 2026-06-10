from typing import Union

account = str(input("Введите аккаунта:   "))


def get_mask_account(account: Union[str], number: int = 2) -> Union[str, int]:
    """Функция заменяет часть строки на *"""

    if len(account) != 20:
        print("Не верно введен номер аккаунта:   ")
        return account

    else:
        mask_account: str = "*" * number + account[-4:]

    return mask_account


print("Номер аккаунта:   ", get_mask_account(account))
