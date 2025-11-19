from Student import Student
from Lecture import Lecture

class Course:
    def __init__(self, name: str, description: str, lectures: list = None):
        self.name = name
        self.description = description
        self.lectures = lectures if lectures is not None else []
        self.students = []
    
    def add_student(self, student: Student) -> None:
        """Добавление студента в список курса"""
        if student not in self.students:
            self.students.append(student)
    
    def remove_student(self, student: Student) -> None:
        """Удаление студента из списка курса"""
        if student in self.students:
            self.students.remove(student)
    
    def add_lecture(self, lecture: Lecture) -> None:
        """Добавление лекции в курс"""
        self.lectures.append(lecture)
    
    def view_lectures(self) -> None:
        """Просмотр списка лекций курса"""
        if not self.lectures:
            print(f"На курсе '{self.name}' пока нет лекций")
        else:
            print(f"Лекции курса '{self.name}':")
            for i, lecture in enumerate(self.lectures, 1):
                print(f"{i}. {lecture.name} - {lecture.date} {lecture.time}")
                print(f"   Преподаватель: {lecture.teacher}")
                print(f"   Описание: {lecture.description}")
                print()
    
    def view_info(self) -> None:
        """Просмотр информации о курсе"""
        print(f"Курс: {self.name}")
        print(f"Описание: {self.description}")
        print(f"Количество лекций: {len(self.lectures)}")
        print(f"Количество студентов: {len(self.students)}")
    
    def __str__(self) -> str:
        return f"Курс: {self.name} - {self.description}"