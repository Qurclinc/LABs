import socket
import datetime as dt
import os

from fastapi import FastAPI

from core import crypter
from schemas import WmfMessage, WmfExchangeData, WmfInitData
from utils import check_server_alive, check_timestamp, SECOND_PORT

app = FastAPI()

MAPPING_TABLE = {}

@app.get("/hello", response_model=WmfExchangeData)
async def hello(name: str) -> WmfExchangeData:
    """Абонент обращается к центру, чтобы получить общие с ним ключи и получить выделенный порт

    Аргументы:
        name (str): Имя абонента (уникальное). Ситуации коллизии имён не учитывал (лаб. среда позволяет)

    Возвращает:
        WmfExchangeData: Сгенерированный ключ абонента и доверенного центра, порт
    """
    generated_key=os.urandom(2).hex() # Ключ для S-AES максимум 4 байта. Сделал случайный
    
    # Сопоставление имени пользователя общего с доверенным центром ключа и портом для общения с клиентом
    MAPPING_TABLE[name] = {
        "trust_key": generated_key
    }
    
    return WmfExchangeData(
        generated_key=generated_key
    )
    
@app.post("/initiate")
async def send_message(init: WmfInitData):
    """Инициализирует обмен между центром и абонентами. Тот, кто инициализирует - генерирует случайный
    приватный ключ для шифрования дальнейший сообщений по протоколу S-AES. Центру  он поступает в
    симметрично зашифрованном виде тем же S-AES при помощи сессионного ключа между центром и первым
    абонентом. Центр расшифровывает ключ и сравнивает временную метку с учётом погрешности на сеть и рантайм.
    Если время удовлетворительное, то отправляет секретный ключ второму абоненту, зашифрованный общим
    с ним ключом

    Аргументы:
        init (WmfInitData): Параметры инициализации
    """
    
    # Пользователи из таблицы соответствия по их именам. Необходимо для сопоставления
    # Общих с центром ключей, а также порта для отправки шифрованного ключа второму абоненту
    userA = MAPPING_TABLE[init.from_username]
    userB = MAPPING_TABLE[init.to_username]
    
    
    K_AS = userA["trust_key"] # Общий ключ центра и первого (инициализирующего) абонента
    decrypted_key = crypter.decrypt(init.secret_key, K_AS) # Ключ в расшифрованном виде
    # Если временная метка валидна, только тогда имеет смысл выполнять остальное
    if check_timestamp(dt.datetime.now().timestamp(), init.timestamp): 
        K_BS = userB["trust_key"] # Общий ключ центра и второго абонента
        
        # Зашифрованный секретный ключ первого абонента общим ключом центра и второго абонента
        secret_key = crypter.encrypt(decrypted_key, K_BS) 
        
        # Если второй пользователь не "поприветствовал" сервер - у него нет порта. И не с кем общаться
        if not(check_server_alive(SECOND_PORT)):
            raise
        
        # Отправка данных осуществляется через сокет
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(("127.0.0.1", SECOND_PORT))
            sock.sendall(f"INIT {secret_key} {dt.datetime.now().timestamp()}".encode())
    