import json
import os
from typing import Optional, Dict, List
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
URL = "https://api.apilayer.com/exchangerates_data/latest"

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CACHE_FILE = os.path.join(BASE_DIR, "data", "exchange_rates.json")
TRANSACTIONS_FILE = os.path.join(BASE_DIR, "data", "operations.json")


def save_cache(data: dict):
    """Сохраняет словарь всех курсов в JSON-файл."""

    try:
        os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"[ОШИБКА] Не удалось записать кэш на диск: {e}")


def load_cache() -> Optional[dict]:
    if not os.path.exists(CACHE_FILE):
        return None
    try:
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"[ОШИБКА] Кэш на диске поврежден или не читается: {e}")
        return None


def fetch_from_api(base_currency: str) -> Optional[Dict[str, float]]:
    """Запрашивает свежий курс у сайта."""
    if not API_KEY:
        print("[ОШИБКА] Переменная окружения API_KEY не найдена!")
        return None

    try:
        response = requests.get(
            URL,
            headers={"apikey": API_KEY},
            params={"base": base_currency, "symbols": "RUB"},
            timeout=5
        )

        if response.status_code != 200:
            print(f"[DEBUG] API статус: {response.status_code} для {base_currency}")
            return None

        data = response.json()


        rate_container = data.get("quotes") or data.get("rates")
        rub_rate = rate_container.get("RUB") if rate_container else None

        if rub_rate is None:
            return None

        result = {"RUB": float(rub_rate), "timestamp": data.get("date")}

        # Сохраняем данные
        cache_to_save = {}
        existing_cache = load_cache()
        if existing_cache:
            cache_to_save.update(existing_cache)

        cache_to_save[base_currency] = result
        save_cache(cache_to_save)

        return result

    except requests.RequestException as e:
        print(f"[INFO] Нет подключения к сети ({e}). Попробуем найти данные в файле.")
        return None
    except Exception as e:
        print(f"[ОШИБКА СЕТИ] При получении курса {base_currency}: {e}")
        return None

def get_rates(base_currency: str) -> Optional[Dict[str, float]]:
    """ Главная точка входа. Сначала сеть -> Сохранение в файл.
    Затем чтение из файла при ошибке сети."""

    fresh_data = fetch_from_api(base_currency)
    if fresh_data:
        return fresh_data

    cached_data = load_cache()
    if cached_data and base_currency in cached_data:
        print(
            f"[INFO] Используем закешированный курс для {base_currency} от {cached_data[base_currency].get('timestamp')}")
        return cached_data[base_currency]

    print(f"[КРИТИЧЕСКАЯ ОШИБКА] Курс для {base_currency} не найден.")
    return None


def convert_to_rub(tx: dict, rate: float, currency_code: str) -> Optional[float]:
    """ Конвертация без доступа к сети.
    Принимает транзакцию, ГОТОВЫЙ ЧИСЛОВОЙ КОЭФФИЦИЕНТ курса и код валюты. """

    if not isinstance(tx, dict):
        return None

    amount_str = tx.get('amount')

    try:
        value = float(amount_str)
    except (ValueError, TypeError):
        return None

    if currency_code == "RUB":
        return value

    # Для USD/EUR используем кэшированный курс
    if rate is None:
        return None

    return round(value * rate, 2)

def load_transactions() -> List[Dict]:
    """ Загружает список транзакций из JSON-файла.
        Если файл отсутствует или поврежден, возвращает пустой список,
        предотвращая падение программы с необработанным исключением. """

    try:
        with open(TRANSACTIONS_FILE) as f:
            return json.load(f)
    except Exception:
        return []



