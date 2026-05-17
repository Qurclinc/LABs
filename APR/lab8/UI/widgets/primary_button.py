from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QFont

class PrimaryButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFont(QFont("Consolas", 10, QFont.Weight.Bold.value))
