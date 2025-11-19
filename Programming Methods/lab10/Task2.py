import random

def generate_list(length: int) -> int:
    return [random.randint(-50, 51) for _ in range(length)]

def get_differences(l1: list, l2:list) -> list:
    if len(l1) != len(l2):
        raise TypeError("Списки должны быть одинаковой длины")
    return [x - y for x, y in zip(l1, l2)]

def main():
    l1, l2 = generate_list(5), generate_list(5)
    print(f"Первый список: {l1}\nВторой список: {l2}\n")
    differences = get_differences(l1, l2)
    print(f"Разность: {differences}")
    
if __name__ == "__main__":
    main()