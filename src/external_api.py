import os
from typing import Dict, Optional

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
URL = "https://api.apilayer.com/exchangerates_data/latest"


def get_rates(base_currency: str) -> Optional[Dict[str, float]]:
    """Делает ОДИН запрос к API и возвращает словарь {валюта: курс}."""
    if not API_KEY:
        print("[ОШИБКА] Переменная окружения API_KEY не найдена!")
        return None

    try:
        response = requests.get(
            URL,
            headers={"apikey": API_KEY},
            params={"base": base_currency, "symbols": "RUB"},
            timeout=5,
        )

        if response.status_code != 200:
            print(f"[DEBUG] Не удалось получить курс для {base_currency}. Статус:" f" {response.status_code}")
            return None

        data = response.json()
        rate_container = data.get("quotes") or data.get("rates")
        if not rate_container:
            return None

        rub_rate = rate_container.get("RUB")
        if rub_rate is None:
            return None

        return {"RUB": float(rub_rate)}

    except Exception as e:
        print(f"[ОШИБКА СЕТИ] При получении курса {base_currency}->RUB: {e}")
        return None
