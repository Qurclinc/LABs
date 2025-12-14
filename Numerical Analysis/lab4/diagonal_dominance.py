import numpy as np

def check_rows(A: np.ndarray, b: np.ndarray):
    print("\n1. Проверка диагонального преобладания по СТРОКАМ:")
    row_dominance = True

    for i in range(len(A[0])):
        diag_elem = abs(A[i, i])
        row_sum = sum([abs(x) for x in A[i]]) - diag_elem
        
        condition = diag_elem > row_sum
        row_dominance = row_dominance and condition
        
        print(f"Строка {i+1}: |{A[i, i]:3}| = {diag_elem:3} > {row_sum:3} = Σ|остальные|? {'ДА' if condition else 'НЕТ'}")

    print(f"\nИтог по строкам: Диагональное преобладание — {'ДА' if row_dominance else 'НЕТ'}")

def check_cols(A: np.ndarray, b: np.ndarray):
    print("\n\n2. Проверка диагонального преобладания по СТОЛБЦАМ:")
    col_dominance = True
    N = len(A[0])
    
    for i in range(N):
        diag_elem = abs(A[i, i])
        # col_sum = np.sum(np.abs(A[:, j])) - diag_elem
        col_sum = sum([abs(A[j][i]) for j in range(N)]) - diag_elem
        
        condition = diag_elem > col_sum
        col_dominance = col_dominance and condition
        
        print(f"Столбец {i+1}: |{A[i, i]:4}| = {diag_elem:3} > {col_sum:3} = Σ|остальные|? {'ДА' if condition else 'НЕТ'}")

    print(f"\nИтог по столбцам: Диагональное преобладание — {'ДА' if col_dominance else 'НЕТ'}")

def main():
    A = np.array([
        [76, 21, 6, -34],
        [12, -114, 8, 9],
        [16, 24, -100, 35],
        [23, -8, 5, -75]
    ])

    b = np.array([-142, 83, -121, 85])
    check_rows(A, b)
    check_cols(A, b)


if __name__ == "__main__":
    main()