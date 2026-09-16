import os
import requests
import threading
import socket
import datetime as dt

from schemas import WmfInitData
from core import crypter
from utils import check_timestamp

class User:
    def __init__(self, name: str, port: int, center_ip: str = "127.0.0.1"):
        self.name = name # Имя для связи
        self._key = None # Приватный ключ; используется в S-AES для шифрования СООБЩЕНИЙ
        self.trust_key = None # Шифрует/расшифровывает приватный ключ. Он выдаётся центром доверия
        self.port = port # Выделенный порт для общения клиентов. Задаётся заранее
        self.center_ip = center_ip # Адрес доверенного центра
        self.url_prefix = f"http://{self.center_ip}:8000"
        
    @property
    def key(self):
        return self._key
    
    @key.setter
    def key(self, value: str):
        self._key = value
        
    def initiate(self, other_username: str):
        """Запускает инициалиазацию диалога. 

        Аргументы:
            other_username (str): Имя пользователя, с которым будет переписка
        """
        if not(self.trust_key): # Без обмена ключом с центром - нет смысла
            raise
        
        if not(self._key):
            self._key = os.urandom(2).hex() # Ну и ключ надо бы сгенерировать
        
        # Ключ для шифрования сообщений передаётся зашифрованным.
        enc_key = crypter.encrypt(self.key, self.trust_key)
        print(self) # Вывод для удобства, и чтобы проследить секретный ключ инициализатора
        data = WmfInitData(
            from_username=self.name,
            to_username=other_username,
            secret_key=enc_key,
            timestamp=dt.datetime.now().timestamp()
        )
        response = requests.post(f"{self.url_prefix}/initiate", json=data.model_dump())
        print(response.text)
    
    def say_hello(self):
        """Отправляет доверенному центру приветственное сообщение, означающее готовность клиента
        участвовать в обмене информацией. После него у абонента появляется общий с центром ключ
        и выделенный для взаимодействия порт"""
        
        response = requests.get(f"{self.url_prefix}/hello?name={self.name}").json()
        self.trust_key = response["generated_key"]
        # Результаты запроса сохраняются в поля объекта, а в отдельном фоновом процессе
        # запускается обработчик сокета на выделенном порту
        t = threading.Thread(target=self.start_listening)
        t.start()
        
    def _receive_key(self, data: bytes, received_timestamp: float):
        """Вспомогательная функция, позволяющая избавиться от раздувания функции обработчика.
        Парсит полученную от центра доверия строку, сверяет временную метку, и в случае успеха
        расшифровывает секретный ключ. Таким образом устанавливается защищённый канал связи
        между клиентами

        Аргументы:
            data (bytes): Строка данных, полученная от доверенного центра
            received_timestamp (float): Временная метка, когда были получены данные
        """
        _, secret_key, timestamp = data.decode().split()
        if check_timestamp(float(timestamp), received_timestamp):
            decrypted_key = crypter.decrypt(secret_key, self.trust_key)
            self.key = decrypted_key # Секретный ключ должен совпасть с отправителем
        
    def start_listening(self):
        """Обработчик сокета запускается в фоне и предназначен для получения секретного ключа
        и временной метки для установления соединения, а также служит способом получения 
        информации от клиентов
        """
        with socket.socket(socket.AF_INET) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(("127.0.0.1", self.port))
            sock.listen(5)
            # print(f"User {self.name} is listening...")
            
            # Запущенный в фоне, работает в бесконечном цикле, ожидая подключения
            while True:
                client_socket, _ = sock.accept() # Адрес отправителя не интересен
                with client_socket:
                    raw_data = client_socket.recv(64)
                    
                    # Если в запросе есть INIT - значит его прислал центр и такой запрос
                    # нужно обработать особым образом 
                    if raw_data.startswith(b"INIT"):
                        now = dt.datetime.now().timestamp() # Временная метка берётся заранее, чтобы погрешность на сеть была меньше
                        self._receive_key(raw_data, now)
                        print("Connection established")
                        print(self)
                        continue
                    if not raw_data: # Пустые запросы игнорируются
                        continue
                    print(f"Received message: {raw_data.decode()}")
                    decrypted_data = crypter.decrypt(raw_data.decode()[:4], self.key)
                    print(f"Decrypted message: {decrypted_data}")
                    print("Enter message: ", end="")
                    
                    
    def __repr__(self) -> str:
        """Строковое представление об абонентах. Удобно чтобы делать вывод в консоль простым
        print

        Возвращает:
            str: Строку информации
        """
        return f"User {self.name}:\n \
trust key: {self.trust_key}\n \
private key: {self.key}\n \
allocated port:{self.port}"