from math import isfinite

from .errors import ToolkitError

OPERATORS = {"+", "-", "*", "/"}


def tokenize(expression: str) -> list[str]:
    """Разбить строку на числа без знака и отдельные операторы."""
    if not expression.strip():
        raise ToolkitError("Пустое выражение")

    tokens: list[str] = []
    i = 0

    while i < len(expression):
        char = expression[i]

        # Пропускаем пробелы между числами и знаками операций.
        if char.isspace():
            i += 1
            continue

        if char in OPERATORS:
            tokens.append(char)
            i += 1
            continue

        if char in "0123456789.":
            start = i
            dots = 0

            # Читаем число целиком, пока идут цифры или точка.
            while i < len(expression) and (expression[i] in "0123456789."):
                if expression[i] == ".":
                    dots += 1
                i += 1

            number = expression[start:i]
            if dots > 1 or number == ".":
                raise ToolkitError(f"Неверное число: {number}")

            tokens.append(number)
            continue

        raise ToolkitError(f"Недопустимый символ: {char}")

    return tokens


def validate(tokens: list[str]) -> None:
    """Проверить чередование чисел и операций, разрешая один унарный знак."""
    if not tokens:
        raise ToolkitError("Пустое выражение")

    # В начале выражения нужно число, а после числа — операция.
    expecting_number = True
    i = 0

    while i < len(tokens):
        token = tokens[i]

        if expecting_number:
            # В этой позиции плюс или минус относится к следующему числу.
            if token in {"+", "-"}:
                i += 1
                if i >= len(tokens) or tokens[i] in OPERATORS:
                    raise ToolkitError("Пропущен операнд")
                token = tokens[i]

            if token in OPERATORS:
                raise ToolkitError("Два оператора подряд")

            try:
                number = float(token)
            except ValueError as exc:
                raise ToolkitError(f"Неверное число: {token}") from exc
            if not isfinite(number):
                raise ToolkitError("Число должно быть конечным")

            expecting_number = False
        else:
            if token not in OPERATORS:
                raise ToolkitError("Пропущен оператор")
            expecting_number = True

        i += 1

    # Если после последней операции числа нет, выражение не закончено.
    if expecting_number:
        raise ToolkitError("Пропущен операнд")


def _split_expression(tokens: list[str]) -> tuple[list[float], list[str]]:
    """Объединить унарные знаки с числами после проверки токенов."""
    numbers: list[float] = []
    operators: list[str] = []
    i = 0
    expecting_number = True

    while i < len(tokens):
        if expecting_number:
            sign = 1.0
            if tokens[i] == "+":
                i += 1
            elif tokens[i] == "-":
                sign = -1.0
                i += 1

            # Сохраняем число уже с его знаком.
            numbers.append(sign * float(tokens[i]))
            expecting_number = False
        else:
            operators.append(tokens[i])
            expecting_number = True

        i += 1

    return numbers, operators


def calculate_tokens(tokens: list[str]) -> float:
    """Проверить токены и вычислить результат с учётом приоритета."""
    validate(tokens)
    numbers, operators = _split_expression(tokens)

    values = [numbers[0]]
    low_priority: list[str] = []

    # Сначала считаем умножение и деление, а сложение и вычитание оставляем.
    for operator, number in zip(operators, numbers[1:]):
        if operator == "*":
            values[-1] *= number
        elif operator == "/":
            if number == 0:
                raise ToolkitError("Деление на ноль")
            values[-1] /= number
        else:
            # Новое слагаемое может содержать свои умножения или деления.
            values.append(number)
            low_priority.append(operator)

        if not isfinite(values[-1]):
            raise ToolkitError("Результат выходит за диапазон float")

    # Теперь остались только сложение и вычитание. Идём слева направо.
    result = values[0]
    for operator, number in zip(low_priority, values[1:]):
        if operator == "+":
            result += number
        else:
            result -= number
        if not isfinite(result):
            raise ToolkitError("Результат выходит за диапазон float")

    return result


def calculate(expression: str) -> float:
    """Вычислить выражение без ввода с клавиатуры и вывода на экран."""
    tokens = tokenize(expression)
    return calculate_tokens(tokens)
