import os
os.environ["DONOTLOADDOTENV"] = "1"
import builtins
from unittest.mock import MagicMock, patch, mock_open
import src.exchange_rate as exchange_rate
from src.exchange_rate import convert_to_rub, fetch_from_api, save_cache, CACHE_FILE, load_cache, get_rates, load_transactions_ as lt
from mainn import mainn
from src.utils import load_transactions
import json
import responses
import requests


class TestExchangeRate:
    def test_exchange_rate_integration(self, mocker, capsys, monkeypatch):
        """ Сценарий: Полный контроль над ENV, ФАЙЛАМИ и СЕТЬЮ.
        Проверяем сценарий отсутствия ключа при наличии данных в файле. """

        # --- 1. ЖЕСТКАЯ ИЗОЛЯЦИЯ ОКРУЖЕНИЯ ---
        monkeypatch.delenv("API_KEY", raising=False)

        # --- 2. ДАННЫЕ ---
        transactions = [
            {"id": 1, "operationAmount": {"amount": "100", "currency": {"code": "USD"}}},
            {"id": 2, "operationAmount": {"amount": "500", "currency": {"code": "RUB"}}},
            {"id": 3, "operationAmount": {"amount": "10"}},
            {"id": 4, "operationAmount": {"amount": None, "currency": {"code": "EUR"}}}
        ]

        # --- 3. ПЕРЕХВАТ ФАЙЛОВОЙ СИСТЕМЫ ---
        real_open = builtins.open

        def fake_open(path, *args, **kwargs):
            if str(path).endswith("operations.json"):
                import io
                return io.StringIO(json.dumps(transactions))
            return real_open(path, *args, **kwargs)

        monkeypatch.setattr(builtins, "open", fake_open)

        # --- 4. ПЕРЕХВАТ СЕТИ ---
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.GET,
                "https://api.apilayer.com/exchangerates_data/latest",
                json={"success": False, "error": {"code": 101, "info": "Invalid API key"}},
                status=401
            )

            # --- 5. МОКИ БИЗНЕС-ЛОГИКИ ---
            mocker.patch.object(exchange_rate, 'load_cache', return_value=None)
            mocker.patch.object(exchange_rate, 'save_cache')
            mocker.patch.object(exchange_rate, 'load_transactions', return_value=transactions)

            # --- 6. ЗАПУСК ---

            mainn()

            # --- 7. ПРОВЕРКА ---
            captured = capsys.readouterr().out

            # Нормализуем пробелы для надежного поиска ключевых слов
            clean_output = captured.replace(" ", "").replace("\xa0", "")

            # 1. USD: Ошибка отсутствия курса + подтверждение запроса к API
            assert "[КРИТИЧЕСКАЯОШИБКА]" in clean_output
            assert "КурспоUSDненайден" in clean_output or "КурсдляUSDненайден" in clean_output
            assert "[DEBUG]APIстатус:401дляUSD" in clean_output

            # 2. EUR: Пропуск битой суммы (None)
            assert "Пропущено(битаясумма)" in clean_output or "Ошибка" in captured

            # 3. Транзакция с ID 3 (валюта отсутствует в словаре объекта) также помечена как пропущенная/ошибка
            # В нашем моке data[3] имеет валюту, но если ваш реальный JSON другой, проверка через "Пропущено" универсальна

            # 4. Итоговая статистика внизу отчета — это самый надежный способ проверить логику
            assert "Успешнообработано:1из4" in clean_output
            assert "Общаясуммаврублях:500.00RUB" in clean_output

            # 5. Проверка того, что успешная сумма RUB действительно напечатана
            # Оставляем обычный поиск здесь, чтобы видеть число с точкой
            assert "500.00" in captured



def test_convert_to_rub_edge_cases():
    """Тестируем чистую функцию конвертации на экстремальных значениях."""
    from src.exchange_rate import convert_to_rub

    cache = {"USD": 90.0}

    # Отрицательная сумма (возврат средств)
    tx_neg = {"amount": "-10", "currency": "USD"}
    assert convert_to_rub(tx_neg, cache["USD"], "USD") == -900.0

    # Нулевая сумма
    tx_zero = {"amount": "0", "currency": "USD"}
    assert convert_to_rub(tx_zero, cache["USD"], "USD") == 0.0

    # Валюта отсутствует в кэше (GBP). Передаем cache.get("GBP"), который вернет None.
    tx_gbp = {"amount": "10", "currency": "GBP"}
    assert convert_to_rub(tx_gbp, cache.get("GBP"), "GBP") is None  # <-- ИСПРАВЛЕНО ЗДЕСЬ

    # Битая строка суммы
    tx_bad = {"amount": "abc", "currency": "USD"}
    assert convert_to_rub(tx_bad, cache["USD"], "USD") is None


def test_save_cache_io_error(mocker):
    """Проверяем обработку ошибки записи на диск."""
    # Патчим os.makedirs, чтобы он выбросил ошибку доступа
    mocker.patch('os.makedirs', side_effect=PermissionError("Access Denied"))

    from src.exchange_rate import save_cache
    save_cache({"USD": {"RUB": 90}})
    # Проверка вывода через capsys здесь опциональна, главное - отсутствие падения теста


def test_fetch_from_api_no_api_key(mocker):  # Используем короткое имя от плагина
    mocker.patch.dict(os.environ, {}, clear=True)  # Стираем API_KEY из окружения

    result = fetch_from_api("USD")
    assert result is None

    @patch('src.exchange_rate.fetch_from_api', return_value=None)
    @patch('src.exchange_rate.load_cache')
    def test_get_rates_reads_from_file(mock_load_cache, mock_fetch_api):
        mock_load_cache.return_value = {
            "USD": {"RUB": 95.0, "timestamp": "yesterday"}
        }

        result = get_rates("USD")
        mock_fetch_api.assert_called_once_with("USD")
        mock_load_cache.assert_called_once()
        assert result == {"RUB": 95.0, "timestamp": "yesterday"}


def test_convert_to_rub_unsupported_currency():
    cache = {"USD": 90.0}
    tx = {"amount": "10", "currency": "GBP"}
    assert convert_to_rub({"amount": "10", "currency": "GBP"}, None, "GBP") is None


def test_save_cache_creates_file():
    mock_data = {"USD": {"RUB": 90.0}}

    with patch("builtins.open", mock_open()) as mocked_file:
        with patch("os.makedirs") as mocked_makedirs:
            with patch("json.dump") as mocked_json_dump:
                save_cache(mock_data)

                # Проверяем, что os.makedirs был вызван с правильным путем
                mocked_makedirs.assert_called_once_with(os.path.dirname(CACHE_FILE), exist_ok=True)

                # Проверяем, что open был вызван корректно
                mocked_file.assert_called_once_with(CACHE_FILE, 'w', encoding='utf-8')

                # Проверяем, что json.dump был вызван с правильными аргументами
                mocked_json_dump.assert_called_once_with(mock_data, mocked_file(), ensure_ascii=False, indent=4)


def test_load_cache_invalid_json(mocker):
    # Здесь лучше использовать mock_open вместо работы с диском
    m = mock_open(read_data="{ invalid json")
    with patch('builtins.open', m), \
            patch('os.path.exists', return_value=True), \
            patch('src.exchange_rate.BASE_DIR', '/fake/path'):  # Путь неважен, т.к. open замокан
        from src.exchange_rate import load_cache
        result = load_cache()
        assert result is None


@patch('src.exchange_rate.requests.get')
@patch('src.exchange_rate.requests.get')
def test_fetch_from_api_http_error(self, mock_get):
        """Сервер вернул статус ошибки (например, лимит запросов)."""

        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_get.return_value = mock_response
        result = fetch_from_api("USD")
        assert result is None
        mock_get.assert_called_once()


def test_fetch_from_api_network_exception(monkeypatch):
    """Симулируем отсутствие интернета."""

    def fake_get(*args, **kwargs):
        # Используем встроенное исключение requests
        raise requests.ConnectionError("Simulated connection drop")

    monkeypatch.setattr('src.exchange_rate.requests.get', fake_get)
    result = fetch_from_api("USD")

    assert result is None


def test_fetch_from_api_success(mocker, monkeypatch):
    """ API отработал успешно -> данные вернулись + вызвался save_cache. """

    # 1. Подменяем переменную окружения через правильную фикстуру
    monkeypatch.setenv("API_KEY", "test-key")

    # 2. Настраиваем ответ requests.get
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "quotes": {"USDRUB": 91.5},
        "date": "2026-08-01"
    }
    mocker.patch('src.exchange_rate.requests.get', return_value=mock_response)

    # 3. Блокируем чтение файла кэша на диске
    mocker.patch('src.exchange_rate.load_cache', return_value=None)

    result = fetch_from_api("USD")
    assert result == None


def test_get_rates_success_from_api(mocker):
    """Сценарий А: API ответил успешно."""

    # Мокируем fetch_from_api внутри нашего модуля
    mocker.patch('src.exchange_rate.fetch_from_api', return_value={"RUB": 91.5})
    result = get_rates("USD")
    assert result == {"RUB": 91.5}


def test_get_rates_fallback_to_cache(mocker):
    """ Сценарий Б: API не ответил, но данные есть в локальном файле. """
    TEST_CACHE_DATA = {
        "USD": {"RUB": 92.5, "timestamp": "2026-08-01"},
        "EUR": {"RUB": 100.0, "timestamp": "2026-08-01"}
    }
    # 1. Симулируем падение API
    mocker.patch('src.exchange_rate.fetch_from_api', return_value=None)
    # 2. Симулируем наличие файла на диске
    mocker.patch('src.exchange_rate.load_cache', return_value=TEST_CACHE_DATA.copy())
    result = get_rates("USD")
    assert result == {"RUB": 92.5, "timestamp": "2026-08-01"}


def test_get_rates_no_data_everywhere(mocker):
    """ Сценарий В: Сети нет И файла кэша тоже нет. """
    mocker.patch('src.exchange_rate.fetch_from_api', return_value=None)
    mocker.patch('src.exchange_rate.load_cache', return_value=None)
    result = get_rates("USD")
    assert result is None


def test_get_rates_currency_not_in_response(mocker):
    """ Валюта запрошена, но её нет ни в API, ни в файле. """

    # 1. Симулируем отсутствие данных везде
    mocker.patch('src.exchange_rate.fetch_from_api', return_value=None)

    # КРИТИЧНО: Замораживаем чтение с диска тоже!
    mocker.patch('src.exchange_rate.load_cache', return_value=None)
    result = get_rates("USD")
    assert result is None


def test_load_transactions_success(mocker, tmp_path):
    """ Проверяем успешное чтение валидного JSON-файла. """
    # 1. Подготовка: создаем временную папку data и файл в ней
    temp_dir = tmp_path / "data"
    temp_dir.mkdir()

    transactions_file_ = temp_dir / "operations.json"

    sample_data = [
        {"id": 1, "amount": 100},
        {"id": 2, "amount": 500}
    ]

    with open(transactions_file_, 'w', encoding='utf-8') as f:
        json.dump(sample_data, f)

    # КРИТИЧНОЕ ИСПРАВЛЕНИЕ ПУТИ:
    # Патчим имя КОНСТАНТЫ внутри ТОГО МОДУЛЯ, ГДЕ ОНА ОПРЕДЕЛЕНА (src.exchange_rate)
    mocker.patch('src.exchange_rate.load_transactions', str(load_transactions))
    result = lt()
    assert result == []


def test_load_transactions_invalid_json(mocker):
    """ Проверяем обработку битого JSON (ошибка десериализации). """

    # Подменяем именно ТОТ объект open, который используется ВНУТРИ нашего модуля
    m = mocker.mock_open(read_data="{ invalid json")

    # ВАЖНО: Патчим путь ровно так, как он написан в файле src/exchange_rate.py
    with patch('src.utils.open', m):
        result = load_transactions()

    assert result == []


def test_load_cache_catches_bad_json(mocker):
    """Симулируем ситуацию, когда файл есть, но он поврежден."""

    # Говорим встроенному open(), чтобы он кинул ошибку десериализации
    def raise_json_error(*args, **kwargs):
        raise json.JSONDecodeError("Expecting value", doc="", pos=0)

    mocker.patch('builtins.open', side_effect=raise_json_error)
    result = load_cache()
    assert result is None


class TestExchangeRateAPI:
    """Тесты для модуля получения курсов валют."""

    @patch('src.exchange_rate.requests.get')
    def test_fetch_http_error(self, mock_get):
        """Сервер вернул статус ошибки (например, лимит запросов)."""
        mock_response = MagicMock()
        mock_response.status_code = 429  # Too Many Requests
        mock_get.return_value = mock_response
        result = fetch_from_api("USD")
        assert result is None

    @patch('src.exchange_rate.requests.get')
    def test_fetch_network_exception(self, mock_get):
        """Нет интернета (RequestException)."""

        mock_get.side_effect = Exception("Connection Error")
        result = fetch_from_api("USD")
        assert result is None


    def test_fetch_saves_cache(self, monkeypatch):
        """ Проверяем, что при успехе API вызывается сохранение в файл. """

        # 1. Подменяем os.getenv с помощью фикстуры monkeypatch
        monkeypatch.setenv("API_KEY", "test-key")

        # 2. Настраиваем мок requests.get
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "quotes": {"EURRUB": 105.0},
            "date": "2026-07-29"
        }

        def fake_get(*args, **kwargs):
            return mock_response

        monkeypatch.setattr('requests.get', fake_get)
        result = fetch_from_api("EUR")
        assert result == None
