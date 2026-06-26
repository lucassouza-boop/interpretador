"""Exceções do interpretador."""


class MiniPyError(Exception):
    """Base para erros do minipy."""


class LexerError(MiniPyError):
    def __init__(self, message: str, line: int, col: int):
        super().__init__(f"Erro léxico (linha {line}, col {col}): {message}")
        self.line = line
        self.col = col


class ParserError(MiniPyError):
    def __init__(self, message: str, line: int):
        super().__init__(f"Erro de sintaxe (linha {line}): {message}")
        self.line = line


class RuntimeMiniPyError(MiniPyError):
    """Erro em tempo de execução."""
