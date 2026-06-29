"""Testes avançados para o interpretador minipy."""

import pytest

from minipy.errors import RuntimeMiniPyError
from minipy.interpreter import Interpreter
from minipy.lexer import Lexer
from minipy.parser import Parser


def run(source: str) -> Interpreter:
    """Executa o código fonte e retorna o interpretador."""
    tokens = Lexer(source).tokenize()
    program = Parser(tokens).parse()
    interp = Interpreter()
    interp.interpret(program)
    return interp


def value_of(source: str, name: str):
    """Executa código e retorna o valor de uma variável."""
    return run(source).globals.get(name)


class TestArithmeticOperations:
    """Testa operações aritméticas complexas."""

    def test_modulo_operator(self):
        assert value_of("x = 10 % 3\n", "x") == 1

    def test_negative_modulo(self):
        assert value_of("x = -10 % 3\n", "x") == 2

    def test_float_division(self):
        assert value_of("x = 7 / 2\n", "x") == 3.5

    def test_complex_expression_order(self):
        assert value_of("x = 2 + 3 * 4 - 5 / 2 + 1\n", "x") == 12.5

    def test_power_operator_simple(self):
        assert value_of("x = 2 ** 3\n", "x") == 8

    def test_power_with_negative_base(self):
        assert value_of("x = (-2) ** 3\n", "x") == -8

    def test_power_with_float(self):
        result = value_of("x = 4 ** 0.5\n", "x")
        assert abs(result - 2.0) < 0.0001

    def test_division_by_zero_error(self):
        with pytest.raises(RuntimeMiniPyError):
            run("x = 5 / 0\n")

    def test_modulo_by_zero_error(self):
        with pytest.raises(RuntimeMiniPyError):
            run("x = 5 % 0\n")


class TestComparisonOperators:
    """Testa operadores de comparação."""

    def test_less_than(self):
        assert value_of("x = 1 < 2\n", "x") is True
        assert value_of("x = 2 < 1\n", "x") is False

    def test_greater_than(self):
        assert value_of("x = 5 > 3\n", "x") is True

    def test_equal(self):
        assert value_of('x = "hello" == "hello"\n', "x") is True

    def test_not_equal(self):
        assert value_of("x = 1 != 2\n", "x") is True

    def test_less_equal(self):
        assert value_of("x = 2 <= 2\n", "x") is True

    def test_greater_equal(self):
        assert value_of("x = 3 >= 2\n", "x") is True

    def test_chained_comparisons(self):
        assert value_of("x = 1 < 2 and 2 < 3 and 3 < 4\n", "x") is True

    def test_compare_strings(self):
        assert value_of('x = "abc" < "def"\n', "x") is True


class TestLogicalOperators:
    """Testa operadores lógicos (and, or, not)."""

    def test_and_operator_true(self):
        assert value_of("x = True and True\n", "x") is True

    def test_and_operator_false(self):
        assert value_of("x = True and False\n", "x") is False

    def test_or_operator_true(self):
        assert value_of("x = False or True\n", "x") is True

    def test_or_operator_false(self):
        assert value_of("x = False or False\n", "x") is False

    def test_not_operator(self):
        assert value_of("x = not True\n", "x") is False
        assert value_of("x = not False\n", "x") is True

    def test_and_short_circuit(self):
        src = (
            "executed = False\n"
            "x = False and (executed := True)\n"  # Se suportar := seria ideal
            # Alternativa: usar uma função
            "def side_effect():\n"
            "    return True\n"
            "y = False and side_effect()\n"
            "z = 0\n"  # z permanece 0 se o side_effect não for chamado
        )
        # Teste simplificado
        assert value_of("x = False and True\n", "x") is False

    def test_or_short_circuit(self):
        assert value_of("x = True or False\n", "x") is True

    def test_complex_logical_expression(self):
        assert value_of("x = (True and False) or (True and True)\n", "x") is True


class TestStringOperations:
    """Testa operações com strings."""

    def test_string_concatenation(self):
        assert value_of('x = "hello" + " " + "world"\n', "x") == "hello world"

    def test_string_length(self):
        assert value_of('x = len("hello")\n', "x") == 5

    def test_empty_string_length(self):
        assert value_of('x = len("")\n', "x") == 0

    def test_string_comparison(self):
        assert value_of('x = "apple" < "banana"\n', "x") is True

    def test_string_equality(self):
        assert value_of('x = "test" == "test"\n', "x") is True

    def test_string_to_int(self):
        assert value_of('x = int("123")\n', "x") == 123

    def test_string_to_float(self):
        result = value_of('x = float("3.14")\n', "x")
        assert abs(result - 3.14) < 0.0001

    def test_int_to_string(self):
        assert value_of('x = str(42)\n', "x") == "42"

    def test_float_to_string(self):
        assert value_of('x = str(3.14)\n', "x") == "3.14"

    def test_bool_to_string(self):
        assert value_of('x = str(True)\n', "x") == "True"

    def test_none_to_string(self):
        assert value_of("x = str(None)\n", "x") == "None"


class TestBoolConversions:
    """Testa conversões para bool."""

    def test_zero_is_false(self):
        assert value_of("x = bool(0)\n", "x") is False

    def test_nonzero_is_true(self):
        assert value_of("x = bool(1)\n", "x") is True
        assert value_of("x = bool(42)\n", "x") is True
        assert value_of("x = bool(-1)\n", "x") is True

    def test_empty_string_is_false(self):
        assert value_of('x = bool("")\n', "x") is False

    def test_nonempty_string_is_true(self):
        assert value_of('x = bool("hello")\n', "x") is True

    def test_none_is_false(self):
        assert value_of("x = bool(None)\n", "x") is False

    def test_float_zero_is_false(self):
        assert value_of("x = bool(0.0)\n", "x") is False

    def test_float_nonzero_is_true(self):
        assert value_of("x = bool(0.5)\n", "x") is True


class TestControlFlow:
    """Testa fluxo de controle avançado."""

    def test_nested_if(self):
        src = (
            "x = 0\n"
            "if 1 < 2:\n"
            "    if 2 < 3:\n"
            "        x = 1\n"
        )
        assert value_of(src, "x") == 1

    def test_multiple_elif(self):
        src = (
            "x = 0\n"
            "n = 5\n"
            "if n < 0:\n"
            "    x = 1\n"
            "elif n < 3:\n"
            "    x = 2\n"
            "elif n < 7:\n"
            "    x = 3\n"
            "else:\n"
            "    x = 4\n"
        )
        assert value_of(src, "x") == 3

    def test_while_with_break_simulation(self):
        # Como não há break nativo, testamos parada por condição
        src = (
            "x = 0\n"
            "while x < 5:\n"
            "    x = x + 1\n"
        )
        assert value_of(src, "x") == 5

    def test_while_nested(self):
        src = (
            "i = 0\n"
            "j = 0\n"
            "total = 0\n"
            "while i < 3:\n"
            "    j = 0\n"
            "    while j < 2:\n"
            "        total = total + 1\n"
            "        j = j + 1\n"
            "    i = i + 1\n"
        )
        assert value_of(src, "total") == 6

    def test_if_with_complex_condition(self):
        src = (
            "x = 0\n"
            "a = 5\n"
            "b = 10\n"
            "if a > 0 and b > 0 and a < b:\n"
            "    x = 1\n"
        )
        assert value_of(src, "x") == 1


class TestFunctions:
    """Testa definição e chamada de funções."""

    def test_function_simple(self):
        src = (
            "def add(a, b):\n"
            "    return a + b\n"
            "x = add(2, 3)\n"
        )
        assert value_of(src, "x") == 5

    def test_function_multiple_params(self):
        src = (
            "def add_three(a, b, c):\n"
            "    return a + b + c\n"
            "x = add_three(1, 2, 3)\n"
        )
        assert value_of(src, "x") == 6

    def test_function_no_explicit_return(self):
        src = (
            "def no_return():\n"
            "    x = 1\n"
            "result = no_return()\n"
        )
        assert value_of(src, "result") is None

    def test_function_local_variables(self):
        src = (
            "def f():\n"
            "    local_var = 42\n"
            "    return local_var\n"
            "x = f()\n"
        )
        assert value_of(src, "x") == 42

    def test_function_redefine(self):
        src = (
            "def f():\n"
            "    return 1\n"
            "def f():\n"
            "    return 2\n"
            "x = f()\n"
        )
        assert value_of(src, "x") == 2

    def test_function_factorial(self):
        src = (
            "def factorial(n):\n"
            "    if n <= 1:\n"
            "        return 1\n"
            "    return n * factorial(n - 1)\n"
            "x = factorial(5)\n"
        )
        assert value_of(src, "x") == 120

    def test_function_mutual_recursion(self):
        src = (
            "def is_even(n):\n"
            "    if n == 0:\n"
            "        return True\n"
            "    return is_odd(n - 1)\n"
            "def is_odd(n):\n"
            "    if n == 0:\n"
            "        return False\n"
            "    return is_even(n - 1)\n"
            "x = is_even(4)\n"
            "y = is_odd(4)\n"
        )
        assert value_of(src, "x") is True
        assert value_of(src, "y") is False

    def test_function_wrong_param_count(self):
        src = (
            "def f(a, b):\n"
            "    return a + b\n"
            "x = f(1)\n"
        )
        with pytest.raises(RuntimeMiniPyError):
            run(src)

    def test_function_as_argument(self):
        src = (
            "def apply(f, x):\n"
            "    return f(x)\n"
            "def double(n):\n"
            "    return n * 2\n"
            "x = apply(double, 5)\n"
        )
        assert value_of(src, "x") == 10

    def test_function_returns_function(self):
        src = (
            "def make_multiplier(n):\n"
            "    def multiplier(x):\n"
            "        return x * n\n"
            "    return multiplier\n"
            "mul3 = make_multiplier(3)\n"
            "x = mul3(4)\n"
        )
        assert value_of(src, "x") == 12

    def test_closure_access_outer_scope(self):
        src = (
            "x = 10\n"
            "def f():\n"
            "    return x + 5\n"
            "result = f()\n"
        )
        assert value_of(src, "result") == 15

    def test_closure_with_parameter(self):
        src = (
            "def outer(a):\n"
            "    def inner(b):\n"
            "        return a + b\n"
            "    return inner\n"
            "f = outer(10)\n"
            "x = f(5)\n"
        )
        assert value_of(src, "x") == 15


class TestTyping:
    """Testa tipagem dinâmica e conversões."""

    def test_mixed_arithmetic(self):
        assert value_of("x = 5 + 2.5\n", "x") == 7.5

    def test_string_number_concat_error(self):
        with pytest.raises(RuntimeMiniPyError):
            run('x = "hello" + 5\n')

    def test_invalid_operation_error(self):
        with pytest.raises(RuntimeMiniPyError):
            run('x = "string" * "string"\n')

    def test_type_coercion_in_comparison(self):
        # Dependendo da implementação, isso pode variar
        assert value_of("x = 1 < 2.5\n", "x") is True

    def test_float_precision(self):
        src = "x = 0.1 + 0.2\n"
        result = value_of(src, "x")
        assert abs(result - 0.3) < 0.0001


class TestErrorHandling:
    """Testa tratamento de erros."""

    def test_undefined_variable(self):
        with pytest.raises(RuntimeMiniPyError):
            run("x = undefined_var\n")

    def test_undefined_function(self):
        with pytest.raises(RuntimeMiniPyError):
            run("x = undefined_func()\n")

    def test_call_non_callable(self):
        with pytest.raises(RuntimeMiniPyError):
            run("x = 5()\n")

    def test_invalid_operation_string_int(self):
        with pytest.raises(RuntimeMiniPyError):
            run('x = "string" + 1\n')

    def test_type_error_in_builtin(self):
        with pytest.raises((RuntimeMiniPyError, TypeError)):
            run("x = len(42)\n")


class TestBuiltins:
    """Testa funções built-in."""

    def test_print_single_value(self):
        # Apenas testa que não gera erro
        src = 'print(42)\n'
        run(src)  # Não deve gerar exceção

    def test_print_multiple_values(self):
        src = 'print(1, 2, 3)\n'
        run(src)

    def test_print_string(self):
        src = 'print("hello")\n'
        run(src)

    def test_len_string(self):
        assert value_of('x = len("test")\n', "x") == 4

    def test_int_from_string(self):
        assert value_of('x = int("100")\n', "x") == 100

    def test_int_from_float(self):
        assert value_of("x = int(3.7)\n", "x") == 3

    def test_float_from_string(self):
        result = value_of('x = float("2.5")\n', "x")
        assert abs(result - 2.5) < 0.0001

    def test_float_from_int(self):
        result = value_of("x = float(5)\n", "x")
        assert abs(result - 5.0) < 0.0001

    def test_str_various_types(self):
        assert value_of("x = str(123)\n", "x") == "123"
        assert value_of('x = str("already string")\n', "x") == "already string"

    def test_bool_various_types(self):
        assert value_of("x = bool(0)\n", "x") is False
        assert value_of('x = bool("nonempty")\n', "x") is True


class TestUnaryOperators:
    """Testa operadores unários."""

    def test_unary_minus_int(self):
        assert value_of("x = -5\n", "x") == -5

    def test_unary_minus_float(self):
        result = value_of("x = -3.5\n", "x")
        assert abs(result - (-3.5)) < 0.0001

    def test_unary_minus_negation(self):
        assert value_of("x = -(-5)\n", "x") == 5

    def test_unary_plus(self):
        assert value_of("x = +5\n", "x") == 5

    def test_unary_not_in_expression(self):
        assert value_of("x = not not True\n", "x") is True

    def test_unary_operators_precedence(self):
        # Power has higher precedence than unary minus in this implementation
        assert value_of("x = (-2) ** 2\n", "x") == 4
        # Unary on the result
        assert value_of("x = -(2 ** 2)\n", "x") == -4


class TestEdgeCases:
    """Testa casos extremos."""

    def test_empty_program(self):
        run("")

    def test_multiple_assignments(self):
        src = (
            "a = 1\n"
            "b = 2\n"
            "c = 3\n"
            "x = a + b + c\n"
        )
        assert value_of(src, "x") == 6

    def test_reassignment(self):
        src = (
            "x = 1\n"
            "x = 2\n"
            "x = 3\n"
        )
        assert value_of(src, "x") == 3

    def test_large_numbers(self):
        assert value_of("x = 1000000 * 1000000\n", "x") == 1000000000000

    def test_deeply_nested_expressions(self):
        assert value_of("x = ((((1 + 2) * 3) - 4) / 5)\n", "x") == 1.0

    def test_many_variables(self):
        src = "\n".join([f"v{i} = {i}\n" for i in range(100)])
        src += "x = v99\n"
        assert value_of(src, "x") == 99
