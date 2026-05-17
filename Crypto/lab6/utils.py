from typing import Literal
import random

from constants import ALPHABET, URL
import requests

def encode_text(text: str, lang: Literal["rus", "eng"]) -> int:
    if lang not in ["rus", "eng"]:
        raise KeyError
    base = len(ALPHABET[lang]) + 1
    result = 0
    for char in text:
        result = result * base + (ALPHABET[lang].index(char) + 1) # + 1 чтобы не терялось
    return result

def decode_text(text: int, lang: Literal["rus", "eng"]):
    if lang not in ["rus", "eng"]:
        raise KeyError
    base = len(ALPHABET[lang]) + 1
    result = []
    while text > 0:
        idx = text % base
        result.append(ALPHABET[lang][idx - 1]) # -1 чтобы не ломалось
        text //= base
    return "".join(reversed(result))

def verify_primality(n: int):
    payload = {"n": str(n), "k": 10} 
    results = []
    for r in [
        requests.post(f"{URL}/ferm", json=payload),
        requests.post(f"{URL}/strassen", json=payload),
        requests.post(f"{URL}/rabin", json=payload),
    ]:
        results.append(r.json())
    return all(results)

def get_primitive_root(n: int, rnd: bool = False):
    onlysingle = not(rnd)
    payload = {"n": str(n), "onlysingle": onlysingle}
    response = requests.post(f"{URL}/primitiveroot", json=payload)
    if rnd:
        return random.choice(response.json())
    return response.json()[0]