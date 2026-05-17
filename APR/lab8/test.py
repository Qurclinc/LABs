import secrets
import random
import os
import numpy as np
from PIL import Image

def init_iv(data):
    iv_len = len(data) % secrets.randbits(8)
    step = ((len(data) - 1) // iv_len) // 3
    return {
        "length": iv_len,
        "step": step,
        "iv": [secrets.randbits(8) for _ in range(iv_len)]
    }

def encrypt(data, key, output, iv):
    seed = sum(iv["iv"]) # Установка сида
    key = list(key) # ключ как список для удобства
    vector = iv["iv"] # сам вектор
    random.seed(seed)
    random.shuffle(key) # перемешка картинки по сиду. необходимо будет для декрипта также её шафлить
    print(list(data[:100]))
    data = xor(data, key) # ксор. шифрование
    data = list(data) 
    step = iv["step"] # шаг
    for i, el in enumerate(vector): # каждый step'ый элемент это кусок iv. придётсся собирать
        data.insert(i * step, el)
    return [iv["length"], step] + data

def xor(data, key):
    result = []
    len_key = len(key)
    for i, ch in enumerate(data):
        result += [ch ^ int(key[i % len_key])]
    return bytes(result)

def read_file(filepath: os.PathLike) -> bytes:
        with open(filepath, "rb") as f:
            return f.read()
    
def write_file(filepath: os.PathLike, data) -> bytes:
    with open(filepath, "wb") as f:
        f.write(data)

key = np.asarray(Image.open("./cxder.jpg")).tobytes()
data = read_file("./Качьянов_В_Д_23КБсРЗПО_2_Реш_лин_ур_ий.docx")
iv = init_iv(data)
encrypt(data, key, "./out.enc", iv)
# res = xor(data, key)
# write_file("./data.docx", res)