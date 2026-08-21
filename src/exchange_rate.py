import json
import os
from typing import Dict, List, Optional, TypedDict, cast
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
URL = "https://api.apilayer.com/exchangerates_data/latest"

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CACHE_FILE = os.path.join(BASE_DIR, "data", "exchange_rates.json")


class RateData(TypedDict):
    RUB: float
    timestamp: str


def save_cache(data: dict) -> None:
    """Сохраняет словарь всех курсов в JSON-файл."""
    try:
        os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except OSError as e:
        print(f"[ОШИБКА] Не удалось записать кэш на диск: {e}")


def load_cache() -> Optional[Dict[str, RateData]]:
    if not os.path.exists(CACHE_FILE):
        return None
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            # Явно приводим тип загруженного JSON к ожидаемому словарю
            raw_data = json.load(f)
            return cast(Optional[Dict[str, RateData]], raw_data)
    except (OSError, json.JSONDecodeError) as e:
        print(f"[ОШИБКА] Кэш на диске поврежден или не читается: {e}")
        return None


def fetch_from_api(base_currency: str) -> Optional[RateData]:
    """Запрашивает свежий курс у сайта."""
    if not API_KEY:
        print("[ОШИБКА] Переменная окружения API_KEY не найдена!")
        return None

    try:
        response = requests.get(
            URL, headers={"apikey": API_KEY}, params={"base": base_currency, "symbols": "RUB"}, timeout=5
        )

        if response.status_code != 200:
            print(f"[DEBUG] API статус: {response.status_code} для {base_currency}")
            return None

        data = response.json()

        # Используем .get() с дефолтами, чтобы избежать TypeError при обращении к None
        rates_container = data.get("rates") or data.get("quotes", {})

        rub_rate_raw = rates_container.get("RUB")
        date_str = data.get("date")

        if rub_rate_raw is None or date_str is None:
            return None

        result: RateData = {"RUB": float(rub_rate_raw), "timestamp": date_str}

        cache_to_save = {}
        existing_cache = load_cache()
        if isinstance(existing_cache, dict):
            cache_to_save.update(existing_cache)

        cache_to_save[base_currency] = result
        save_cache(cache_to_save)

        return result

    except (requests.RequestException, Exception) as e:

        print(f"[INFO] Нет подключения к сети ({e}). Попробуем найти данные в файле.")

        return None

    except (ValueError, KeyError) as e:

        print(f"[ОШИБКА СЕТИ/ДАННЫХ] При получении курса {base_currency}: {e}")

        return None


def get_rates(base_currency: str) -> Optional[RateData]:
    fresh_data = fetch_from_api(base_currency)
    if fresh_data:
        return fresh_data

    cached_data = load_cache()
    if cached_data and base_currency in cached_data:
        print(
            f"[INFO] Используем закешированный курс для {base_currency} от"
            f" {cached_data[base_currency].get('timestamp')}"
        )
        return cached_data[base_currency]

    print(f"[КРИТИЧЕСКАЯ ОШИБКА] Курс для {base_currency} не найден ни в сети, ни в кэше.")
    return None


# Строгая структура транзакции для mypy
class Transaction(TypedDict, total=False):
    amount: str | int | float
    currency: str


def convert_to_rub(tx: Transaction, rate: Optional[float], currency_code: str) -> Optional[float]:
    """Конвертация без доступа к сети."""

    # Проверка валюты делается сразу, чтобы избежать лишних вычислений
    if currency_code == "RUB":
        # Для рублей коэффициент должен быть строго 1.0
        if rate is not None and abs(rate - 1.0) > 1e-9:
            print(f"[ПРЕДУПРЕЖДЕНИЕ] Для RUB передан некорректный курс {rate}. Игнорируем.")
        return _safe_parse_amount(tx)

    if rate is None:
        return None

    value = _safe_parse_amount(tx)
    if value is None:
        return None

    return round(value * rate, 2)


def _safe_parse_amount(tx: Transaction) -> Optional[float]:
    """Безопасное извлечение суммы из транзакции."""
    amount_str = tx.get("amount")
    if amount_str is None:
        return None
    try:
        return float(amount_str)
    except ValueError, TypeError:
        return None


    """Загружает список транзакций из JSON-файла."""
    try:
            data = json.load(f)
            # Убеждаемся, что вернулся именно список словарей
            if isinstance(data, list):
                return cast(List[Transaction], data)
            return []
    except FileNotFoundError:
        # Файл еще не создан — это штатная ситуация
        return []
    except (OSError, json.JSONDecodeError) as e:
        print(f"[ОШИБКА] Транзакции повреждены или не читаются: {e}")
        return []
