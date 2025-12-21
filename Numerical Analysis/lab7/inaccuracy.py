import sympy as sp
import numpy as np
from scipy.optimize import minimize_scalar

# def xd():
#     x = sp.symbols("x")
#     func = sp.sin(0.2*x - 3) / (x**2 + 1)
#     d = sp.simplify(sp.diff(func))
#     abs_d = sp.Abs(d)
#     func = sp.lambdify(x, d, "math")
#     print(func(3), func(4), sep="\n")
    
def df(count: int = 1):
    x = sp.symbols("x")
    d = sp.sin(0.2*x - 3) / (x**2 + 1)
    for c in range(count):
        d = sp.diff(d)
    return sp.simplify(d)

def find_extrema_scipy(d):
    x = sp.symbols("x")
    
    # Численная функция
    f_prime_num = sp.lambdify(x, d, 'numpy')
    
    # Функция для максимума модуля
    def abs_f_prime(x):
        return abs(f_prime_num(x))
    
    # 1. Находим максимум |f'(x)|
    result_max = minimize_scalar(lambda x: -abs_f_prime(x), 
                                 bounds=(3, 4), 
                                 method='bounded')
    M1 = abs_f_prime(result_max.x)
    
    # 2. Находим минимум f'(x)
    result_min = minimize_scalar(f_prime_num, 
                                 bounds=(3, 4), 
                                 method='bounded')
    m1 = f_prime_num(result_min.x)
    
    print("Результаты (scipy):")
    print(f"M₁ = max|f'(x)| = {M1:.10f} при x ≈ {result_max.x:.8f}")
    print(f"m₁ = min f'(x)  = {m1:.10f} при x ≈ {result_min.x:.8f}")
    
    return M1, m1, result_max.x, result_min.x

if __name__ == "__main__":
    # d = df(1)
    d = df(2)
    M1, m1, x_max, x_min = find_extrema_scipy(d)
    d = df(4)
    M1, m1, x_max, x_min = find_extrema_scipy(d)
    # M1 = 0.025779 
    # m1 = 0.015457
    # R = 10**-3
    # a, b = 3, 4
    # print((2 * R) / (M1 * (b - a)))
    # print((2 * R) / (m1 * (b - a)))