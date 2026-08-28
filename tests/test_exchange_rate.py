import json
from unittest.mock import MagicMock, mock_open, patch
import pytest
import requests
from src import exchange_rate


# ==========================================
# Тесты для функций работы с файловым кэшем
# ==========================================

def test_save_cache_success():
    """Тест успешного сохранения кэша."""
    test_data = {"USD": {"RUB": 90.0, "timestamp": "2026-01-01"}}
    m_open = mock_open()

    with patch("os.makedirs") as mock_makedirs, patch("builtins.open", m_open):
        exchange_rate.save_cache(test_data)

        # Проверяем, что папка для кэша создается автоматически
        mock_makedirs.assert_called_once()
        # Проверяем, что в файл был записан сериализованный JSON
        m_open.assert_called_once_with(exchange_rate.CACHE_FILE, "w", encoding="utf-8")


def test_save_cache_os_error():
    """Тест перехвата OSError при сохранении кэша (например, нет прав доступа)."""
    with patch("os.makedirs", side_effect=OSError("Permission denied")):
        # Функция не должна выбрасывать исключение наружу, а должна его обработать
        exchange_rate.save_cache({"data": "test"})


def test_load_cache_file_not_found():
    """Тест загрузки кэша, когда файла физически не существует."""
    with patch("os.path.exists", return_value=False):
        assert exchange_rate.load_cache() is None


def test_load_cache_success():
    """Тест успешного чтения корректных данных из кэша."""
    cached_data = {"USD": {"RUB": 90.5, "timestamp": "2026-08-27"}}
    m_open = mock_open(read_data=json.dumps(cached_data))

    with patch("os.path.exists", return_value=True), patch("builtins.open", m_open):
        result = exchange_rate.load_cache()
        assert result == cached_data


def test_load_cache_json_decode_error():
    """Тест обработки исключения при поврежденном JSON в файле кэша."""
    m_open = mock_open(read_data="{invalid json")

    with patch("os.path.exists", return_value=True), patch("builtins.open", m_open):
        assert exchange_rate.load_cache() is None


# ==========================================
# Тесты для функций работы с внешним API
# ==========================================

def test_fetch_from_api_no_api_key():
    """Тест поведения функции, если в системе отсутствует API_KEY."""
    with patch("src.exchange_rate.API_KEY", None):
        assert exchange_rate.fetch_from_api("USD") is None


@patch("requests.get")
def test_fetch_from_api_success(mock_get):
    """Тест успешного запроса к API, сохранения данных в кэш и возврата результата."""
    # Имитируем успешный JSON-ответ от сервера
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "rates": {"RUB": 91.5},
        "date": "2026-08-27"
    }
    mock_get.return_value = mock_response

    with patch("src.exchange_rate.API_KEY", "test_key"), \
            patch("src.exchange_rate.load_cache", return_value={}), \
            patch("src.exchange_rate.save_cache") as mock_save:
        result = exchange_rate.fetch_from_api("USD")

        assert result == {"RUB": 91.5, "timestamp": "2026-08-27"}
        # Проверяем, что данные ушли на запись в кэш
        mock_save.assert_called_once_with({"USD": result})


@patch("requests.get")
def test_fetch_from_api_server_error(mock_get):
    """Тест поведения программы при коде ответа сервера, отличном от 200."""
    mock_response = MagicMock()
    mock_response.status_code = 429  # Too Many Requests (исчерпан лимит)
    mock_get.return_value = mock_response

    with patch("src.exchange_rate.API_KEY", "test_key"):
        assert exchange_rate.fetch_from_api("USD") is None


@patch("requests.get", side_effect=requests.RequestException("Timeout"))
def test_fetch_from_api_network_exception(mock_get):
    """Тест обработки падения сети / таймаута соединения."""
    with patch("src.exchange_rate.API_KEY", "test_key"):
        assert exchange_rate.fetch_from_api("USD") is None


# ==========================================
# Тесты для связующей функции get_rates
# ==========================================

def test_get_rates_from_api_first():
    """Если API работает, get_rates должен сразу вернуть свежие данные."""
    api_data = {"RUB": 95.0, "timestamp": "2026-08-27"}
    with patch("src.exchange_rate.fetch_from_api", return_value=api_data):
        assert exchange_rate.get_rates("USD") == api_data


def test_get_rates_fallback_to_cache():
    """Если API лежит, но данные есть в кэше — get_rates должен вытащить их из кэша."""
    cached_data = {"EUR": {"RUB": 100.0, "timestamp": "2026-08-20"}}
    with patch("src.exchange_rate.fetch_from_api", return_value=None), \
            patch("src.exchange_rate.load_cache", return_value=cached_data):
        assert exchange_rate.get_rates("EUR") == {"RUB": 100.0, "timestamp": "2026-08-20"}


def test_get_rates_critical_error():
    """Если сеть упала и в кэше ничего нет — возвращается None."""
    with patch("src.exchange_rate.fetch_from_api", return_value=None), \
            patch("src.exchange_rate.load_cache", return_value=None):
        assert exchange_rate.get_rates("USD") is None


# ==========================================
# Тесты математики конвертации в рубли
# ==========================================

@pytest.mark.parametrize(
    "tx, rate, currency, expected",
    [
        ({"amount": "100.50", "currency": "USD"}, 90.0, "USD", 9045.0),
        ({"amount": 50, "currency": "EUR"}, 100.0, "EUR", 5000.0),
        # Сумма в RUB возвращает исходное число, игнорируя переданный курс
        ({"amount": "1500.00", "currency": "RUB"}, 1.5, "RUB", 1500.0),
        # Если курс для не-рублей равен None, конвертация невозможна
        ({"amount": "100", "currency": "USD"}, None, "USD", None),
        # Битая сумма (текст вместо числа) приводит к возврату None
        ({"amount": "broken_str", "currency": "USD"}, 90.0, "USD", None),
        # Отсутствие поля amount приводит к возврату None
        ({"currency": "USD"}, 90.0, "USD", None),
    ]
)
def test_convert_to_rub(tx, rate, currency, expected):
    """Параметризованный тест всех математических сценариев конвертации."""
    assert exchange_rate.convert_to_rub(tx, rate, currency) == expected


# ==========================================
# Тесты для load_transactions
# ==========================================

def test_load_transactions_not_found():
    """Тест обработки ситуации, когда файла транзакций не существует."""
    with patch("os.path.exists", return_value=False):
        assert exchange_rate.load_transactions() == []


def test_load_transactions_success():
    """Тест успешного парсинга валидного списка транзакций."""
    mock_data = [{"amount": 100, "currency": "RUB"}]
    m_open = mock_open(read_data=json.dumps(mock_data))

    with patch("os.path.exists", return_value=True), patch("builtins.open", m_open):
        assert exchange_rate.load_transactions() == mock_data


def test_load_transactions_not_a_list():
    """Тест защиты структуры данных: если в JSON лежит словарь вместо списка, возвращается пустой список."""
    m_open = mock_open(read_data=json.dumps({"not_a_list": True}))

    with patch("os.path.exists", return_value=True), patch("builtins.open", m_open):
        assert exchange_rate.load_transactions() == []
