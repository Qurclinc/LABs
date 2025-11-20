import numpy as np

def print_matrix(matrix: np.array):
    for line in matrix:
        for elem in line:
            print(f"{elem:0.10f}", end="\t")
        print()
    print()

def find_det(matrix: np.array) -> float:
    mult = 1
    for i in range(len(matrix)):
        mult *= matrix[i][i]
        print(f"Шаг {i + 1}:\nРаботаем с диагональным элементом a[{i},{i}] = {matrix[i][i]}")
        print(f"Текущее произведение: {mult}")
        # print(f"Шаг {i + 1} прямого хода:\nДелим {i + 1}-ю строку на коэффициент a{i + 1}{i + 1} = {matrix[i][i]}")
        matrix[i] /= matrix[i][i]
        for j in range(i + 1, len(matrix)):
            # print(f"Вычисляем коэффициенты. Для этого вычитаем из {j + 1}-ой строки {i + 1}-ую строку умноженную на элемент a{j + 1}{i + 1} = {matrix[j][i]}")
            matrix[j] -= matrix[i] * matrix[j][i]
        print(f"Матрица после шага {i + 1}: ")
        print_matrix(matrix)
    return mult
        

if __name__ == "__main__":
    
    A = np.array([
        np.array([0.12, -1.14, 0.08, 0.09]),
        np.array([0.16, 0.24, -1, -0.35]),
        np.array([0.23, -0.08, 0.05, -0.75]),
        np.array([-0.86, 0.23, 0.18, 0.17])
    ])
    
    print("Метод Гаусса без выбора\ndet⁡〖A)=a_11∙det⁡〖A^((1))=a_11∙a_22^((1) )∙det⁡〖A^((2))=a_11∙a_22^((1) )∙…∙a_nn^((n-1)")
    det_A = find_det(A)
    print(f"Итоговый определитель: {det_A:0.20f}")