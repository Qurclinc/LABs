from PyQt6.QtWidgets import QMessageBox

class ErrorDialog(QMessageBox):
    def __init__(self, message):
        super().__init__()
        self.setWindowTitle("ERROR")
        self.setIcon(QMessageBox.Critical)
        self.setText(message)
