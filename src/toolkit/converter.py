from math import isfinite

from .errors import ToolkitError

# Сколько метров содержится в одной единице длины.
LENGTH = {
    "mm": 0.001,
    "cm": 0.01,
    "m": 1.0,
    "km": 1000.0,
}

# Для массы за основу берём грамм.
MASS = {
    "g": 1.0,
    "kg": 1000.0,
}

ABSOLUTE_ZERO = {"c": -273.15, "f": -459.67, "k": 0.0}


def _group(unit: str) -> str | None:
    if unit in LENGTH:
        return "length"
    if unit in MASS:
        return "mass"
    if unit in ABSOLUTE_ZERO:
        return "temperature"
    return None


def _to_celsius(value: float, unit: str) -> float:
    # Сначала переводим исходную температуру в градусы Цельсия.
    if unit == "c":
        return value
    if unit == "f":
        return (value - 32) * 5 / 9
    return value - 273.15


def _from_celsius(value: float, unit: str) -> float:
    # Затем из градусов Цельсия получаем нужную шкалу.
    if unit == "c":
        return value
    if unit == "f":
        return value * 9 / 5 + 32
    return value + 273.15


def convert(value: float | str, from_unit: str, to_unit: str) -> float:
    """Перевести конечное число между единицами одной группы."""
    # CLI передаёт строку, поэтому проверяем, можно ли получить из неё число.
    try:
        value = float(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ToolkitError("Неверное числовое значение") from exc
    if not isfinite(value):
        raise ToolkitError("Неверное числовое значение: требуется конечное число")

    # Например, KM и km должны обозначать одну единицу.
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()

    from_group = _group(from_unit)
    to_group = _group(to_unit)

    if from_group is None:
        raise ToolkitError(f"Неизвестная единица: {from_unit}")
    if to_group is None:
        raise ToolkitError(f"Неизвестная единица: {to_unit}")
    # Нельзя перевести массу в длину или температуру.
    if from_group != to_group:
        raise ToolkitError("Несовместимые единицы")

    if from_group == "temperature":
        # Сравниваем с границей в той шкале, которую ввёл пользователь.
        if value < ABSOLUTE_ZERO[from_unit]:
            raise ToolkitError("Температура ниже абсолютного нуля")
        # Точную границу переводим без накопления погрешности в формулах.
        if value == ABSOLUTE_ZERO[from_unit]:
            return ABSOLUTE_ZERO[to_unit]

    if from_unit == to_unit:
        return value

    # Отношение коэффициентов показывает, во сколько раз меняется число.
    if from_group == "length":
        result = value * (LENGTH[from_unit] / LENGTH[to_unit])
    elif from_group == "mass":
        result = value * (MASS[from_unit] / MASS[to_unit])
    else:
        celsius = _to_celsius(value, from_unit)
        result = _from_celsius(celsius, to_unit)

    if not isfinite(result):
        raise ToolkitError("Результат выходит за диапазон float")
    return float(result)
