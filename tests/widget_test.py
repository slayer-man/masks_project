#from tests.mask_test import get_mask_card_number, get_mask_account


get_mask_account = ()
get_mask_card_number = ()


def mask_account_card(letters_digits: str) -> str:

    if not letters_digits:
        return "Ошибка ввода: пустая строка"

    if not isinstance(letters_digits, str):
        raise TypeError(f"Ожидалась строка, получен {type(letters_digits).__name__}")

    letters = []
    digits = []

    for letter in letters_digits:
        if letter.isalpha() or letter.isspace():
            letters.append(letter)
        elif letter.isdigit():
            digits.append(letter)

    letters_str = "".join(letters).strip()
    digits_str = "".join(digits)

    if not digits_str:
        return "Ошибка ввода: не найдено цифр"
    if not letters_str:
        return "Ошибка ввода: не найдено букв"

    if letters_str == "Счет":
        if len(digits_str) != 20:
            return f"Ошибка ввода: номер счета должен содержать 20 цифр (получено {len(digits_str)})"
        return f"{letters_str} {get_mask_account(digits_str)}"
    else:
        if len(digits_str) != 16:
            if len(digits_str) > 16:
                return f"Ошибка ввода: номер содержит {len(digits_str)} цифр (ожидается 16). Возможно, введены лишние цифры"
            else:
                return f"Ошибка ввода: номер карты содержит {len(digits_str)} цифр (ожидается 16)"
        if len(letters_str) < 2:
            return "Ошибка ввода: название карты слишком короткое"
        return f"{letters_str} {get_mask_card_number(digits_str)}"
