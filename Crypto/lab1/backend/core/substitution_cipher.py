from .constants import ALPHABET
from typing import Literal

# prim_key = "рчдыовзшхюунцфиэьъаякёмщйлсжптбге"
# prim_key = "яюэьыъщшчцхфутсрпонмлкйизжёедгвба"
# ЗИМА = ЧЦТЯ

def crypt(
    mode: Literal["encrypt", "decrypt"],
    plain_text: str,
    lang: Literal["rus", "eng"] = "eng",
    key: str = None,
):
    literals = ALPHABET[lang]
    alpha_length = len(literals)
    
    if len(key) != alpha_length:
        raise KeyError
    
    result = ""
    if mode == "decrypt":
        key, literals = literals, key
        
    for char in plain_text:
        result += literals[key.index(char)]
        
    return result