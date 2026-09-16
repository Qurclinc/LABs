import os
from simple_fields import build_field
from galois import Galois


# g = Galois(2**4)
# g.addition()
# g.multiplication()

def menu() -> str:
    os.system("clear")
    print("===================")
    print("1) Поле Zp")
    print("2) Поле GF(q)")
    print("0) Выход")
    print("===================")
    print("$ ", end="")
    
def submenu():
    os.system("clear")
    print("===================")
    print("1) Числа")
    print("2) Буквы")
    print("0) Назад")
    print("===================")
    print("$ ", end="")

def main():
    while True:
        menu()
        choice = input()
        match choice:
            case "1":
                submenu()
                subchoice = input()
                is_letter = None
                match subchoice:
                    case "1":
                        is_letter = False
                    case "2":
                        is_letter = True
                    case _:
                        continue
                if is_letter is None:
                    continue
                p = int(input("Введите простое целое число p = "))
                build_field(p, is_letters=is_letter)
                input("Поле успешно сохранено в директорию out\nНажмите любую кнопку чтобы продолжить...")
            case "2":
                try:
                    os.system("clear")
                    # eval небезопасно, зато подходит
                    q = int(eval(input("Введите q = p^m (m > 1; p - простое, p <= 29)\nq = ")))
                    GF = Galois(q)
                except Exception:
                    input("Некорректное q\nНажмите любую кнопку чтобы продолжения...")
                    continue
                
                GF.addition()
                GF.multiplication()
                input("Поле успешно сохранено в директорию out\nНажмите любую кнопку чтобы продолжить...")
            case "0":
                print("Выход...")
                break

if __name__ == "__main__":
    main()