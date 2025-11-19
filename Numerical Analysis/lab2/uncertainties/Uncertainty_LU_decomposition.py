import numpy as np

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

def form_b_tilda(A: np.array, x: np.array) -> np.array:
    n = len(A)
    b_tilda = np.zeros(n)
    for i in range(n):
        res = 0
        for j in range(n):
            res += A[i][j] * x[j]
        b_tilda[i] = res
    return b_tilda

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
    print("Решение системы Ly = b:")
    for i in range(n):
        res = b[i]
        print(f"y[{i + 1}] = b[{i + 1}]", end="")
        for j in range(i):
            res -= L[i][j] * answers[j]
            print(f" - L[{i + 1},{j + 1}]*y[{j + 1}]", end="")
        answers[i] = res  # Не делим, т.к. L[i][i] = 1
        print(f" = {res:.10f}")
    return answers
    
def solve_Ux_equals_y(U: np.array, y: np.array) -> dict:
    n = len(U)
    answers = dict()
    print("Решение системы Ux = y:")
    for i in range(n - 1, -1, -1):
        res = y[i]
        print(f"x[{i + 1}] = (y[{i + 1}]", end="")
        for j in range(i + 1, n):
            res -= U[i][j] * answers[j]
            print(f" - U[{i + 1},{j + 1}]*x[{j + 1}]", end="")
        answers[i] = res / U[i][i]  # Делим на диагональный элемент U
        print(f") / U[{i + 1},{i + 1}] = {answers[i]:.10f}")
    return answers

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
    
    print("\n\n")
    print("Проверка:\nL * U")
    print_matrix(L.dot(U))
    print("Что совпадает с исходной матрицей A.")
    
    print()
    
    print("Решаем систему Ly=b (прямая подстановка)")
    y_dict = solve_Ly_equals_b(L, b)
    y = np.array([y_dict[i] for i in range(len(y_dict))])

    print("\nРешаем систему Ux=y (обратная подстановка)")
    x_dict = solve_Ux_equals_y(U, y)

    print(f"\nОкончательное решение:")
    for i in range(len(x_dict)):
        print(f"x{i + 1} = {x_dict[i]:.10f}")
        
    print()
        
    b_tilda = form_b_tilda(A, list(x_dict.values())[::-1])
    print("Найдём вектор погрешностей Δb = b̃ - b")
    b_delta = b - b_tilda
    print_line(b_delta)
    print("В качестве нормы выберем максимумы по модулю:")
    max_b_delta, max_b = max(map(abs, b_delta)), max(map(abs, b))
    print(f"max(||Δb||) = {max_b_delta:0.20f}")
    print(f"max(||b||) = {max_b}")
    print(f"Таким образом, погрешность решение δb = {max_b_delta / max_b:0.20f}")