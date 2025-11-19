import datetime as dt
from Student import Student
from Lecture import Lecture
from Course import Course

def main():
    # Создаем лекции
    lecture1 = Lecture(
        "Введение в Python", 
        "Основы языка Python", 
        dt.date(2024, 1, 15), 
        dt.time(10, 0), 
        "Иван Иванов"
    )
    
    lecture2 = Lecture(
        "Функции и модули", 
        "Работа с функциями и модулями в Python", 
        dt.date(2024, 1, 22), 
        dt.time(10, 0), 
        "Петр Петров"
    )
    
    # Создаем курс
    python_course = Course(
        "Python для начинающих",
        "Изучение основ программирования на Python",
        [lecture1, lecture2]
    )
    
    # Создаем студентов
    student1 = Student("Алексей", "Сидоров")
    student2 = Student("Мария", "Иванова")
    
    # Демонстрация функциональности
    print("=== ЗАПИСЬ НА КУРС ===")
    student1.enroll(python_course)
    student2.enroll(python_course)
    
    print("\n=== ПРОСМОТР КУРСОВ СТУДЕНТА ===")
    student1.view_courses()
    
    print("\n=== ИНФОРМАЦИЯ О КУРСЕ ===")
    python_course.view_info()
    
    print("\n=== ПРОСМОТР ЛЕКЦИЙ КУРСА ===")
    python_course.view_lectures()
    
    print("\n=== ОТМЕНА ЗАПИСИ ===")
    student2.unenroll(python_course)
    
    print("\n=== ПРОСМОТР КУРСОВ ПОСЛЕ ОТПИСКИ ===")
    student2.view_courses()
    
if __name__ == "__main__":
    main()