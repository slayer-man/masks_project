import json
import logging
import os
from pathlib import Path
from typing import Dict, List, Optional, TypedDict, cast

import requests
from dotenv import load_dotenv

# === НАСТРОЙКА ЛОГИРОВАНИЯ ===
logger = logging.getLogger("exchange_rate")
logger.setLevel(logging.DEBUG)

# Вычисляем путь к папке логов относительно корня проекта
BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)  # Автоматически создаем папку logs, если её нет

log_file_path = os.path.join(LOG_DIR, "exchange_rate.log")
file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# === ОСТАЛЬНЫЕ НАСТРОЙКИ ПУТЕЙ ===
load_dotenv()
API_KEY = os.getenv("API_KEY")
URL = "https://api.apilayer.com/exchangerates_data/latest"

CACHE_FILE = os.path.join(BASE_DIR, "data", "exchange_rates.json")
TRANSACTIONS_FILE = os.path.join(BASE_DIR, "data", "operations.json")


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
    """Запрашивает свежий курс у сайта и логирует HTTP-статусы ответов."""
    if not API_KEY:
        logger.error("Переменная окружения API_KEY не найдена!")
        return None

    try:
        response = requests.get(
            URL,
            headers={"apikey": API_KEY},
            params={"base": base_currency, "symbols": "RUB"},
            timeout=15,  # Увеличен до 15 секунд, чтобы избежать Read timed out
        )

        # === ЛОГИРОВАНИЕ КОДОВ ОТВЕТА ===
        if response.status_code == 200:
            data = response.json()
            rates_container = data.get("rates") or data.get("quotes", {})
            rub_rate_raw = rates_container.get("RUB")
            date_str = data.get("date")

            if rub_rate_raw is None or date_str is None:
                logger.error(f"API вернул статус 200, но структура JSON повреждена для {base_currency}")
                return None

            result: RateData = {"RUB": float(rub_rate_raw), "timestamp": date_str}

            # Обновление кэша
            cache_to_save = {}
            existing_cache = load_cache()
            if isinstance(existing_cache, dict):
                cache_to_save.update(existing_cache)
            cache_to_save[base_currency] = result
            save_cache(cache_to_save)

            logger.info(f"Данные для {base_currency} успешно загружены С САЙТА. Код ответа: {response.status_code}")
            return result

        # Если код НЕ 200 (например, 401, 429, 500)
        else:
            logger.error(
                f"Ошибка сервера APILayer! Курс для {base_currency} не получен. "
                f"Код статуса HTTP: {response.status_code} ({response.reason})"
            )
            return None

    except requests.exceptions.Timeout as e:
        logger.info(f"Превышено время ожидания ответа от сервера (Timeout 15s): {e}. Переходим на кэш.")
        return None
    except (requests.RequestException, Exception) as e:
        logger.info(f"Сбой сетевого соединения ({e}). Будет произведена попытка чтения локального кэша.")
        return None


def get_rates(base_currency: str) -> Optional[RateData]:
    """Возвращает курс валюты, записывая точный источник данных в лог-файл."""
    fresh_data = fetch_from_api(base_currency)
    if fresh_data:
        return fresh_data

    cached_data = load_cache()
    if cached_data and base_currency in cached_data:
        # Логируем чтение из файла
        logger.warning(
            f"Сеть недоступна. Данные для {base_currency} взяты ИЗ ЛОКАЛЬНОГО"
            f" ФАЙЛА-КЭША от {cached_data[base_currency].get('timestamp')}"
        )
        return cached_data[base_currency]

    logger.critical(f"Курс для {base_currency} не найден ни в сети, ни в кэше.")
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


def load_transactions() -> List[Transaction]:
    """Загружает список транзакций из правильного файла JSON."""
    # ДОБАВЛЯЕМ ДЕБАГ-ВЫВОД:
    print(f"[DEBUG] Python ищет файл тут: {os.path.abspath(TRANSACTIONS_FILE)}")

    if not os.path.exists(TRANSACTIONS_FILE):
        print(f"[ОШИБКА] Файл отсутствует по пути: {TRANSACTIONS_FILE}")
        return []
    try:
        with open(TRANSACTIONS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return cast(List[Transaction], data)
            return []
    except (OSError, json.JSONDecodeError) as e:
        print(f"[ОШИБКА] Транзакции повреждены или не читаются: {e}")
        return []
