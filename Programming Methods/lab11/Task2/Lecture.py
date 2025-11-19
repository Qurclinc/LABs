import datetime as dt

class Lecture:
    def __init__(self, name: str, description: str, date: dt.date, time: dt.time, teacher: str):
        self.name = name
        self.description = description
        self.date = date
        self.time = time
        self.teacher = teacher
    
    def __str__(self) -> str:
        return f"Лекция: {self.name} ({self.date} {self.time})\nПреподаватель: {self.teacher}\nОписание: {self.description}"