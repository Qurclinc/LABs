"""Постоянные значения, необходимые для корректной работы программы. Вынесены сюда для удобного
доступа из любой части кода
"""
from pathlib import Path

ALPHABET = {
    "rus": "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ ",
    "eng": "ABCDEFGHIJKLMNOPQRSTUVWXYZ "
}

URL = "http://localhost:8000/api"
OUTPUT_DIR = str(Path("./out").absolute())