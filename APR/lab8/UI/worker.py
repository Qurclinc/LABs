from pathlib import Path
from typing import Literal
from Services.crypter import Crypter
from PyQt6.QtCore import QThread, pyqtSignal

class Worker(QThread):
    finished = pyqtSignal(bool, str)
    error = pyqtSignal(str)
    
    def __init__(
        self,
        crypter: Crypter,
        mode: Literal["encrypt", "decrypt"],
        src: str | Path,
        dst: str | Path
    ):
        super().__init__()
        self.crypter = crypter
        self.mode = mode
        self.src = src
        self.dst = dst
        
    def run(self):
        try:
            if self.mode == "encrypt":
                result = self.crypter.encrypt(self.src, self.dst)
            else:
                result = self.crypter.decrypt(self.src, self.dst)
            self.finished.emit(*result)
        except FileExistsError as e:
            self.error.emit(str(e))