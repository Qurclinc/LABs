from math import sqrt

# Функция
def f(x: float) -> float:
    return sqrt(x + 1) - (1 / x)

# Производная
def df(x: float) -> float:
    return (1 / (2 * sqrt(x + 1))) + (1 / x ** 2)

def print_info(n: int, x_new: float, q: float):
    print(f"{n:<5}\t{x_new:<12.8f}\t{f(x_new):<12.8f}\t{df(x_new):<12.8f}\t{q:<12.8f}")

step = 0
def Newtons_method(xi: float, E: float = 0.000001) -> float:
    global step
    step += 1
    xn = xi - (f(xi) / df(xi))
    q = abs(f(xn)) / 1.9352  # ДОБАВЛЕН МОДУЛЬ!
    print_info(step - 1, xn, q)
    if q < E:
        return xn
    return Newtons_method(xn)

if __name__ == "__main__":
    x0 = 0.7
    print("Шаг\tx_n\t\tf(x_n)\t\tf'(x_n)\t\tq")
    result = Newtons_method(x0)
    print(f"\nРезультат: x = {result}")