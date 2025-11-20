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
        # print(f"Вычисление {i + 1}-го столбца матриц L и U:")
        for j in range(n):
            if i <= j:
                tmp = 0
                for k in range(i):
                    tmp += L[i][k] * U[k][j]
                U[i][j] = A[i][j] - tmp
                # print(f"U[{i + 1},{j + 1}] = A[{i + 1},{j + 1}] - ΣL[{i + 1},k]*U[k,{j + 1}] = {U[i][j]}")
            if i > j:
                tmp = 0
                for k in range(j):
                    tmp += L[i][k] * U[k][j]
                L[i][j] = (A[i][j] - tmp) / U[j][j]
                # print(f"L[{i + 1},{j + 1}] = (A[{i + 1},{j + 1}] - ΣL[{i + 1},k]*U[k,{j + 1}]) / U[{j + 1}{j + 1}] = {L[i][j]}")
    return L, U

def find_det(matrix: np.array) -> float:
    mult = 1
    for i in range(len(matrix)):
        print(f"u[{i},{i}] = {matrix[i][i]}")
        mult *= matrix[i][i]
    return mult

if __name__ == "__main__":
    
    A = np.array([
        np.array([0.12, -1.14, 0.08, 0.09]),
        np.array([0.16, 0.24, -1, -0.35]),
        np.array([0.23, -0.08, 0.05, -0.75]),
        np.array([-0.86, 0.23, 0.18, 0.17])
    ])
    
    b = np.array([0.83, -1.21, -0.65, 1.42])
    
    print("Метод LU-разложения\ndet(A) = det(L) * det(U) = 1 * (u11 * u22 * u33 * u44), где uii - диагональные элементы U")
    
    _, U = build_LU_matrix(A)
    
    print("Итоговая матрица U:")
    print_matrix(U)
    
    det_A = find_det(U)
    print(f"Итоговый определитель: {det_A:0.20f}")