# minipy

Minipy é um interpretador simples, escrito em Python, para um subconjunto da linguagem Python. O projeto demonstra, em um escopo didático, como funciona um pipeline de execução composto por lexer, parser e interpreter.

## O que o projeto faz

O interpretador aceita programas com:

- tipos básicos como `int`, `float`, `str`, `bool` e `None`
- variáveis e atribuições
- operações aritméticas, comparações e expressões lógicas
- estruturas de controle como `if`, `elif`, `else` e `while`
- funções, retornos e chamadas recursivas
- built-ins como `print`, `len`, `str`, `int`, `float` e `bool`

## Arquitetura

```text
código fonte
   │
   ▼
[ Lexer ]      tokens          minipy/lexer.py
   │
   ▼
[ Parser ]     AST             minipy/parser.py + minipy/ast_nodes.py
   │
   ▼
[ Interpreter ] resultado      minipy/interpreter.py + minipy/environment.py
```

## Instalação

Requisitos:

- Python 3.10+

Instalação local:

```bash
python -m pip install -e .
```

## Uso

Executar o REPL interativo:

```bash
python -m minipy
```

Executar um arquivo de exemplo:

```bash
python -m minipy examples/fib.mp
```

Você também pode usar o entrypoint instalado pelo pacote:

```bash
minipy examples/fib.mp
```

## Exemplo rápido

```python
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print(fib(10))
```

## Estrutura do repositório

```text
minipy/
  __init__.py
  __main__.py        # entrada CLI e REPL
  tokens.py          # definição dos tokens
  lexer.py           # conversão de texto em tokens
  ast_nodes.py       # nós da AST
  parser.py          # construção da AST
  interpreter.py     # execução da AST
  environment.py     # gerenciamento de escopo
  errors.py          # exceções do interpretador
examples/
  fib.mp             # exemplo de programa suportado
tests/
  test_lexer.py
  test_interpreter.py
```

## Desenvolvimento e testes

Instale as dependências de desenvolvimento:

```bash
python -m pip install -e .[dev]
```

Execute a suíte de testes:

```bash
pytest
```

## Documentação adicional

Consulte [docs/guia-de-uso.md](docs/guia-de-uso.md) para uma visão mais detalhada da linguagem e do fluxo de execução.

