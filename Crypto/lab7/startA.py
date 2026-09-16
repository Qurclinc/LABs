import socket
from wmf.user import User
from core import crypter
from utils import FIRST_PORT, SECOND_PORT

userA = User(name="Aboba", port=FIRST_PORT)
userA.say_hello()

# print(userA)
other_username = input("Enter other's username for process initialization\n")
userA.initiate(other_username)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.connect(("127.0.0.1", SECOND_PORT))
    while True:
        msg = input("Enter message: ")[:4]
        enc_msg = crypter.encrypt(msg, userA.key)
        sock.sendall(f"{enc_msg[:4]}".encode())