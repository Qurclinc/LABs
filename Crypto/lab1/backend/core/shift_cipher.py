from .constants import ALPHABET
from typing import Literal

def crypt(
    mode: Literal["encrypt", "decrypt"],
    plain_text: str,
    lang: Literal["rus", "eng"] = "eng",
    key: int = 3,
):
    literals = ALPHABET[lang]
    alpha_length = len(literals)
    
    if key < 0 or key > alpha_length:
        raise KeyError
    shift = key if (mode == "encrypt") else alpha_length - key
    result = ""
    for char in plain_text.lower():
        if char not in literals:
            result += char
        else:
            result += literals[(literals.index(char) + shift) % alpha_length]
    return result