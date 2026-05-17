from PyQt6.QtWidgets import QWidget

class BorderedWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("BorderedWidget")