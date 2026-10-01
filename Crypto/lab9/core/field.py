from abc import ABC, abstractmethod

class Field(ABC):
    """Абстрактный класс поля
    """
    
    @abstractmethod
    def _find_primitive(self):
        """Поиск образующего элемента"""
        pass
    
    @abstractmethod
    def pow(self, a, n):
        """Возведение в степень

        Аргументы:
            a (_type_): Основание
            n (_type_): Степень
        """
        pass