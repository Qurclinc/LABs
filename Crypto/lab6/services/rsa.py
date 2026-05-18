from typing import Dict
from math import gcd

from Crypto.Util.number import getPrime

from .cryptosystem import Cryptosystem, ExchangeError
from utils import verify_primality, inverse, bin_pow

class RSAClient(Cryptosystem):
    def __init__(self, bits: int = 64):
        self.E = 65537 # Считается стандартом
        while True:
            self.p = getPrime(bits)
            self.q = getPrime(bits)
            self.N = self.p * self.q
            self.phi = (self.p - 1) * (self.q - 1)
            if gcd(self.E, self.phi) != 1 or \
                not(verify_primality(self.p)) or \
                not(verify_primality(self.q)):                    
                continue
            
            break
        self.d = inverse(self.E, self.phi)
        
        self._other_public_key = None
        
    @property
    def public_key(self):
        return {"E": self.E, "N": self.N}
    
    @property
    def private_key(self):
        return {"d": self.d, "p": self.p, "q": self.q}
    
    def send_message(self, message: int):
        if not(self.other_public_key):
            raise ExchangeError
        E = self.other_public_key["E"]
        N = self.other_public_key["N"]
        return bin_pow(message, E, N)
    
    def read_message(self, ciphertext: int):
        if not(self.other_public_key):
            raise ExchangeError
        return bin_pow(ciphertext, self.d, self.N)