"""Entrada CLI: REPL interativo ou execução de arquivo."""

import sys

from minipy.errors import MiniPyError
from minipy.interpreter import Interpreter
from minipy.lexer import Lexer
from minipy.parser import Parser


def _run_source(source: str, interp: Interpreter) -> None:
    tokens = Lexer(source).tokenize()
    program = Parser(tokens).parse()
    interp.interpret(program)


def run_file(path: str) -> int:
    with open(path, encoding="utf-8") as f:
        source = f.read()
    interp = Interpreter()
    try:
        _run_source(source, interp)
    except MiniPyError as e:
        print(e, file=sys.stderr)
        return 1
    return 0


def repl() -> int:
    interp = Interpreter()
    print("minipy REPL — Ctrl-D para sair")
    while True:
        try:
            line = input(">>> ")
        except EOFError:
            print()
            return 0
        except KeyboardInterrupt:
            print()
            continue
        if not line.strip():
            continue
        try:
            _run_source(line + "\n", interp)
        except MiniPyError as e:
            print(e, file=sys.stderr)
        except Exception as e:  # noqa: BLE001
            print(f"erro: {e}", file=sys.stderr)


def main() -> int:
    if len(sys.argv) > 1:
        return run_file(sys.argv[1])
    return repl()


if __name__ == "__main__":
    sys.exit(main())
