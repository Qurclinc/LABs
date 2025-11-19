from math import sqrt

# Функция
def f(x: float) -> float:
    return sqrt(x + 1) - (1 / x)

# Производная
def df(x: float) -> float:
    return (1 / (2 * sqrt(x + 1))) + (1 / x ** 2)

def print_info(n: int, xn: float, xi: float):
    print(f"{step - 1:<5}\t{xi:<12.8f}\t{f(xi):<12.12f}\t{df(xi):<12.8f}\t{abs(xn-xi):<12.12f}")

step = 0
def Newtons_method(xi: float, E: float = 0.000001) -> float:
    global step
    step += 1
    xn = xi - (f(xi) / df(xi))
    print_info(step, xn, xi)
    if abs(xn - xi) < E:
        return xn
    return Newtons_method(xn)

if __name__ == "__main__":
    x0 = 0.7
    print(Newtons_method(x0))
    print(step)