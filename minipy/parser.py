"""Parser: tokens -> AST.

Statements por descida recursiva; expressões por Pratt parsing
(precedência por níveis de binding).
"""

from minipy.ast_nodes import (
    Assign,
    BinOp,
    Call,
    ExprStmt,
    FuncDef,
    If,
    Literal,
    LogicalOp,
    Name,
    Program,
    Return,
    UnaryOp,
    While,
)
from minipy.errors import ParserError
from minipy.tokens import Token, TokenType as T

# precedência de operadores binários (maior liga mais forte)
_BINARY_PREC = {
    T.OR: 1,
    T.AND: 2,
    T.EQ: 3, T.NE: 3, T.LT: 3, T.GT: 3, T.LE: 3, T.GE: 3,
    T.PLUS: 4, T.MINUS: 4,
    T.STAR: 5, T.SLASH: 5, T.PERCENT: 5,
    T.DOUBLESTAR: 7,   # acima do unário
}

_OP_TEXT = {
    T.PLUS: "+", T.MINUS: "-", T.STAR: "*", T.SLASH: "/", T.PERCENT: "%",
    T.DOUBLESTAR: "**", T.EQ: "==", T.NE: "!=", T.LT: "<", T.GT: ">",
    T.LE: "<=", T.GE: ">=",
}


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0

    # ---- utilitários ----
    @property
    def _cur(self) -> Token:
        return self.tokens[self.pos]

    def _check(self, *types: T) -> bool:
        return self._cur.type in types

    def _advance(self) -> Token:
        tok = self.tokens[self.pos]
        if tok.type != T.EOF:
            self.pos += 1
        return tok

    def _expect(self, type_: T) -> Token:
        if self._cur.type != type_:
            raise ParserError(
                f"esperado {type_.name}, obtido {self._cur.type.name}",
                self._cur.line,
            )
        return self._advance()

    def _match(self, *types: T) -> bool:
        if self._check(*types):
            self._advance()
            return True
        return False

    def _skip_newlines(self):
        while self._check(T.NEWLINE):
            self._advance()

    # ---- entrada ----
    def parse(self) -> Program:
        body = []
        self._skip_newlines()
        while not self._check(T.EOF):
            body.append(self._statement())
            self._skip_newlines()
        return Program(body)

    # ---- statements ----
    def _statement(self) -> object:
        t = self._cur.type
        if t == T.DEF:
            return self._func_def()
        if t == T.IF:
            return self._if_stmt()
        if t == T.WHILE:
            return self._while_stmt()
        if t == T.RETURN:
            return self._return_stmt()
        return self._simple_stmt()

    def _simple_stmt(self) -> object:
        # atribuição "NAME = expr" ou expressão
        if self._check(T.NAME) and self.tokens[self.pos + 1].type == T.ASSIGN:
            target = self._advance().value
            self._expect(T.ASSIGN)
            value = self._expression()
            self._end_simple()
            return Assign(target, value)
        expr = self._expression()
        self._end_simple()
        return ExprStmt(expr)

    def _end_simple(self):
        if not self._check(T.EOF):
            self._expect(T.NEWLINE)

    def _block(self) -> list:
        self._expect(T.COLON)
        self._expect(T.NEWLINE)
        self._expect(T.INDENT)
        stmts = []
        self._skip_newlines()
        while not self._check(T.DEDENT, T.EOF):
            stmts.append(self._statement())
            self._skip_newlines()
        self._match(T.DEDENT)
        return stmts

    def _func_def(self) -> FuncDef:
        self._expect(T.DEF)
        name = self._expect(T.NAME).value
        self._expect(T.LPAREN)
        params = []
        if not self._check(T.RPAREN):
            params.append(self._expect(T.NAME).value)
            while self._match(T.COMMA):
                params.append(self._expect(T.NAME).value)
        self._expect(T.RPAREN)
        body = self._block()
        return FuncDef(name, params, body)

    def _if_stmt(self) -> If:
        self._advance()  # if / elif
        cond = self._expression()
        body = self._block()
        orelse: list = []
        if self._check(T.ELIF):
            orelse = [self._if_stmt()]
        elif self._match(T.ELSE):
            orelse = self._block()
        return If(cond, body, orelse)

    def _while_stmt(self) -> While:
        self._expect(T.WHILE)
        cond = self._expression()
        body = self._block()
        return While(cond, body)

    def _return_stmt(self) -> Return:
        self._expect(T.RETURN)
        value = None
        if not self._check(T.NEWLINE, T.EOF):
            value = self._expression()
        self._end_simple()
        return Return(value)

    # ---- expressões (Pratt) ----
    def _expression(self, min_prec: int = 0) -> object:
        left = self._unary()
        while True:
            t = self._cur.type
            prec = _BINARY_PREC.get(t)
            if prec is None or prec < min_prec:
                break
            self._advance()
            # ** é associativo à direita
            next_min = prec if t == T.DOUBLESTAR else prec + 1
            right = self._expression(next_min)
            if t in (T.AND, T.OR):
                left = LogicalOp("and" if t == T.AND else "or", left, right)
            else:
                left = BinOp(_OP_TEXT[t], left, right)
        return left

    def _unary(self) -> object:
        if self._check(T.NOT):
            self._advance()
            return UnaryOp("not", self._unary())
        if self._check(T.MINUS):
            self._advance()
            return UnaryOp("-", self._unary())
        if self._check(T.PLUS):
            self._advance()
            return UnaryOp("+", self._unary())
        return self._call()

    def _call(self) -> object:
        expr = self._primary()
        while self._check(T.LPAREN):
            self._advance()
            args = []
            if not self._check(T.RPAREN):
                args.append(self._expression())
                while self._match(T.COMMA):
                    args.append(self._expression())
            self._expect(T.RPAREN)
            expr = Call(expr, args)
        return expr

    def _primary(self) -> object:
        tok = self._cur
        t = tok.type
        if t in (T.INT, T.FLOAT, T.STRING, T.TRUE, T.FALSE, T.NONE):
            self._advance()
            return Literal(tok.value)
        if t == T.NAME:
            self._advance()
            return Name(tok.value)
        if t == T.LPAREN:
            self._advance()
            expr = self._expression()
            self._expect(T.RPAREN)
            return expr
        raise ParserError(f"token inesperado {t.name}", tok.line)
