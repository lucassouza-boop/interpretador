import pytest

from minipy.errors import RuntimeMiniPyError
from minipy.interpreter import Interpreter
from minipy.lexer import Lexer
from minipy.parser import Parser


def run(source: str) -> Interpreter:
    tokens = Lexer(source).tokenize()
    program = Parser(tokens).parse()
    interp = Interpreter()
    interp.interpret(program)
    return interp


def value_of(source: str, name: str):
    return run(source).globals.get(name)


def test_arithmetic_precedence():
    assert value_of("x = 1 + 2 * 3\n", "x") == 7


def test_power_right_assoc():
    assert value_of("x = 2 ** 3 ** 2\n", "x") == 512


def test_unary_minus():
    assert value_of("x = -5 + 2\n", "x") == -3


def test_comparison_and_logic():
    assert value_of("x = 1 < 2 and 3 >= 3\n", "x") is True
    assert value_of("x = not (1 == 1)\n", "x") is False


def test_if_elif_else():
    src = "n = 5\nif n < 0:\n    s = -1\nelif n == 0:\n    s = 0\nelse:\n    s = 1\n"
    assert value_of(src, "s") == 1


def test_while_loop():
    src = "i = 0\ntotal = 0\nwhile i < 5:\n    total = total + i\n    i = i + 1\n"
    assert value_of(src, "total") == 10


def test_function_recursion():
    src = (
        "def fib(n):\n"
        "    if n < 2:\n"
        "        return n\n"
        "    return fib(n - 1) + fib(n - 2)\n"
        "r = fib(10)\n"
    )
    assert value_of(src, "r") == 55


def test_closure_scope():
    src = (
        "def make_adder(x):\n"
        "    def adder(y):\n"
        "        return x + y\n"
        "    return adder\n"
        "add5 = make_adder(5)\n"
        "r = add5(3)\n"
    )
    assert value_of(src, "r") == 8


def test_string_concat_and_builtins():
    assert value_of('x = "ab" + "cd"\n', "x") == "abcd"
    assert value_of('x = len("hello")\n', "x") == 5
    assert value_of('x = int("42") + 1\n', "x") == 43


def test_division_by_zero():
    with pytest.raises(RuntimeMiniPyError):
        run("x = 1 / 0\n")


def test_undefined_name():
    with pytest.raises(RuntimeMiniPyError):
        run("x = y + 1\n")
