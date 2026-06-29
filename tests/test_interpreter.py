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


def test_float_operations():
    assert value_of("x = 1.5 + 2.5\n", "x") == 4.0
    assert value_of("x = 10.0 - 3.5\n", "x") == 6.5


def test_boolean_true_false():
    assert value_of("x = True\n", "x") is True
    assert value_of("x = False\n", "x") is False


def test_none_value():
    assert value_of("x = None\n", "x") is None


def test_multiple_statements():
    src = "a = 1\nb = 2\nc = a + b\n"
    assert value_of(src, "c") == 3


def test_function_with_multiple_arguments():
    src = (
        "def add_three(a, b, c):\n"
        "    return a + b + c\n"
        "result = add_three(1, 2, 3)\n"
    )
    assert value_of(src, "result") == 6


def test_nested_function_calls():
    src = (
        "def double(x):\n"
        "    return x * 2\n"
        "def quadruple(x):\n"
        "    return double(double(x))\n"
        "result = quadruple(5)\n"
    )
    assert value_of(src, "result") == 20


def test_variable_shadowing():
    src = (
        "x = 10\n"
        "def f():\n"
        "    x = 20\n"
        "    return x\n"
        "result = f()\n"
    )
    assert value_of(src, "result") == 20
    assert value_of(src, "x") == 10


def test_string_operations():
    src = 'x = "hello" + " " + "world"\n'
    assert value_of(src, "x") == "hello world"


def test_string_length():
    assert value_of('x = len("python")\n', "x") == 6


def test_integer_conversion():
    assert value_of('x = int("123")\n', "x") == 123


def test_float_conversion():
    result = value_of('x = float("3.14")\n', "x")
    assert abs(result - 3.14) < 0.0001


def test_string_conversion():
    assert value_of("x = str(42)\n", "x") == "42"


def test_boolean_conversion():
    assert value_of("x = bool(1)\n", "x") is True
    assert value_of("x = bool(0)\n", "x") is False


def test_modulo_operation():
    assert value_of("x = 10 % 3\n", "x") == 1


def test_power_operation():
    assert value_of("x = 2 ** 10\n", "x") == 1024


def test_negative_number_operations():
    assert value_of("x = -5 + 10\n", "x") == 5
    assert value_of("x = 5 + (-3)\n", "x") == 2


def test_comparison_chain():
    assert value_of("x = 1 < 2 and 2 < 3\n", "x") is True


def test_logical_or():
    assert value_of("x = False or True\n", "x") is True
    assert value_of("x = False or False\n", "x") is False


def test_not_operator():
    assert value_of("x = not True\n", "x") is False
    assert value_of("x = not False\n", "x") is True


def test_while_increment():
    src = (
        "count = 0\n"
        "while count < 10:\n"
        "    count = count + 1\n"
    )
    assert value_of(src, "count") == 10


def test_nested_while():
    src = (
        "i = 0\n"
        "total = 0\n"
        "while i < 3:\n"
        "    j = 0\n"
        "    while j < 4:\n"
        "        total = total + 1\n"
        "        j = j + 1\n"
        "    i = i + 1\n"
    )
    assert value_of(src, "total") == 12


def test_if_true_condition():
    src = (
        "x = 0\n"
        "if True:\n"
        "    x = 1\n"
    )
    assert value_of(src, "x") == 1


def test_if_false_condition():
    src = (
        "x = 0\n"
        "if False:\n"
        "    x = 1\n"
    )
    assert value_of(src, "x") == 0


def test_if_else_condition_true():
    src = (
        "x = 0\n"
        "if 5 > 3:\n"
        "    x = 1\n"
        "else:\n"
        "    x = 2\n"
    )
    assert value_of(src, "x") == 1


def test_if_else_condition_false():
    src = (
        "x = 0\n"
        "if 2 > 5:\n"
        "    x = 1\n"
        "else:\n"
        "    x = 2\n"
    )
    assert value_of(src, "x") == 2


def test_factorial_recursive():
    src = (
        "def fac(n):\n"
        "    if n <= 1:\n"
        "        return 1\n"
        "    return n * fac(n - 1)\n"
        "result = fac(6)\n"
    )
    assert value_of(src, "result") == 720


def test_function_returns_none():
    src = (
        "def no_return():\n"
        "    x = 42\n"
        "result = no_return()\n"
    )
    assert value_of(src, "result") is None


def test_function_with_local_and_global():
    src = (
        "global_var = 100\n"
        "def f():\n"
        "    return global_var + 50\n"
        "result = f()\n"
    )
    assert value_of(src, "result") == 150


def test_function_redefinition():
    src = (
        "def f():\n"
        "    return 1\n"
        "def f():\n"
        "    return 2\n"
        "result = f()\n"
    )
    assert value_of(src, "result") == 2


def test_wrong_argument_count():
    src = (
        "def f(a, b):\n"
        "    return a + b\n"
        "x = f(1)\n"
    )
    with pytest.raises(RuntimeMiniPyError):
        run(src)


def test_division_by_zero_error():
    with pytest.raises(RuntimeMiniPyError):
        run("x = 1 / 0\n")


def test_undefined_variable_error():
    with pytest.raises(RuntimeMiniPyError):
        run("x = undefined\n")


def test_call_non_callable_error():
    with pytest.raises(RuntimeMiniPyError):
        run("x = 42()\n")
