import socket
from core import crypter
from wmf.user import User
from utils import FIRST_PORT, SECOND_PORT

userB = User(name="Biba", port=SECOND_PORT)
userB.say_hello()

print(userB)
# res = input("Start initialization? (Enter for confirm)")
# print(res)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.connect(("127.0.0.1", FIRST_PORT))
    while True:
        if not(userB.key):
            continue
        msg = input("Enter message: ")[:4]
        enc_msg = crypter.encrypt(msg, userB.key)
        sock.sendall(f"{enc_msg[:4]}".encode())