"""Interpreter: avalia a AST (tree-walking)."""

import operator

from minipy import ast_nodes as ast
from minipy.environment import Environment
from minipy.errors import RuntimeMiniPyError


class _Return(Exception):
    """Controle de fluxo interno para `return`."""

    def __init__(self, value):
        self.value = value


class Function:
    """Função definida pelo usuário (closure)."""

    def __init__(self, decl: ast.FuncDef, closure: Environment):
        self.decl = decl
        self.closure = closure

    def call(self, interp: "Interpreter", args: list):
        if len(args) != len(self.decl.params):
            raise RuntimeMiniPyError(
                f"{self.decl.name}() espera {len(self.decl.params)} "
                f"argumento(s), recebeu {len(args)}"
            )
        env = self.closure.child()
        for name, value in zip(self.decl.params, args):
            env.set(name, value)
        try:
            interp.exec_block(self.decl.body, env)
        except _Return as r:
            return r.value
        return None

    def __repr__(self):
        return f"<função {self.decl.name}>"


_BINARY = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "%": operator.mod,
    "**": operator.pow,
    "==": operator.eq,
    "!=": operator.ne,
    "<": operator.lt,
    ">": operator.gt,
    "<=": operator.le,
    ">=": operator.ge,
}


class Interpreter:
    def __init__(self):
        self.globals = Environment()
        self._install_builtins()

    def _install_builtins(self):
        self.globals.set("print", _Builtin("print", self._b_print))
        self.globals.set("len", _Builtin("len", lambda a: len(a[0])))
        self.globals.set("str", _Builtin("str", lambda a: _to_str(a[0])))
        self.globals.set("int", _Builtin("int", lambda a: int(a[0])))
        self.globals.set("float", _Builtin("float", lambda a: float(a[0])))
        self.globals.set("bool", _Builtin("bool", lambda a: bool(a[0])))

    @staticmethod
    def _b_print(args):
        print(" ".join(_to_str(a) for a in args))
        return None

    # ---- entrada ----
    def interpret(self, program: ast.Program):
        for stmt in program.body:
            self.execute(stmt, self.globals)

    def exec_block(self, stmts: list, env: Environment):
        for stmt in stmts:
            self.execute(stmt, env)

    # ---- statements ----
    def execute(self, node, env: Environment):
        method = getattr(self, f"_exec_{type(node).__name__}", None)
        if method is None:
            raise RuntimeMiniPyError(f"statement não suportado: {type(node).__name__}")
        return method(node, env)

    def _exec_Assign(self, node: ast.Assign, env):
        env.set(node.target, self.evaluate(node.value, env))

    def _exec_ExprStmt(self, node: ast.ExprStmt, env):
        self.evaluate(node.expr, env)

    def _exec_If(self, node: ast.If, env):
        if _truthy(self.evaluate(node.condition, env)):
            self.exec_block(node.body, env)
        elif node.orelse:
            self.exec_block(node.orelse, env)

    def _exec_While(self, node: ast.While, env):
        while _truthy(self.evaluate(node.condition, env)):
            self.exec_block(node.body, env)

    def _exec_FuncDef(self, node: ast.FuncDef, env):
        env.set(node.name, Function(node, env))

    def _exec_Return(self, node: ast.Return, env):
        value = self.evaluate(node.value, env) if node.value is not None else None
        raise _Return(value)

    # ---- expressões ----
    def evaluate(self, node, env: Environment):
        method = getattr(self, f"_eval_{type(node).__name__}", None)
        if method is None:
            raise RuntimeMiniPyError(f"expressão não suportada: {type(node).__name__}")
        return method(node, env)

    def _eval_Literal(self, node: ast.Literal, env):
        return node.value

    def _eval_Name(self, node: ast.Name, env):
        return env.get(node.ident)

    def _eval_BinOp(self, node: ast.BinOp, env):
        left = self.evaluate(node.left, env)
        right = self.evaluate(node.right, env)
        try:
            return _BINARY[node.op](left, right)
        except ZeroDivisionError:
            raise RuntimeMiniPyError("divisão por zero")
        except TypeError as e:
            raise RuntimeMiniPyError(f"operação inválida '{node.op}': {e}")

    def _eval_UnaryOp(self, node: ast.UnaryOp, env):
        val = self.evaluate(node.operand, env)
        if node.op == "-":
            return -val
        if node.op == "+":
            return +val
        if node.op == "not":
            return not _truthy(val)
        raise RuntimeMiniPyError(f"operador unário inválido: {node.op}")

    def _eval_LogicalOp(self, node: ast.LogicalOp, env):
        left = self.evaluate(node.left, env)
        if node.op == "and":
            return self.evaluate(node.right, env) if _truthy(left) else left
        return left if _truthy(left) else self.evaluate(node.right, env)

    def _eval_Call(self, node: ast.Call, env):
        callee = self.evaluate(node.callee, env)
        args = [self.evaluate(a, env) for a in node.args]
        if isinstance(callee, Function):
            return callee.call(self, args)
        if isinstance(callee, _Builtin):
            return callee.fn(args)
        raise RuntimeMiniPyError(f"objeto não chamável: {callee!r}")


class _Builtin:
    def __init__(self, name, fn):
        self.name = name
        self.fn = fn

    def __repr__(self):
        return f"<built-in {self.name}>"


def _truthy(value) -> bool:
    return bool(value)


def _to_str(value) -> str:
    if value is True:
        return "True"
    if value is False:
        return "False"
    if value is None:
        return "None"
    return str(value)
