import datetime as dt
from typing import List, Optional

class Student:
    def __init__(self, name: str, surname: str, courses=None):
        self.name = name
        self.surname = surname
        self.courses = courses if courses is not None else []
    
    def enroll(self, course) -> None:
        if course not in self.courses:
            self.courses.append(course)
            course.add_student(self)
            print(f"{self.name} {self.surname} записан на курс '{course.name}'")
        else:
            print(f"{self.name} {self.surname} уже записан на курс '{course.name}'")
    
    def unenroll(self, course) -> None:
        """Отмена записи студента с курса"""
        if course in self.courses:
            self.courses.remove(course)
            course.remove_student(self)
            print(f"{self.name} {self.surname} отписан от курса '{course.name}'")
        else:
            print(f"{self.name} {self.surname} не был записан на курс '{course.name}'")
    
    def view_courses(self) -> None:
        """Просмотр списка курсов студента"""
        if not self.courses:
            print(f"{self.name} {self.surname} не записан на курсы")
        else:
            print(f"Курсы студента {self.name} {self.surname}:")
            for i, course in enumerate(self.courses, 1):
                print(f"{i}. {course.name} - {course.description}")
    
    def view_lectures(self, course) -> None:
        """Просмотр лекций конкретного курса"""
        if course in self.courses:
            course.view_lectures()
        else:
            print(f"Студент не записан на курс '{course.name}'")