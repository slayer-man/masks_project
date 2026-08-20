# tests/test_tables.py
from pathlib import Path
from unittest.mock import patch
import pandas as pd
import pytest
from src.tables import read_csv_to_dict, read_excel_to_dict


@pytest.fixture
def sample_data():
    """Фикстура с тестовыми данными."""
    return [
        {"id": 1, "amount": 100, "status": "EXECUTED"},
        {"id": 2, "amount": 200, "status": "PENDING"},
    ]


@patch("pandas.read_csv")
def test_read_csv_to_dict(mock_read_csv, sample_data):
    """Тест успешного чтения CSV файла."""
    mock_read_csv.return_value = pd.DataFrame(sample_data)
    result = read_csv_to_dict(Path("fake_path.csv"))
    assert result == sample_data


@patch("pandas.read_excel")
def test_read_excel_to_dict(mock_read_excel, sample_data):
    """Тест успешного чтения Excel файла."""
    mock_read_excel.return_value = pd.DataFrame(sample_data)
    result = read_excel_to_dict(Path("fake_path.xlsx"))
    assert result == sample_data


def test_read_csv_file_not_found():
    """Тест поведения функции, если CSV файл отсутствует."""
    result = read_csv_to_dict(Path("non_existent_file.csv"))
    assert result == []


def test_read_excel_file_not_found():
    """Тест поведения функции, если Excel файл отсутствует."""
    result = read_excel_to_dict(Path("non_existent_file.xlsx"))
    assert result == []


# === ВСТАВЛЯЙТЕ НОВЫЙ ТЕСТ СЮДА (В САМЫЙ КОНЕЦ) ===


@patch("pandas.read_excel")
@patch("pandas.read_csv")
def test_main_block_output(mock_read_csv, mock_read_excel, capsys):
    """Тестирует вывод на экран при прямом запуске файла tables.py."""

    # 1. Готовим фейковые DataFrame для pandas
    mock_read_csv.return_value = pd.DataFrame(
        [{"id": 123, "status": "CSV_DATA"}]
    )
    mock_read_excel.return_value = pd.DataFrame(
        [{"id": 456, "status": "EXCEL_DATA"}]
    )

    # 2. Находим путь к файлу tables.py относительно файла теста
    current_dir = Path(__file__).resolve().parent
    tables_script_path = current_dir.parent / "src" / "tables.py"

    # 3. Читаем код файла и выполняем его в контексте главного скрипта
    with open(tables_script_path, "r", encoding="utf-8") as file:
        code = file.read()

    # Запускаем код, имитируя __main__
    global_context = {"__name__": "__main__", "__file__": str(tables_script_path)}
    exec(code, global_context)

    # 4. Перехватываем текст из консоли
    captured = capsys.readouterr()

    # 5. Проверяем, что print() вывел всё правильно
    assert "Вывод данных из .csv файла:" in captured.out
    assert "{'id': 123, 'status': 'CSV_DATA'}" in captured.out

    assert "Вывод данных из .xlsx файла:" in captured.out
    assert "{'id': 456, 'status': 'EXCEL_DATA'}" in captured.out
