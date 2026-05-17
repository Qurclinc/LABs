import base64
import os
import secrets
import random
import re

from pathlib import Path
from typing import Tuple, List
import numpy as np
from PIL import Image

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF2

class Crypter:
    def __init__(self):
        self.key: bytes = None
        self.data_filepath: Path = None
        self.CHUNK_SIZE = 4 * 1024 # 4KB
        
    def __init_iv(self, filepath: Path):
        # print(filepath, type(filepath))
        data_length = filepath.stat().st_size
        
        if data_length < 64:
            raise ValueError(
                f"File too small for encryption: {data_length} bytes. "
                f"Minimum required: 64 bytes"
            )
        
        iv_len = data_length % secrets.randbits(8) + 32
        step = ((data_length - 1) // iv_len) // 3
        return {
            "length": iv_len,
            "step": step,
            "iv": [secrets.randbits(8) for _ in range(iv_len)]
        }
        
    def __derieve_key(self, shuffled_key: str, salt: bytes):
        master_key = PBKDF2(
            password="".join(map(hex, shuffled_key)),
            salt=salt,
            dkLen=32,
            count=1_000_000,
            hmac_hash_module=SHA256
        )
        
        return master_key
        
    def __proceed_chunk(self, input_filepath: Path, skip_first_line: bool = False):
        with open(input_filepath, "rb") as fin:
            if skip_first_line:
                fin.readline()
            while True:
                chunk = fin.read(self.CHUNK_SIZE)
                if not chunk:
                    break
                yield chunk
                
    def __collect_vector(self, input_filepath: Path, length: int, step: int) -> List[int]:
        collected = 0
        count = 0
        vector = []
        for chunk in self.__proceed_chunk(input_filepath, skip_first_line=True):
            for i, el in enumerate(chunk):
                if count % step == 0 and count != 0:
                    vector.append(int(el))
                    collected += 1
                if collected == length:
                    return vector
                count += 1
        return vector
        
    def set_key(self, image_path: Path) -> None:
        if not(os.path.exists(image_path)):
            raise FileNotFoundError
        self.key = np.asarray(Image.open(image_path)).tobytes()
    
    def encrypt(self, input_filepath: Path | str, output_filepath: Path | str) -> Tuple[bool, str]:
        if isinstance(input_filepath, str): input_filepath = Path(input_filepath)
        if isinstance(output_filepath, str): output_filepath = Path(output_filepath)
        
        
        if not self.key:
            raise KeyError
        
        length, step, vector = self.__init_iv(input_filepath).values()
        if len(vector) < 32:
            raise KeyError
        # print(length, step, vector)
        
        seed = sum(vector)
        random.seed(seed)
        shuffled_key = list(self.key)
        random.shuffle(shuffled_key)
        
        salt, nonce = map(lambda y: b"".join(map(lambda x: chr(x).encode(), y)), (vector[:16], vector[16:32]))
        master_key = self.__derieve_key(shuffled_key, salt)
        
        cipher = AES.new(master_key, mode=AES.MODE_GCM, nonce=nonce)
        
        with open(output_filepath, "wb") as f:
            f.write(
                str(length).encode() + \
                f"0x{secrets.token_hex(2)}".encode() + \
                str(step).encode() + \
                f"0x{secrets.token_hex(2)}".encode() + \
                b"0" * 24 + \
                f"0x{secrets.token_hex(2)}".encode() + \
                b"\n"
            )
        
        counter = 0
        inserted = 0
        with open(output_filepath, "ab") as fout:
            for chunk in self.__proceed_chunk(input_filepath):
                encrypted_chunk = cipher.encrypt(chunk)
                chunk_res = bytearray()
                for byte in encrypted_chunk:
                    chunk_res.append(byte)
                    counter += 1
                    if counter % step == 0 and inserted != length:
                        chunk_res.append(vector[inserted])
                        inserted += 1
                        counter += 1
                fout.write(chunk_res)
                
                
        tag = cipher.digest()
        with open(output_filepath, "r+b") as fout:
            fout.seek(0)
            header = (
                str(length).encode() + \
                f"0x{secrets.token_hex(2)}".encode() + \
                str(step).encode() + \
                f"0x{secrets.token_hex(2)}".encode() + \
                base64.urlsafe_b64encode(tag) + \
                f"0x{secrets.token_hex(2)}".encode() + \
                b"\n"
            )
            fout.write(header)
            
        return (True, "Success")
    
    def decrypt(self, input_filepath: Path, output_filepath: Path) -> Tuple[bool, str]:
        if isinstance(input_filepath, str): input_filepath = Path(input_filepath)
        if isinstance(output_filepath, str): output_filepath = Path(output_filepath)
        
        with open(input_filepath, "rb") as f:
            line = f.readline()
            
        iv_length, step, tag, _ = re.split(r"0x[0-9a-fA-F]{4}", str(line)[2:])
        iv_length, step, tag = int(iv_length), int(step), base64.urlsafe_b64decode(tag)
        
        vector = self.__collect_vector(input_filepath, iv_length, step)
        seed = sum(vector)
        
        random.seed(seed)
        shuffled_key = list(self.key)
        random.shuffle(shuffled_key)
        
        salt, nonce = map(lambda y: b"".join(map(lambda x: chr(x).encode(), y)), (vector[:16], vector[16:32]))
        master_key = self.__derieve_key(shuffled_key, salt)
        
        cipher = AES.new(master_key, mode=AES.MODE_GCM, nonce=nonce)
        
        counter = 0
        truncated = 0
        with open(output_filepath, "wb") as fout:
            for chunk in self.__proceed_chunk(input_filepath, skip_first_line=True):
                chunk_res = bytearray()
                for byte in chunk:
                    if counter % step == 0 and counter != 0 and truncated < iv_length:
                        truncated += 1
                        counter += 1
                        continue
                    chunk_res.append(byte)
                    counter += 1
                decrypted_chunk = cipher.decrypt(bytes(chunk_res))
                fout.write(decrypted_chunk)
                
        try:
            cipher.verify(tag)
        except ValueError:
            return (False, "MAC check failed — Data is corrupted")
                
        return (True, "Success")