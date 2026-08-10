from src.exchange_rate import convert_to_rub, get_rates, load_transactions


def mainn():
    """Функция которая считывает данные по курсам валют,
    переводит валюту в рубли"""

    transactions = load_transactions()
    print("--- Загрузка транзакций ---")
    if not transactions:
        print("Файл не найден или пуст.")
        return

    total_rub = 0.0
    count_success = 0

    print("Получение курсов валют...")
    usd_data = get_rates("USD")
    eur_data = get_rates("EUR")

    rates_cache = {}
    if usd_data and "RUB" in usd_data:
        rates_cache["USD"] = usd_data["RUB"]
    if eur_data and "RUB" in eur_data:
        rates_cache["EUR"] = eur_data["RUB"]

    print("\n--- Начало конвертации ---")

    for t in transactions:
        op_amount = t.get("operationAmount", {})
        amount_str = op_amount.get("amount")
        cur_obj = op_amount.get("currency", {})

        display_cur = ""
        if isinstance(cur_obj, dict):
            code = cur_obj.get("code")
            if code:
                display_cur = code.upper()

        rub_amount = None
        display_amt = "-"
        result_str = "Ошибка"

        # === ПРОВЕРКА НА СУММУ И ВАЛЮТУ ===
        # Сначала проверяем наличие строки суммы
        if not amount_str:
            result_str = "Пропущено (битая сумма)"

        elif not display_cur:
            result_str = "Пропущено (нет данных)"

        else:
            # Если данные есть, пробуем распарсить число
            try:
                value = float(amount_str)
                display_amt = f"{value:,.2f}".replace(",", " ")
            except ValueError, TypeError:
                display_amt = "-"
                result_str = "Пропущено (битая сумма)"

            else:
                # Логика конвертации ТОЛЬКО если сумма валидна
                if display_cur == "RUB":
                    rub_amount = value

                elif display_cur in ("USD", "EUR"):
                    currency_rate = rates_cache.get(display_cur)

                    if currency_rate is None:
                        result_str = "Ошибка RUB"
                    else:
                        tx_for_api = {"amount": str(value), "currency": display_cur}
                        rub_amount = convert_to_rub(tx_for_api, currency_rate, display_cur)

                        if rub_amount is not None:
                            pass  # Успех определим ниже общим условием
                        else:
                            result_str = "Ошибка RUB"

                else:
                    result_str = "Ошибка RUB"

        # ФИНАЛЬНОЕ присвоение статуса успеха и подсчет
        if rub_amount is not None:
            total_rub += rub_amount
            count_success += 1
            result_str = f"{rub_amount:,.2f} RUB".replace(",", " ")

        print(f"{display_amt} {display_cur} -> {result_str}")

    print("-" * 40)
    print(f"Успешно обработано: {count_success} из {len(transactions)}")
    final_total = f"{total_rub:,.2f}".replace(",", " ")
    print(f"Общая сумма в рублях: {final_total} RUB")


if __name__ == "__main__":
    mainn()
