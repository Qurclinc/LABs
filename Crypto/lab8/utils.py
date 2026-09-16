import pandas as pd
import operator
from typing import List, Tuple

MAPPING = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" # Да есть библиотечная версия но я решил так.
OPERATIONS = {
    "Addition": operator.add,
    "Multiplication": operator.mul
}
ALLOWED_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

def number_to_letter(num: int) -> str:
    """Осуществляет перевод числа в буквенное представление. Латинский алфавит, формат как в 
    Excel: при ячейке за длиной алфавита, первая буква дублируется и так далее

    Аргументы:
        num (int): Целое число для конвертации

    Возвращает:
        str: Текстовое представление
    """
    chars = []
    num += 1 # Для базы с 0. Иначе A=1 а не A=0
    while num > 0:
        # А вот тут надо делать num-1 чтобы в итоге получать при выходе за длину алфавита двойные буквы и так далее
        num, remainder = divmod(num - 1, 26)
        chars.append(MAPPING[remainder])
    return "".join(reversed(chars))

def form_table(
    filename: str,
    signs: List[str | int],
    result_data: List[List[str | int]]
):
    """Запись результирующей таблицы в файл .csv с использованием модуля работы с данными Pandas

    Аргументы:
        filename (str): Имя файла без расширения. .cvs допишется автоматически
        signs (List[str  |  int]): Список текста для подписей. Они симметричные
        result_data (List[List[str  |  int]]): Данные полученные в программе
    """
    df = pd.DataFrame(result_data, index=signs, columns=signs)
    df.to_csv(f"out/{filename}.csv", index=True)
    

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