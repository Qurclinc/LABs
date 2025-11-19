from Point3D import Point3D

def main():
    
    # 1. Создание точек
    print("1. СОЗДАНИЕ ТОЧЕК:")
    p1 = Point3D(1, 2, 3)
    p2 = Point3D(4, 5, 6)
    print(f"p1 = {p1}")
    print(f"p2 = {p2}")
    print()
    
    # 2. Демонстрация дескрипторов (валидация)
    print("2. ДЕСКРИПТОРЫ - ВАЛИДАЦИЯ ТИПОВ:")
    try:
        p1.x = "не число"  # Должно вызвать ошибку
    except TypeError as e:
        print(f"Ошибка при установке строки: {e}")
    
    try:
        p1.x = 10.5  # Корректное значение
        print(f"Корректное значение установлено: p1.x = {p1.x}")
    except TypeError as e:
        print(f"Ошибка: {e}")
    print()
    
    # 3. Сложение
    print("3. СЛОЖЕНИЕ:")
    p3 = p1 + p2
    print(f"p1 + p2 = {p3}")
    
    p1 += p2
    print(f"p1 += p2 → {p1}")
    print()
    
    # 4. Вычитание  
    print("4. ВЫЧИТАНИЕ:")
    p4 = p3 - p2
    print(f"p3 - p2 = {p4}")
    
    p3 -= p2
    print(f"p3 -= p2 → {p3}")
    print()
    
    # 5. Умножение
    print("5. УМНОЖЕНИЕ:")
    p5 = p1 * p2
    print(f"p1 * p2 = {p5}")
    
    p1 *= p2
    print(f"p1 *= p2 → {p1}")
    print()
    
    # 6. Расстояние между точками
    print("6. РАССТОЯНИЕ МЕЖДУ ТОЧКАМИ:")
    dist = p1.get_distance(p2)
    print(f"Расстояние между {p1} и {p2} = {dist:.2f}")
    print()
    
    # 7. Создание точки из другой точки
    print("7. СОЗДАНИЕ ИЗ ДРУГОЙ ТОЧКИ:")
    p6 = Point3D.from_point(p1)
    print(f"Копия p1: {p6}")
    print(f"Это разные объекты: {p1 is p6}")
    print()
    
    # 8. Демонстрация всех операций в цепочке
    print("8. ЦЕПОЧКА ОПЕРАЦИЙ:")
    a = Point3D(1, 1, 1)
    b = Point3D(2, 2, 2)
    c = Point3D(3, 3, 3)
    
    result = a + b - c * a
    print(f"a + b - c * a = {result}")
    
    # 9. Проверка работы с разными типами чисел
    print("9. РАБОТА С РАЗНЫМИ ТИПАМИ ЧИСЕЛ:")
    p_int = Point3D(1, 2, 3)        # int
    p_float = Point3D(1.5, 2.5, 3.5) # float
    print(f"Точка с int: {p_int}")
    print(f"Точка с float: {p_float}")
    print(f"Их сумма: {p_int + p_float}")

if __name__ == "__main__":
    main()