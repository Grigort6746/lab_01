import os
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def run_toolkit(*args: str) -> subprocess.CompletedProcess[str]:
    # Передаём процессу путь к пакету и кодировку для русских сообщений.
    env = os.environ.copy()
    env["PYTHONPATH"] = str(PROJECT_ROOT / "src")
    env["PYTHONIOENCODING"] = "utf-8"

    return subprocess.run(
        [sys.executable, "-m", "toolkit", *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
        env=env,
        cwd=PROJECT_ROOT,
        timeout=10,
    )


def test_help() -> None:
    result = run_toolkit("--help")
    assert result.returncode == 0
    assert "Калькулятор" in result.stdout
    assert result.stderr == ""


def test_calc_cli() -> None:
    # Минус в начале выражения не должен считаться ключом команды.
    result = run_toolkit("calc", "-2*-3")
    assert result.returncode == 0
    assert result.stdout.strip() == "6"
    assert result.stderr == ""


def test_convert_cli() -> None:
    result = run_toolkit("convert", "1000", "--from", "mm", "--to", "m")
    assert result.returncode == 0
    assert result.stdout.strip() == "1"
    assert result.stderr == ""


def test_convert_bad_number() -> None:
    result = run_toolkit("convert", "abc", "--from", "m", "--to", "cm")
    assert result.returncode == 2
    assert "Неверное числовое значение" in result.stderr
    assert result.stdout == ""
