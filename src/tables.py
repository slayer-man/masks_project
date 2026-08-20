from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent


def read_csv_to_dict(file_path: Path) -> list[dict]:
    """Считывает CSV файл и возвращает список словарей."""
    try:
        df = pd.read_csv(file_path)
        return df.to_dict(orient="records")
    except FileNotFoundError:
        return []


def read_excel_to_dict(file_path: Path) -> list[dict]:
    """Считывает Excel файл и возвращает список словарей."""
    try:
        df = pd.read_excel(file_path)
        return df.to_dict(orient="records")
    except FileNotFoundError:
        return []


# Этот блок выполнится ТОЛЬКО если запустить файл напрямую,
# но не помешает во время тестов.
if __name__ == "__main__":
    csv_path = BASE_DIR / "data" / "transactions.csv"
    excel_path = BASE_DIR / "data" / "transactions_excel.xlsx"

    print("Вывод данных из .csv файла:")
    for row in read_csv_to_dict(csv_path):
        print(row)

    print("\nВывод данных из .xlsx файла:")
    for row in read_excel_to_dict(excel_path):
        print(row)
