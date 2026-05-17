from PyQt6.QtWidgets import QMessageBox

class SuccessDialog(QMessageBox):
    def __init__(self, message):
        super().__init__()
        self.setWindowTitle("SUCCESS")
        self.setText(message)
