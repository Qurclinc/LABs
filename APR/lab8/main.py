import os
import sys

from pathlib import Path
from PyQt6.QtWidgets import QApplication

from UI.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    app.setStyleSheet(Path(os.path.join(os.path.abspath("UI"), "style.qss")).read_text()) 
    
    window = MainWindow()
    window.show()
    
    
    sys.exit(app.exec())