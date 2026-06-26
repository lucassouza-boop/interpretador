"""Nós da AST (Abstract Syntax Tree)."""

from dataclasses import dataclass, field


class Node:
    """Base de todos os nós."""


# ---- expressões ----
@dataclass
class Literal(Node):
    value: object


@dataclass
class Name(Node):
    ident: str


@dataclass
class BinOp(Node):
    op: str
    left: Node
    right: Node


@dataclass
class UnaryOp(Node):
    op: str
    operand: Node


@dataclass
class LogicalOp(Node):
    op: str          # "and" | "or"
    left: Node
    right: Node


@dataclass
class Call(Node):
    callee: Node
    args: list = field(default_factory=list)


# ---- statements ----
@dataclass
class Assign(Node):
    target: str
    value: Node


@dataclass
class ExprStmt(Node):
    expr: Node


@dataclass
class If(Node):
    condition: Node
    body: list
    orelse: list = field(default_factory=list)


@dataclass
class While(Node):
    condition: Node
    body: list


@dataclass
class FuncDef(Node):
    name: str
    params: list
    body: list


@dataclass
class Return(Node):
    value: Node | None


@dataclass
class Program(Node):
    body: list
