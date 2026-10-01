from pathlib import Path

ALPHABET = {
    "rus": "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ ",
    "eng": "ABCDEFGHIJKLMNOPQRSTUVWXYZ "
}

URL = "http://localhost:8000/api"
OUTPUT_DIR = str(Path("./out").absolute())