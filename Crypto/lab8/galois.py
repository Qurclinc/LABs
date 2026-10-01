import itertools
from typing import List
from utils import is_power_of_prime, form_table

class Galois:
    """Конечное поле многочленов GF(q), q=p^m, p <= 29, m > 1, p - простое
    """
    def __init__(self, q: int):
        self.p, self.m = is_power_of_prime(q)
        # Удобно по индексу подгрузить данные из файликов для простого p
        with open(f"./tables/minimal_irreducibles_{self.p}.txt") as f:
            self.irreducable = f.readlines()[self.m - 2].strip()
        
        # Все значения приведённые к многочленам для итераций и подписи колонок
        self.all_coeffs = [
            list(coeffs)
            for coeffs in itertools.product(
                [x for x in range(self.p)], repeat=self.m
            )
        ]    
        self.devisor = self._to_coefficients(self.irreducable)
        self.primitive_element = self.find_primitive_element()
        
        print("Неприводимый многочлен: ", self.irreducable)
        print(self.devisor)
        
    def addition(self):
        """Строит таблицу сложений в поле GF(q)"""
        result = []
        
        # Итеративный пробег по всевозможным комбинациям коэффициентов при степенях многочлена
        for poly1 in self.all_coeffs:
            line = []
            for poly2 in self.all_coeffs:
                coeffs = [0] * self.m # Удобно сразу обозначить размер для доступа по индексам
                for i in range(self.m):
                    # Коэффициент при каждой степени в случае суммы равен сумме коэффициентов при той же степени слагаемых многочленов, взятые по модулю p
                    coeffs[i] = (poly1[i] + poly2[i]) % self.p 
                line.append(self._to_polynominal(coeffs))
            result.append(line)
            
        # Подписи на лету переводятся в буквенное представление для приличного отображения в таблице
        form_table(
            filename="PolyAddition",
            signs=[self._to_polynominal(c) for c in self.all_coeffs],
            result_data=result
        )
        
    def multiplication(self):
        """Строит таблицу произведений в поле GF(q)"""
        result = []
        # 2 * (m - 1) - максимальная степень которую можно получить ДО редукции (т.к. макстмально возможная степень - это сумма степеней старших членов)
        # +1 для учёта нулевой степени
        size = ((2 * (self.m - 1) + 1))
        
        # Такой же итеративный проход по всем возможным комбинациям
        for poly1 in self.all_coeffs:
            line = []
            for poly2 in self.all_coeffs:
                coeffs = [0] * size # Резервируем теоретически максимально возможное произведение
                # Для перемножения необходимо пробежаться по каждому коэффициенту и перемножить его на остальные
                for i, x1 in enumerate(poly1):
                    for j, x2 in enumerate(poly2):
                        # Сразу накопление с модулем чтобы операции были легче
                        coeffs[i + j] = (coeffs[i + j] + x1 * x2) % self.p 
                self._reduce(coeffs) # Возвращаемся в наше поле
                line.append(self._to_polynominal(coeffs))
            result.append(line)
            
        form_table(
            filename="PolyMultiplication",
            signs=[self._to_polynominal(c) for c in self.all_coeffs],
            result_data=result
        )
        
    def find_primitive_element(self):
        max_size = ((2 * (self.m - 1) + 1))
        for c in self.all_coeffs[1:]:
            gained_coeffs = [self.all_coeffs[1]]
            for i in range(1, len(self.all_coeffs)):
                coeffs = [0] * max_size
                for i, x1 in enumerate(gained_coeffs[-1]):
                    for j, x2 in enumerate(c):
                        coeffs[i + j] = (coeffs[i + j] + x1 * x2) % self.p
                self._reduce(coeffs)
                if coeffs in gained_coeffs:
                    break
                gained_coeffs.append(coeffs)
            if len(gained_coeffs) == len(self.all_coeffs) - 1:
                # print(c)
                return c
        return None
        
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
            
    def _to_polynominal(self, coeffs: List[int]) -> str:
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