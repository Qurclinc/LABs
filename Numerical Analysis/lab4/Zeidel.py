from copy import deepcopy
import sympy as sp
import numpy as np

def check_condition():
    print("Необходимое условие сходимости метода Гаусса-Зейделля.\n\n")
    lam = sp.symbols("λ")
    A = sp.Matrix([
        [76.0, 21.0, 6.0, -34.0],
        [12.0, -114.0, 8.0, 9.0],
        [16.0, 24.0, -100.0, -35.0],
        [23.0, -8.0, 5.0, -75.0]
    ])
    N = A.shape[0]
    matrix = deepcopy(A)
    for i in range(N):
        for j in range(N):
            if j < i:
                matrix[i, j] = A[i, j] * lam
            elif j == i:
                matrix[i, j] = A[i, j] * lam
    
    sp.pprint(matrix)
    
    det = matrix.det()
    print("\nНеобходимо решить уравнение:\n\n")
    sp.pprint(det)
    
    roots = [root for root in sp.solve(det, lam) if root.is_real]
    if roots:
        for root in roots:
            print(f"{root:.12f} {'< 1' if root < 1 else ''}")
    else:
        print("Действительных корней нет.")

def print_line(k: int, max_delta: int, x: np.ndarray):
    if k == 0:
            delta_str = "N/A"
    elif max_delta < 1e-4:
        delta_str = f"{max_delta:.2e}"
    else:
        delta_str = f"{max_delta:.8f}"
    
    # Форматированный вывод
    print(f"{k:^3} | {x[0]:^12.8f} | {x[1]:^12.8f} | {x[2]:^12.8f} | {x[3]:^12.8f} | {delta_str:^20}")

def gauss_seidel(
    A: np.ndarray, b: np.ndarray, x0: np.ndarray, E: float = 10**-6, max_iterations: int = 30
):
    
    N = len(b)
    x = x0.copy()
    x_new = x.copy()
    history = []
    
    print("МЕТОД ГАУССА-ЗЕЙДЕЛЯ (Формула 1)")
    print(f"{'k':^3} | {'x1':^12} | {'x2':^12} | {'x3':^12} | {'x4':^12} | {'max|Δx|':^20}")
    print("-" * 85)
    print(f"{0:^3} | {x[0]:^12.4f} | {x[1]:^12.4f} | {x[2]:^12.4f} | {x[3]:^12.4f} | {'-':^20}")
    
    for iter in range(1, max_iterations + 1):
        x_old = x.copy()
        
        for i in range(N):
            sum_news = sum([A[i][j] * x_new[j] for j in range(i)])
            sum_olds = sum([A[i][j] * x_old[j] for j in range(i + 1, N)])
            x_new[i] = (b[i] - sum_news - sum_olds) / A[i][i]

        x = x_new.copy()
        history.append(x)
        max_delta = np.max(np.abs(x - x_old))
        print_line(iter, max_delta, x)
        
        if max_delta < E:
            print("-" * 85)
            print(f"Сходимость достигнута на {iter}-й итерации (ε = {E})")
            break
    
    return x, history

def gauss_seidel_matrix(
    A: np.ndarray, b: np.ndarray, x0: np.ndarray, E: float = 10 ** -6, max_iterations: int = 30
):
    N = len(b)
    x = sp.Matrix(x0.copy())
    x_new = x.copy()
    
    L = sp.Matrix(np.tril(A, -1))
    D = sp.Matrix(np.diag(np.diag(A)))
    R = sp.Matrix(np.triu(A, 1))
    b = sp.Matrix(b)
    
    print("МЕТОД ГАУССА-ЗЕЙДЕЛЯ (Матричная формула)")
    print(f"{'k':^3} | {'x1':^12} | {'x2':^12} | {'x3':^12} | {'x4':^12} | {'max|Δx|':^20}")
    print("-" * 85)
    print(f"{0:^3} | {x[0]:^12.4f} | {x[1]:^12.4f} | {x[2]:^12.4f} | {x[3]:^12.4f} | {'N/A':^20}")
    
    DL_rev = (D + L).inv()
    B = -1 * DL_rev * R
    C = DL_rev * b
    
    for iter in range(1, max_iterations):
        x_old = x.copy()
        
        x_new = B * x_old + C
        
        x = x_new.copy()
        max_delta = np.max(np.abs(x - x_old))
        print_line(iter, max_delta, x)
        
        if max_delta < E:
            print("-" * 85)
            print(f"Сходимость достигнута на {iter}-й итерации (ε = {E})")
            break
    return x
    

def main():
    A = np.array([
        np.array([76.0, 21.0, 6.0, -34.0]),
        np.array([12.0, -114.0, 8.0, 9.0]),
        np.array([16.0, 24.0, -100.0, -35.0]),
        np.array([23.0, -8.0, 5.0, -75.0])
    ])
    b = np.array([-142.0, 83.0, -121.0, 85.0])
    check_condition()
    
    print("\n\n\n")
    x0 = b.copy()
    # x0 = np.array([1.0, 1.0, 1.0, 1.0])
    # x0 = np.zeros(len(b))
    
    solution, history = gauss_seidel(A, b, x0)
    print(f"\n\nРешение системы:\n")
    for i, val in enumerate(solution):
        print(f"x{i + 1} = {val}")
    
    print("\n\n\n\n")
    
    solution = gauss_seidel_matrix(A, b, x0)
    for i, val in enumerate(solution):
        print(f"x{i + 1} = {val}")
    

if __name__ == "__main__":
    main()