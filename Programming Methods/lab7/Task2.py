def main():
    A, B, C = map(int, input("Введите A, B, C: ").split())
    Num = (A // C) * (B // C)
    print(f"На прямоугольнике {A}x{B} можно разместить {Num} квадратов.")
    S = A * B - Num * C ** 2
    print(f"Не занятая площадь: {S}")
    
if __name__ == "__main__":
    main()