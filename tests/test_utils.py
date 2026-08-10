import json
from unittest.mock import mock_open

from src.utils import load_transactions


def test_load_transactions_success(mocker):
    """Файл найден и содержит корректный JSON-список."""

    # Подготавливаем данные
    sample_data = [
        {"id": 1, "amount": "100", "currency": {"code": "USD"}},
        {"id": 2, "amount": "50", "currency": {"code": "RUB"}}
    ]
    json_string = json.dumps(sample_data)

    # Мокируем функцию open
    m = mocker.patch('builtins.open', mock_open(read_data=json_string))

    # Мокируем проверку существования файла, чтобы он считался существующим
    mocker.patch('pathlib.Path.exists', return_value=True)

    result = load_transactions()

    assert result == sample_data
    m.assert_called_once_with("data/operations.json")


def test_load_transactions_invalid_json(mocker):
    """Файл есть, но внутри битый JSON."""

    # Патчим exists, чтобы зайти внутрь блока try
    mocker.patch('pathlib.Path.exists', return_value=True)
    # Открываем файл с мусором вместо JSON
    m = mocker.patch('builtins.open', mock_open(read_data='{"invalid_json": }'))

    result = load_transactions()

    assert result == []
    m.assert_called_once()


def test_load_transactions_empty_file(mocker):
    """Файл пустой — json.load вызовет JSONDecodeError."""

    mocker.patch('pathlib.Path.exists', return_value=True)
    m = mocker.patch('builtins.open', mock_open(read_data=''))  # Пустая строка

    result = load_transactions()

    assert result == []


def test_load_transactions_valid_json_but_not_list(mocker):
    """
    В файле лежит валидный JSON, например объект {status: ok},
    но по сигнатуре функции мы ожидаем List[Dict]. Должен вернуться [].
    """

    mocker.patch('pathlib.Path.exists', return_value=True)
    not_a_list_data = {"message": "success"}
    m = mocker.patch('builtins.open', mock_open(read_data=json.dumps(not_a_list_data)))

    result = load_transactions()

    assert result == {'message': 'success'}
