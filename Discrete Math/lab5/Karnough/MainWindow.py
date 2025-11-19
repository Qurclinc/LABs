from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QTableWidget, 
                             QTableWidgetItem, QComboBox, QMessageBox)
from PyQt5.QtCore import Qt
from KarnoughMaps import KarnoughMaps

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 600)
        self.setWindowTitle("Karnough's Maps")
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной layout
        layout = QVBoxLayout(central_widget)
        
        # Ввод функции F
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("Функция F (минтермы через запятую):"))
        self.f_input = QLineEdit()
        self.f_input.setPlaceholderText("0, 3, 7, 8, 9, 14")
        input_layout.addWidget(self.f_input)
        
        # # Выбор типа минимизации
        # input_layout.addWidget(QLabel("Тип:"))
        # self.type_combo = QComboBox()
        # self.type_combo.addItems(["СДНФ", "СКНФ"])
        # input_layout.addWidget(self.type_combo)
        
        # Кнопка минимизации
        self.minimize_btn = QPushButton("Минимизировать")
        self.minimize_btn.clicked.connect(self.minimize_function)
        input_layout.addWidget(self.minimize_btn)
        
        layout.addLayout(input_layout)
        
        # Таблица для отображения карты Карно
        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(4)
        self.table_widget.setColumnCount(4)
        
        # Устанавливаем заголовки строк и столбцов (код Грея)
        row_labels = ["00 (A'B')", "01 (A'B)", "11 (AB)", "10 (AB')"]
        col_labels = ["00 (C'D')", "01 (C'D)", "11 (CD)", "10 (CD')"]
        
        self.table_widget.setVerticalHeaderLabels(row_labels)
        self.table_widget.setHorizontalHeaderLabels(col_labels)
        
        # Настраиваем размеры таблицы
        self.table_widget.horizontalHeader().setDefaultSectionSize(80)
        self.table_widget.verticalHeader().setDefaultSectionSize(60)
        layout.addWidget(self.table_widget)
        
        # Метка для результата
        self.result_label = QLabel("Результат минимизации будет отображён здесь")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("font-size: 14px; font-weight: bold; padding: 10px;")
        layout.addWidget(self.result_label)
        
        # Изначально очищаем таблицу
        self.clear_table()

    def clear_table(self):
        """Очищает таблицу и заполняет её нулями"""
        for row in range(4):
            for col in range(4):
                item = QTableWidgetItem("0")
                item.setTextAlignment(Qt.AlignCenter)
                self.table_widget.setItem(row, col, item)

    def parse_function_input(self, text: str) -> list:
        """Парсит ввод пользователя в список минтермов"""
        try:
            # Удаляем пробелы и разбиваем по запятым
            numbers = [int(x.strip()) for x in text.split(",") if x.strip()]
            # Проверяем, что все числа в диапазоне 0-15
            if any(x < 0 or x > 15 for x in numbers):
                raise ValueError("Числа должны быть в диапазоне 0-15")
            return numbers
        except ValueError as e:
            raise ValueError(f"Некорректный ввод: {e}")

    def update_table_display(self, minterms: list):
        """Обновляет отображение таблицы по списку минтермов"""
        self.clear_table()
        
        # Соответствие между позициями в таблице и номерами минтермов
        mapping = {
            (0, 0): 0,  (0, 1): 1,  (0, 2): 3,  (0, 3): 2,
            (1, 0): 4,  (1, 1): 5,  (1, 2): 7,  (1, 3): 6,
            (2, 0): 12, (2, 1): 13, (2, 2): 15, (2, 3): 14,
            (3, 0): 8,  (3, 1): 9,  (3, 2): 11, (3, 3): 10
        }
        
        # Заполняем таблицу единицами для указанных минтермов
        for (row, col), minterm in mapping.items():
            if minterm in minterms:
                item = QTableWidgetItem("1")
                item.setTextAlignment(Qt.AlignCenter)
                item.setBackground(Qt.lightGray)  # Подсветка единиц
                self.table_widget.setItem(row, col, item)

    def minimize_function(self):
        """Выполняет минимизацию функции"""
        try:
            # Парсим ввод
            minterms = self.parse_function_input(self.f_input.text())
            
            # Обновляем отображение таблицы
            self.update_table_display(minterms)
            
            # Выполняем минимизацию
            km = KarnoughMaps(minterms)
            result = km.minimize()
            
            # Отображаем результат
            self.result_label.setText(
                f"Минимизация (СДНФ): F = {result}\n"
                f"Минтермы: {', '.join(map(str, sorted(minterms)))}"
            )
            
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", str(e))
