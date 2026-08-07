import os
from unittest.mock import patch, MagicMock
import pytest

from src.external_api import get_rates, convert_to_rub


class TestExternalAPI:

    @patch('src.external_api.requests.get')
    def test_get_rates_success_standard_format(self, mock_get):
        """Проверяем успешный ответ API со структурой 'rates' (например, Frankfurter.app)."""

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "base": "EUR",
            "rates": {"RUB": 100.5}
        }
        mock_get.return_value = mock_response

        result = get_rates("EUR")

        assert result == {"RUB": 100.5}

    @patch('src.external_api.requests.get')
    def test_get_rates_http_error(self, mock_get):
        """Если сервер вернул 429 или 500, должна вернуться None."""
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_get.return_value = mock_response

        result = get_rates("USD")
        assert result is None

    @patch('src.external_api.requests.get')
    def test_get_rates_missing_key_in_json(self, mock_get):
        """Если в JSON нет ключей quotes/rates или RUB внутри них."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"some_other_key": 123}
        mock_get.return_value = mock_response

        result = get_rates("USD")
        assert result is None

    @patch('src.external_api.requests.get')
    def test_get_rates_network_exception(self, mock_get):
        """Сетевой сбой (таймаут, обрыв связи)."""
        mock_get.side_effect = Exception("Connection aborted")

        result = get_rates("USD")
        assert result is None

    # --- Тесты функции конвертации (без сети) ---

    def test_convert_to_rub_valid_usd(self):
        cache = {"USD": 92.0, "EUR": 100.0}
        tx = {"amount": "100", "currency": "USD"}
        assert convert_to_rub(tx, cache) == 9200.0

    def test_convert_to_rub_valid_rub(self):
        cache = {"USD": 92.0}
        tx = {"amount": "500", "currency": "RUB"}
        assert convert_to_rub(tx, cache) == 500.0

    def test_convert_to_rub_currency_not_in_cache(self):
        cache = {"USD": 92.0}
        tx = {"amount": "10", "currency": "GBP"}
        assert convert_to_rub(tx, cache) is None

    def test_convert_to_rub_invalid_amount_string(self):
        cache = {"USD": 92.0}
        tx = {"amount": "not_a_number", "currency": "USD"}
        assert convert_to_rub(tx, cache) is None

    def test_convert_to_rub_empty_tx_dict(self):
        cache = {"USD": 92.0}
        assert convert_to_rub({}, cache) is None

    def test_convert_to_rub_zero_amount(self):
        cache = {"USD": 92.0}
        tx = {"amount": "0", "currency": "USD"}
        assert convert_to_rub(tx, cache) == 0.0

API_RESPONSE_FIXER = {
    "success": True,
    "date": "2026-07-27",
    "quotes": {"USDRUB": 92.5}
}

API_RESPONSE_STANDARD = {
    "base": "USD",
    "date": "2026-07-27",
    "rates": {"RUB": 92.5}
}