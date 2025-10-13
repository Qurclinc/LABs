from math import sqrt, sin, cos


def phi(x: float) -> float:
    U = 0.4125
    return x - U * (sqrt(x + 1) - (1 / x))

def print_info(n: int, xn1: float, xn: float):
    q = 0.8017
    print(f"{n:<5}\t{xn1:<12.8f}\t{xn:<12.8f}\t{abs(xn1-xn):<12.8f}\t{((1-q) / q ) * abs(xn1 - xn):<12.8f} ")

step = 0
def iterations_method(x: float, E: float = 0.000001) -> float:
    q = 0.8017
    global step
    xn = phi(x)
    step += 1
    print_info(step - 1, x, xn)
    if ((1-q) / q ) * abs(x - xn) <= E:
        return xn
    return iterations_method(xn)

if __name__ == "__main__":
    x0 = 0.75
    iterations_method(x0)



