from .constants import ALPHABET
from typing import Literal

def crypt(
    mode: Literal["encrypt", "decrypt"],
    plain_text: str,
    lang: Literal["rus", "eng"] = "eng",
    key: str = "aboba"
):
    literals = ALPHABET[lang]
    alpha_length = len(literals)
    
    if mode == "decrypt":
        key = ''.join([literals[(-1 * literals.index(ch) + alpha_length) % alpha_length] for ch in key])
        
    result = ""
    key_len = len(key)
    i = 0
    for char in plain_text.lower():
        if char not in literals:
            result += char
        else:
            result += literals[(literals.index(char) + literals.index(key[i % key_len])) % alpha_length]
            i += 1
    return result
