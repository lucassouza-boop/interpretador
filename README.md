# minipy

Interpretador tree-walking simples para um subconjunto de Python, escrito em Python.

## Pipeline

```
código fonte
   │
   ▼
[ Lexer ]      tokens          minipy/lexer.py
   │
   ▼
[ Parser ]     AST             minipy/parser.py  (+ minipy/ast_nodes.py)
   │
   ▼
[ Interpreter ] resultado      minipy/interpreter.py (+ minipy/environment.py)
```

## Recursos suportados

- Tipos: `int`, `float`, `str`, `bool`, `None`
- Variáveis e atribuição
- Operadores aritméticos: `+ - * / % **`
- Comparação: `== != < > <= >=`
- Lógicos: `and or not`
- Controle de fluxo: `if / elif / else`, `while`
- Funções: `def`, `return`, chamadas, parâmetros
- Built-ins: `print`, `len`, `str`, `int`, `float`, `bool`

## Uso

```bash
# REPL interativo
python -m minipy

# Executar arquivo
python -m minipy examples/fib.mp
```

## Estrutura

```
minipy/
  __init__.py
  __main__.py        # entrada CLI + REPL
  tokens.py          # tipos de token
  lexer.py           # texto -> tokens
  ast_nodes.py       # nós da AST
  parser.py          # tokens -> AST (Pratt parser)
  interpreter.py     # avalia AST
  environment.py     # escopo de variáveis
  errors.py          # exceções do interpretador
examples/
  fib.mp
tests/
  test_lexer.py
  test_interpreter.py
```

## Testes

```bash
pytest
```
