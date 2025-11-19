def find_volume(a: float, b: float, c: float) -> float:
    if any(x <= 0 for x in [a, b, c]):
        raise ValueError("Стороны должны быть положительными")
    return a * b * c
    
def main():
    a, b, c = map(float, input("Введите a, b, c: ").split())
    print(find_volume(a, b, c))
    
if __name__ == "__main__":
    main()