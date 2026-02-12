from typing import Callable, Literal

from schemas.historical_ciphers import ShiftCipher, SubstitutionCipher, VigenereCipher


async def process_cipher(
    cipher: ShiftCipher | SubstitutionCipher | VigenereCipher,
    crypt_func: Callable,
    keygen_function: Callable | None
):
    response = {}
    
    if cipher.key in [-1, ""]:
        key = keygen_function()
        cipher.key = key
        response["key"] = key
        
    result = crypt_func(cipher.mode, cipher.plain_text, cipher.lang, cipher.key)
    
    if cipher.mode == "encrypt":
        response["cipher_text"] = result
    else:
        response["plain_text"] = result
        
    return response