import numpy as np

def trianglize(matrix: np.array) -> np.array:
    for i in range(len(matrix)):
        matrix[i] /= matrix[i][i]
        for j in range(i + 1, len(matrix)):
            print(f"Вычисляем коэффициенты. Для этого вычитаем из {j + 1}-ой строки {i + 1}-ую строку умноженную на элемент a{j + 1}{i + 1} = {matrix[j][i]}")
            matrix[j] -= matrix[i] * matrix[j][i]
    return matrix

def reverse(matrix: np.array) -> dict:
    answers = dict()
    for i in range(len(matrix) - 1, -1, -1):
        res = matrix[i][-1]
        for j in range(len(matrix)):
            if answers.get(j):
                res -= matrix[i][j] * answers[j]
        answers[i] = res
    return answers

def solve_gauss(A: np.array):
    result = reverse(trianglize(A))
    solution = dict()
    for k, v in reversed(result.items()):
        solution[k] = float(v)
    return solution
