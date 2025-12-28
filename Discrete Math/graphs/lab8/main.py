import numpy as np
import sys
import matplotlib

matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import networkx as nx
from collections import deque
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QTextEdit, QGroupBox,
                             QMessageBox, QSplitter, QFrame, QFormLayout, QTabWidget,
                             QTableWidget, QTableWidgetItem, QHeaderView, QSpinBox,
                             QComboBox, QCheckBox, QGridLayout, QScrollArea, QSizePolicy,
                             QSlider, QToolBar, QAction, QStatusBar, QListWidget, QListWidgetItem)
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QColor, QBrush, QPalette, QIcon, QKeySequence


class WaveAlgorithm:
    """Реализация волнового алгоритма для поиска минимального пути"""

    def __init__(self, adjacency_matrix):
        """
        Инициализация алгоритма

        Args:
            adjacency_matrix: матрица смежности графа
        """
        self.adj_matrix = adjacency_matrix
        self.n = len(adjacency_matrix)

    def find_min_path(self, start, end):
        """
        Нахождение минимального пути от start до end

        Args:
            start: начальная вершина (0-based)
            end: конечная вершина (0-based)

        Returns:
            tuple: (length, path, T, P, steps_log)
            length: длина пути (-1 если пути нет, 0 если start == end)
            path: список вершин пути
            T: массив временных меток
            P: массив меток предыдущих вершин
            steps_log: журнал выполнения алгоритма
        """
        # Инициализация
        T = [0] * self.n  # Временные метки
        P = [0] * self.n  # Метки предыдущих вершин

        # Если начальная и конечная вершины совпадают
        if start == end:
            return 0, [start + 1], T, P, ["Начальная и конечная вершины совпадают"]

        # Инициализация списков фронта волны
        OF = [start]  # Старый фронт (текущая волна)
        NF = []  # Новый фронт (следующая волна)

        T[start] = 1
        P[start] = 0

        current_time = 1
        steps_log = []
        steps_log.append(f"ШАГ 1: Инициализация")
        steps_log.append(f"  Начальная вершина: {start + 1}")
        steps_log.append(f"  Конечная вершина: {end + 1}")
        steps_log.append(f"  Установлено T[{start + 1}] = {current_time}")

        iteration = 1

        while True:
            steps_log.append(f"\nИТЕРАЦИЯ {iteration}:")
            steps_log.append(f"  OF = {[v + 1 for v in OF]}")
            steps_log.append(f"  Текущее время T = {current_time}")

            # Обработка вершин в OF
            for vertex in OF:
                steps_log.append(f"  Обрабатываем вершину {vertex + 1}:")

                # Просмотр соседних вершин
                for neighbor in range(self.n):
                    if self.adj_matrix[vertex][neighbor] == 1:
                        steps_log.append(f"    Сосед: {neighbor + 1}, T = {T[neighbor]}")

                        if T[neighbor] == 0:  # Вершина еще не помечена
                            T[neighbor] = current_time + 1
                            P[neighbor] = vertex + 1  # Сохраняем 1-based индексы
                            NF.append(neighbor)
                            steps_log.append(
                                f"    -> Помечаем: T[{neighbor + 1}] = {T[neighbor]}, P[{neighbor + 1}] = {vertex + 1}")
                            steps_log.append(f"    -> Добавляем {neighbor + 1} в NF")

            steps_log.append(f"  После обработки: NF = {[v + 1 for v in NF]}")

            # Проверка условий завершения
            if not NF:
                steps_log.append(f"\nШАГ 6: NF пуст - пути не существует")
                return -1, [], T, P, steps_log

            if end in NF:
                steps_log.append(f"\nШАГ 6: Найдена конечная вершина {end + 1} в NF")
                steps_log.append(f"  Длина пути: {current_time}")

                # Восстановление пути
                path = []
                current = end

                # Сначала добавляем конечную вершину
                path.append(current + 1)

                # Восстанавливаем путь в обратном порядке
                while current != start:
                    prev_vertex = P[current] - 1  # Переводим в 0-based
                    if prev_vertex < 0:  # Защита от ошибок
                        break
                    path.insert(0, prev_vertex + 1)
                    current = prev_vertex

                # Добавляем начальную вершину
                if path[0] != start + 1:
                    path.insert(0, start + 1)

                steps_log.append(f"  Восстановленный путь: {' → '.join(map(str, path))}")
                return current_time, path, T, P, steps_log

            # Подготовка к следующей итерации
            OF = NF.copy()
            NF = []
            current_time += 1
            iteration += 1

            if iteration > self.n * 2:  # Защита от бесконечного цикла
                steps_log.append(f"\nПРЕРЫВАНИЕ: Превышено максимальное количество итераций")
                return -1, [], T, P, steps_log


class MatrixTableWidget(QTableWidget):
    """Виджет таблицы для отображения матриц с темной темой"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setAlternatingRowColors(True)
        self.setFont(QFont("Courier New", 8))
        
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
                color: #1a1b26
            }
        """)

        # Настраиваем заголовки
        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)

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
                    # СИНИЙ для единиц
                    item.setBackground(QBrush(QColor('#7aa2f7')))
                    item.setForeground(QBrush(QColor('#1a1b26')))
                else:
                    # Темный фон для нулей
                    item.setBackground(QBrush(QColor('#24283b')))
                    item.setForeground(QBrush(QColor('#c0caf5')))
                self.setItem(i, j, item)

        for i in range(n):
            self.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)
            self.verticalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)


class GraphCanvas(FigureCanvas):
    """Холст для отрисовки графов с выделением пути и темной темой"""

    def __init__(self, parent=None, width=5, height=5, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor='#1a1b26')
        self.ax = self.fig.add_subplot(111, facecolor='#1a1b26')
        super().__init__(self.fig)
        self.setParent(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Настраиваем темную тему для холста
        self.setStyleSheet("background-color: #1a1b26; border: 1px solid #3b4261;")

    def draw_graph_with_path(self, G, path_vertices=None, start_vertex=None, end_vertex=None, title=""):
        """Отрисовка графа с выделением пути в темной теме"""
        self.ax.clear()
        
        # Устанавливаем темный фон
        self.ax.set_facecolor('#1a1b26')
        self.fig.patch.set_facecolor('#1a1b26')

        if G is None or len(G.nodes()) == 0:
            self.ax.text(0.5, 0.5, "Граф не сгенерирован",
                         ha='center', va='center', fontsize=12, color='#c0caf5')
            self.ax.set_xlim(0, 1)
            self.ax.set_ylim(0, 1)
            self.draw()
            return

        # Используем spring layout для красивой визуализации
        pos = nx.spring_layout(G, seed=42, k=1.5, iterations=100)

        # Определяем цвета вершин в темной теме
        node_colors = []
        node_sizes = []

        for node in G.nodes():
            if path_vertices and (node + 1) in path_vertices:
                # Вершины на пути
                if node + 1 == start_vertex:
                    node_colors.append('#FF6B6B')  # Красный - начальная
                elif node + 1 == end_vertex:
                    node_colors.append('#2ECC71')  # Зеленый - конечная
                else:
                    node_colors.append('#7aa2f7')  # Синий - промежуточные
                node_sizes.append(800)
            else:
                # Обычные вершины
                node_colors.append('#24283b')  # Темно-серый
                node_sizes.append(500)

        # Рисуем все вершины
        nx.draw_networkx_nodes(G, pos, ax=self.ax,
                               node_color=node_colors,
                               node_size=node_sizes,
                               edgecolors='#c0caf5',  # Светлая обводка
                               linewidths=2)

        # Рисуем все ребра серым цветом
        nx.draw_networkx_edges(G, pos, ax=self.ax,
                               edge_color='#3b4261',  # Темно-серый
                               width=1.5,
                               alpha=0.5)

        # Если есть путь, рисуем ребра пути цветом акцента
        if path_vertices and len(path_vertices) > 1:
            path_edges = []
            for i in range(len(path_vertices) - 1):
                u = path_vertices[i] - 1  # Переводим в 0-based
                v = path_vertices[i + 1] - 1
                if G.has_edge(u, v):
                    path_edges.append((u, v))

            if path_edges:
                nx.draw_networkx_edges(G, pos, ax=self.ax,
                                       edgelist=path_edges,
                                       edge_color='#ff9e64',  # Оранжевый для пути
                                       width=3,
                                       alpha=0.8,
                                       style='solid')

        # Рисуем метки вершин
        labels = {node: str(node + 1) for node in G.nodes()}
        nx.draw_networkx_labels(G, pos, ax=self.ax,
                                labels=labels,
                                font_size=10,
                                font_weight='bold',
                                font_color='#c0caf5')  # Светлый текст

        # Настраиваем заголовок
        self.ax.set_title(title, fontsize=12, fontweight='bold', pad=15, color='#7aa2f7')
        
        # Отключаем оси
        self.ax.axis('off')
        
        # Настраиваем границы
        for spine in self.ax.spines.values():
            spine.set_edgecolor('#3b4261')
            
        self.fig.tight_layout()
        self.draw()


class GraphOperations:
    """Класс для операций с графами для волнового алгоритма"""

    def __init__(self, n):
        self.n = n
        self.adj_matrix = None
        self.inc_matrix = None
        self.G_nx = None
        self.generate_graph()

    def generate_graph(self, density=0.3):
        """Генерация случайного связного графа"""
        self.adj_matrix = np.zeros((self.n, self.n), dtype=int)

        # Сначала создаем связный остов (дерево)
        for i in range(1, self.n):
            parent = np.random.randint(0, i)
            self.adj_matrix[i][parent] = 1
            self.adj_matrix[parent][i] = 1

        # Добавляем случайные ребра для достижения нужной плотности
        total_possible_edges = self.n * (self.n - 1) // 2
        current_edges = self.n - 1  # Ребра в остове
        target_edges = int(total_possible_edges * density)

        while current_edges < target_edges and current_edges < total_possible_edges:
            i = np.random.randint(0, self.n)
            j = np.random.randint(0, self.n)
            if i != j and self.adj_matrix[i][j] == 0:
                self.adj_matrix[i][j] = 1
                self.adj_matrix[j][i] = 1
                current_edges += 1

        # Генерация матрицы инцидентности
        self.generate_incidence_matrix()

        # Создание графа для networkx
        self.create_nx_graph()

        return self.adj_matrix

    def generate_incidence_matrix(self):
        """Генерация матрицы инцидентности"""
        edges = []
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if self.adj_matrix[i][j] == 1:
                    edges.append((i, j))

        self.inc_matrix = np.zeros((self.n, len(edges)), dtype=int)

        for edge_idx, (u, v) in enumerate(edges):
            self.inc_matrix[u][edge_idx] = 1
            self.inc_matrix[v][edge_idx] = 1

        return self.inc_matrix

    def create_nx_graph(self):
        """Создание графа networkx из матрицы смежности"""
        self.G_nx = nx.Graph()
        self.G_nx.add_nodes_from(range(self.n))
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if self.adj_matrix[i][j] == 1:
                    self.G_nx.add_edge(i, j)

    def get_vertex_degrees(self):
        """Получение степеней вершин"""
        degrees = []
        for i in range(self.n):
            degree = sum(self.adj_matrix[i])
            degrees.append(degree)
        return degrees

    def find_min_path_wave(self, start, end):
        """Нахождение минимального пути с помощью волнового алгоритма"""
        if self.adj_matrix is None:
            return -1, [], [], [], []

        wave_algo = WaveAlgorithm(self.adj_matrix)
        length, path, T, P, steps_log = wave_algo.find_min_path(start - 1, end - 1)

        return length, path, T, P, steps_log


class WaveAlgorithmApp(QMainWindow):
    """Главное окно приложения с темной темой"""

    def __init__(self):
        super().__init__()
        self.graph_ops = None
        self.init_ui()
        self.generate_graph()

    def init_ui(self):
        """Инициализация интерфейса с темной темой"""
        self.setWindowTitle("Волновой алгоритм для поиска минимального пути в графе")
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
            QSpinBox, QSlider {
                background-color: #24283b;
                color: #c0caf5;
                border: 1px solid #7aa2f7;
                border-radius: 3px;
                padding: 3px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                background-color: #3b4261;
                border: 1px solid #7aa2f7;
            }
            QPushButton {
                background-color: #7aa2f7;
                color: #1a1b26;
                border: 1px solid #7aa2f7;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 11px;
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
            QTextEdit, QListWidget {
                background-color: #24283b;
                color: #c0caf5;
                border: 1px solid #3b4261;
                border-radius: 3px;
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
            QSplitter::handle {
                background-color: #7aa2f7;
            }
            QSplitter::handle:hover {
                background-color: #9ece6a;
            }
        """)

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(5)
        main_layout.setContentsMargins(5, 5, 5, 5)

        # Заголовок
        title = QLabel("ВОЛНОВОЙ АЛГОРИТМ ПОИСКА МИНИМАЛЬНОГО ПУТИ")
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
        control_group = QGroupBox("УПРАВЛЕНИЕ ГРАФОМ И ПОИСКОМ ПУТИ")
        control_group.setFont(QFont("Arial", 10, QFont.Bold))
        control_layout = QGridLayout(control_group)
        control_layout.setSpacing(10)

        # Количество вершин
        control_layout.addWidget(QLabel("Количество вершин (n > 8):"), 0, 0)
        self.n_spinbox = QSpinBox()
        self.n_spinbox.setRange(9, 20)
        self.n_spinbox.setValue(12)
        self.n_spinbox.setFixedWidth(80)
        control_layout.addWidget(self.n_spinbox, 0, 1)

        # Плотность графа
        control_layout.addWidget(QLabel("Плотность графа:"), 0, 2)
        self.density_slider = QSlider(Qt.Horizontal)
        self.density_slider.setRange(10, 70)
        self.density_slider.setValue(30)
        self.density_slider.setFixedWidth(100)
        control_layout.addWidget(self.density_slider, 0, 3)
        self.density_label = QLabel("0.3")
        self.density_label.setFixedWidth(40)
        control_layout.addWidget(self.density_label, 0, 4)
        self.density_slider.valueChanged.connect(self.update_density_label)

        # Начальная вершина
        control_layout.addWidget(QLabel("Начальная вершина:"), 1, 0)
        self.start_spinbox = QSpinBox()
        self.start_spinbox.setRange(1, 20)
        self.start_spinbox.setValue(1)
        self.start_spinbox.setFixedWidth(80)
        control_layout.addWidget(self.start_spinbox, 1, 1)

        # Конечная вершина
        control_layout.addWidget(QLabel("Конечная вершина:"), 1, 2)
        self.end_spinbox = QSpinBox()
        self.end_spinbox.setRange(1, 20)
        self.end_spinbox.setValue(5)
        self.end_spinbox.setFixedWidth(80)
        control_layout.addWidget(self.end_spinbox, 1, 3)

        # Кнопка генерации
        self.generate_btn = QPushButton("СГЕНЕРИРОВАТЬ ГРАФ")
        self.generate_btn.clicked.connect(self.generate_graph)
        control_layout.addWidget(self.generate_btn, 0, 5)

        # Кнопка поиска пути
        self.find_path_btn = QPushButton("НАЙТИ МИНИМАЛЬНЫЙ ПУТЬ")
        self.find_path_btn.clicked.connect(self.find_min_path)
        control_layout.addWidget(self.find_path_btn, 1, 5)

        main_layout.addWidget(control_group)

        # Основной сплиттер
        main_splitter = QSplitter(Qt.Horizontal)
        main_splitter.setHandleWidth(3)
        main_splitter.setStyleSheet("QSplitter::handle { background-color: #7aa2f7; }")

        # Левая часть - матрицы и информация
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(2, 2, 2, 2)

        # Вкладки для левой части
        self.left_tabs = QTabWidget()
        self.left_tabs.setFont(QFont("Arial", 9, QFont.Bold))

        # Создаем вкладки левой части
        self.create_left_tabs()

        left_layout.addWidget(self.left_tabs)
        main_splitter.addWidget(left_widget)

        # Правая часть - визуализация и журнал
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(2, 2, 2, 2)

        # Вкладки для правой части
        self.right_tabs = QTabWidget()
        self.right_tabs.setFont(QFont("Arial", 9, QFont.Bold))

        # Создаем вкладки правой части
        self.create_right_tabs()

        right_layout.addWidget(self.right_tabs)
        main_splitter.addWidget(right_widget)

        # Устанавливаем начальные размеры
        main_splitter.setSizes([800, 900])
        main_layout.addWidget(main_splitter, 1)

        # Статусная строка
        self.status_label = QLabel("Готов к работе. Сгенерируйте граф и найдите путь.")
        self.status_label.setFont(QFont("Arial", 9))
        self.status_label.setStyleSheet("color: #c0caf5; padding: 5px;")
        main_layout.addWidget(self.status_label)

    def create_left_tabs(self):
        """Создание вкладок левой части"""
        # Вкладка с матрицей смежности
        self.adj_table = MatrixTableWidget()

        adj_container = QWidget()
        adj_layout = QVBoxLayout(adj_container)
        adj_layout.setContentsMargins(0, 0, 0, 0)

        adj_label = QLabel("Матрица смежности S (основа для волнового алгоритма)")
        adj_label.setFont(QFont("Arial", 10, QFont.Bold))
        adj_label.setStyleSheet("color: #7aa2f7; padding: 5px;")
        adj_label.setAlignment(Qt.AlignCenter)
        adj_layout.addWidget(adj_label)

        adj_hint = QLabel("Синим выделены единицы (наличие ребра)")
        adj_hint.setFont(QFont("Arial", 8))
        adj_hint.setStyleSheet("color: #a9b1d6; padding: 2px;")
        adj_hint.setAlignment(Qt.AlignCenter)
        adj_layout.addWidget(adj_hint)

        adj_layout.addWidget(self.adj_table)

        scroll_adj = QScrollArea()
        scroll_adj.setWidget(adj_container)
        scroll_adj.setWidgetResizable(True)
        self.left_tabs.addTab(scroll_adj, "Матрица смежности")

        # Вкладка с матрицей инцидентности
        self.inc_table = MatrixTableWidget()

        inc_container = QWidget()
        inc_layout = QVBoxLayout(inc_container)
        inc_layout.setContentsMargins(0, 0, 0, 0)

        inc_label = QLabel("Матрица инцидентности")
        inc_label.setFont(QFont("Arial", 10, QFont.Bold))
        inc_label.setStyleSheet("color: #7aa2f7; padding: 5px;")
        inc_label.setAlignment(Qt.AlignCenter)
        inc_layout.addWidget(inc_label)

        inc_layout.addWidget(self.inc_table)

        scroll_inc = QScrollArea()
        scroll_inc.setWidget(inc_container)
        scroll_inc.setWidgetResizable(True)
        self.left_tabs.addTab(scroll_inc, "Матрица инцидентности")

        # Вкладка со свойствами графа
        info_container = QWidget()
        info_layout = QVBoxLayout(info_container)

        info_label = QLabel("СВОЙСТВА ГРАФА")
        info_label.setFont(QFont("Arial", 10, QFont.Bold))
        info_label.setStyleSheet("color: #7aa2f7; padding: 10px;")
        info_label.setAlignment(Qt.AlignCenter)
        info_layout.addWidget(info_label)

        self.graph_info_text = QTextEdit()
        self.graph_info_text.setFont(QFont("Courier New", 9))
        self.graph_info_text.setReadOnly(True)
        info_layout.addWidget(self.graph_info_text)

        self.left_tabs.addTab(info_container, "Свойства графа")

    def create_right_tabs(self):
        """Создание вкладок правой части"""
        # Вкладка с визуализацией графа
        self.graph_canvas = GraphCanvas(self, width=6, height=5.5)

        viz_container = QWidget()
        viz_layout = QVBoxLayout(viz_container)
        viz_layout.setContentsMargins(0, 0, 0, 0)

        viz_label = QLabel("ВИЗУАЛИЗАЦИЯ ГРАФА С ПУТЕМ")
        viz_label.setFont(QFont("Arial", 10, QFont.Bold))
        viz_label.setStyleSheet("color: #7aa2f7; padding: 5px;")
        viz_label.setAlignment(Qt.AlignCenter)
        viz_layout.addWidget(viz_label)

        # Легенда
        legend_widget = QWidget()
        legend_layout = QGridLayout(legend_widget)
        legend_layout.setHorizontalSpacing(15)
        legend_layout.setVerticalSpacing(5)

        legend_items = [
            ("Начальная вершина", "#FF6B6B"),
            ("Конечная вершина", "#2ECC71"),
            ("Вершины пути", "#7aa2f7"),
            ("Обычные вершины", "#24283b"),
            ("Ребра пути", "#ff9e64"),
            ("Обычные ребра", "#3b4261")
        ]

        for i, (text, color) in enumerate(legend_items):
            row = i // 2
            col = (i % 2) * 2
            
            color_label = QLabel("■")
            color_label.setStyleSheet(f"color: {color}; font-size: 16px;")
            text_label = QLabel(text)
            text_label.setStyleSheet("font-size: 9px; color: #c0caf5;")
            
            legend_layout.addWidget(color_label, row, col)
            legend_layout.addWidget(text_label, row, col + 1)

        legend_layout.setColumnStretch(4, 1)
        viz_layout.addWidget(legend_widget)
        viz_layout.addWidget(self.graph_canvas)

        scroll_viz = QScrollArea()
        scroll_viz.setWidget(viz_container)
        scroll_viz.setWidgetResizable(True)
        self.right_tabs.addTab(scroll_viz, "Визуализация")

        # Вкладка с журналом выполнения алгоритма
        log_container = QWidget()
        log_layout = QVBoxLayout(log_container)

        log_label = QLabel("ЖУРНАЛ ВЫПОЛНЕНИЯ ВОЛНОВОГО АЛГОРИТМА")
        log_label.setFont(QFont("Arial", 10, QFont.Bold))
        log_label.setStyleSheet("color: #7aa2f7; padding: 10px;")
        log_label.setAlignment(Qt.AlignCenter)
        log_layout.addWidget(log_label)

        self.algorithm_log = QTextEdit()
        self.algorithm_log.setFont(QFont("Courier New", 9))
        self.algorithm_log.setReadOnly(True)
        log_layout.addWidget(self.algorithm_log)

        self.right_tabs.addTab(log_container, "Журнал алгоритма")

        # Вкладка с массивами T и P
        arrays_container = QWidget()
        arrays_layout = QVBoxLayout(arrays_container)

        arrays_label = QLabel("МАССИВЫ T И P ВОЛНОВОГО АЛГОРИТМА")
        arrays_label.setFont(QFont("Arial", 10, QFont.Bold))
        arrays_label.setStyleSheet("color: #7aa2f7; padding: 10px;")
        arrays_label.setAlignment(Qt.AlignCenter)
        arrays_layout.addWidget(arrays_label)

        # Виджет для отображения массивов
        self.arrays_text = QTextEdit()
        self.arrays_text.setFont(QFont("Courier New", 10))
        self.arrays_text.setReadOnly(True)
        arrays_layout.addWidget(self.arrays_text)

        self.right_tabs.addTab(arrays_container, "Массивы T и P")

    def update_density_label(self, value):
        """Обновление метки плотности графа"""
        density = value / 100.0
        self.density_label.setText(f"{density:.1f}")

    def generate_graph(self):
        """Генерация нового графа"""
        n = self.n_spinbox.value()
        density = self.density_slider.value() / 100.0

        # Обновляем диапазоны для вершин
        self.start_spinbox.setRange(1, n)
        self.end_spinbox.setRange(1, n)

        self.graph_ops = GraphOperations(n)
        self.graph_ops.generate_graph(density)

        # Обновляем матрицы
        self.adj_table.set_matrix(self.graph_ops.adj_matrix)
        self.inc_table.set_matrix(self.graph_ops.inc_matrix)

        # Обновляем информацию о графе
        self.update_graph_info()

        # Очищаем результаты предыдущего поиска
        self.clear_path_results()

        # Обновляем визуализацию
        self.update_visualization()

        self.status_label.setText(f"Граф сгенерирован! Вершин: {n}, Плотность: {density:.2f}")

    def update_graph_info(self):
        """Обновление информации о графе"""
        if self.graph_ops is None:
            return

        degrees = self.graph_ops.get_vertex_degrees()

        text = "\n"
        text += "ОСНОВНЫЕ ХАРАКТЕРИСТИКИ ГРАФА\n"
        text += "=" * 35 + "\n\n"

        text += f"Количество вершин: {self.graph_ops.n}\n"

        # Подсчет ребер
        edge_count = np.sum(self.graph_ops.adj_matrix) // 2
        text += f"Количество ребер: {edge_count}\n"

        # Максимально возможное количество ребер
        max_edges = self.graph_ops.n * (self.graph_ops.n - 1) // 2
        density = edge_count / max_edges if max_edges > 0 else 0
        text += f"Плотность графа: {density:.3f}\n\n"

        text += "СТЕПЕНИ ВЕРШИН:\n"
        text += "-" * 20 + "\n"
        for i, deg in enumerate(degrees):
            text += f"  Вершина {i + 1}: степень {deg}\n"

        # Анализ вершин
        isolated = [i + 1 for i, deg in enumerate(degrees) if deg == 0]
        pendant = [i + 1 for i, deg in enumerate(degrees) if deg == 1]
        dominating = [i + 1 for i, deg in enumerate(degrees) if deg == self.graph_ops.n - 1]

        text += f"\nИЗОЛИРОВАННЫЕ ВЕРШИНЫ (степень 0): "
        text += f"{isolated if isolated else 'нет'}\n"

        text += f"КОНЦЕВЫЕ ВЕРШИНЫ (степень 1): "
        text += f"{pendant if pendant else 'нет'}\n"

        text += f"ДОМИНИРУЮЩИЕ ВЕРШИНЫ (степень n-1): "
        text += f"{dominating if dominating else 'нет'}\n"

        self.graph_info_text.setText(text)

    def clear_path_results(self):
        """Очистка результатов поиска пути"""
        self.algorithm_log.clear()
        self.arrays_text.clear()

        # Очищаем визуализацию пути
        if self.graph_ops and self.graph_ops.G_nx:
            self.graph_canvas.draw_graph_with_path(
                self.graph_ops.G_nx,
                title="Граф G (путь не найден)"
            )

    def update_visualization(self, path_vertices=None):
        """Обновление визуализации графа"""
        if self.graph_ops is None or self.graph_ops.G_nx is None:
            return

        start_vertex = self.start_spinbox.value() if path_vertices else None
        end_vertex = self.end_spinbox.value() if path_vertices else None

        title = "Граф G"
        if path_vertices:
            if len(path_vertices) > 0:
                title = f"Минимальный путь {start_vertex} → {end_vertex}"
            else:
                title = f"Путь {start_vertex} → {end_vertex} не существует"

        self.graph_canvas.draw_graph_with_path(
            self.graph_ops.G_nx,
            path_vertices=path_vertices,
            start_vertex=start_vertex,
            end_vertex=end_vertex,
            title=title
        )

    def find_min_path(self):
        """Поиск минимального пути с помощью волнового алгоритма"""
        if self.graph_ops is None:
            QMessageBox.warning(self, "Предупреждение", "Сначала сгенерируйте граф!")
            return

        start = self.start_spinbox.value()
        end = self.end_spinbox.value()

        if start < 1 or start > self.graph_ops.n or end < 1 or end > self.graph_ops.n:
            QMessageBox.warning(self, "Ошибка", "Номера вершин должны быть в диапазоне от 1 до n")
            return

        try:
            # Выполнение волнового алгоритма
            length, path, T, P, steps_log = self.graph_ops.find_min_path_wave(start, end)

            # Отображение журнала выполнения
            log_text = "\n".join(steps_log)
            self.algorithm_log.setText(log_text)

            # Отображение массивов T и P
            self.display_arrays(T, P, start, end, length, path)

            # Обновление визуализации
            self.update_visualization(path)

            # Прокрутка журнала вверх
            self.algorithm_log.verticalScrollBar().setValue(0)

            # Обновление статуса
            if length == -1:
                self.status_label.setText(f"Путь от {start} до {end} не существует")
            elif length == 0:
                self.status_label.setText(f"Вершины {start} и {end} совпадают")
            else:
                self.status_label.setText(f"Найден путь от {start} до {end} длиной {length}")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при поиске пути: {str(e)}")

    def display_arrays(self, T, P, start, end, length, path):
        """Отображение массивов T и P"""
        if not T or not P:
            return

        text = "\n"
        text += "РЕЗУЛЬТАТЫ ПОИСКА ПУТИ\n"
        text += "=" * 25 + "\n\n"

        text += f"Начальная вершина: {start}\n"
        text += f"Конечная вершина: {end}\n\n"

        if length == -1:
            text += "ПУТЬ НЕ СУЩЕСТВУЕТ\n"
            text += "Не существует маршрута от начальной до конечной вершины.\n"
        elif length == 0:
            text += "НАЧАЛЬНАЯ И КОНЕЧНАЯ ВЕРШИНЫ СОВПАДАЮТ\n"
            text += f"Длина пути: {length}\n"
            text += f"Путь: [{start}]\n"
        else:
            text += f"ПУТЬ НАЙДЕН\n"
            text += f"Длина пути (количество ребер): {length}\n"
            text += f"Количество вершин в пути: {len(path)}\n"
            text += f"Минимальный путь: {' → '.join(map(str, path))}\n\n"

        text += "\n" + "=" * 40 + "\n\n"
        text += "МАССИВЫ ВОЛНОВОГО АЛГОРИТМА\n"
        text += "=" * 30 + "\n\n"

        text += "T[i] - время достижения вершины i\n"
        text += "P[i] - предыдущая вершина в пути к вершине i\n\n"

        text += f"{'Вершина i':<10} {'T[i]':<10} {'P[i]':<10}\n"
        text += "-" * 35 + "\n"

        for i in range(len(T)):
            t_val = T[i] if T[i] > 0 else "0"
            p_val = P[i] if P[i] > 0 else "0"
            text += f"{i + 1:<10} {t_val:<10} {p_val:<10}\n"

        self.arrays_text.setText(text)


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
    
    window = WaveAlgorithmApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()