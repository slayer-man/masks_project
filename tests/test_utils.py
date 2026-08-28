import json
from unittest.mock import MagicMock, mock_open, patch
import pandas as pd
import pytest
from src import utils


# ==========================================
# Тесты для load_transactions (JSON)
# ==========================================

def test_load_transactions_json_success():
    """Тест успешного чтения корректного JSON-файла."""
    mock_data = [{"id": 12345, "state": "EXECUTED"}]
    m_open = mock_open(read_data=json.dumps(mock_data))

    with patch("builtins.open", m_open):
        result = utils.load_transactions()
        assert result == mock_data


def test_load_transactions_json_file_not_found():
    """Тест ситуации, когда JSON-файл отсутствует (генерируется ошибка)."""
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = utils.load_transactions()
        assert result == []


def test_load_transactions_json_invalid_format():
    """Тест обработки исключения, если файл содержит некорректный JSON."""
    m_open = mock_open(read_data="{invalid json")

    with patch("builtins.open", m_open):
        result = utils.load_transactions()
        assert result == []


# ==========================================
# Тесты для load_csv_transactions (CSV)
# ==========================================

def test_load_csv_transactions_not_exists():
    """Тест, если CSV-файл не существует по указанному пути."""
    with patch("os.path.exists", return_value=False):
        assert utils.load_csv_transactions("dummy_path.csv") == []


def test_load_csv_transactions_success():
    """Тест успешного чтения CSV и преобразования во вложенную структуру."""
    # Сымитируем содержимое CSV-файла с разделителем ';'
    csv_content = (
        "id;state;date;description;from;to;amount;currency_name;currency_code\n"
        "1;EXECUTED;2026-08-28;Перевод;Visa;Счет;500.0;руб.;RUB\n"
    )
    m_open = mock_open(read_data=csv_content)

    with patch("os.path.exists", return_value=True), patch("builtins.open", m_open):
        result = utils.load_csv_transactions("transactions.csv")

        assert len(result) == 1
        assert result[0]["id"] == "1"
        assert result[0]["state"] == "EXECUTED"
        assert result[0]["operationAmount"]["amount"] == "500.0"
        assert result[0]["operationAmount"]["currency"]["code"] == "RUB"


def test_load_csv_transactions_exception():
    """Тест перехвата ошибок во время обработки CSV-файла."""
    with patch("os.path.exists", return_value=True), \
            patch("builtins.open", side_effect=OSError("Read error")):
        assert utils.load_csv_transactions("transactions.csv") == []


# ==========================================
# Тесты для load_xlsx_transactions (XLSX)
# ==========================================

def test_load_xlsx_transactions_not_exists():
    """Тест, если XLSX-файл не существует по указанному пути."""
    with patch("os.path.exists", return_value=False):
        assert utils.load_xlsx_transactions("dummy_path.xlsx") == []


@patch("pandas.read_excel")
def test_load_xlsx_transactions_success(mock_read_excel):
    """Тест успешного парсинга таблицы Excel (XLSX) через pandas."""
    # Создаем DataFrame, имитирующий плоскую таблицу транзакций
    mock_df = pd.DataFrame([{
        "id": 2,
        "state": "CANCELED",
        "date": "2026-08-28",
        "description": "Покупка",
        "from": "Mastercard",
        "to": "Магазин",
        "amount": 1200,
        "currency_name": "руб.",
        "currency_code": "RUB"
    }])
    mock_read_excel.return_value = mock_df

    with patch("os.path.exists", return_value=True):
        result = utils.load_xlsx_transactions("transactions.xlsx")

        assert len(result) == 1
        assert result[0]["id"] == "2"
        assert result[0]["state"] == "CANCELED"
        assert result[0]["operationAmount"]["amount"] == "1200"
        assert result[0]["operationAmount"]["currency"]["code"] == "RUB"


@patch("pandas.read_excel", side_effect=Exception("Excel parsing error"))
def test_load_xlsx_transactions_exception(mock_read_excel):
    """Тест обработки ошибок и сбоев при парсинге Excel."""
    with patch("os.path.exists", return_value=True):
        assert utils.load_xlsx_transactions("transactions.xlsx") == []
