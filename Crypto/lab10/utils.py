import os
from typing import Literal
import random

from constants import ALPHABET, URL
import requests

def encode_text(text: str, lang: Literal["rus", "eng"]) -> int:
    if lang not in ["rus", "eng"]:
        raise KeyError
    abc = ALPHABET[lang]
    base = len(abc)
    l = len(text) - 1
    result = 0
    for i, ch in enumerate(text):
        result += base ** (l - i) * (abc.index(ch) + 1)
        # print(f"{base}^{l - i} * {abc.index(ch) + 1}")
    return result

def decode_text(number: int, lang: Literal["rus", "eng"]):
    if lang not in ["rus", "eng"]:
        raise KeyError
    abc = ALPHABET[lang]
    base = len(abc)
    result = []
    while number > 0:
        result.append(number % base)
        number //= base
    return "".join(abc[i - 1] for i in result[::-1])

def h(number: int, p: int):
    if not(verify_primality(p)):
        raise TypeError("p - не простое число")
    result = 0
    h0 = len(str(number))
    prev = h0
    while number > 0:
        Mi = number % 10
        number //= 10
        # print(f"{Mi} + 2 * {prev} + 1")
        result = bin_pow((Mi + 2 * prev + 1), 2, p - 1)
        prev = result
    return result + 1

def bin_pow(a: int, n: int, m: int):
    payload = {"a": str(a), "n": str(n), "m": str(m)}
    response = requests.post(f"{URL}/binpow", json=payload)
    return int(response.json())

def inverse(a: int, m: int):
    payload = {"a": str(a), "m": str(m)}
    response = requests.post(f"{URL}/inverse", json=payload)
    return int(response.json())

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

def clear():
    os.system("cls" if os.name == "nt" else "clear")