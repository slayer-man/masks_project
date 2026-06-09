account = input("Введите аккаунта:   ")


def get_mask_account(account, number=2):
    """Функция заменяет часть строки на *"""

    if len(account) != 20:
        print("Не верно введен номер аккаунта:   ")
        return account

    else:
        mask_account = "*" * number + account[-4:]

    return mask_account


# Проверка
# get_mask_account('00001234567812345678', 3)

print("Номер аккаунта:   ", get_mask_account(account))
