# Лабораторная работа 1

Калькулятор и конвертер величин.

Калькулятор поддерживает `+`, `-`, `*`, `/`, дробные числа и унарные знаки.
Скобки не поддерживаются.

Единицы конвертера: `mm`, `cm`, `m`, `km`, `g`, `kg`, `c`, `f`, `k`.

## Установка

Команды для PowerShell из папки проекта:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

## Запуск

```powershell
.\.venv\Scripts\python.exe -m toolkit --help
.\.venv\Scripts\python.exe -m toolkit calc "2+3*4"
.\.venv\Scripts\python.exe -m toolkit convert 1000 --from mm --to m
```

При успехе код завершения — `0`, при ошибке — `2`. Ошибки выводятся в `stderr`.

## Проверка

```powershell
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\ruff.exe check .
```
