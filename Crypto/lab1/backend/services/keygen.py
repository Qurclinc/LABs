import random
import secrets

from typing import Literal

from core.constants import ALPHABET

class Keygen():
    
    def __init__(self):
        self._alphabet = None
        self._lang = None
        self._length = 6
        
    @property
    def lang(self):
        return self._lang
    
    @lang.setter
    def lang(self, value: Literal["rus", "eng"]):
        if value not in ["rus", "eng"]:
            raise KeyError
        self._lang = value
        self._alphabet = ALPHABET[self._lang]
        
    @property
    def length(self):
        return self._length
    
    @length.setter
    def length(self, value):
        if value <= 0:
            raise ValueError
        self._length = value
    
    def __generate_random_index(self) -> int:
        value = secrets.randbits(8)
        return value % len(self._alphabet)
    
    def generate_integer_key(self) -> int:
        return self.__generate_random_index()

    def generate_random_alphabet(self) -> str:
        shuffled = list(self._alphabet)
        random.shuffle(shuffled)
        return "".join(shuffled)
        
    
    def generate_random_word(self):
        return "".join([self._alphabet[self.__generate_random_index()] for _ in range(self._length)])
    
keygen = Keygen()