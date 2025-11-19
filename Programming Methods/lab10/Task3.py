import time
import random

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Функция {func.__name__} заняла {end - start:.6f} секунд")
        return result
    return wrapper

def generate_list(length: int) -> int:
    return [random.randint(-50, 51) for _ in range(length)]

@timer
def find_volume(a: float, b: float, c: float) -> float:
    if any(x <= 0 for x in [a, b, c]):
        raise ValueError("Стороны должны быть положительными")
    return a * b * c

@timer
def get_differences(l1: list, l2:list) -> list:
    if len(l1) != len(l2):
        raise TypeError("Списки должны быть одинаковой длины")
    return [x - y for x, y in zip(l1, l2)]

if __name__ == "__main__":
    print(find_volume(5, 5, 5))
    print()
    l1, l2 = generate_list(5), generate_list(5)
    print(f"Первый список: {l1}\nВторой список: {l2}\n")
    differences = get_differences(l1, l2)
    print(f"Разность: {differences}")