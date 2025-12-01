import numpy as np

# Исходные данные из матрицы
A = np.array([
    np.array([1.984, 0.588, 0, 0, 0]),
    np.array([0.951, 6.697, 0.628, 0, 0]),
    np.array([0, 1.257, 15.875, 2.153, 0]),
    np.array([0, 0, 5.027, 31.006, 4.398]),
    np.array([0, 0, 0, -0.951, 53.579])
])

d = np.array([28.05, 80.829, 5.081, 3.579, 1])

n = len(A)

# print(np.linalg.solve(A, d))

# Извлекаем диагонали
a = np.zeros(n)  # нижняя побочная диагональ
b = np.zeros(n)  # главная диагональ
c = np.zeros(n)  # верхняя побочная диагональ

for i in range(n):
    b[i] = A[i][i]  # главная диагональ
    if i > 0:
        a[i] = A[i][i - 1]  # элемент под главной диагональю
    if i < n - 1:
        c[i] = A[i][i + 1]  # элемент над главной диагональю

print(f"Главная диагональ: {b}")
print(f"Нижняя диагональ: {a}")
print(f"Верхняя диагональ: {c}\n")

# alpha_prev = 0.0
# beta_prev = 0.0

# print(f"ШАГ 0 (начальные значения):")
# print(f"  α₋₁ = {alpha_prev:.5f}")
# print(f"  β₋₁ = {beta_prev:.5f}")

# 1.1 Вычисление прогоночных коэффициентов
alpha = np.zeros(n + 1)
beta =  np.zeros(n + 1)

#alpha[0] = -1 * (c[0] / b[0])
#beta[0] = d[0] / b[0]

# print(f"Начальные значения:")
# print(f"  α₁ = -c[1] / b1 = {alpha[0]:.5f}")
# print(f"  β₁ = d[1] / b[1] = {beta[0]:.5f}")

# Вычисляем прогоночные коэффициенты для всех i от 0 до n-1
for i in range(0, n):
    print(f"\nШАГ i = {i + 1}:")
    
    denominator = a[i] * alpha[i] + b[i]
    alpha[i + 1] = -c[i] / denominator
    beta[i + 1] = (d[i] - a[i] * beta[i]) / denominator

    print(f"  Знаменатель = b[{i + 1}] + a[{i + 1}]·α[{i}] = {b[i]:.5f} + {a[i]:.5f}·{alpha[i]:.5f}")
    print(f"                = {b[i]:.5f} + {a[i] * alpha[i]:.5f} = {denominator:.5f}")
    print(f"  α[{i + 1}] = -c[{i + 1}] / b[{i + 1}] + a[{i + 1}]·α[{i}] = -{c[i]:.5f} / {denominator:.5f} = {alpha[i + 1]:.5f}")
    print(f"  β[{i + 1}] = (d[{i + 1}] - a[{i + 1}]·β[{i}]) / b[{i + 1}] + a[{i + 1}]·α[{i}]")
    print(f"         = ({d[i]:.5f} - {a[i]:.5f}·{beta[i]:.5f}) / {denominator:.5f}")
    print(f"         = ({d[i]:.5f} - {a[i] * beta[i]:.5f}) / {denominator:.5f} = {beta[i + 1]:.5f}")

print(f"\nВектор α: {[f'{val:.5f}' for val in alpha[1:]]}")
print(f"Вектор β: {[f'{val:.5f}' for val in beta[1:]]}")

# 1.2 Вычисление вектора решения (обратный ход)
x = np.zeros(n)
# x[n - 1] = (d[n - 1] - a[n - 1] * beta[n - 1]) / (a[n - 1] * alpha[n - 1] + b[n - 1])
x[n - 1] = beta[n]

for i in range(n - 2, -1, -1):
    x[i] = alpha[i + 1] * x[i + 1] + beta[i + 1]

print("Прогоночные коэффициенты:")
for i in range(1, n + 1):
    print(f"α{i} = {round(alpha[i], 5):.5f}, β{i} = {round(beta[i], 5):.5f}")

print("\nРешение системы:")
for i in range(n):
    print(f"x{i + 1} = {round(x[i], 5):.5f}")


print("ОЦЕНКА ПОГРЕШНОСТИ ПО ПРАВОЙ ЧАСТИ")

# Вычисление вектора невязки
delta_b = np.dot(A, x) - d

print("\nВектор невязки Δb:")
for i in range(n):  
    print(f"Δb{i + 1} = {delta_b[i]:.20f}")


# # Вычисление норм (норма-максимум)
norm_delta_b = max(abs(val) for val in delta_b)
norm_d = max(abs(val) for val in d)

# Относительная погрешность
delta_b_rel = norm_delta_b / norm_d

print(f"\nНорма невязки ||Δb|| = {norm_delta_b:.20f}")
print(f"Норма правой части ||d|| = {norm_d:.20f}")
print(f"Относительная погрешность δb = {delta_b_rel:.20f}")
print(f"Относительная погрешность в процентах: {delta_b_rel * 100:.10f}%")
