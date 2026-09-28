import pytest

from toolkit.converter import convert
from toolkit.errors import ToolkitError


def test_length() -> None:
    result = convert(1000, "mm", "m")
    assert result == 1.0
    assert isinstance(result, float)


def test_mass() -> None:
    assert convert(1.5, "kg", "g") == 1500.0


def test_celsius_to_fahrenheit() -> None:
    assert convert(0, "c", "f") == 32.0


def test_absolute_zero() -> None:
    # При расчётах с float допускаем небольшую погрешность.
    assert convert(-273.15, "c", "k") == pytest.approx(0.0)


def test_uppercase_units() -> None:
    assert convert(2, "KM", "M") == 2000.0


def test_below_absolute_zero() -> None:
    with pytest.raises(ToolkitError):
        convert(-274, "c", "k")


def test_incompatible_units() -> None:
    with pytest.raises(ToolkitError):
        convert(1, "kg", "m")


def test_unknown_unit() -> None:
    with pytest.raises(ToolkitError):
        convert(1, "inch", "m")
