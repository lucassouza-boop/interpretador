# Calcula Fibonacci de forma recursiva e iterativa

def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

i = 0
while i <= 10:
    print("fib", i, "=", fib(i))
    i = i + 1

# versão iterativa
def fib_iter(n):
    a = 0
    b = 1
    count = 0
    while count < n:
        temp = a + b
        a = b
        b = temp
        count = count + 1
    return a

print("fib_iter(10) =", fib_iter(10))
