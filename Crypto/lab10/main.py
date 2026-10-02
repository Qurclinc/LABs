from core.rsa import RSA
from constants import OUTPUT_DIR
from utils import clear, encode_text, h

def choose_lang():
    """Вынесенная функция для выбора языка с клавиатуры

    Возвращает:
        str: Значение для параметра языка
    """
    lang = ""
    while lang not in ("R", "E"):
        lang = input("Выберите язык ([E]ng/[R]us)")
    return "eng" if lang == "E" else "rus"

def menu():
    clear()
    print("============================")
    print("1) Сгенерировать новые ключи")
    print("2) Написать и подписать сообщение")
    print("3) Проверить подпись")
    print("...")
    print("0) Выход")
    print("============================")
    print("$ ", end="")
    
def submenu():
    clear()
    print("============================")
    print("1) С восстановлением")
    print("2) Без восстановления")
    print("...")
    print("0) Назад")
    print("============================")
    print("$ ", end="")
    
    
def main():
    while True:
        menu()
        choice = int(input())
        
        match choice:
            case 1:
                bits = int(input("Введите размер ключей RSA (в битах): "))
                rsa = RSA(bits)
                rsa.generate_keys()
                rsa.save_keys()
                print("Ключи успешно сгенерированы и сохранены")
                del rsa
            case 2:
                rsa = RSA()
                submenu()
                subchoice = int(input())
                if subchoice == 0:
                    print("Назад...")
                    continue
                
                message = input("Введите сообщение: ")
                lang = choose_lang()
                encoded_msg = encode_text(message, lang=lang)
                p = int(input("Введите простое p (для функции h(M)): ")) if subchoice == 2 else None
                msg_name = input("Введите название файла для сохранения сообщения: ")
                sign_name = input("Введите название файла для сохранения подписи: ")
                try:
                    rsa.load_privkey()
                    rsa.sign(encoded_msg, lang=lang, p=p, msg_name=msg_name, sign_name=sign_name)
                except TypeError as ex:
                    print(str(ex))
                    continue
                except KeyError:
                    print("Ошибка файла с приватным ключом")
                    continue
                print("Сообщение успешно сохранено и подписано")
                del rsa
            case 3:
                rsa = RSA()
                submenu()
                subchoice = int(input())
                if subchoice == 0:
                    print("Назад...")
                    continue
                
                lang = choose_lang()
                p = int(input("Введите простое p (для функции h(M)): ")) if subchoice == 2 else None
                msg_name = input("Введите название файла для чтения сообщения: ")
                sign_name = input("Введите название файла для чтения подписи: ")
                try:
                    with (
                        open(f"{OUTPUT_DIR}/{msg_name}", "r") as msg,
                        open(f"{OUTPUT_DIR}/{sign_name}", "r") as sign
                    ):
                        M = encode_text(msg.read(), lang=lang)
                        S = int(sign.read())
                        compare_to = h(M, p) if p else M
                        rsa.load_pubkey()
                        print("Подпись совпадает" if rsa.verify_sign(S, compare_to) else "Подпись отличается")
                except FileNotFoundError:
                    print("Осутствует какой-либо из файлов: сообщение или подпись. Перепроверьте название")
                    continue
                except TypeError as ex:
                    print(str(ex))
                    continue
                except KeyError:
                    print("Ошибка файла с публичным ключом")
                    continue
                del rsa
            case 0:
                print("Выход...")
                break
            case _:
                print("Неизветная команда")
        input()

if __name__ == "__main__":
    main()