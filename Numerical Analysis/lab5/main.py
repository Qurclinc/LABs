from typing import List
import math
import sympy as sp
import numpy as np
from GaussMethod import solve_gauss

def f(x: float) -> float:
    return (math.log(x) ** (13/7))

def L(x: float) -> float:
    return (3.8947 * (((x - 11) * (x - 14)) / 18)) \
            + 5.0746 * (((x - 8) * (x - 14)) / -9) \
            + 6.063 * (((x - 8) * (x - 11)) / 18)
            
def f3(x0: float):
    x = sp.symbols("x", positive=True)
    func = (sp.log(x)) ** sp.Rational(13, 7)
    d3 = sp.diff(func, x, 3)
    d3 = sp.simplify(d3)
    print(d3)
    func = sp.lambdify(x, d3, "math")
    return func(12.5)
    
def R():
    return f3(12.5) * (1/6) * abs((12.5 - 8) * (12.5 - 11) * (12.5 - 14)) # (abs(math.prod(x - xi for xi in xs)))

if __name__ == "__main__":
    a = 12.5
    print(f"f(a) = {f(a)}")
    print(f"L(a) = {L(a)}")

    a, b = f(a), L(a)
    delta = abs(a - b)
    print(delta)
    
    R2 = R()
    print(R2)
    print(f"R2(12.5) < {delta}")
    
    A = np.array([
        np.array([1, 8, 8**2, 3.8947]),
        np.array([1, 11, 11**2, 5.0746]),
        np.array([1, 14, 14**2, 6.0630])
    ], dtype=float)
    res = solve_gauss(A)
    print(res)
    
    L2 = res[2] * 12.5 ** 2 + res[1] * 12.5 + res[0]
    R2 = abs(5.588426 - L2)
    print(L2)
    print(R2)
    
