from math import sqrt, sin

# def f(x: float) -> float:
#     return sqrt(x + 1) - (1 / x)

# def f(x: float) -> float:
#     return x ** 2 - 10 * sin(x)

def f(x):
    return (x + 2.01) ** 3

def print_info(n: int, a: float, b: float, c: float):
    print(f"{step - 1:<5}\t{a:<12.8f}\t{c:<12.8f}\t{b:<12.8f}\t{f(a):<12.8f}\t{f(c):<12.8f}\t{f(b):<12.8f}\t{abs(a-b):<12.8f}")

step = 0
def bisections_method(left: float, right: float, E: float = 10**-1):
    global step
    step += 1
    middle = (left + right) / 2
    print_info(step, left, right, middle)
    if abs(right - left) <= E or f(middle) == 0:
        return middle
    if f(left) * f(middle) < 0:
        return bisections_method(left, middle)
    elif f(left) * f(middle) > 0:
        return bisections_method(middle, right)
    
        
if __name__ == "__main__":
    bisections_method(-3, -1)
