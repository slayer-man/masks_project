from pathlib import Path
import pytest
from src.decorators import log


def test_successful_call_logs_to_file(tmp_path: Path) -> None:
    """Проверяем запись успешного вызова в файл."""

    # Создаем временный путь к файлу
    log_file = tmp_path / "success.log"

    @log(filename=str(log_file))
    def add(a: int, b: int) -> int:
        return a + b

    result = add(10, 20)
    assert result == 30

    content = log_file.read_text(encoding="utf-8")
    assert "Функция 'add' вызвана" in content
    assert "Функция 'add' вернула: 30" in content
    assert "Ошибка" not in content


def test_console_logging_without_filename(capsys: pytest.CaptureFixture[str]) -> None:
    """Проверяем вывод в консоль через фикстуру capsys."""

    @log()
    def greet(name: str) -> str:
        return f"Привет, {name}"

    result = greet("Алексей")
    captured = capsys.readouterr()

    assert result == "Привет, Алексей"
    # В stdout попадает то, что было напечатано функцией write -> print
    assert "Функция 'greet' вызвана" in captured.out
    assert "Функция 'greet' вернула: 'Привет, Алексей'" in captured.out


def test_multiple_calls_append_to_file(tmp_path: Path) -> None:
    """Проверяем режим дозаписи ('a'), а не перезаписи файла."""

    log_file = tmp_path / "append.log"

    @log(filename=str(log_file))
    def identity(x: int) -> int:
        return x

    identity(1)
    identity(2)

    lines = log_file.read_text(encoding="utf-8").splitlines()

    # Ищем строки с результатами
    results = [line for line in lines if "вернула" in line]
    assert len(results) == 2
    assert "1" in results[0]
    assert "2" in results[1]


def test_preserves_function_metadata() -> None:
    """Проверяем работу wraps."""

    @log()
    def documented_func() -> None:
        """Важная документация функции."""
        pass

    assert documented_func.__name__ == "documented_func"
    assert documented_func.__doc__ == "Важная документация функции."
