from pathlib import Path
from unittest.mock import patch
import pandas as pd
import pytest
from src.tables import read_csv_to_dict, read_excel_to_dict
import sys
import runpy



@pytest.fixture
def sample_data():
    """Фикстура с тестовыми данными."""
    return [
        {"id": 1, "amount": 100, "status": "EXECUTED"},
        {"id": 2, "amount": 200, "status": "PENDING"},
    ]


# 1. Тесты для успешного чтения функций
@patch("pandas.read_csv")
def test_read_csv_to_dict_success(mock_read_csv, sample_data):
    """Тест успешного чтения CSV файла."""
    mock_read_csv.return_value = pd.DataFrame(sample_data)
    result = read_csv_to_dict(Path("fake_path.csv"))
    assert result == sample_data


@patch("pandas.read_excel")
def test_read_excel_to_dict_success(mock_read_excel, sample_data):
    """Тест успешного чтения Excel файла."""
    mock_read_excel.return_value = pd.DataFrame(sample_data)
    result = read_excel_to_dict(Path("fake_path.xlsx"))
    assert result == sample_data


# 2. Тесты для обработки ошибок (когда файлов нет)
@patch("pandas.read_csv")
def test_read_csv_file_not_found(mock_read_csv):
    """Тест: CSV файл не найден."""
    mock_read_csv.side_effect = FileNotFoundError
    result = read_csv_to_dict(Path("missing.csv"))
    assert result == []


@patch("pandas.read_excel")
def test_read_excel_file_not_found(mock_read_excel):
    """Тест: Excel файл не найден."""
    mock_read_excel.side_effect = FileNotFoundError
    result = read_excel_to_dict(Path("missing.xlsx"))
    assert result == []


# 3. Тест для блока __main__
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

    # 2. Находим путь к файлу src/tables.py
    current_dir = Path(__file__).resolve().parent
    tables_script_path = current_dir.parent / "src" / "tables.py"

    # 3. Убираем модуль из кэша Python, чтобы run_path выполнил его как новый файл
    # Это полностью убирает предупреждение RuntimeWarning
    if "src.tables" in sys.modules:
        del sys.modules["src.tables"]

    # 4. Запускаем файл по его пути, имитируя __main__
    runpy.run_path(str(tables_script_path), run_name="__main__")

    # 5. Перехватываем текст, который ушел в print()
    captured = capsys.readouterr()

    # 6. Проверяем заголовки и сами данные в выводе
    assert "Вывод данных из .csv файла:" in captured.out
    assert "{'id': 123, 'status': 'CSV_DATA'}" in captured.out

    assert "Вывод данных из .xlsx файла:" in captured.out
    assert "{'id': 456, 'status': 'EXCEL_DATA'}" in captured.out
