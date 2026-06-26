# Guia de uso do Minipy

Este documento complementa o README com detalhes práticos sobre a linguagem suportada pelo interpretador.

## 1. Sintaxe básica

O Minipy suporta instruções simples como atribuições, operações e chamadas de função.

```python
x = 10
y = x + 5
print(y)
```

## 2. Estruturas de controle

### Condicionais

```python
if x > 0:
    print("positivo")
elif x == 0:
    print("zero")
else:
    print("negativo")
```

### Loops

```python
count = 0
while count < 3:
    print(count)
    count = count + 1
```

## 3. Funções

```python
def soma(a, b):
    return a + b

print(soma(2, 3))
```

Funções podem ser recursivas, como no exemplo de Fibonacci.

## 4. Built-ins suportados

A linguagem oferece alguns built-ins básicos:

- `print(...)`
- `len(...)`
- `str(...)`
- `int(...)`
- `float(...)`
- `bool(...)`

## 5. Execução

Você pode rodar um arquivo com:

```bash
python -m minipy caminho/para/arquivo.mp
```

Ou entrar no REPL:

```bash
python -m minipy
```
