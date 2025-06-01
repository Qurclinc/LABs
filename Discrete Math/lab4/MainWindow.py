import sys
import screeninfo

from Ui_MainWindow import Ui_MainWindow
from PyQt5.QtWidgets import QTableWidgetItem, QApplication, QMainWindow, QHeaderView

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        size = screeninfo.get_monitors()[0]
        WIDTH, HEIGHT = 800, 600
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setGeometry(int(size.width / 2 - (WIDTH / 2)), int(size.height / 2 - (HEIGHT / 2)), WIDTH, HEIGHT)
        self.setFixedSize(WIDTH, HEIGHT)
        self.ui.tableWidget.setColumnCount(4)
        self.ui.tableWidget.setHorizontalHeaderLabels(["x", "y", "z", "F"])
        
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        row = 0
        for x in (0, 1):
            for y in (0, 1):
                for z in (0, 1):
                    F = (x or (not(y)) or z) and ((not(x)) and (not(y)) and (not(z)))
                    self.ui.tableWidget.insertRow(row)
                    self.ui.tableWidget.setItem(row, 0, QTableWidgetItem(str(x)))
                    self.ui.tableWidget.setItem(row, 1, QTableWidgetItem(str(y)))
                    self.ui.tableWidget.setItem(row, 2, QTableWidgetItem(str(z)))
                    self.ui.tableWidget.setItem(row, 3, QTableWidgetItem(str(int(F))))
                    
                    row += 1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())