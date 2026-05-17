from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


class AppLabel(QLabel):
    def __init__(
        self,
        text="",
        parent=None,
        align=Qt.AlignmentFlag.AlignLeft,
        size=9,
        bold=False
    ):
        super().__init__(text, parent)

        weight = QFont.Weight.Bold if bold else QFont.Weight.Normal

        self.setFont(
            QFont(
                "Consolas",
                size,
                weight.value
            )
        )

        if align is not None:
            self.setAlignment(align)
