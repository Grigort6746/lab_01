import pytest

from toolkit.calculator import calculate
from toolkit.errors import ToolkitError


def test_priority() -> None:
    # Умножение выполняется раньше сложения.
    assert calculate("2+3*4") == 14
    assert calculate("10-3-2") == 5


def test_division() -> None:
    assert calculate("10 / 4") == 2.5


def test_negative_numbers() -> None:
    assert calculate("-2 * -3") == 6


def test_unary_signs() -> None:
    assert calculate("1+-2") == -1
    assert calculate("+2") == 2


def test_float_and_spaces() -> None:
    assert calculate(" 1.5 * 2 ") == 3


def test_empty_expression() -> None:
    # Для неверного ввода ожидаем исключение, а не число.
    with pytest.raises(ToolkitError):
        calculate("")


def test_two_operators() -> None:
    with pytest.raises(ToolkitError):
        calculate("2*/3")


def test_invalid_symbol() -> None:
    with pytest.raises(ToolkitError):
        calculate("2+a")


def test_zero_division() -> None:
    with pytest.raises(ToolkitError):
        calculate("1/0")


def test_missing_operand() -> None:
    with pytest.raises(ToolkitError):
        calculate("2+")
