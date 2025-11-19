import numpy as np

swaps = []

def print_matrix(matrix: np.array):
    for line in matrix:
        for elem in line:
            print(f"{elem:0.10f}", end="\t")
        print()
    print()
    
    
def print_line(line: np.array):
    for elem in line:
        print(f"{elem:0.20f}", end="\t")
    print()

def swap_columns(matrix: np.array, i: int, j: int):
    global swaps
    for k in range(len(matrix)):
        matrix[k][i], matrix[k][j] = matrix[k][j], matrix[k][i]
    swaps.append((i, j))
        
def find_max_in_line(line: np.array) -> tuple[int, float]:
    index, maximum = 0, line[0]
    for i, elem in enumerate(line):
        if elem > maximum:
            maximum = elem
            index = i
    return (maximum, index)

def trianglize(matrix: np.array) -> np.array:
    for i in range(len(matrix)):
        line = list(map(float, map(abs, matrix[i][:len(matrix)])))
        max_elem, max_index = find_max_in_line(line)
        print(f"Шаг {i + 1} прямого хода:\nРаботаем с {i + 1}-ой строкой. Ищем максимальный по модулю элемент в строке {i + 1}:\n\
Строка: {' '.join(map(str, matrix[i][:len(matrix)]))}\nМаксимальный элемент по модулю: {max_elem} в столбце {max_index + 1}")
        if i == max_index:
            print("Перестановка не требуется.") 
        else:
            print(f"Переставим столбцы {i + 1} и {max_index + 1}.")
            swap_columns(matrix, i, max_index)
        matrix[i] /= matrix[i][i]
        print_matrix(matrix)
        for j in range(i + 1, len(matrix)):
            print(f"Вычисляем коэффициенты. Для этого вычитаем из {j + 1}-ой строки {i + 1}-ую строку умноженную на элемент a{j + 1}{i + 1} = {matrix[j][i]}")
            matrix[j] -= matrix[i] * matrix[j][i]
            print_matrix(matrix)
    return matrix

def reverse(matrix: np.array) -> np.array:
    print("Таким образом, получаем СЛАУ вида:")
    print_matrix(matrix)
    answers = dict()
    for i in range(len(matrix) - 1, -1, -1):
        res = matrix[i][-1]
        for j in range(len(matrix)):
            if answers.get(j):
                res -= matrix[i][j] * answers[j]
        answers[i] = res
    
    return answers

def normalize_answers(answers: dict) -> dict:
    global swaps
    n = len(answers)
    
    # Определяем, где оказалась каждая переменная после всех перестановок
    positions = list(range(n))
    for i, j in swaps:
        positions[i], positions[j] = positions[j], positions[i]
    
    # Теперь positions[i] показывает, какая исходная переменная находится на i-й позиции
    # Нам нужно обратное отображение
    reverse_map = {positions[i]: i for i in range(n)}
    
    correct_answers = {}
    for i in range(n):
        correct_answers[i] = answers[reverse_map[i]]
    
    return correct_answers

def form_b_tilda(A: np.array, x: np.array) -> np.array:
    n = len(A)
    b_tilda = np.zeros(n)
    for i in range(n):
        res = 0
        for j in range(n):
            res += A[i][j] * x[j]
        b_tilda[i] = res
    return b_tilda

if __name__ == "__main__":
    src = np.array([
        np.array([0.12, -1.14, 0.08, 0.09, 0.83]),
        np.array([0.16, 0.24, -1, -0.35, -1.21]),
        np.array([0.23, -0.08, 0.05, -0.75, -0.65]),
        np.array([-0.86, 0.23, 0.18, 0.17, 1.42])
    ])
    
    A = np.array([
        np.array([0.12, -1.14, 0.08, 0.09]),
        np.array([0.16, 0.24, -1, -0.35]),
        np.array([0.23, -0.08, 0.05, -0.75]),
        np.array([-0.86, 0.23, 0.18, 0.17])
    ])
    
    b = np.array([0.83, -1.21, -0.65, 1.42])
    
    print("Прямой ход:\n\n")
    AA = trianglize(src)
    
    res = reverse(AA)
    res = normalize_answers(res)
    print("Обратный ход:")
    for k, v in res.items():
        print(f"x{k + 1} = {float(v)}")
    print()
    print(f"Решение СЛАУ: ({', '.join([i for i in map(str, res.values())])})")
    print()
    
    b_tilda = form_b_tilda(A, res)
    print("Найдём вектор погрешностей Δb = b̃ - b")
    b_delta = b - b_tilda
    print_line(b_delta)
    print("В качестве нормы выберем максимумы по модулю:")
    max_b_delta, max_b = max(map(abs, b_delta)), max(map(abs, b))
    print(f"max(||Δb||) = {max_b_delta:0.20f}")
    print(f"max(||b||) = {max_b}")
    print(f"Таким образом, погрешность решение δb = {max_b_delta / max_b:0.20f}")