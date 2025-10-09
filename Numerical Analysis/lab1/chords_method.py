from typing import List
from math import sqrt

def print_info(step: int, xn1: float, xnn1: float, xn: float):
    print(f"{step:<5}\t{xn1:<12.8f}\t{xnn1:<12.8f}\t{xn:<12.8f}\t{f(xnn1):<12.8f}\t{f(xn):<12.8f}\t{abs(xn1 - xn):<12.8f}")

# Функция
def f(x: float) -> float:
    return sqrt(x + 1) - (1 / x)

def chords_method(x0: float, x1: float, E: float = 0.000001):
    x = [x0, x1]
    n = 1
    while True:
        x += [x[n - 1] - f(x[n - 1]) * ((x[n] - x[n - 1]) / (f(x[n]) - f(x[n - 1])))]
        print_info(n - 1, x[n + 1], x[n - 1], x[n])
        if abs(x[n + 1] - x[n]) <= E:
            break
        
        n += 1
    
if __name__ == "__main__":
    chords_method(0.7, 0.8)