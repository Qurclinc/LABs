import random
from typing import List
import math
from Crypto.Util.number import isPrime

from .field import Field

class Finite(Field):
    """Конечное поле чисел GF*(p)
    """
    def __init__(self, p: int):
        if not(isPrime(p)):
            raise TypeError
        self.p = p # Простой модуль
        self.g = self._find_primitive() # Первообразный корень
        
    def pow(self, a: int, n: int) -> int:
        """Бинарное возведение числа a в степень n по модулю p

        Аргументы:
            a (int): Основание
            n (int): Степень

        Возвращает:
            int: a^n % p
        """
        
        a %= self.p # Чтобы наверняка было в поле
        result = a
        for d in bin(n)[3:]: # Двоичное представление
            match d:
                case "1": # Если единица - в квадрат и умножить
                    result = (result * result) % self.p
                    result = (result * a) % self.p
                case "0": # Если ноль - в квадрат
                    result = (result * result) % self.p
        return result
        
    def _factorize(self, n: int) -> List[int]:
        """Разложение числа n на простые множители

        Аргументы:
            n (int): Число из поля GF*(p)

        Возвращает:
            List[int]: Простые множители
        """
        factors = []
        
        # Двойка проверяется отдельно
        if n % 2 == 0:
            factors.append(2)
            
        while n % 2 == 0:
            n //= 2
            
        # Пробег по оставшимся потенциальным делителям
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0: # Если они есть
                factors.append(i) # То они заносятся в список
                while n % i == 0: # И мы делим на них, пока это возможно без остатка
                    n //= i
                    
        if n > 1: # Что осталось от числа - тоже является множителем
            factors.append(n)
                    
        return factors[:]
        
    def _find_primitive(self) -> int:
        """Находит случайный первообразный корень

        Возвращает:
            int: Первообразный корень
        """
        n = self.p
        phi = n - 1
        factors = self._factorize(phi)
        while True:
            # for g in range(1, n):
            g = random.randint(1, n)
            if math.gcd(g, n) != 1:
                continue
            is_primitive = True
            for prime in factors:
                # Проверка условий что число подходит
                potential_primitive_root = self.pow(g, phi // prime)
                if potential_primitive_root == 1:
                    is_primitive = False
                    break
            if is_primitive:
                return g