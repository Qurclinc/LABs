import sympy as sp
import numpy as np

def print_line(max_delta: float, k: int, x: np.ndarray):
    if max_delta == 0:
        delta_str = "0.0"
    elif max_delta >= 0.01:
        delta_str = f"{max_delta:.4f}"
    elif max_delta >= 1e-4:
        delta_str = f"{max_delta:.6f}"
    elif max_delta >= 1e-6:
        delta_str = f"{max_delta:.2e}".replace('e-0', 'e-')
    else:
        delta_str = f"{max_delta:.2e}".replace('e-0', 'e-')
    
    print(f"{k:^3} | {x[0]:^12.6f} | {x[1]:^12.6f} | {x[2]:^12.6f} | {x[3]:^12.6f} | {delta_str:^20}")

def check_condition():
    print("Необходимое условие сходимости метода Якоби.\n\n")
    lam = sp.symbols("λ")
    A = sp.Matrix([
        [76.0 * lam, 21.0, 6.0, -34.0],
        [12.0, -114.0 * lam, 8.0, 9.0],
        [16.0, 24.0, -100.0 * lam, -35.0],
        [23.0, -8.0, 5.0, -75.0 * lam]
    ])
    
    print("Необходимо найти определитель матрицы:\n")
    sp.pprint(A)
    
    print("\n\nПриравнять его к нулю и найти значение λ\n")
    det = sp.simplify(A.det())
    sp.pprint(det)
    
    roots = [root for root in sp.solve(det, lam) if root.is_real]
    
    if roots:
        for root in roots:
            print(root)
    else:
        print("Нет действительных корней.")
    
def jacobi(A: np.ndarray, b: np.ndarray, x0: np.ndarray, E: float = 10**-6, max_iterations: int = 30):
    
    N = len(b)
    x = x0.copy()
    x_new = np.zeros_like(x)
    history = [x0.copy()]
    
    print("=" * 85)
    print(f"{'k':^3} | {'x1':^12} | {'x2':^12} | {'x3':^12} | {'x4':^12} | {'max|Δx|':^20}")
    print("-" * 85)
    print(f"{0:^3} | {x[0]:^12.4f} | {x[1]:^12.4f} | {x[2]:^12.4f} | {x[3]:^12.4f} | {'-':^20}")
    
    for iter in range(1, max_iterations + 1):
        x_old = x.copy()
        
        for i in range(N):
            sum_i = sum([A[i][j] * x_old[j] for j in range(N) if i != j])
            x_new[i] = (b[i] - sum_i) / A[i][i]
                
        x = x_new.copy()
        history.append(x.copy())
        max_delta = np.max(np.abs(x - x_old))
        
        print_line(max_delta, iter, x)
        if max_delta < E:
            print("-" * 85)
            print(f"Сходимость достигнута на {iter}-й итерации (ε = {E})")
            break
        
    return x, history

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
    solution, history = jacobi(A, b, x0)
    print(f"\n\nРешение системы:\n")
    for i, val in enumerate(solution):
        print(f"x{i + 1} = {val}")
    

if __name__ == "__main__":
    main()