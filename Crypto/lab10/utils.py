import os
from typing import Literal
import random

from constants import ALPHABET, URL
import requests

def encode_text(text: str, lang: Literal["rus", "eng"]) -> int:
    """Переводит текст сообщения в его десятичное представление. Работает по приниципу перевода
    систем счисления

    Аргументы:
        text (str): Исходный текст
        lang (Literal["rus", "eng"]): Язык текста

    Исключения:
        KeyError: Передан некорректный язык

    Возвращает:
        int: Десятичное представление сообщения
    """
    if lang not in ["rus", "eng"]:
        raise KeyError
    abc = ALPHABET[lang]
    base = len(abc) + 1 # Основание
    l = len(text) - 1
    result = 0
    for i, ch in enumerate(text):
        result += base ** (l - i) * (abc.index(ch) + 1)
        # print(f"{base}^{l - i} * {abc.index(ch) + 1}")
    return result

def decode_text(number: int, lang: Literal["rus", "eng"]):
    """Переводит десятичное представления сообщения обратно в текст. Тоже работает по приниципу 
    перевода систем счисления

    Аргументы:
        number (str): Десятичное представление
        lang (Literal["rus", "eng"]): Язык текста

    Исключения:
        KeyError: Передан некорректный язык

    Возвращает:
        str: Строковое представление сообщения
        """
    if lang not in ["rus", "eng"]:
        raise KeyError
    abc = ALPHABET[lang]
    base = len(abc) + 1
    result = []
    while number > 0:
        result.append(number % base)
        number //= base
    return "".join(abc[i - 1] for i in result[::-1])

def h(number: int, p: int) -> int:
    """Учебная хеш-функция

    Аргументы:
        number (int): Десятичное представление хешируемых данных
        p (int): Простое число, необходимое для алгоритма

    Исключения:
        ValueError: Передано не простое p

    Возвращает:
        int: Хеш-сумма данных
    """
    if not(verify_primality(p)):
        raise ValueError("p - не простое число")
    result = 0
    h0 = len(str(number)) # За h0 берётся количество десятичных разрядов
    prev = h0 # Дабы не тянуть весь список, лучше хранить просто предыдущее значение
    while number > 0:
        Mi = number % 10 # Самый младший разряд числа
        number //= 10 # Сразу отбрасываем его
        # print(f"{Mi} + 2 * {prev} + 1")
        result = bin_pow((Mi + 2 * prev + 1), 2, p - 1) # hi = (Mi + 2*h0 + 1)^2 mod (p - 1)
        prev = result # Перезапись предыдущего
    return result + 1 # h(M) = hn + 1

def bin_pow(a: int, n: int, m: int) -> int:
    """Бинарное возведение числа a в степень n по модулю m.
    Обращается к API эндпоинту из лаб. работы №5!

    Аргументы:
        a (int): Основание
        n (int): Степень
        m (int): Модуль

    Возвращает:
        int: a^n mod m
    """
    payload = {"a": str(a), "n": str(n), "m": str(m)}
    response = requests.post(f"{URL}/binpow", json=payload)
    return int(response.json())

def inverse(a: int, m: int):
    """Мультипликативное обратное для a по модулю m.
    Обращается к API эндпоинту из лаб. работы №5!

    Аргументы:
        a (int): Число
        m (int): Модуль

    Возвращает:
        int: Мультпликативное обратное
    """
    payload = {"a": str(a), "m": str(m)}
    response = requests.post(f"{URL}/inverse", json=payload)
    return int(response.json())

def verify_primality(n: int) -> bool:
    """Проверяет простоту числа используя три вероятностных теста: Ферма, Соловея-Штрассена и Рабина-Миллера.
    Обращается к API эндпоинту из лаб. работы №5!

    Аргументы:
        n (int): Целое число

    Возвращает:
        bool: Простое ли число
    """
    payload = {"n": str(n), "k": 10} 
    results = []
    for r in [
        requests.post(f"{URL}/ferm", json=payload),
        requests.post(f"{URL}/strassen", json=payload),
        requests.post(f"{URL}/rabin", json=payload),
    ]:
        results.append(r.json())
    return all(results)

def get_primitive_root(n: int, rnd: bool = False):
    onlysingle = not(rnd)
    payload = {"n": str(n), "onlysingle": onlysingle}
    response = requests.post(f"{URL}/primitiveroot", json=payload)
    if rnd:
        return random.choice(response.json())
    return response.json()[0]

def clear():
    os.system("cls" if os.name == "nt" else "clear")