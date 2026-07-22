import datetime
import traceback
from functools import wraps
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable[[Callable], Callable]:
    """
    Декоратор для логирования вызова функций,
    их результатов и исключений.
    """

    def write(msg: str, current_filename: str | None) -> None:
        """Вспомогательная функция записи сообщения в файл или консоль."""

        if current_filename:
            with open(current_filename, "a", encoding="utf-8") as file:
                file.write(msg + "\n")
        else:
            print(msg)

    def decorator(func):
        """Внутренний декоратор, оборачивающий целевую функцию."""

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """Обертка, фиксирующая жизненный цикл выполнения функции."""

            tme = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Передаем конкретный filename сюда
            write(f"[{tme}] Функция '{func.__name__}' вызвана.", filename)

            try:
                res = func(*args, **kwargs)
                write(f"[{tme}] Функция '{func.__name__}' вернула: {repr(res)}", filename)
                return res
            except Exception as error:
                err_tme = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # И обязательно сюда, чтобы ошибка ушла в нужный файл
                write(
                    f"[{err_tme}] Ошибка в '{func.__name__}': {type(error).__name__}: {error}\n"
                    f"Аргументы: {args}, {kwargs}\n{traceback.format_exc()}",
                    filename,
                )
                raise

        return wrapper

    return decorator


# --- Примеры использования ---


# Логирование в файл
@log(filename="log.txt")
def my_function(x: int, y: int) -> int:
    """Функция складывающая два числа"""
    return x + y


print("Результат my_function:", my_function(10, 5))

try:
    my_function(5, "A")
except TypeError:
    pass


# Логирование в консоль
@log()
def multiply(a: int, b: int) -> int:
    return a + b


print("Результат multiply:", multiply(5, 2))

# Теперь эта ошибка будет записана ТОЛЬКО в консоль,
# так как у данного экземпляра декоратора filename равен None
try:
    multiply(5, "A")
except TypeError:
    pass
