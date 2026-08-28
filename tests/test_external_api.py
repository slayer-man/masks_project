from unittest.mock import MagicMock, patch
import pytest
import requests
from src import external_api


@patch("requests.get")
def test_get_rates_success_rates(mock_get):
    """Тест успешного запроса, когда API возвращает структуру с ключом 'rates'."""
    # Создаем mock-ответ сервера
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "success": True,
        "base": "USD",
        "date": "2026-08-27",
        "rates": {"RUB": 91.50}
    }
    mock_get.return_value = mock_response

    # Подменяем API_KEY, чтобы тест не зависел от файла .env
    with patch("src.external_api.API_KEY", "mock_api_key"):
        result = external_api.get_rates("USD")

        # Проверяем корректность парсинга
        assert result == {"RUB": 91.50}
        # Проверяем, что requests.get вызван с правильными параметрами
        mock_get.assert_called_once_with(
            external_api.URL,
            headers={"apikey": "mock_api_key"},
            params={"base": "USD", "symbols": "RUB"},
            timeout=5
        )


@patch("requests.get")
def test_get_rates_success_quotes(mock_get):
    """Тест успешного запроса, когда API возвращает альтернативную структуру с ключом 'quotes'."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "success": True,
        "quotes": {"RUB": 99.20}
    }
    mock_get.return_value = mock_response

    with patch("src.external_api.API_KEY", "mock_api_key"):
        result = external_api.get_rates("EUR")
        assert result == {"RUB": 99.20}


def test_get_rates_no_api_key():
    """Тест ситуации, когда переменная окружения API_KEY отсутствует (None или пустая)."""
    with patch("src.external_api.API_KEY", None):
        result = external_api.get_rates("USD")
        assert result is None


@patch("requests.get")
def test_get_rates_server_error(mock_get):
    """Тест поведения функции при ошибке сервера (код ответа не 200, например 401 или 429)."""
    mock_response = MagicMock()
    mock_response.status_code = 401  # Unauthorized / Неверный ключ
    mock_get.return_value = mock_response

    with patch("src.external_api.API_KEY", "wrong_key"):
        result = external_api.get_rates("USD")
        assert result is None


@patch("requests.get")
def test_get_rates_missing_container(mock_get):
    """Тест ситуации, когда в ответе API вообще нет ни 'rates', ни 'quotes'."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"unexpected_json": True}
    mock_get.return_value = mock_response

    with patch("src.external_api.API_KEY", "mock_api_key"):
        result = external_api.get_rates("USD")
        assert result is None


@patch("requests.get")
def test_get_rates_missing_rub_key(mock_get):
    """Тест ситуации, когда контейнер валют есть, но ключа 'RUB' внутри него нет."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "rates": {"EUR": 0.85}  # Ключа RUB нет
    }
    mock_get.return_value = mock_response

    with patch("src.external_api.API_KEY", "mock_api_key"):
        result = external_api.get_rates("USD")
        assert result is None


@patch("requests.get", side_effect=requests.RequestException("Сбой сети / Timeout"))
def test_get_rates_network_exception(mock_get):
    """Тест обработки сетевых исключений (таймаут, потеря связи и т.д.)."""
    with patch("src.external_api.API_KEY", "mock_api_key"):
        # Функция должна перехватить Exception, вывести ошибку в принт и вернуть None, а не упасть
        result = external_api.get_rates("USD")
        assert result is None
