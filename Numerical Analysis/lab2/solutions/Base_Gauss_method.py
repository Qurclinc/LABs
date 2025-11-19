import numpy as np

def print_matrix(matrix: np.array):
    for line in matrix:
        for elem in line:
            print(f"{elem:0.10f}", end="\t")
        print()
    print()

def trianglize(matrix: np.array) -> np.array:
    for i in range(len(matrix)):
        print(f"Шаг {i + 1} прямого хода:\nДелим {i + 1}-ю строку на коэффициент a{i + 1}{i + 1} = {matrix[i][i]}")
        matrix[i] /= matrix[i][i]
        print_matrix(matrix)
        for j in range(i + 1, len(matrix)):
            print(f"Вычисляем коэффициенты. Для этого вычитаем из {j + 1}-ой строки {i + 1}-ую строку умноженную на элемент a{j + 1}{i + 1} = {matrix[j][i]}")
            matrix[j] -= matrix[i] * matrix[j][i]
            print_matrix(matrix)
    return matrix

def reverse(matrix: np.array) -> dict:
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
    print("Обратный ход:")
    for k, v in reversed(res.items()):
        print(f"x{k + 1} = {float(v)}")
    print()
    print(f"Решение СЛАУ: ({', '.join([i for i in map(str, res.values())][::-1])})")