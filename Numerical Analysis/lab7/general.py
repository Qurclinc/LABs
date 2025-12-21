import math
import sympy as sp

def rectangle_print_line(i: int, xi: int, res: float):
    print(f"{i}\t{xi:.3f}\t{res:.6f}")

def f(x: float) -> float:
    return (math.sin(0.2 * x - 3)) / (x ** 2 + 1)
