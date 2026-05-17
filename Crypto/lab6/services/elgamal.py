import random
from typing import Tuple
from Crypto.Util.number import getPrime

from .cryptosystem import Cryptosystem
from utils import verify_primality, get_primitive_root

class ElgamalCleint(Cryptosystem):
    
    def __init__(self, bits: int = 64):
        self.P = getPrime(bits)
        self.G = int(get_primitive_root(self.P))
        self.x = random.randint(2, self.P - 1)
        self.Y = pow(self.G, self.x, self.P)
        
        self._other_public_key = None
        
    @property
    def public_key(self):
        return {"Y": self.Y, "P": self.P, "G": self.G}
    
    @property
    def private_key(self):
        return {"x": self.x}
        
    def send_message(self, message: int):
        Y = self.other_public_key["Y"]
        P = self.other_public_key["P"]
        G = self.other_public_key["G"]
        k = random.randint(2, P - 1)
        A = pow(G, k, P)
        B = (pow(Y, k, P) * message) % P
        return (A, B)
    
    def read_message(self, ciphertext: Tuple[int, int]):
        A, B = ciphertext
        m = (B * pow(A, self.P - 1 - self.x, self.P)) % self.P
        return m