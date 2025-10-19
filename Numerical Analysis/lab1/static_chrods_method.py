from typing import List
from math import sqrt

def print_info(step: int, xn: float, xn1: float, q: float):
    print(f"{step:<5}\t{xn:<12.8f}\t{xn1:<12.8f}\t{f(xn):<12.8f}\t{abs(xn1 - xn):<12.8f}\t{q:<12.8f}")

# Функция
def f(x: float) -> float:
    return sqrt(x + 1) - (1 / x)

def chords_method(x0: float, c: float, E: float = 0.000001):
    x = [x0]
    n = 0
    m = 1.9352
    while True:
        x += [(c * f(x[n]) - x[n] * f(c)) / (f(x[n]) - f(c))]
        q = abs(f(x[n])) / m
        print_info(n, x[n], x[n+1], q)
        if abs(x[n + 1] - x[n]) < q < E:
            break
        n += 1
    
if __name__ == "__main__":
    chords_method(0.8, 0.7)