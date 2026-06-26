"""minipy - interpretador tree-walking para um subconjunto de Python."""

from minipy.interpreter import Interpreter
from minipy.lexer import Lexer
from minipy.parser import Parser

__version__ = "0.1.0"


def run(source: str):
    """Lexer -> Parser -> Interpreter. Retorna o interpretador usado."""
    tokens = Lexer(source).tokenize()
    program = Parser(tokens).parse()
    interp = Interpreter()
    interp.interpret(program)
    return interp


__all__ = ["Lexer", "Parser", "Interpreter", "run", "__version__"]
