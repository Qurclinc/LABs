from typing import Dict, Any
from abc import ABC

class ExchangeError(Exception):
    pass

class Cryptosystem(ABC):
    
    @property
    def public_key(self):
        pass
    
    @property
    def private_key(self):
        pass
    
    @property
    def other_public_key(self):
        return self._other_public_key
    
    @other_public_key.setter
    def other_public_key(self, other_public_key: Dict[str, int]):
        self._other_public_key = other_public_key
    
    def send_message(self, message: Any):
        pass
    
    def read_message(self, ciphertext: Any):
        pass
    
    @staticmethod
    def exchange(client1, client2):
        client1.other_public_key = client2.public_key
        client2.other_public_key = client1.public_key