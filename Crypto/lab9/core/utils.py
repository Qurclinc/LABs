import random
from typing import Tuple

ALLOWED_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] # После 29 у меня нет таблиц
    

def is_power_of_prime(q: int) -> Tuple[int, int]:
    """Проверяет, является ли число q степенью какого-либо простого числа 
    (из допустимого параметра: на p > 29 не брал таблицы, в репозитории это максимум)

    Аргументы:
        q (int): Целое число, являющееся степенью (больше 1) простого числа

    Возвращает:
        Tuple[int]: Первое значение - простой степенью какого числа является q, а второе значение
        определяет саму степень (необходимо для сопоставления строки таблицы)
    """
    if q < 2:
        return tuple()
    
    for p in ALLOWED_PRIMES:
        if q % p == 0:
            n = q
            counter = 0
            while n % p == 0:
                n //= p
                counter += 1
            if n == 1:
                return (p, counter)
            
    return tuple()

def perform_finite(p):
    from core.finite import Finite
    gf = Finite(p)

    G = gf.g
    print(f"G = {G}")
    a, b = random.randint(2, p - 2), random.randint(2, p - 2)
    print(f"a = {a}\nb = {b}")

    A = gf.pow(G, a)
    B = gf.pow(G, b)
    print(f"A = {A}\nB = {B}")

    K1 = gf.pow(B, a)
    K2 = gf.pow(A, b)
    print(K1, K2)

def perform_galois(q: int):
    from core.galois import Galois
    gf = Galois(q)
    G = gf.g
    print(f"G = {gf.to_polynominal(G)}")

    a = gf.random_polynom()
    b = gf.random_polynom()
    print(f"a = {gf.to_polynominal(a)}\nb = {gf.to_polynominal(b)}")

    A = gf.pow(G, a)
    B = gf.pow(G, b)
    print(f"A = {gf.to_polynominal(A)}\nB = {gf.to_polynominal(B)}")

    K1 = gf.pow(B, a)
    K2 = gf.pow(A, b)

    print(f"K = {gf.to_polynominal(K1)}\t\tK = {gf.to_polynominal(K2)}")