from typing import Literal
from pydantic import BaseModel

class BaseCipher(BaseModel):
    mode: Literal["encrypt", "decrypt"]
    plain_text: str
    lang: Literal["rus", "eng"]
    
class ShiftCipher(BaseCipher):
    key: int
    
class SubstitutionCipher(BaseCipher):
    key: str | int
    
class VigenereCipher(SubstitutionCipher):
    length: int | None

# class Response(BaseModel):
#     cipher_text: str | None
#     plain_text: str | None
#     key: int | str | None