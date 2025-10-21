from typing import List
from math import sqrt, sin, cos

def print_info(step: int, xn1: float, xnn1: float, xn: float, q: float):
    print(f"{step:<5}\t{xn1:<12.8f}\t{xnn1:<12.8f}\t{xn:<12.8f}\t{f(xnn1):<12.8f}\t{f(xn):<12.8f}\t{abs(xn1 - xn):<12.12f}\t{q:<12.12f}")

# Функция
# def f(x: float) -> float:
#     return sqrt(x + 1) - (1 / x)

def f(x: float) -> float:
    return x ** 2 - 10 * sin(x)

def chords_method(x0: float, x1: float, E: float = 10 ** -10):
    x = [x0, x1]
    n = 1
    # m = 1.9352
    m = 12.1739
    while True:
        q = abs(f(x[n])) / m
        x += [x[n - 1] - f(x[n - 1]) * ((x[n] - x[n - 1]) / (f(x[n]) - f(x[n - 1])))]
        print_info(n - 1, x[n + 1], x[n - 1], x[n], q)
        # if q < E:
        #     break
        if abs(x[n + 1] - x[n]) <= E:
            break
        
        n += 1
    
if __name__ == "__main__":
    chords_method(2.4, 2.5)
