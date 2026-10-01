import os
from core.utils import perform_finite, perform_galois
# from core.finite import Finite
# from core.galois import Galois

def menu():
    os.system("clear")
    print("===============================")
    print("1) Поле чисел GF*(p)")
    print("2) Поле многочленов GF*(p^m)")
    print("...")
    print("0) Выход")
    print("===============================")
    print("$ ", end="")
    

def main():
    while True:
        menu()
        try:
            choice = int(input())
        except Exception:
            continue
        match choice:
            case 1:
                p = int(input("Введите число: "))
                perform_finite(p)
            case 2:
                q = eval(input("Введите p^m: "))
                perform_galois(q)
            case 0:
                print("Выход...")
                break
            case _:
                print("Неизвестная команда")
        input()
        
if __name__ == "__main__":
    main()