from math import sqrt, sin, cos

# # Функция
# def f(x: float) -> float:
#     return sqrt(x + 1) - (1 / x)

# # Производная
# def df(x: float) -> float:
#     return (1 / (2 * sqrt(x + 1))) + (1 / x ** 2)


def f(x: float) -> float:
    return x**2 -10 * sin (x)

def df(x: float) -> float:
    return 2 * x - 10 * cos (x)

def print_info(n: int, x_new: float, q: float):
    print(f"{n:<5}\t{x_new:<12.8f}\t{f(x_new):<12.8f}\t{df(x_new):<12.8f}\t{q:<12.12f}")

step = 0
def Newtons_method(xi: float, E: float = 10 ** -10) -> float:
    global step
    step += 1
    xn = xi - (f(xi) / df(xi))
    # q = abs(f(xi)) / 1.9352  # ДОБАВЛЕН МОДУЛЬ!
    q = abs(f(xi)) / 12.1739
    print_info(step - 1, xi, q)
    if q < E:
        return xn
    return Newtons_method(xn)

if __name__ == "__main__":
    # x0 = 0.7
    x0 = 2.5
    print("Шаг\tx_n\t\tf(x_n)\t\tf'(x_n)\t\tq")
    result = Newtons_method(x0)
    print(f"\nРезультат: x = {result}")