from src.widget import get_date
import pytest

@pytest.mark.parametrize(
    "date_string, expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),   # Базовый ISO
        ("2026-07-03", "03.07.2026"),                   # Базовый ISO
        ("2026-07-03T12:30:00", "03.07.2026"),          # ISO с временем
        ("2026-01-01T00:00:00Z", "01.01.2026"),         # ISO с UTC

    ]
)
def test_get_date(date_string, expected):
    assert get_date(date_string) == expected

def test_get_date_invalid_format():
    # Проверяем, что некорректная строка вызывает ошибку
    with pytest.raises(ValueError):
        get_date("не-дата")
