import numpy as np

def swap_rows(matrix: np.array, i: int, j: int):
    temp = matrix[i].copy()
    matrix[i] = matrix[j]
    matrix[j] = temp
    
swaps = []
def swap_columns(matrix: np.array, i: int, j: int):
    global swaps
    for k in range(len(matrix)):
        matrix[k][i], matrix[k][j] = matrix[k][j], matrix[k][i]
    swaps.append((i, j))

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
        
def find_max(matrix: np.array, start: int) -> tuple[int, int, float]:
    i_res, j_res, maximum = start, start, abs(matrix[0][0])
    for i in range(start, len(matrix)):
        for j in range(start, len(matrix[i]) - 1):
            if abs(matrix[i][j]) > maximum:
                i_res = i
                j_res = j
                maximum = abs(matrix[i][j])
    return (i_res, j_res, maximum)

def trianglize(matrix: np.array) -> np.array:
    for i in range(len(matrix)):
        max_i, max_j, max_elem = find_max(matrix, i)
        print(f"Шаг {i + 1} прямого хода:\nРаботаем с {i + 1}-ой строкой. Ищем максимальный по модулю элемент в матрице:\n\
Максимальный элемент по модулю a{max_i + 1}{max_j + 1} = {max_elem}")
        print_matrix(matrix)
        show_after_perms = False
        if i == max_i:
            print("Перестановка строк не требуется.") 
        else:
            show_after_perms = True
            print(f"Переставим строки {i + 1} и {max_i + 1}.\n")
            swap_rows(matrix, i, max_i)

        if i == max_j:
            print("Перестановка столбцов не требуется.") 
        else:
            show_after_perms = True
            print(f"Переставим столбцы {i + 1} и {max_j+ 1}.")
            swap_columns(matrix, i, max_j)
        if show_after_perms:
            print("Матрица после перестановок")
            print_matrix(matrix)
            
        print("Перезапускаем вычисления для сохранения треугольной формы:")
        for k in range(i + 1):
            print(f"Делим {k + 1}-ю строку на диагональный элемент a[{k + 1},{k + 1}] = {matrix[k][k]}")
            matrix[k] /= matrix[k][k]
            print_matrix(matrix)
            for j in range(k + 1, len(matrix)):
                print(f"Вычитаем из {j + 1}-ой строки {k + 1}-ую строку умноженную на элемент a[{j + 1},{k + 1}] = {matrix[j][k]}")
                matrix[j] -= matrix[k] * matrix[j][k]
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
    print_matrix(AA)
    
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