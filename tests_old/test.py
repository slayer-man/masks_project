from src.masks import get_mask_account, get_mask_card_number

def mask_account_card(account_card: str) -> str:
    """Функция принимает в качестве аргумента строку, содержащую тип и номер карты или счета, и возвращает строку с замаскированным номером"""

    account_card_info = account_card.rsplit(' ', 1)

    if "Счет" in account_card:
        return f"{account_card_info[0]} {get_mask_account(account_card_info[1])}"

    else:
        return f"{account_card_info[0]} {get_mask_card_number(account_card_info[1])}"


if __name__ == "__main__":
    test_1 = "Visa Platinum 8990922113665229"
    test_2 = "Счет 73654108430135874305"
    print(mask_account_card(test_1))
    print(mask_account_card(test_2))