import os
from data.data_dict_processing import my_list_dict
from src.exchange_rate import convert_to_rub, get_rates, load_transactions
from src.masks import get_mask_account, get_mask_card_number
from src.processing import filter_by_state, sort_by_date
from src.search import process_bank_search
from src.utils import load_csv_transactions, load_xlsx_transactions
from src.widget import get_date, mask_account_card

# Находим корень проекта для вычисления точных путей к папке data/
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE_PATH = os.path.join(BASE_DIR, "data", "transactions.csv")
XLSX_FILE_PATH = os.path.join(BASE_DIR, "data", "transactions_excel.xlsx")


def main():
    """Основная функция, отвечающая за логику интерфейса и связь всех модулей проекта."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    # 1. Выбор типа файла
    while True:
        user_choice = input("\nПользователь: ").strip()
        if user_choice == "1":
            print("\nПрограмма: Для обработки выбран JSON-файл.")
            transactions = load_transactions()
            break
        elif user_choice == "2":
            print("\nПрограмма: Для обработки выбран CSV-файл.")
            # ВЫЗОВ ФУНКЦИИ CSV:
            print(f"[DEBUG] Ищем файл тут: {CSV_FILE_PATH}")
            transactions = load_csv_transactions(CSV_FILE_PATH)
            break
        elif user_choice == "3":
            print("\nПрограмма: Для обработки выбран XLSX-файл.")
            # ВЫЗОВ ФУНКЦИИ EXCEL:
            print(f"[DEBUG] Ищем файл тут: {XLSX_FILE_PATH}")
            transactions = load_xlsx_transactions(XLSX_FILE_PATH)
            break
        else:
            print(
                "Программа: Неверный пункт меню. Пожалуйста, выберите 1, 2 или"
                " 3."
            )

    if not transactions:
        print("\nПрограмма: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # 2. Выбор статуса операции с помощью цифр (1, 2, 3)
    # Создаем словарь для быстрого сопоставления цифры со статусом
    status_mapping = {
        "1": "EXECUTED",
        "2": "CANCELED",
        "3": "PENDING"
    }

    while True:
        print("\nПрограмма: Введите цифру статуса, по которому необходимо выполнить фильтрацию:")
        print("1. EXECUTED")
        print("2. CANCELED")
        print("3. PENDING")

        user_status_choice = input("\nПользователь: ").strip()

        # Проверяем, есть ли введенная цифра в нашем словаре
        if user_status_choice in status_mapping:
            chosen_status = status_mapping[user_status_choice]
            print(f'\nПрограмма: Операции отфильтрованы по статусу "{chosen_status}"')

            # Передаем уже готовую строчку в вашу функцию фильтрации
            filtered_tx = filter_by_state(transactions, state=chosen_status)
            break
        else:
            print(f'\nПрограмма: Пункт меню "{user_status_choice}" недоступен. Пожалуйста, выберите 1, 2 или 3.')

    # 3. Сортировка по дате с помощью цифр (1, 2)
    print("\nПрограмма: Отсортировать операции по дате? Да/Нет")
    confirm_sort = input("\nПользователь: ").strip().lower()

    if confirm_sort == "да":
        while True:
            print("\nПрограмма: Выберите направление сортировки:")
            print("1. По возрастанию")
            print("2. По убыванию")

            sort_choice = input("\nПользователь: ").strip()

            if sort_choice == "1":
                print("\nПрограмма: Выбрана сортировка по возрастанию.")
                filtered_tx = sort_by_date(filtered_tx, reverse=False)
                break
            elif sort_choice == "2":
                print("\nПрограмма: Выбрана сортировка по убыванию.")
                filtered_tx = sort_by_date(filtered_tx, reverse=True)
                break
            else:
                print(f'\nПрограмма: Пункт меню "{sort_choice}" недоступен. Пожалуйста, выберите 1 или 2.')

    # 4. Фильтрация по валюте (Только RUB)
    print("\nПрограмма: Выводить только рублевые транзакции? Да/Нет")
    only_rub = input("\nПользователь: ").strip().lower()

    if only_rub == "да":
        rub_tx = []
        for t in filtered_tx:
            op_amount = t.get("operationAmount", {})
            cur_obj = op_amount.get("currency", {}) if isinstance(op_amount, dict) else {}
            code = cur_obj.get("code", "").upper() if isinstance(cur_obj, dict) else ""
            if code == "RUB":
                rub_tx.append(t)
        filtered_tx = rub_tx

    # 5. Фильтрация по ключевому слову в описании (re)
    print("\nПрограмма: Отфильтровать список транзакций по определенному слову в описании? Да/Нет")
    confirm_search = input("\nПользователь: ").strip().lower()

    if confirm_search == "да":
        search_word = input("\nПрограмма: Введите слово для поиска:\nПользователь: ").strip()
        filtered_tx = process_bank_search(filtered_tx, search_word)


      # Получаем курсы валют ОДИН раз перед циклом для экономии запросов и чистых логов
    print("\nПрограмма: Получение актуальных курсов валют...")
    rates_memory_cache = {}

    for code in ("USD", "EUR"):
        rate_data = get_rates(code)
        if rate_data and "RUB" in rate_data:
            rates_memory_cache[code] = rate_data["RUB"]

    print("\nПрограмма: Распечатываю итоговый список транзакций...\n")

    if not filtered_tx:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"Программа: \nВсего банковских операций в выборке: {len(filtered_tx)}\n")

    for t in filtered_tx:
        raw_date = t.get("date", "")
        date_str = get_date(raw_date) if raw_date else "Дата неизвестна"
        desc = t.get("description", "Без описания")

        # Маскирование
        from_info = t.get("from", "")
        to_info = t.get("to", "")
        masked_from = ""
        if from_info:
            text_part, num_part = mask_account_card(from_info)
            masked_from = f"{text_part} {get_mask_account(num_part)}" if "Счет" in text_part else f"{text_part} {get_mask_card_number(num_part)}"

        masked_to = ""
        if to_info:
            text_part, num_part = mask_account_card(to_info)
            masked_to = f"{text_part} {get_mask_account(num_part)}" if "Счет" in text_part else f"{text_part} {get_mask_card_number(num_part)}"

        transfer_line = f"{masked_from} -> {masked_to}" if masked_from else masked_to

        # Сумма и валюта
        op_amount = t.get("operationAmount", {})
        amount_str = op_amount.get("amount", "0")
        cur_obj = op_amount.get("currency", {}) if isinstance(op_amount, dict) else {}
        code = cur_obj.get("code", "").upper() if isinstance(cur_obj, dict) else ""
        currency_name = cur_obj.get("name", "руб.")

        display_amt = amount_str

        if code == "RUB":
            try:
                display_amt = int(float(amount_str))
            except (ValueError, TypeError):
                pass
        elif code in ("USD", "EUR"):
            # Быстро берем курс из кэша в оперативной памяти
            rate_value = rates_memory_cache.get(code)

            if rate_value:
                tx_for_api = {"amount": amount_str, "currency": code}
                rub_amount = convert_to_rub(tx_for_api, rate_value, code)
                if rub_amount is not None:
                    display_amt = int(rub_amount)
                    currency_name = "руб. (сконвертировано из " + code + ")"

        print(f"{date_str} {desc}")
        if transfer_line:
            print(transfer_line)
        print(f"Сумма: {display_amt} {currency_name}\n")


if __name__ == "__main__":
    main()
