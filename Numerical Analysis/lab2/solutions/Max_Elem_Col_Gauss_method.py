import numpy as np

def swap_rows(matrix: np.array, i: int, j: int):
    temp = matrix[i].copy()
    matrix[i] = matrix[j]
    matrix[j] = temp

def print_matrix(matrix: np.array):
    for line in matrix:
        for elem in line:
            print(f"{elem:0.10f}", end="\t")
        print()
    print()
        
def find_max_in_column(line: np.array) -> tuple[int, float]:
    index, maximum = 0, line[0]
    for i, elem in enumerate(line):
        if elem > maximum:
            maximum = elem
            index = i
    return (maximum, index)

def trianglize(matrix: np.array) -> np.array:
    print_matrix(matrix)
    for i in range(len(matrix)):
        column = []
        for j in range(i, len(matrix)):
            column.append(abs(float(matrix[j][i])))
        max_elem, max_index = find_max_in_column(column)
        max_index += i
        print(f"Шаг {i + 1} прямого хода:\nРаботаем с {i + 1}-ым столбцом. Ищем максимальный по модулю элемент в столбце {i + 1}:\n\
Столбец: {' '.join(map(str, column))}\nМаксимальный элемент по модулю: {max_elem} в строке {max_index + 1}")
        if i == max_index:
            print("Перестановка не требуется.") 
        else:
            swap_rows(matrix, i, max_index)
            print(f"Переставим строки {i + 1} и {max_index + 1}.\n")
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

if __name__ == "__main__":
    A = np.array([
        np.array([0.12, -1.14, 0.08, 0.09, 0.83]),
        np.array([0.16, 0.24, -1, -0.35, -1.21]),
        np.array([0.23, -0.08, 0.05, -0.75, -0.65]),
        np.array([-0.86, 0.23, 0.18, 0.17, 1.42])
    ])
    print("Прямой ход:\n\n")
    AA = trianglize(A)
    
    res = reverse(AA)
    # res = normalize_answers(res)
    print("Обратный ход:")
    for k, v in res.items():
        print(f"x{k + 1} = {float(v)}")
    print()
    print(f"Решение СЛАУ: ({', '.join([i for i in map(str, res.values())][::-1])})")