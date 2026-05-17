from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget
)

from services import RSAClient, ElgamalCleint
from .crypto_tab import CryptoTab

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CryptoLab 6")

        layout = QVBoxLayout()

        tabs = QTabWidget()
        tabs.addTab(CryptoTab(RSAClient), "RSA")
        tabs.addTab(CryptoTab(ElgamalCleint), "ElGamal")

        layout.addWidget(tabs)
        self.setLayout(layout)