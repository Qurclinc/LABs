import json
import os
from typing import Literal
from math import gcd

from Crypto.Util.number import getPrime

from utils import h

# class ExchangeError(Exception):
#     pass

from utils import verify_primality, inverse, bin_pow, decode_text
from constants import OUTPUT_DIR

class RSA():
    """Основной класс, реализующий цифровую подпись с алгоритмом RSA
    """
    def __init__(self, bits: int = 64):
        self.bits = bits
        self.p: int
        self.q: int
        self.d: int
        
        self.N: int
        self.E: int
        
    def generate_keys(self):
        """Генерация ключей заданой длины (в битах) при создании экземпляра
        """
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
        """Сохраняет ключи на диск для последующего распространения и использования

        Аргументы:
            pub_name (str, optional): Имя файла, содержащего публичный ключ. По умолчанию "pubkey".
            priv_name (str, optional): Имя файла, содержащего приватный ключ. По умолчанию "privkey".
        """
        with open(f"{OUTPUT_DIR}/{pub_name}.json", "w", encoding="utf-8") as file:
            json.dump(self.public_key, file, indent=4)
        with open(f"{OUTPUT_DIR}/{priv_name}.json", "w", encoding="utf-8") as file:
            json.dump(self.private_key, file, indent=4)
        
    def load_pubkey(self, pub_name: str = "pubkey"):
        """Загружает в экземпляр данные публичного ключа из файла

        Аргументы:
            pub_name (str, optional): Имя файла, содержащего публичный ключ. По умолчанию "pubkey".

        Исключения:
            KeyError: Ошибка файла с публичным ключом
        """
        try:
            with open(f"{OUTPUT_DIR}/{pub_name}.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                self.E = data["E"]
                self.N = data["N"]
        except (FileNotFoundError, KeyError):
            raise KeyError
            
    def load_privkey(self,  priv_name: str = "privkey"):
        """Загружает в экземпляр данные приватного ключа из файла

        Аргументы:
            priv_name (str, optional): Имя файла, содержащего приватный ключ. По умолчанию "privkey".

        Исключения:
            KeyError: Ошибка файла с приватным ключом
        """
        try:
            with open(f"{OUTPUT_DIR}/{priv_name}.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                self.d = data["d"]
                self.p = data["p"]
                self.q = data["q"]
                self.N = self.p * self.q
        except (FileNotFoundError, KeyError):
            raise KeyError
        
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
        """Генерирует цифровую подпись сообщения M, переданного в закодированном (числовом) формате
        Если передано p - тогда происходит подпись без восстановления

        Аргументы:
            message (int): Сообщение, переведённое в десятичное представление
            lang (Literal["eng", "rus"], optional): Язык сообщения. По умолчанию "eng".
            p (int | None, optional): Простое число, необходимо для алгоритма хеширования. По умолчанию None.
            msg_name (str, optional): Имя файла, куда сохранить сообщение. По умолчанию "message.txt".
            sign_name (str, optional): Имя файла, куда сохранить подпись. По умолчанию "sign.txt".
        """
        M = message
        with open(f"{OUTPUT_DIR}/{msg_name}", "w") as text_file:
            text_file.write(decode_text(M, lang)) # Записывается сообщение в текстовом виде
        S = bin_pow(
            h(M, p) if p else M, # Если задано p - подписывается хеш сообщение, а не оно само
            self.d,
            self.N
        )
        with open(f"{OUTPUT_DIR}/{sign_name}", "w") as sign_file:
            sign_file.write(str(S))
        
        
    def verify_sign(
        self,
        sign: int,
        compare_to: int
    ) -> bool:
        """Проверяет переданную цифровую подпись

        Аргументы:
            sign (int): Значение подписи, которую нужно проверить
            compare_to (int): Значение, которому должна быть равна подпись

        Возвращает:
            bool: Совпала ли подпись
        """
        S = sign
        return bin_pow(S, self.E, self.N) == compare_to

    def reset(self):
        """Сброс всех ключей в рантайме алгоритма
        """
        self.p = None
        self.q = None
        self.d = None
        self.E = None
        self.N = None