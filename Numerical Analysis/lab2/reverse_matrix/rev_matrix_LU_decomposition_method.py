import numpy as np

def print_matrix(matrix: np.array):
    for line in matrix:
        for elem in line:
            print(f"{elem:0.10f}", end="\t")
        print()
    print()

def build_LU_matrix(A: np.array):
    n = len(A)
    L, U = np.zeros((n, n)), np.zeros((n, n))
    for i in range(n):
        L[i][i] = 1
    
    for i in range(n):
        print(f"Вычисление {i + 1}-го столбца матриц L и U:")
        for j in range(n):
            if i <= j:
                tmp = 0
                for k in range(i):
                    tmp += L[i][k] * U[k][j]
                U[i][j] = A[i][j] - tmp
                print(f"U[{i + 1},{j + 1}] = A[{i + 1},{j + 1}] - ΣL[{i + 1},k]*U[k,{j + 1}] = {U[i][j]}")
            if i > j:
                tmp = 0
                for k in range(j):
                    tmp += L[i][k] * U[k][j]
                L[i][j] = (A[i][j] - tmp) / U[j][j]
                print(f"L[{i + 1},{j + 1}] = (A[{i + 1},{j + 1}] - ΣL[{i + 1},k]*U[k,{j + 1}]) / U[{j + 1}{j + 1}] = {L[i][j]}")
    return L, U

def solve_Ly_equals_b(L: np.array, b: np.array) -> dict:
    n = len(L)
    answers = dict()
    # print("Решение системы Ly = b:")
    for i in range(n):
        res = b[i]
        # print(f"y[{i + 1}] = b[{i + 1}]", end="")
        for j in range(i):
            res -= L[i][j] * answers[j]
            # print(f" - L[{i + 1},{j + 1}]*y[{j + 1}]", end="")
        answers[i] = res  # Не делим, т.к. L[i][i] = 1
        # print(f" = {res:.10f}")
    return answers
    
def solve_Ux_equals_y(U: np.array, y: np.array) -> dict:
    n = len(U)
    answers = dict()
    # print("Решение системы Ux = y:")
    for i in range(n - 1, -1, -1):
        res = y[i]
        # print(f"x[{i + 1}] = (y[{i + 1}]", end="")
        for j in range(i + 1, n):
            res -= U[i][j] * answers[j]
            # print(f" - U[{i + 1},{j + 1}]*x[{j + 1}]", end="")
        answers[i] = res / U[i][i]  # Делим на диагональный элемент U
        # print(f") / U[{i + 1},{i + 1}] = {answers[i]:.10f}")
    return answers

def find_reverse_matrix_LU(L: np.array, U: np.array) -> np.array:
    n = len(L)
    rev_A = np.zeros((n, n))
    for i in range(n):
        Ei = np.zeros(n)
        Ei[i] = 1
        # print("Решаем систему Ly=b (прямая подстановка)")
        y_dict = solve_Ly_equals_b(L, Ei)
        y = np.array([y_dict[i] for i in range(len(y_dict))])

        # print("\nРешаем систему Ux=y (обратная подстановка)")
        x_dict = solve_Ux_equals_y(U, y)

        # print(f"\nОкончательное решение:")
        X = []
        for j in range(len(x_dict)):
            rev_A[j][i] = x_dict[j]
            # print(f"x{j + 1} = {x_dict[j]:.10f}")
            X += [x_dict[j]]
        print(f"X{i + 1} = {X}")
        
    return rev_A

if __name__ == "__main__":
    
    A = np.array([
        np.array([0.12, -1.14, 0.08, 0.09]),
        np.array([0.16, 0.24, -1, -0.35]),
        np.array([0.23, -0.08, 0.05, -0.75]),
        np.array([-0.86, 0.23, 0.18, 0.17])
    ])
    
    b = np.array([0.83, -1.21, -0.65, 1.42])
    
    print("Представим матрицу A в виде произведение нижней треугольной матрицы L и верхней треугольной матрицы U:\nA = L * U")
    L, U = build_LU_matrix(A)
    print("Итоговая матрица L:")
    print_matrix(L)
    print("Итоговая матрица U:")
    print_matrix(U)
    
    print()
    print("Структура обратной матрицы: ")
    rev_A = find_reverse_matrix_LU(L, U)
    print()
    print("Полученная обратная матрица: ")
    print_matrix(rev_A)
    
    print("Проверка: A * A^-1 = E")
    print_matrix(A.dot(rev_A))