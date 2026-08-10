import os
from typing import Dict, Optional

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
URL = "https://api.apilayer.com/exchangerates_data/latest"


def get_rates(base_currency: str) -> Optional[Dict[str, float]]:
    """
    Делает ОДИН запрос к API и возвращает словарь {валюта: курс}.
    Например: {"RUB": 78.15}
    """
    if not API_KEY:
        print("[ОШИБКА] Переменная окружения API_KEY не найдена!")
        return None

    try:
        response = requests.get(
            URL, headers={"apikey": API_KEY}, params={"base": base_currency, "symbols": "RUB"}, timeout=5
        )

        # Если сервер вернул ошибку (например, лимит исчерпан), выходим
        if response.status_code != 200:
            print(f"[DEBUG] Не удалось получить курс для {base_currency}. Статус: {response.status_code}")
            return None

        data = response.json()

        # Универсальный поиск курса: сначала ищем 'quotes', затем 'rates'
        rate_container = data.get("quotes") or data.get("rates")
        if not rate_container:
            print(f"[DEBUG] Неожиданная структура ответа для {base_currency}: нет ключей quotes/rates.")
            return None

        rub_rate = rate_container.get("RUB")
        if rub_rate is None:
            print(f"[DEBUG] Курс RUB не найден в ответе для базовой валюты {base_currency}.")
            return None

        return {"RUB": float(rub_rate)}

    except Exception as e:
        print(f"[ОШИБКА СЕТИ] При получении курса {base_currency}->RUB: {e}")
        return None


def convert_to_rub(tx: dict, cache: dict) -> Optional[float]:
    """
    Конвертирует сумму, используя заранее полученные курсы из словаря cache.
    НЕ делает запросов к сети.
    """
    if not isinstance(tx, dict):
        return None

    amount = tx.get("amount")
    currency = str(tx.get("currency", "")).upper()

    try:
        value = float(amount)
    except ValueError, TypeError:
        return None

    # Рубли конвертировать не нужно
    if currency == "RUB":
        return value

    # Проверяем, есть ли нужный нам курс в нашем кэше
    rate = cache.get(currency)

    # Если курса нет в кэше (например, была валюта GBP, а мы её не запрашивали)
    if rate is None:
        return None

    return round(value * rate, 2)
