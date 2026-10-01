import random
import itertools
from typing import List, Tuple
from core.utils import is_power_of_prime
from .field import Field

class Galois(Field):
    """Конечное поле многочленов GF*(q), q=p^m, p <= 29, m > 1, p - простое
    """
    def __init__(self, q: int):
        self.p, self.m = is_power_of_prime(q)
        # Удобно по индексу подгрузить данные из файликов для простого p
        with open(f"./tables/minimal_irreducibles_{self.p}.txt") as f:
            self.irreducable = f.readlines()[self.m - 2].strip()
        
        # Все значения приведённые к многочленам для итераций
        self.all_coeffs = [
            list(coeffs)
            for coeffs in itertools.product(
                [x for x in range(self.p)], repeat=self.m
            )
        ]
        
        self.max_size = ((2 * (self.m - 1) + 1)) # Вынес макс. длину результата перемножения полиномов
        self.devisor = self._to_coefficients(self.irreducable) # Неприводимый многочлен из таблицы
        
        self.g = self._find_primitive() # Примитивный элемент
        
        print("Неприводимый многочлен: ", self.irreducable)
        # print(self.devisor)
        
    def pow(self, a: List[int], n: List[int]) -> List[int]:
        """Возводит многочлен a в степень n в поле GF*(p^m)

        Аргументы:
            a (List[int]): Коэффициенты многочлена
            n (List[int]): Степень

        Возвращает:
            List[int]: Возведённый в степень многочлен
        """
        idx_n = self.all_coeffs.index(n) # Удобная конвертация полинома в число. Хотя можно было и попробовать из ССЧ конвертнуть в 10-ую
        # print(n, self.to_polynominal(n), idx_n, sep="\t\t")
        current = self.all_coeffs[1]
        
        # Такое же последовательное перемножение пока многочлен не встанет в свою нужную степень
        while idx_n > 0:
            coeffs = [0] * self.max_size
            for i, x1 in enumerate(current):
                for j, x2 in enumerate(a):
                    coeffs[i + j] = (coeffs[i + j] + x1 * x2) % self.p
            self._reduce(coeffs)
            current = coeffs[:]
            idx_n -= 1
        return current
        
    def _find_primitive(self) -> List[int]:
        """Находит случайный образующий элемент поля GF*(p^m)

        Возвращает:
            List[int]: Примитивный элемент
        """
        while True: # Пока хоть один не найдётся
            c = random.choice(self.all_coeffs[1:]) # Выбирается случайный из потенциальных примитивных элементов
            gained_coeffs = [self.all_coeffs[1]] # Для верификации что ничего не зациклилось и не повторяется вынуждены хранить историю 
            for i in range(1, len(self.all_coeffs)): # Пробег по всем коэффициентам
                coeffs = [0] * self.max_size # Резервация максимально возможного результата перемножения коэффициентов
                for i, x1 in enumerate(gained_coeffs[-1]): # Коэффициенты предыдущего элемента
                    for j, x2 in enumerate(c): # Коэффициенты кандидата на примитивный элемент
                        coeffs[i + j] = (coeffs[i + j] + x1 * x2) % self.p # Вычисление коэффициента
                self._reduce(coeffs) # Остаток от деления чтобы не вылезти за поле
                if coeffs in gained_coeffs: # Если такой элемент уже порождался - значит кандидат не подходит
                    break
                gained_coeffs.append(coeffs) # Сохраняем историю
            if len(gained_coeffs) == len(self.all_coeffs) - 1: # Если всё прошли - логичное завершение
                # print(gained_coeffs)
                return c
        
    def random_polynom(self) -> List[int]:
        """Случайный полином из поля GF(p^m)

        Возвращает:
            List[int]: Коэффициенты полинома
        """
        return random.choice(self.all_coeffs[1:])
        
    def _reduce(self, coeffs: List[int]):
        """Выполняет деление многочлена на неприводимый многочлен и возвращает остаток
        (остаток сохраняется в переданный coeffs)

        Аргументы:
            coeffs (List[int]): Коэффициенты в порядке от старшего к младшему
        """
        
        # Очистка от лишних нулей слева
        while coeffs and coeffs[0] == 0:
            coeffs.pop(0)
            
        # Пока степень делимого не меньше степени делителя
        while len(coeffs) >= len(self.devisor):
            
            # Старший коэффициент делимого
            lead = coeffs[0]
            for i in range(len(self.devisor)):
                coeffs[i] = (
                    (coeffs[i] - lead * self.devisor[i]) % self.p
                )
                
            # Удаление старшего члена
            coeffs.pop(0)
            
            # Очистка от ведущих нулей до нужного раз
            while coeffs and coeffs[0] == 0:
                coeffs.pop(0)
                
        # Дополнение остатка нулями слева до размера элемента поля
        while len(coeffs) < self.m:
            coeffs.insert(0, 0)
        
    def _to_coefficients(self, polynom: str) -> List[int]:
        """Переводит буквенное представление многочлена в список коэффициентов.

        Аргументы:
            polynom (str): Текстовое представление полинома
        
        Возвращает:
            List[int]: Список коэффициентов
        """
        polynom = map(str.strip, polynom.split("+"))
        coeffs = [0] * (self.m + 1)

        for i, x in enumerate(list(polynom)):
            # Жёский парсинг текста
            power = 0
            coef = 1
            if "*" in x:
                coef, x = map(str.strip, x.split("*"))
            if "^" in x:
                x, power = x.split("^")
            elif "x" in x:
                power = 1
            elif x.isdigit():
                coef = x
            # print(f"coef={coef}, x={x}, power={power}, {-1 * int(coef)}")

            # coeffs[len(coeffs) - int(power) - 1] = -1 * int(coef) % self.p
            coeffs[len(coeffs) - int(power) - 1] = int(coef)
            
        return coeffs
            
    def to_polynominal(self, coeffs: List[int]) -> str:
        """Переводит представление из коэффициентов в текстовый формат многочлена

        Аргументы:
            coeffs (List[int]): Список коэффициентов

        Возвращает:
            str: Текстовое представление
        """
        result = []
        n = len(coeffs)
        
        for i, coef in enumerate(coeffs):
            if coef == 0:
                continue
            
            power = n - i - 1
            if power == 0:
                result.append(str(coef))
            elif power == 1:
                result.append("x" if coef == 1 else f"{coef}x")
            # степень >= 2: x^k или kx^k
            else:
                result.append(f"x^{power}" if coef == 1 else f"{coef}x^{power}")
                
        if not(result):
            return "0"
        return " + ".join(result)