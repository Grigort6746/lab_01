import argparse
import sys

from .calculator import calculate
from .converter import convert
from .errors import ToolkitError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="toolkit",
        description="Калькулятор и конвертер величин",
    )
    # Пользователь должен выбрать одну из двух команд: calc или convert.
    subparsers = parser.add_subparsers(dest="command", required=True)

    calc_parser = subparsers.add_parser("calc", help="вычислить выражение")
    calc_parser.add_argument("expression", help="выражение в кавычках")

    convert_parser = subparsers.add_parser("convert", help="конвертировать величину")
    convert_parser.add_argument("value")
    convert_parser.add_argument("--from", dest="from_unit", required=True)
    convert_parser.add_argument("--to", dest="to_unit", required=True)

    return parser


def _format_number(value: float) -> str:
    # Для целого результата выводим 6 вместо 6.0.
    if value.is_integer():
        return str(int(value))
    return str(value)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    arguments = list(sys.argv[1:] if argv is None else argv)
    # Например, -2*-3 является выражением, хотя начинается как ключ CLI.
    if (
        len(arguments) == 2
        and arguments[0] == "calc"
        and arguments[1] not in {"-h", "--help", "--"}
    ):
        arguments.insert(1, "--")
    # argparse проверяет обязательные аргументы и обрабатывает --help.
    args = parser.parse_args(arguments)

    try:
        if args.command == "calc":
            result = calculate(args.expression)
        else:
            result = convert(args.value, args.from_unit, args.to_unit)

        print(_format_number(result))
        return 0
    except ToolkitError as exc:
        # Ошибки отправляем в отдельный поток и возвращаем код из задания.
        print(f"Ошибка: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    # Передаём системе код завершения, который вернула main().
    raise SystemExit(main())
