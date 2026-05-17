from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget
from PyQt6.QtCore import Qt
from PyQt6 import QtGui

from pathlib import Path
from screeninfo import get_monitors

from UI.widgets.app_label import AppLabel
from UI.tabs.crypto_tab import CryptoTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.WIDTH = 600
        self.HEIGHT = 650

        self.setWindowTitle("PixCrypt v2.0")
        icon_path = Path(__file__).parent / "img" / "icon.png"
        self.setWindowIcon(QtGui.QIcon(str(icon_path)))

        self.setMinimumSize(self.WIDTH, self.HEIGHT)
        self.setMaximumSize(self.WIDTH, self.HEIGHT)

        self.init_ui()
        self.center_on_screen()

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        header = AppLabel(
            "PixCrypt",
            size=16,
            bold=True,
            align=Qt.AlignmentFlag.AlignCenter
        )
        header.setObjectName("header")
        layout.addWidget(header)

        tabs = QTabWidget()
        
        tabs.addTab(CryptoTab("encrypt"), "ENCRYPT")
        tabs.addTab(CryptoTab("decrypt"), "DECRYPT")

        layout.addWidget(tabs)

    def center_on_screen(self):
        monitors = get_monitors()
        monitor = monitors[0]

        x = monitor.x + (monitor.width - self.WIDTH) // 2
        y = monitor.y + (monitor.height - self.HEIGHT) // 2

        self.move(x, y)
