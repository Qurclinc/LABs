from utils import number_to_letter, form_table, OPERATIONS

def build_field(
    p: int,
    is_letters: bool = False
):
    """Строит конечное поле. Валидация на простоту значения p не осуществляется, допуская что
    оно изначально простое. В ином случае, алгоритм не упадёт, но в таблице появятся делители нуля

    Аргументы:
        p (int): Простое число
        is_letters (bool, optional): Режим работы. Если True, то с буквами. Изначально с цифрами
    """
    for name, operation in OPERATIONS.items():
        result = []
        signs = []
        for x in range(p):
            val = number_to_letter(x) if is_letters else x
            line = []
            signs.append(val)
            for y in range(p):
                value = operation(x, y) % p
                value = number_to_letter(value) if is_letters else value
                line.append(value)
            result.append(line)
        form_table(filename=name, signs=signs,  result_data=result)
