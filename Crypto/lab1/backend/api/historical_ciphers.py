from fastapi import APIRouter, HTTPException

from core import shift_crypt, substitution_crypt, vigenere_crypt
from schemas.historical_ciphers import ShiftCipher, SubstitutionCipher, VigenereCipher
from services.historical_cipher_process import process_cipher
from services.keygen import keygen

router = APIRouter(prefix="/historical", tags=["Historical ciphers"])

# Shift 
@router.post("/shift")
async def shift_cipher(cipher: ShiftCipher):
    
    keygen.lang = cipher.lang
    try:
        return await process_cipher(
            cipher, shift_crypt, keygen.generate_integer_key
        )
    except KeyError:
        raise HTTPException(400, "Bad request")
    

@router.post("/substitution")
async def substitution_cipher(cipher: SubstitutionCipher):
    
    keygen.lang = cipher.lang
    try:
        return await process_cipher(
            cipher, substitution_crypt, keygen.generate_random_alphabet
        )
    except KeyError as ex:
        print(str(ex))
        raise HTTPException(400, "Bad request")
    
    
@router.post("/vigenere")
async def vigenere_cipher(cipher: VigenereCipher):
    
    keygen.lang = cipher.lang
    if cipher.length:
        keygen.length = cipher.length
    
    try:
        return await process_cipher(
            cipher, vigenere_crypt, keygen.generate_random_word
        )
    except KeyError:
        raise HTTPException(400, "Bad request")
