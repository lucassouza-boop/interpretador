"""Lexer: texto fonte -> lista de tokens.

Trata indentação ao estilo Python emitindo tokens INDENT/DEDENT.
"""

from minipy.errors import LexerError
from minipy.tokens import KEYWORDS, Token, TokenType

_TWO_CHAR = {
    "**": TokenType.DOUBLESTAR,
    "==": TokenType.EQ,
    "!=": TokenType.NE,
    "<=": TokenType.LE,
    ">=": TokenType.GE,
}

_ONE_CHAR = {
    "+": TokenType.PLUS,
    "-": TokenType.MINUS,
    "*": TokenType.STAR,
    "/": TokenType.SLASH,
    "%": TokenType.PERCENT,
    "=": TokenType.ASSIGN,
    "<": TokenType.LT,
    ">": TokenType.GT,
    "(": TokenType.LPAREN,
    ")": TokenType.RPAREN,
    ",": TokenType.COMMA,
    ":": TokenType.COLON,
}


class Lexer:
    def __init__(self, source: str):
        self.src = source
        self.pos = 0
        self.line = 1
        self.col = 1
        self.tokens: list[Token] = []
        self.indents = [0]          # pilha de níveis de indentação
        self.paren_depth = 0        # dentro de () newlines são ignorados

    # ---- utilitários ----
    def _peek(self, offset: int = 0) -> str:
        i = self.pos + offset
        return self.src[i] if i < len(self.src) else ""

    def _advance(self) -> str:
        ch = self.src[self.pos]
        self.pos += 1
        if ch == "\n":
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return ch

    def _add(self, type_: TokenType, value: object, col: int):
        self.tokens.append(Token(type_, value, self.line, col))

    # ---- laço principal ----
    def tokenize(self) -> list[Token]:
        at_line_start = True
        while self.pos < len(self.src):
            if at_line_start and self.paren_depth == 0:
                self._handle_indent()
                at_line_start = False
                if self.pos >= len(self.src):
                    break

            ch = self._peek()

            if ch == "\n":
                col = self.col
                self._advance()
                if self.paren_depth == 0:
                    if self.tokens and self.tokens[-1].type != TokenType.NEWLINE:
                        self._add(TokenType.NEWLINE, "\\n", col)
                    at_line_start = True
                continue

            if ch in " \t":
                self._advance()
                continue

            if ch == "#":
                while self._peek() and self._peek() != "\n":
                    self._advance()
                continue

            if ch.isdigit() or (ch == "." and self._peek(1).isdigit()):
                self._number()
                continue

            if ch.isalpha() or ch == "_":
                self._name()
                continue

            if ch in "\"'":
                self._string()
                continue

            self._operator()

        # fecha NEWLINE final e DEDENTs pendentes
        if self.tokens and self.tokens[-1].type != TokenType.NEWLINE:
            self._add(TokenType.NEWLINE, "\\n", self.col)
        while len(self.indents) > 1:
            self.indents.pop()
            self._add(TokenType.DEDENT, None, self.col)
        self._add(TokenType.EOF, None, self.col)
        return self.tokens

    # ---- indentação ----
    def _handle_indent(self):
        count = 0
        start = self.pos
        while self._peek() in (" ", "\t"):
            count += 1 if self._peek() == " " else 8
            self._advance()
        # linha em branco ou comentário: não afeta indentação
        if self._peek() in ("\n", "#", ""):
            return
        if count > self.indents[-1]:
            self.indents.append(count)
            self._add(TokenType.INDENT, count, self.col)
        else:
            while count < self.indents[-1]:
                self.indents.pop()
                self._add(TokenType.DEDENT, None, self.col)
            if count != self.indents[-1]:
                raise LexerError("indentação inconsistente", self.line, self.col)
        _ = start

    # ---- literais ----
    def _number(self):
        col = self.col
        start = self.pos
        is_float = False
        while self._peek().isdigit():
            self._advance()
        if self._peek() == ".":
            is_float = True
            self._advance()
            while self._peek().isdigit():
                self._advance()
        text = self.src[start:self.pos]
        if is_float:
            self._add(TokenType.FLOAT, float(text), col)
        else:
            self._add(TokenType.INT, int(text), col)

    def _name(self):
        col = self.col
        start = self.pos
        while self._peek().isalnum() or self._peek() == "_":
            self._advance()
        text = self.src[start:self.pos]
        type_ = KEYWORDS.get(text, TokenType.NAME)
        value = text
        if type_ == TokenType.TRUE:
            value = True
        elif type_ == TokenType.FALSE:
            value = False
        elif type_ == TokenType.NONE:
            value = None
        self._add(type_, value, col)

    def _string(self):
        col = self.col
        quote = self._advance()
        chars: list[str] = []
        while True:
            ch = self._peek()
            if ch == "":
                raise LexerError("string não terminada", self.line, col)
            if ch == quote:
                self._advance()
                break
            if ch == "\\":
                self._advance()
                esc = self._advance()
                chars.append({"n": "\n", "t": "\t", "\\": "\\",
                              quote: quote}.get(esc, esc))
                continue
            chars.append(self._advance())
        self._add(TokenType.STRING, "".join(chars), col)

    def _operator(self):
        col = self.col
        two = self._peek() + self._peek(1)
        if two in _TWO_CHAR:
            self._advance()
            self._advance()
            self._add(_TWO_CHAR[two], two, col)
            return
        ch = self._peek()
        if ch in _ONE_CHAR:
            self._advance()
            if ch == "(":
                self.paren_depth += 1
            elif ch == ")":
                self.paren_depth = max(0, self.paren_depth - 1)
            self._add(_ONE_CHAR[ch], ch, col)
            return
        raise LexerError(f"caractere inesperado {ch!r}", self.line, col)
