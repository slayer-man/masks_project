from mainn import mainn as run_app
from src.exchange_rate import convert_to_rub


def test_main_success_flow(mocker, capsys, sample_transactions):
    mocker.patch('mainn.load_transactions', return_value=sample_transactions)

    # Мокируем функцию внутри модуля mainn
    mocker.patch('mainn.get_rates', side_effect=[
        {"RUB": 90.0},
        {"RUB": 100.0}
    ])

    run_app()
    captured = capsys.readouterr().out  # Это СТРОКА

    assert "100.00 USD -> 9 000.00 RUB" in captured
    assert "500.00 RUB -> 500.00 RUB" in captured  # <--- ИСПРАВЛЕНО: убрали .out
    assert "Пропущено (нет данных)" in captured
    assert "Пропущено (битая сумма)" in captured
    assert "Общая сумма в рублях: 9 500.00 RUB" in captured
    assert "Успешно обработано: 2 из 4" in captured


def test_convert_to_rub_edge_cases():
    """Тестируем чистую функцию на экстремальных значениях."""


    cache = {"USD": 90.0, "EUR": 100.0}

    # Отрицательная сумма
    tx_neg = {"amount": "-10", "currency": "USD"}
    assert convert_to_rub(tx_neg, cache["USD"], "USD") == -900.0

    # Нулевая сумма
    tx_zero = {"amount": "0", "currency": "USD"}
    assert convert_to_rub(tx_zero, cache["USD"], "USD") == 0.0

    # Валюта отсутствует в кэше (GBP)
    tx_gbp = {"amount": "10", "currency": "GBP"}
    # ПЕРЕДАЕМ ЧИСЛО (или None), а не весь словарь cache
    assert convert_to_rub(tx_gbp, cache.get("GBP"), "GBP") is None

    # Битая строка суммы
    tx_bad = {"amount": "abc", "currency": "USD"}
    assert convert_to_rub(tx_bad, cache["USD"], "USD") is None