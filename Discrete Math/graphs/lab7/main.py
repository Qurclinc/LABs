import numpy as np
import sys
import matplotlib

matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import networkx as nx
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QTextEdit, QGroupBox,
                             QMessageBox, QSplitter, QFrame, QFormLayout, QTabWidget,
                             QTableWidget, QTableWidgetItem, QHeaderView, QSpinBox,
                             QComboBox, QCheckBox, QGridLayout, QScrollArea, QSizePolicy)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QBrush, QPalette


class MatrixTableWidget(QTableWidget):
    """Виджет таблицы для отображения матриц с темной темой"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setAlternatingRowColors(True)
        self.setFont(QFont("Courier New", 9))
        
        # Настраиваем темную тему для таблицы
        self.setStyleSheet("""
            QTableWidget {
                background-color: #1a1b26;
                color: #c0caf5;
                gridline-color: #3b4261;
                border: 1px solid #3b4261;
            }
            QTableWidget::item {
                border: 1px solid #3b4261;
                padding: 2px;
                background-color: #76a3f6;
                color: #1a1b26
            }
            QHeaderView::section {
                background-color: #24283b;
                color: #7aa2f7;
                padding: 4px;
                border: 1px solid #3b4261;
                font-weight: bold;
            }
            QTableWidget::item:selected {
                background-color: #76a3f6;
                color: #1a1b26;
            }
        """)

        # Настраиваем заголовки
        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.verticalHeader().setStyleSheet("""
            QHeaderView::section {
                background-color: #24283b;
                color: #7aa2f7;
                padding: 4px;
                border: 1px solid #3b4261;
                font-weight: bold;
            }
        """)

    def set_matrix(self, matrix, labels=None):
        """Установка матрицы для отображения"""
        if matrix is None:
            self.clear()
            self.setRowCount(0)
            self.setColumnCount(0)
            return

        n = len(matrix)
        self.setRowCount(n)
        self.setColumnCount(n)

        if labels is None:
            labels = [str(i + 1) for i in range(n)]

        self.setHorizontalHeaderLabels(labels)
        self.setVerticalHeaderLabels(labels)

        for i in range(n):
            for j in range(n):
                item = QTableWidgetItem(str(matrix[i][j]))
                item.setTextAlignment(Qt.AlignCenter)
                if matrix[i][j] == 1:
                    # СИНИЙ для единиц (как было в старой версии)
                    item.setBackground(QBrush(QColor('#7aa2f7')))  # Синий фон
                    item.setForeground(QBrush(QColor('#1a1b26')))  # Темный текст на светлом фоне
                else:
                    # Темный фон для нулей
                    item.setBackground(QBrush(QColor('#24283b')))
                    item.setForeground(QBrush(QColor('#c0caf5')))  # Светлый текст
                self.setItem(i, j, item)

        # Настраиваем заголовки
        for i in range(n):
            self.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)
            self.verticalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)


class GraphCanvas(FigureCanvas):
    """Холст для отрисовки графов с темной темой"""

    def __init__(self, parent=None, width=5, height=5, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor='#1a1b26')
        self.ax = self.fig.add_subplot(111, facecolor='#1a1b26')
        super().__init__(self.fig)
        self.setParent(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Настраиваем темную тему для холста
        self.setStyleSheet("background-color: #1a1b26; border: 1px solid #3b4261;")

    def draw_graph(self, G, title="", vertex_labels=True, edge_labels=False):
        """Отрисовка графа с темной темой - ВОЗВРАЩАЕМ КАК БЫЛО"""
        self.ax.clear()
        
        # Устанавливаем черный фон
        self.ax.set_facecolor('#1a1b26')
        self.fig.patch.set_facecolor('#1a1b26')

        if G is None or len(G.nodes()) == 0:
            self.ax.text(0.5, 0.5, "Пустой граф",
                         ha='center', va='center', fontsize=12, color='#c0caf5')
            self.ax.set_xlim(0, 1)
            self.ax.set_ylim(0, 1)
            self.draw()
            return

        # Используем spring layout для красивой визуализации
        if len(G.nodes()) <= 15:
            pos = nx.spring_layout(G, seed=42, k=2.0, iterations=100)
        else:
            pos = nx.circular_layout(G)

        # Определяем цвета вершин по их свойствам - ВОЗВРАЩАЕМ КАК БЫЛО
        node_colors = []
        for node in G.nodes():
            if G.degree(node) == 0:  # Изолированная вершина
                node_colors.append('#FF6B6B')  # Красный
            elif G.degree(node) == 1:  # Концевая вершина
                node_colors.append('#FFD166')  # Желтый
            else:
                node_colors.append('#4ECDC4')  # Бирюзовый

        # Рисуем граф
        node_size = 400 if len(G.nodes()) > 20 else 500
        nx.draw_networkx_nodes(G, pos, ax=self.ax,
                               node_color=node_colors,
                               node_size=node_size,
                               edgecolors='#c0caf5',  # Светлая обводка
                               linewidths=1)

        nx.draw_networkx_edges(G, pos, ax=self.ax,
                               edge_color='#bb9af7',  # Фиолетовый
                               width=2.0,
                               alpha=0.8)

        if vertex_labels:
            # Метки вершин
            if len(G.nodes()) <= 20:  # Для больших графов не показываем все метки
                labels = {}
                for node in G.nodes():
                    if hasattr(G.nodes[node], 'label'):
                        labels[node] = G.nodes[node]['label']
                    else:
                        labels[node] = str(node + 1)  # Просто номера как было
                nx.draw_networkx_labels(G, pos, ax=self.ax,
                                        labels=labels,
                                        font_size=9,
                                        font_weight='bold',
                                        font_color='#c0caf5')  # Светлый текст

        # Настраиваем заголовок
        self.ax.set_title(title, fontsize=12, fontweight='bold', pad=15, color='#7aa2f7')
        
        # Настраиваем оси
        self.ax.spines['bottom'].set_color('#3b4261')
        self.ax.spines['top'].set_color('#3b4261')
        self.ax.spines['left'].set_color('#3b4261')
        self.ax.spines['right'].set_color('#3b4261')
        
        # Устанавливаем цвет делений
        self.ax.tick_params(axis='x', colors='#c0caf5')
        self.ax.tick_params(axis='y', colors='#c0caf5')
        
        # Устанавливаем цвет меток
        self.ax.xaxis.label.set_color('#c0caf5')
        self.ax.yaxis.label.set_color('#c0caf5')
        
        # Отключаем оси для графа
        self.ax.axis('off')
        
        self.fig.tight_layout()
        self.draw()


class GraphOperations:
    """Класс для операций с графами"""

    def __init__(self, n):
        self.n = n
        self.M1 = None
        self.M2 = None
        self.M3 = None
        self.generate_graphs()
        # Автоматически вычисляем все операции при инициализации
        self.calculate_all_operations()

    def generate_graphs(self):
        """Генерация всех графов"""
        # Генерация G1
        self.M1 = np.zeros((self.n, self.n), dtype=int)
        edges_added = 0
        max_edges = min(self.n * (self.n - 1) // 2, self.n * 2 + 5)
        while edges_added < max_edges:
            i = np.random.randint(0, self.n)
            j = np.random.randint(0, self.n)
            if i != j and self.M1[i][j] == 0:
                self.M1[i][j] = 1
                self.M1[j][i] = 1
                edges_added += 1

        # Генерация G2
        self.M2 = np.zeros((self.n, self.n), dtype=int)
        edges_added = 0
        max_edges = min(self.n * (self.n - 1) // 2, self.n * 1.5 + 3)
        while edges_added < max_edges:
            i = np.random.randint(0, self.n)
            j = np.random.randint(0, self.n)
            if i != j and self.M2[i][j] == 0:
                self.M2[i][j] = 1
                self.M2[j][i] = 1
                edges_added += 1

        # Генерация G3 (от 2 до 5 ребер)
        self.M3 = np.zeros((self.n, self.n), dtype=int)
        
        # Генерируем случайное количество ребер от 2 до 5
        num_edges = np.random.randint(2, 6)  # от 2 до 5 включительно
        
        edges_added = 0
        attempts = 0
        max_attempts = 100
        
        while edges_added < num_edges and attempts < max_attempts:
            i = np.random.randint(0, self.n)
            j = np.random.randint(0, self.n)
            
            if i != j and self.M3[i][j] == 0:
                self.M3[i][j] = 1
                self.M3[j][i] = 1
                edges_added += 1
            
            attempts += 1

    def calculate_all_operations(self):
        """Вычисление всех операций над графами"""
        # Объединение
        self.M_union = np.maximum(self.M1, self.M2)
        
        # Пересечение
        self.M_intersection = np.minimum(self.M1, self.M2)
        
        # Декартово произведение G1 × G2
        self.M_product_G1G2, self.n1_G1G2, self.n2_G1G2 = self.cartesian_product(self.M1, self.M2)
        
        # Декартово произведение G1 × G3
        self.M_product_G1G3, self.n1_G1G3, self.n2_G1G3 = self.cartesian_product(self.M1, self.M3)

    def create_nx_graph(self, matrix, labels=None):
        """Создание графа networkx из матрицы смежности"""
        G = nx.Graph()
        if matrix is None:
            return G

        n = len(matrix)

        # Добавляем вершины с метками
        for i in range(n):
            if labels and i < len(labels):
                G.add_node(i, label=labels[i])
            else:
                G.add_node(i, label=str(i + 1))  # Просто номера как было

        # Добавляем ребра
        for i in range(n):
            for j in range(i + 1, n):
                if matrix[i][j] == 1:
                    G.add_edge(i, j)
        return G

    def cartesian_product(self, matrix1, matrix2):
        """Декартово произведение двух графов"""
        n1 = len(matrix1)
        n2 = len(matrix2)
        k = n1 * n2

        M_product = np.zeros((k, k), dtype=int)

        # Правильное построение декартова произведения
        for i in range(n1):
            for a in range(n2):
                # Вершина (i, a)
                idx1 = i * n2 + a

                for j in range(n1):
                    for b in range(n2):
                        # Вершина (j, b)
                        idx2 = j * n2 + b

                        # Условия смежности в декартовом произведении:
                        # 1) i = j и (a, b) - ребро в matrix2
                        if i == j and matrix2[a][b] == 1 and a != b:
                            M_product[idx1][idx2] = 1
                        # 2) a = b и (i, j) - ребро в matrix1
                        elif a == b and matrix1[i][j] == 1 and i != j:
                            M_product[idx1][idx2] = 1

        return M_product, n1, n2


class GraphOperationsApp(QMainWindow):
    """Главное окно приложения с темной темой"""

    def __init__(self):
        super().__init__()
        self.graph_ops = None
        self.init_ui()

    def init_ui(self):
        """Инициализация интерфейса с темной темой"""
        self.setWindowTitle("Визуализатор операций над графами")
        self.setGeometry(50, 50, 1700, 900)

        # Устанавливаем темную тему для всего приложения
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1b26;
            }
            QWidget {
                background-color: #1a1b26;
                color: #c0caf5;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLabel {
                color: #c0caf5;
                padding: 2px;
            }
            QGroupBox {
                border: 2px solid #7aa2f7;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
                color: #7aa2f7;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #7aa2f7;
            }
            QSpinBox {
                background-color: #24283b;
                color: #c0caf5;
                border: 1px solid #7aa2f7;
                border-radius: 3px;
                padding: 3px;
                selection-background-color: #7aa2f7;
                selection-color: #1a1b26;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                background-color: #3b4261;
                border: 1px solid #7aa2f7;
                border-radius: 2px;
                width: 20px;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background-color: #7aa2f7;
            }
            QSpinBox::up-arrow, QSpinBox::down-arrow {
                border: 1px solid #c0caf5;
                width: 3px;
                height: 3px;
            }
            QPushButton {
                background-color: #7aa2f7;
                color: #1a1b26;
                border: 1px solid #7aa2f7;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 11px;
                min-width: 200px;  /* Шире кнопка */
            }
            QPushButton:hover {
                background-color: #9ece6a;
                border-color: #9ece6a;
            }
            QPushButton:pressed {
                background-color: #ff9e64;
                border-color: #ff9e64;
            }
            QTabWidget::pane {
                border: 1px solid #3b4261;
                background-color: #1a1b26;
                border-radius: 4px;
            }
            QTabBar::tab {
                background-color: #24283b;
                color: #c0caf5;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                border: 1px solid #3b4261;
                border-bottom: none;
            }
            QTabBar::tab:selected {
                background-color: #7aa2f7;
                color: #1a1b26;
                font-weight: bold;
                border-color: #7aa2f7;
            }
            QTabBar::tab:hover:!selected {
                background-color: #3b4261;
            }
            QScrollArea {
                border: 1px solid #3b4261;
                background-color: #1a1b26;
            }
            QScrollBar:vertical {
                background-color: #24283b;
                width: 15px;
                border-radius: 7px;
            }
            QScrollBar::handle:vertical {
                background-color: #7aa2f7;
                min-height: 20px;
                border-radius: 7px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #9ece6a;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar:horizontal {
                background-color: #24283b;
                height: 15px;
                border-radius: 7px;
            }
            QScrollBar::handle:horizontal {
                background-color: #7aa2f7;
                min-width: 20px;
                border-radius: 7px;
            }
            QScrollBar::handle:horizontal:hover {
                background-color: #9ece6a;
            }
            QSplitter::handle {
                background-color: #7aa2f7;
            }
            QSplitter::handle:hover {
                background-color: #9ece6a;
            }
        """)

        # Создаем центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(5)
        main_layout.setContentsMargins(5, 5, 5, 5)

        # Заголовок
        title = QLabel("ВИЗУАЛИЗАЦИЯ ОПЕРАЦИЙ НАД ГРАФАМИ")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("""
            QLabel {
                color: #7aa2f7;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1a1b26, stop:0.5 #24283b, stop:1 #1a1b26);
                padding: 15px;
                border-radius: 8px;
                margin: 2px;
                border: 2px solid #7aa2f7;
            }
        """)
        main_layout.addWidget(title)

        # Панель управления
        control_group = QGroupBox("УПРАВЛЕНИЕ ГЕНЕРАЦИЕЙ ГРАФОВ")
        control_group.setFont(QFont("Arial", 10, QFont.Bold))
        control_layout = QHBoxLayout(control_group)
        control_layout.setSpacing(15)

        control_layout.addWidget(QLabel("Количество вершин (n ≥ 5):"))
        self.n_spinbox = QSpinBox()
        self.n_spinbox.setRange(5, 12)  # Теперь можно от 5 вершин
        self.n_spinbox.setValue(10)
        self.n_spinbox.setFixedWidth(80)
        control_layout.addWidget(self.n_spinbox)

        # Кнопка для генерации графов - СДЕЛАЛИ ШИРЕ
        self.generate_btn = QPushButton("Сгенерировать графы")
        self.generate_btn.setFixedWidth(220)  # Шире кнопка
        self.generate_btn.clicked.connect(self.generate_graphs)
        control_layout.addWidget(self.generate_btn)

        control_layout.addStretch()
        main_layout.addWidget(control_group)

        # Основной сплиттер
        main_splitter = QSplitter(Qt.Horizontal)
        main_splitter.setHandleWidth(3)
        main_splitter.setStyleSheet("QSplitter::handle { background-color: #7aa2f7; }")

        # Левая часть - матрицы
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(2, 2, 2, 2)

        matrix_label = QLabel("МАТРИЦЫ СМЕЖНОСТИ")
        matrix_label.setFont(QFont("Arial", 12, QFont.Bold))
        matrix_label.setAlignment(Qt.AlignCenter)
        matrix_label.setStyleSheet("color: #9ece6a; padding: 5px;")
        left_layout.addWidget(matrix_label)

        # Вкладки для матриц
        self.matrix_tabs = QTabWidget()
        self.matrix_tabs.setFont(QFont("Arial", 9, QFont.Bold))
        self.matrix_tabs.setDocumentMode(True)
        self.matrix_tabs.setTabPosition(QTabWidget.North)

        self.create_matrix_tabs()

        left_layout.addWidget(self.matrix_tabs)
        main_splitter.addWidget(left_widget)

        # Правая часть - визуализация
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(2, 2, 2, 2)

        viz_label = QLabel("ВИЗУАЛИЗАЦИЯ ГРАФОВ")
        viz_label.setFont(QFont("Arial", 12, QFont.Bold))
        viz_label.setAlignment(Qt.AlignCenter)
        viz_label.setStyleSheet("color: #ff9e64; padding: 5px;")
        right_layout.addWidget(viz_label)

        # Вкладки для визуализации
        self.viz_tabs = QTabWidget()
        self.viz_tabs.setFont(QFont("Arial", 9, QFont.Bold))
        self.viz_tabs.setDocumentMode(True)

        self.create_visualization_tabs()

        right_layout.addWidget(self.viz_tabs)
        main_splitter.addWidget(right_widget)

        # Устанавливаем начальные размеры
        main_splitter.setSizes([800, 900])
        main_layout.addWidget(main_splitter, 1)

        # Статусная строка
        self.status_label = QLabel("Готов к генерации графов")
        self.status_label.setFont(QFont("Arial", 9))
        self.status_label.setStyleSheet("color: #c0caf5; padding: 5px;")
        main_layout.addWidget(self.status_label)

    def create_matrix_tabs(self):
        """Создание вкладок для матриц"""
        self.matrix_widgets = []
        tab_names = ["G1", "G2", "G3 (2-5 ребер)", "G1 ∪ G2", "G1 ∩ G2",
                     "G1 × G2", "G1 × G3"]

        # Цвета для вкладок
        tab_colors = ["#7aa2f7", "#7aa2f7", "#7aa2f7", 
                     "#9ece6a", "#9ece6a", 
                     "#ff9e64", "#ff9e64"]

        for idx, name in enumerate(tab_names):
            widget = MatrixTableWidget()
            self.matrix_widgets.append(widget)

            # Создаем контейнер с прокруткой
            container = QWidget()
            container.setStyleSheet("background-color: #1a1b26;")
            container_layout = QVBoxLayout(container)
            container_layout.setContentsMargins(0, 0, 0, 0)
            container_layout.addWidget(widget)

            scroll = QScrollArea()
            scroll.setWidget(container)
            scroll.setWidgetResizable(True)
            scroll.setStyleSheet("""
                QScrollArea {
                    border: 1px solid #3b4261;
                    background-color: #1a1b26;
                }
            """)
            
            self.matrix_tabs.addTab(scroll, name)
            self.matrix_tabs.tabBar().setTabTextColor(idx, QColor(tab_colors[idx]))

    def create_visualization_tabs(self):
        """Создание вкладок для визуализации"""
        self.viz_widgets = []
        tab_names = ["Граф G1", "Граф G2", "Граф G3 (2-5 ребер)",
                     "Объединение G1 ∪ G2", "Пересечение G1 ∩ G2",
                     "Декартово произведение G1 × G2",
                     "Декартово произведение G1 × G3"]
        
        # Цвета для вкладок визуализации
        tab_colors = ["#7aa2f7", "#7aa2f7", "#7aa2f7",
                     "#9ece6a", "#9ece6a",
                     "#ff9e64", "#ff9e64"]

        for idx, name in enumerate(tab_names):
            widget = GraphCanvas(self, width=6, height=5.5)
            self.viz_widgets.append(widget)
            
            container = QWidget()
            container.setStyleSheet("background-color: #1a1b26;")
            container_layout = QVBoxLayout(container)
            container_layout.setContentsMargins(0, 0, 0, 0)
            container_layout.addWidget(widget)
            
            scroll = QScrollArea()
            scroll.setWidget(container)
            scroll.setWidgetResizable(True)
            scroll.setStyleSheet("""
                QScrollArea {
                    border: 1px solid #3b4261;
                    background-color: #1a1b26;
                }
            """)
            
            self.viz_tabs.addTab(scroll, name)
            self.viz_tabs.tabBar().setTabTextColor(idx, QColor(tab_colors[idx]))

    def generate_graphs(self):
        """Генерация новых графов и автоматическое вычисление всех операций"""
        n = self.n_spinbox.value()
        
        try:
            self.graph_ops = GraphOperations(n)
            self.status_label.setText(f"Графы успешно сгенерированы. n = {n}")

            # Обновляем все матрицы
            matrices = [
                self.graph_ops.M1,
                self.graph_ops.M2,
                self.graph_ops.M3,
                self.graph_ops.M_union,
                self.graph_ops.M_intersection,
                self.graph_ops.M_product_G1G2,
                self.graph_ops.M_product_G1G3
            ]
            
            # Простые заголовки для графов
            titles = [
                "Граф G1",
                "Граф G2",
                "Граф G3 (2-5 ребер)",
                "Объединение G1 ∪ G2",
                "Пересечение G1 ∩ G2",
                "Декартово произведение G1 × G2",
                "Декартово произведение G1 × G3"
            ]

            for i in range(len(self.matrix_widgets)):
                self.update_matrix_tab(i, matrices[i])
                self.update_visualization_tab(i, matrices[i], titles[i])

            # Проверяем G3
            edge_count = np.sum(self.graph_ops.M3) // 2
            if 2 <= edge_count <= 5:
                self.status_label.setText(f"Графы успешно сгенерированы. n = {n}, G3 содержит {edge_count} ребер")
                print(f"Графы успешно сгенерированы! G3 содержит {edge_count} ребер")
            else:
                self.status_label.setText(f"Графы сгенерированы. n = {n}, G3 содержит {edge_count} ребер (ожидалось 2-5)")
                print(f"Генерация завершена, но G3 содержит {edge_count} ребер вместо 2-5")
                
        except Exception as e:
            self.status_label.setText(f"Ошибка генерации: {str(e)}")
            print(f"Ошибка при генерации графов: {e}")

    def update_matrix_tab(self, index, matrix):
        """Обновление вкладки с матрицей"""
        if index < len(self.matrix_widgets):
            if matrix is not None and len(matrix) > 0:
                # Для декартова произведения используем специальные метки
                if index in [5, 6] and matrix is not None and len(matrix) > 0:
                    # Определяем размеры для декартова произведения
                    if index == 5:
                        n1, n2 = self.graph_ops.n1_G1G2, self.graph_ops.n2_G1G2
                        labels = []
                        for i in range(n1):
                            for j in range(n2):
                                labels.append(f"({i + 1},{j + 1})")
                    else:
                        n1, n2 = self.graph_ops.n1_G1G3, self.graph_ops.n2_G1G3
                        labels = []
                        for i in range(n1):
                            for j in range(n2):
                                labels.append(f"({i + 1},{j + 1})")
                    self.matrix_widgets[index].set_matrix(matrix, labels)
                else:
                    # Для обычных графов используем просто номера
                    self.matrix_widgets[index].set_matrix(matrix)
            else:
                self.matrix_widgets[index].set_matrix(matrix)

    def update_visualization_tab(self, index, matrix, title):
        """Обновление вкладки с визуализацией"""
        if index < len(self.viz_widgets):
            if matrix is not None and len(matrix) > 0:
                # Для декартова произведения создаем специальные метки
                if index in [5, 6]:
                    if index == 5:
                        n1, n2 = self.graph_ops.n1_G1G2, self.graph_ops.n2_G1G2
                        labels = []
                        for i in range(n1):
                            for j in range(n2):
                                labels.append(f"({i + 1},{j + 1})")
                    else:
                        n1, n2 = self.graph_ops.n1_G1G3, self.graph_ops.n2_G1G3
                        labels = []
                        for i in range(n1):
                            for j in range(n2):
                                labels.append(f"({i + 1},{j + 1})")
                    
                    G = self.graph_ops.create_nx_graph(matrix, labels)
                else:
                    G = self.graph_ops.create_nx_graph(matrix)
                
                self.viz_widgets[index].draw_graph(G, title)
            else:
                self.viz_widgets[index].ax.clear()
                self.viz_widgets[index].ax.text(0.5, 0.5, "Нет данных",
                                                ha='center', va='center', fontsize=12, color='#c0caf5')
                self.viz_widgets[index].ax.set_facecolor('#1a1b26')
                self.viz_widgets[index].fig.patch.set_facecolor('#1a1b26')
                self.viz_widgets[index].ax.axis('off')
                self.viz_widgets[index].draw()


def main():
    app = QApplication(sys.argv)
    
    # Устанавливаем темную тему для всего приложения
    app.setStyle("Fusion")
    
    # Создаем темную палитру
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(26, 27, 38))  # #1a1b26
    palette.setColor(QPalette.WindowText, QColor(192, 202, 245))  # #c0caf5
    palette.setColor(QPalette.Base, QColor(36, 40, 59))  # #24283b
    palette.setColor(QPalette.AlternateBase, QColor(26, 27, 38))  # #1a1b26
    palette.setColor(QPalette.ToolTipBase, QColor(26, 27, 38))  # #1a1b26
    palette.setColor(QPalette.ToolTipText, QColor(192, 202, 245))  # #c0caf5
    palette.setColor(QPalette.Text, QColor(192, 202, 245))  # #c0caf5
    palette.setColor(QPalette.Button, QColor(36, 40, 59))  # #24283b
    palette.setColor(QPalette.ButtonText, QColor(192, 202, 245))  # #c0caf5
    palette.setColor(QPalette.BrightText, QColor(255, 255, 255))
    palette.setColor(QPalette.Link, QColor(122, 162, 247))  # #7aa2f7
    palette.setColor(QPalette.Highlight, QColor(122, 162, 247))  # #7aa2f7
    palette.setColor(QPalette.HighlightedText, QColor(26, 27, 38))  # #1a1b26
    
    app.setPalette(palette)
    
    # Устанавливаем стиль для всей программы
    app.setStyleSheet("""
        QToolTip {
            background-color: #1a1b26;
            color: #c0caf5;
            border: 1px solid #7aa2f7;
            padding: 5px;
            border-radius: 3px;
        }
    """)
    
    window = GraphOperationsApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()