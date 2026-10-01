import json
import os
from typing import Literal
from math import gcd

from Crypto.Util.number import getPrime

from utils import h

class ExchangeError(Exception):
    pass

# from .cryptosystem import Cryptosystem, ExchangeError
from utils import verify_primality, inverse, bin_pow, decode_text
from constants import OUTPUT_DIR

class RSA():
    def __init__(self, bits: int = 64):
        self.bits = bits
        self.p: int
        self.q: int
        self.d: int
        
        self.N: int
        self.E: int
        
    def generate_keys(self):
        self.p = getPrime(self.bits)
        self.q = getPrime(self.bits)
        self.N = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)
        while True:
            self.E = int(os.urandom(2).hex(), 16)
            if gcd(self.E, self.phi) != 1 or \
                not(verify_primality(self.p)) or \
                not(verify_primality(self.q)):                    
                continue
            
            break
        self.d = inverse(self.E, self.phi)
        
    def save_keys(self, pub_name: str = "pubkey", priv_name: str = "privkey"):
        with open(f"{OUTPUT_DIR}/{pub_name}.json", "w", encoding="utf-8") as file:
            json.dump(self.public_key, file, indent=4)
        with open(f"{OUTPUT_DIR}/{priv_name}.json", "w", encoding="utf-8") as file:
            json.dump(self.private_key, file, indent=4)
        
    def load_pubkey(self, pub_name: str = "pubkey"):
        with open(f"{OUTPUT_DIR}/{pub_name}.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            self.E = data["E"]
            self.N = data["N"]
            
    def load_privkey(self,  priv_name: str = "privkey"):
        with open(f"{OUTPUT_DIR}/{priv_name}.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            self.d = data["d"]
            self.p = data["p"]
            self.q = data["q"]
            self.N = self.p * self.q
        
    @property
    def public_key(self):
        return {"E": self.E, "N": self.N}
    
    @property
    def private_key(self):
        return {"d": self.d, "p": self.p, "q": self.q}
    
    def sign(
        self,
        message: int,
        lang: Literal["eng", "rus"] = "eng",
        p: int | None = None,
        msg_name: str = "message.txt",
        sign_name: str = "sign.txt"
    ):
        M = message
        with open(f"{OUTPUT_DIR}/{msg_name}", "w") as text_file:
            text_file.write(decode_text(M, lang))
        S = bin_pow(
            h(M, p) if p else M,
            self.d,
            self.N
        )
        with open(f"{OUTPUT_DIR}/{sign_name}", "w") as sign_file:
            sign_file.write(str(S))
        
        
    def verify_sign(
        self,
        sign: int,
        compare_to: int
    ):
        S = sign
        return bin_pow(S, self.E, self.N) == compare_to

    def reset(self):
        self.p = None
        self.q = None
        self.d = None
        self.E = None
        self.N = None
    
    # def send_message(self, message: int):
    #     if not(self.other_public_key):
    #         raise ExchangeError
    #     E = self.other_public_key["E"]
    #     N = self.other_public_key["N"]
    #     return bin_pow(message, E, N)
    
    # def read_message(self, ciphertext: int):
    #     if not(self.other_public_key):
    #         raise ExchangeError
    #     return bin_pow(ciphertext, self.d, self.N)