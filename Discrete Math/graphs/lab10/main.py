import sys
import numpy as np
from collections import deque
import matplotlib

matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import networkx as nx
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QGroupBox,
    QMessageBox, QSplitter, QFrame, QFormLayout, QTabWidget,
    QTableWidget, QTableWidgetItem, QHeaderView, QSpinBox,
    QComboBox, QCheckBox, QGridLayout, QScrollArea, QSizePolicy,
    QSlider, QToolBar, QAction, QStatusBar, QListWidget, QListWidgetItem,
    QDoubleSpinBox
)
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QColor, QBrush, QPalette, QIcon, QKeySequence


class DijkstraAlgorithm:
    """Реализация алгоритма Дейкстры для поиска пути минимального веса"""

    def __init__(self, weight_matrix, GM):
        """
        Инициализация алгоритма

        Args:
            weight_matrix: весовая матрица графа (n x n)
            GM: значение, представляющее бесконечность
        """
        self.W = weight_matrix
        self.n = len(weight_matrix)
        self.GM = GM

    def find_shortest_path(self, u1, u2):
        """
        Нахождение пути минимального веса от u1 до u2

        Args:
            u1: начальная вершина (0-based)
            u2: конечная вершина (0-based)

        Returns:
            tuple: (length, weight, path, d, m, prev, steps_log)
            length: длина пути (-1 если пути нет, 0 если u1 == u2)
            weight: вес найденного пути
            path: список вершин пути
            d: массив весов вершин
            m: массив меток вершин
            prev: массив предыдущих вершин
            steps_log: журнал выполнения алгоритма
        """
        # Преобразуем в 0-based индексы
        u1 = u1 - 1
        u2 = u2 - 1

        # Шаг 1: Инициализация
        d = [self.GM] * self.n  # Веса вершин
        m = [0] * self.n  # Метки вершин (0 - не помечена, 1 - помечена)
        prev = [-1] * self.n  # Предыдущие вершины в пути

        d[u1] = 0  # Вес начальной вершины

        steps_log = []
        steps_log.append("=" * 60)
        steps_log.append("АЛГОРИТМ ДЕЙКСТРЫ - НАЧАЛО РАБОТЫ")
        steps_log.append("=" * 60)
        steps_log.append(f"Начальная вершина: {u1 + 1}")
        steps_log.append(f"Конечная вершина: {u2 + 1}")
        steps_log.append(f"GM (бесконечность): {self.GM}")
        steps_log.append(f"d[{u1 + 1}] = 0")
        steps_log.append(f"d[i] = GM для всех i != {u1 + 1}")
        steps_log.append(f"m[i] = 0 для всех вершин")
        steps_log.append(f"prev[i] = -1 для всех вершин")

        # Если начальная и конечная вершины совпадают
        if u1 == u2:
            steps_log.append(f"\nНачальная и конечная вершины совпадают!")
            steps_log.append(f"Длина пути: 0, Вес пути: 0")
            return 0, 0, [u1 + 1], d, m, prev, steps_log

        # Текущая вершина
        t = u1
        iteration = 1

        while True:
            steps_log.append(f"\n" + "-" * 40)
            steps_log.append(f"ИТЕРАЦИЯ {iteration}")
            steps_log.append(f"Текущая вершина: t = {t + 1}")
            steps_log.append(f"Метка текущей вершины: m[{t + 1}] = 1")

            # Помечаем текущую вершину
            m[t] = 1

            # Шаг 4: Пересчет весов для непомеченных вершин
            steps_log.append(f"\nШаг 4: Пересчет весов для вершин с m[i] = 0")

            updated = False
            for i in range(self.n):
                if m[i] == 0 and self.W[t][i] < self.GM:
                    old_d = d[i]
                    new_d = d[t] + self.W[t][i]
                    if new_d < d[i]:
                        d[i] = new_d
                        prev[i] = t
                        steps_log.append(f"  d[{i + 1}] = min({old_d}, {d[t]} + {self.W[t][i]}) = {new_d}")
                        steps_log.append(f"  prev[{i + 1}] = {t + 1}")
                        updated = True
                    else:
                        steps_log.append(
                            f"  d[{i + 1}] = min({old_d}, {d[t]} + {self.W[t][i]}) = {old_d} (не изменился)")

            if not updated:
                steps_log.append(f"  Веса не изменились")

            # Шаг 5: Поиск непомеченной вершины с минимальным весом
            steps_log.append(f"\nШаг 5: Поиск вершины с минимальным d[i] среди m[i] = 0")

            min_d = self.GM
            min_vertex = -1

            for i in range(self.n):
                if m[i] == 0 and d[i] < min_d:
                    min_d = d[i]
                    min_vertex = i

            if min_vertex == -1:
                steps_log.append(f"  Все непомеченные вершины имеют вес GM - пути не существует!")
                steps_log.append(f"  Результат: length = -1 (пути не существует)")
                return -1, self.GM, [], d, m, prev, steps_log

            steps_log.append(f"  Найдена вершина: {min_vertex + 1} с d = {min_d}")

            # Обновляем текущую вершину
            t = min_vertex

            # Шаг 6: Проверка на достижение конечной вершины
            if t == u2:
                steps_log.append(f"\n" + "=" * 40)
                steps_log.append(f"ДОСТИГНУТА КОНЕЧНАЯ ВЕРШИНА {u2 + 1}")
                steps_log.append(f"Вес пути: d[{u2 + 1}] = {d[u2]}")

                # Восстановление пути
                path = []
                current = u2

                while current != -1:
                    path.insert(0, current + 1)  # Переводим в 1-based
                    current = prev[current]

                # Проверяем, что путь начинается с начальной вершины
                if path[0] != u1 + 1:
                    path.insert(0, u1 + 1)

                steps_log.append(f"Восстановленный путь: {' → '.join(map(str, path))}")
                steps_log.append(f"Количество вершин в пути: {len(path)}")
                steps_log.append(f"Количество ребер в пути: {len(path) - 1}")
                steps_log.append(f"Вес пути: {d[u2]}")

                return len(path) - 1, d[u2], path, d, m, prev, steps_log

            iteration += 1

            # Защита от бесконечного цикла
            if iteration > self.n * 2:
                steps_log.append(f"\nПРЕРЫВАНИЕ: Превышено максимальное количество итераций")
                return -1, self.GM, [], d, m, prev, steps_log


class MatrixTableWidget(QTableWidget):
    """Виджет таблицы с темной темой"""

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

    def set_weight_matrix(self, matrix, labels=None, GM=float('inf')):
        """Установка весовой матрицы для отображения"""
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
                if i == j:
                    value = "0"
                    bg_color = QColor('#24283b')  # Темный для диагонали
                    fg_color = QColor('#c0caf5')  # Светлый текст
                elif matrix[i][j] >= GM:
                    value = "∞"
                    bg_color = QColor('#f7768e')  # Красный для бесконечности
                    fg_color = QColor('#1a1b26')  # Темный текст
                else:
                    value = str(matrix[i][j])
                    if matrix[i][j] > 0:
                        bg_color = QColor('#9ece6a')  # Зеленый для положительных весов
                        fg_color = QColor('#1a1b26')  # Темный текст
                    else:
                        bg_color = QColor('#24283b')  # Темный для нулей
                        fg_color = QColor('#c0caf5')  # Светлый текст

                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignCenter)
                item.setBackground(QBrush(bg_color))
                item.setForeground(QBrush(fg_color))
                self.setItem(i, j, item)

        for i in range(n):
            self.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)
            self.verticalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)


class GraphCanvas(FigureCanvas):
    """Холст для отрисовки взвешенных графов с выделением пути в темной теме"""

    def __init__(self, parent=None, width=5, height=5, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor='#1a1b26')
        self.ax = self.fig.add_subplot(111, facecolor='#1a1b26')
        super().__init__(self.fig)
        self.setParent(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Настраиваем темную тему для холста
        self.setStyleSheet("background-color: #1a1b26; border: 1px solid #3b4261;")

    def draw_weighted_graph_with_path(self, G, pos=None, path_vertices=None,
                                      start_vertex=None, end_vertex=None,
                                      title="", weight_matrix=None, GM=float('inf')):
        """Отрисовка взвешенного графа с выделением пути в темной теме"""
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
        if pos is None:
            pos = nx.spring_layout(G, seed=42, k=1.5, iterations=100)

        # Определяем цвета вершин в темной теме
        node_colors = []
        node_sizes = []

        for node in G.nodes():
            if path_vertices and (node + 1) in path_vertices:
                # Вершины на пути
                if node + 1 == start_vertex:
                    node_colors.append('#f7768e')  # Красный - начальная
                elif node + 1 == end_vertex:
                    node_colors.append('#9ece6a')  # Зеленый - конечная
                else:
                    node_colors.append('#7aa2f7')  # Синий - промежуточные
                node_sizes.append(800)
            else:
                # Обычные вершины
                node_colors.append('#24283b')  # Темный
                node_sizes.append(500)

        # Рисуем все вершины
        nx.draw_networkx_nodes(G, pos, ax=self.ax,
                               node_color=node_colors,
                               node_size=node_sizes,
                               edgecolors='#c0caf5',  # Светлая обводка
                               linewidths=2)

        # Рисуем все ребра с цветами в темной теме
        edge_labels = {}
        all_edges = []

        for u, v in G.edges():
            all_edges.append((u, v))
            if weight_matrix is not None and u < len(weight_matrix) and v < len(weight_matrix):
                weight = weight_matrix[u][v]
                if weight < GM:
                    edge_labels[(u, v)] = f"{weight:.1f}"

        nx.draw_networkx_edges(G, pos, ax=self.ax,
                               edgelist=all_edges,
                               edge_color='#3b4261',  # Темно-серый
                               width=1.5,
                               alpha=0.5)

        # Рисуем подписи весов ребер
        nx.draw_networkx_edge_labels(G, pos, ax=self.ax,
                                     edge_labels=edge_labels,
                                     font_size=8,
                                     font_color='#c0caf5',  # Светлый текст
                                     bbox=dict(facecolor='#1a1b26', edgecolor='#3b4261', alpha=0.9))

        # Если есть путь, рисуем ребра пути
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
    """Класс для операций с взвешенными графами"""

    def __init__(self, n, GM=float('inf')):
        """
        Инициализация операций с графами
        
        Args:
            n: количество вершин
            GM: значение "бесконечности" (Grand Measurement)
        """
        self.n = n
        self.GM = GM
        self.weight_matrix = None
        self.G_nx = None
        self.generate_weighted_graph()

    def generate_weighted_graph(self, density=0.3, max_weight=10):
        """Генерация случайного связного взвешенного графа"""
        self.weight_matrix = np.full((self.n, self.n), self.GM, dtype=float)

        # Заполняем диагональ нулями
        for i in range(self.n):
            self.weight_matrix[i][i] = 0

        # Сначала создаем связный остов (дерево)
        for i in range(1, self.n):
            parent = np.random.randint(0, i)
            weight = np.random.randint(1, max_weight + 1)
            self.weight_matrix[i][parent] = weight
            self.weight_matrix[parent][i] = weight

        # Добавляем случайные ребра для достижения нужной плотности
        total_possible_edges = self.n * (self.n - 1) // 2
        current_edges = self.n - 1  # Ребра в остове
        target_edges = int(total_possible_edges * density)

        while current_edges < target_edges and current_edges < total_possible_edges:
            i = np.random.randint(0, self.n)
            j = np.random.randint(0, self.n)
            if i != j and self.weight_matrix[i][j] >= self.GM:
                weight = np.random.randint(1, max_weight + 1)
                self.weight_matrix[i][j] = weight
                self.weight_matrix[j][i] = weight
                current_edges += 1

        # Создание графа для networkx
        self.create_nx_graph()

        return self.weight_matrix

    def create_nx_graph(self):
        """Создание графа networkx из весовой матрицы"""
        self.G_nx = nx.Graph()
        self.G_nx.add_nodes_from(range(self.n))

        for i in range(self.n):
            for j in range(i + 1, self.n):
                if self.weight_matrix[i][j] < self.GM:
                    self.G_nx.add_edge(i, j, weight=self.weight_matrix[i][j])

    def get_graph_info(self):
        """Получение информации о графе"""
        info = {
            'n': self.n,
            'edges': 0,
            'total_possible_edges': self.n * (self.n - 1) // 2,
            'min_weight': self.GM,
            'max_weight': 0,
            'connected': True
        }

        # Подсчет ребер и весов
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if self.weight_matrix[i][j] < self.GM:
                    info['edges'] += 1
                    weight = self.weight_matrix[i][j]
                    if weight < info['min_weight']:
                        info['min_weight'] = weight
                    if weight > info['max_weight']:
                        info['max_weight'] = weight

        # Вычисляем плотность
        info['density'] = info['edges'] / info['total_possible_edges'] if info['total_possible_edges'] > 0 else 0

        return info

    def find_shortest_path_dijkstra(self, u1, u2):
        """Нахождение кратчайшего пути с помощью алгоритма Дейкстры"""
        if self.weight_matrix is None:
            return -1, self.GM, [], [], [], [], []

        dijkstra = DijkstraAlgorithm(self.weight_matrix, self.GM)
        length, weight, path, d, m, prev, steps_log = dijkstra.find_shortest_path(u1, u2)

        return length, weight, path, d, m, prev, steps_log


class DijkstraApp(QMainWindow):
    """Главное окно приложения с темной темой"""

    def __init__(self):
        super().__init__()
        self.graph_ops = None
        self.init_ui()
        self.generate_graph()

    def init_ui(self):
        """Инициализация интерфейса с темной темой"""
        self.setWindowTitle("Алгоритм Дейкстры - поиск пути минимального веса")
        # Открываем на весь экран, но с фиксированной логикой верстки
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(50, 50, screen.width() - 100, screen.height() - 100)

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
            QSpinBox, QDoubleSpinBox, QSlider {
                background-color: #24283b;
                color: #c0caf5;
                border: 1px solid #7aa2f7;
                border-radius: 3px;
                padding: 3px;
            }
            QSpinBox::up-button, QSpinBox::down-button,
            QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
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
            QCheckBox {
                color: #c0caf5;
            }
            QCheckBox::indicator {
                width: 13px;
                height: 13px;
                border: 2px solid #7aa2f7;
                border-radius: 3px;
                background-color: #24283b;
            }
            QCheckBox::indicator:checked {
                background-color: #7aa2f7;
                border-color: #7aa2f7;
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
        
        # Главный вертикальный layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Заголовок
        title = QLabel("АЛГОРИТМ ДЕЙКСТРЫ - ПОИСК ПУТИ МИНИМАЛЬНОГО ВЕСА В ГРАФЕ")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setStyleSheet("""
            QLabel {
                color: #7aa2f7;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1a1b26, stop:0.5 #24283b, stop:1 #1a1b26);
                padding: 12px;
                border-radius: 6px;
                border: 2px solid #7aa2f7;
            }
        """)
        main_layout.addWidget(title)

        # Панель управления
        control_group = QGroupBox("УПРАВЛЕНИЕ ГРАФОМ И ПАРАМЕТРАМИ")
        control_group.setFont(QFont("Arial", 10, QFont.Bold))
        
        # Используем GridLayout для управления с правильными пропорциями
        control_grid = QGridLayout(control_group)
        control_grid.setSpacing(15)
        control_grid.setContentsMargins(15, 15, 15, 15)

        # Первая строка: Параметры графа
        control_grid.addWidget(QLabel("Количество вершин:"), 0, 0, Qt.AlignRight)
        self.n_spinbox = QSpinBox()
        self.n_spinbox.setRange(3, 15)
        self.n_spinbox.setValue(8)
        self.n_spinbox.setFixedWidth(80)
        control_grid.addWidget(self.n_spinbox, 0, 1)

        control_grid.addWidget(QLabel("Плотность:"), 0, 2, Qt.AlignRight)
        self.density_slider = QSlider(Qt.Horizontal)
        self.density_slider.setRange(10, 70)
        self.density_slider.setValue(30)
        self.density_slider.setFixedWidth(120)
        control_grid.addWidget(self.density_slider, 0, 3)
        self.density_label = QLabel("0.3")
        self.density_label.setFixedWidth(40)
        control_grid.addWidget(self.density_label, 0, 4)
        self.density_slider.valueChanged.connect(self.update_density_label)

        control_grid.addWidget(QLabel("Макс. вес:"), 0, 5, Qt.AlignRight)
        self.max_weight_spinbox = QSpinBox()
        self.max_weight_spinbox.setRange(1, 50)
        self.max_weight_spinbox.setValue(10)
        self.max_weight_spinbox.setFixedWidth(80)
        control_grid.addWidget(self.max_weight_spinbox, 0, 6)

        # Вторая строка: Параметры алгоритма
        control_grid.addWidget(QLabel("GM (∞):"), 1, 0, Qt.AlignRight)
        self.gm_spinbox = QDoubleSpinBox()
        self.gm_spinbox.setRange(100, 10000)
        self.gm_spinbox.setValue(1000)
        self.gm_spinbox.setSingleStep(100)
        self.gm_spinbox.setDecimals(0)
        self.gm_spinbox.setFixedWidth(100)
        control_grid.addWidget(self.gm_spinbox, 1, 1)

        control_grid.addWidget(QLabel("Начальная вершина:"), 1, 2, Qt.AlignRight)
        self.start_spinbox = QSpinBox()
        self.start_spinbox.setRange(1, 15)
        self.start_spinbox.setValue(1)
        self.start_spinbox.setFixedWidth(80)
        control_grid.addWidget(self.start_spinbox, 1, 3)

        control_grid.addWidget(QLabel("Конечная вершина:"), 1, 4, Qt.AlignRight)
        self.end_spinbox = QSpinBox()
        self.end_spinbox.setRange(1, 15)
        self.end_spinbox.setValue(5)
        self.end_spinbox.setFixedWidth(80)
        control_grid.addWidget(self.end_spinbox, 1, 5)

        # Кнопки в отдельной строке
        self.generate_btn = QPushButton("СГЕНЕРИРОВАТЬ ГРАФ")
        self.generate_btn.setFixedHeight(35)
        control_grid.addWidget(self.generate_btn, 2, 0, 1, 3)
        self.generate_btn.clicked.connect(self.generate_graph)

        self.find_path_btn = QPushButton("НАЙТИ ПУТЬ МИНИМАЛЬНОГО ВЕСА")
        self.find_path_btn.setFixedHeight(35)
        control_grid.addWidget(self.find_path_btn, 2, 3, 1, 4)

        # Устанавливаем растягивание колонок
        for i in range(7):
            control_grid.setColumnStretch(i, 1)

        main_layout.addWidget(control_group)

        # Основной сплиттер с фиксированными пропорциями
        main_splitter = QSplitter(Qt.Horizontal)
        main_splitter.setHandleWidth(4)
        main_splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #7aa2f7;
                border-radius: 2px;
            }
            QSplitter::handle:hover {
                background-color: #9ece6a;
            }
        """)

        # Левая часть - матрицы и информация (40% ширины)
        left_widget = QWidget()
        left_widget.setMinimumWidth(400)
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(5)

        # Вкладки для левой части
        self.left_tabs = QTabWidget()
        self.left_tabs.setFont(QFont("Arial", 9, QFont.Bold))
        self.left_tabs.setDocumentMode(True)

        # Создаем вкладки левой части
        self.create_left_tabs()

        left_layout.addWidget(self.left_tabs)
        main_splitter.addWidget(left_widget)

        # Правая часть - визуализация и журнал (60% ширины)
        right_widget = QWidget()
        right_widget.setMinimumWidth(600)
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(5)

        # Вкладки для правой части
        self.right_tabs = QTabWidget()
        self.right_tabs.setFont(QFont("Arial", 9, QFont.Bold))
        self.right_tabs.setDocumentMode(True)

        # Создаем вкладки правой части
        self.create_right_tabs()

        right_layout.addWidget(self.right_tabs)
        main_splitter.addWidget(right_widget)

        # Устанавливаем пропорции сплиттера (40:60)
        main_splitter.setStretchFactor(0, 4)
        main_splitter.setStretchFactor(1, 6)

        main_layout.addWidget(main_splitter, 1)

        # Статусная строка
        self.status_label = QLabel("Готов к работе. Сгенерируйте граф и найдите путь минимального веса.")
        self.status_label.setFont(QFont("Arial", 9))
        self.status_label.setStyleSheet("""
            QLabel {
                color: #c0caf5;
                padding: 8px;
                background-color: #24283b;
                border: 1px solid #3b4261;
                border-radius: 4px;
            }
        """)
        main_layout.addWidget(self.status_label)

    def create_left_tabs(self):
        """Создание вкладок левой части"""
        # Вкладка с весовой матрицей
        self.weight_table = MatrixTableWidget()

        weight_container = QWidget()
        weight_layout = QVBoxLayout(weight_container)
        weight_layout.setContentsMargins(5, 5, 5, 5)
        weight_layout.setSpacing(5)

        weight_label = QLabel("ВЕСОВАЯ МАТРИЦА")
        weight_label.setFont(QFont("Arial", 10, QFont.Bold))
        weight_label.setStyleSheet("color: #7aa2f7; padding: 5px;")
        weight_label.setAlignment(Qt.AlignCenter)
        weight_layout.addWidget(weight_label)

        weight_layout.addWidget(self.weight_table, 1)

        scroll_weight = QScrollArea()
        scroll_weight.setWidget(weight_container)
        scroll_weight.setWidgetResizable(True)
        scroll_weight.setStyleSheet("border: none;")
        self.left_tabs.addTab(scroll_weight, "Весовая матрица")

        # Вкладка с информацией о графе
        info_container = QWidget()
        info_layout = QVBoxLayout(info_container)
        info_layout.setContentsMargins(10, 10, 10, 10)
        info_layout.setSpacing(10)

        info_label = QLabel("ИНФОРМАЦИЯ О ГРАФЕ")
        info_label.setFont(QFont("Arial", 10, QFont.Bold))
        info_label.setStyleSheet("color: #7aa2f7; padding: 5px;")
        info_label.setAlignment(Qt.AlignCenter)
        info_layout.addWidget(info_label)

        self.graph_info_text = QTextEdit()
        self.graph_info_text.setFont(QFont("Courier New", 9))
        self.graph_info_text.setReadOnly(True)
        info_layout.addWidget(self.graph_info_text, 1)

        self.left_tabs.addTab(info_container, "Свойства графа")

    def create_right_tabs(self):
        """Создание вкладок правой части"""
        # Вкладка с визуализацией графа
        self.graph_canvas = GraphCanvas(self, width=8, height=6)

        viz_container = QWidget()
        viz_layout = QVBoxLayout(viz_container)
        viz_layout.setContentsMargins(5, 5, 5, 5)
        viz_layout.setSpacing(5)

        viz_label = QLabel("ВИЗУАЛИЗАЦИЯ ГРАФА")
        viz_label.setFont(QFont("Arial", 10, QFont.Bold))
        viz_label.setStyleSheet("color: #7aa2f7; padding: 5px;")
        viz_label.setAlignment(Qt.AlignCenter)
        viz_layout.addWidget(viz_label)

        # Легенда
        legend_widget = QWidget()
        legend_layout = QGridLayout(legend_widget)
        legend_layout.setHorizontalSpacing(10)
        legend_layout.setVerticalSpacing(5)
        legend_layout.setContentsMargins(5, 5, 5, 5)

        legend_items = [
            ("Начальная вершина", "#f7768e"),
            ("Конечная вершина", "#9ece6a"),
            ("Вершины пути", "#7aa2f7"),
            ("Обычные вершины", "#24283b"),
            ("Ребра пути", "#ff9e64"),
            ("Веса ребер", "#c0caf5")
        ]

        for i, (text, color) in enumerate(legend_items):
            row = i // 2
            col = (i % 2) * 2
            
            color_label = QLabel("■")
            color_label.setStyleSheet(f"color: {color}; font-size: 14px;")
            text_label = QLabel(text)
            text_label.setStyleSheet("font-size: 9px; color: #c0caf5;")
            
            legend_layout.addWidget(color_label, row, col)
            legend_layout.addWidget(text_label, row, col + 1)

        legend_layout.setColumnStretch(4, 1)
        viz_layout.addWidget(legend_widget)
        viz_layout.addWidget(self.graph_canvas, 1)

        scroll_viz = QScrollArea()
        scroll_viz.setWidget(viz_container)
        scroll_viz.setWidgetResizable(True)
        scroll_viz.setStyleSheet("border: none;")
        self.right_tabs.addTab(scroll_viz, "Визуализация")

        # Вкладка с журналом выполнения алгоритма
        log_container = QWidget()
        log_layout = QVBoxLayout(log_container)
        log_layout.setContentsMargins(10, 10, 10, 10)
        log_layout.setSpacing(10)

        log_label = QLabel("ЖУРНАЛ ВЫПОЛНЕНИЯ АЛГОРИТМА")
        log_label.setFont(QFont("Arial", 10, QFont.Bold))
        log_label.setStyleSheet("color: #7aa2f7; padding: 5px;")
        log_label.setAlignment(Qt.AlignCenter)
        log_layout.addWidget(log_label)

        self.algorithm_log = QTextEdit()
        self.algorithm_log.setFont(QFont("Courier New", 9))
        self.algorithm_log.setReadOnly(True)
        log_layout.addWidget(self.algorithm_log, 1)

        self.right_tabs.addTab(log_container, "Журнал алгоритма")

        # Вкладка с массивами d, m, prev
        arrays_container = QWidget()
        arrays_layout = QVBoxLayout(arrays_container)
        arrays_layout.setContentsMargins(10, 10, 10, 10)
        arrays_layout.setSpacing(10)

        arrays_label = QLabel("МАССИВЫ АЛГОРИТМА")
        arrays_label.setFont(QFont("Arial", 10, QFont.Bold))
        arrays_label.setStyleSheet("color: #7aa2f7; padding: 5px;")
        arrays_label.setAlignment(Qt.AlignCenter)
        arrays_layout.addWidget(arrays_label)

        self.arrays_text = QTextEdit()
        self.arrays_text.setFont(QFont("Courier New", 9))
        self.arrays_text.setReadOnly(True)
        arrays_layout.addWidget(self.arrays_text, 1)

        self.right_tabs.addTab(arrays_container, "Массивы d, m, prev")

    def update_density_label(self, value):
        """Обновление метки плотности графа"""
        density = value / 100.0
        self.density_label.setText(f"{density:.1f}")

    def generate_graph(self):
        """Генерация нового взвешенного графа"""
        n = self.n_spinbox.value()
        density = self.density_slider.value() / 100.0
        max_weight = self.max_weight_spinbox.value()
        GM = self.gm_spinbox.value()

        # Обновляем диапазоны для вершин
        self.start_spinbox.setRange(1, n)
        self.end_spinbox.setRange(1, n)

        self.graph_ops = GraphOperations(n, GM)
        self.graph_ops.generate_weighted_graph(density, max_weight)

        # Обновляем весовую матрицу
        self.weight_table.set_weight_matrix(self.graph_ops.weight_matrix, GM=GM)

        # Обновляем информацию о графе
        self.update_graph_info()

        # Очищаем результаты предыдущего поиска
        self.clear_path_results()

        # Обновляем визуализацию
        self.update_visualization()

        self.status_label.setText(f"Граф сгенерирован. Вершин: {n}, Плотность: {density:.2f}, GM: {GM}")

    def update_graph_info(self):
        """Обновление информации о графе"""
        if self.graph_ops is None:
            return

        info = self.graph_ops.get_graph_info()

        text = "=" * 50 + "\n"
        text += "ХАРАКТЕРИСТИКИ ГРАФА\n"
        text += "=" * 50 + "\n\n"

        text += f"Количество вершин: {info['n']}\n"
        text += f"Количество ребер: {info['edges']}\n"
        text += f"Плотность графа: {info['density']:.3f}\n"
        text += f"Минимальный вес: {info['min_weight']}\n"
        text += f"Максимальный вес: {info['max_weight']}\n"
        text += f"GM (бесконечность): {self.graph_ops.GM}\n\n"

        self.graph_info_text.setText(text)

    def clear_path_results(self):
        """Очистка результатов поиска пути"""
        self.algorithm_log.clear()
        self.arrays_text.clear()

        # Очищаем визуализацию пути
        if self.graph_ops and self.graph_ops.G_nx:
            self.graph_canvas.draw_weighted_graph_with_path(
                self.graph_ops.G_nx,
                weight_matrix=self.graph_ops.weight_matrix,
                GM=self.graph_ops.GM,
                title="Взвешенный граф G"
            )

    def update_visualization(self, path_vertices=None):
        """Обновление визуализации графа"""
        if self.graph_ops is None or self.graph_ops.G_nx is None:
            return

        start_vertex = self.start_spinbox.value() if path_vertices else None
        end_vertex = self.end_spinbox.value() if path_vertices else None

        title = "Взвешенный граф G"
        if path_vertices:
            if len(path_vertices) > 0:
                title = f"Путь минимального веса {start_vertex} → {end_vertex}"
            else:
                title = f"Путь {start_vertex} → {end_vertex} не существует"

        self.graph_canvas.draw_weighted_graph_with_path(
            self.graph_ops.G_nx,
            path_vertices=path_vertices,
            start_vertex=start_vertex,
            end_vertex=end_vertex,
            title=title,
            weight_matrix=self.graph_ops.weight_matrix,
            GM=self.graph_ops.GM
        )

    def find_shortest_path(self):
        """Поиск пути минимального веса с помощью алгоритма Дейкстры"""
        if self.graph_ops is None:
            QMessageBox.warning(self, "Предупреждение", "Сначала сгенерируйте граф!")
            return

        u1 = self.start_spinbox.value()
        u2 = self.end_spinbox.value()

        if u1 < 1 or u1 > self.graph_ops.n or u2 < 1 or u2 > self.graph_ops.n:
            QMessageBox.warning(self, "Ошибка", "Номера вершин должны быть в диапазоне от 1 до n")
            return

        try:
            # Выполнение алгоритма Дейкстры
            length, weight, path, d, m, prev, steps_log = self.graph_ops.find_shortest_path_dijkstra(u1, u2)

            # Отображение результатов в журнале
            self.display_results(u1, u2, length, weight, path, d, m, prev, steps_log)

            # Обновление визуализации
            self.update_visualization(path)

            # Отображение массивов d, m, prev
            self.display_arrays(d, m, prev, u1, u2, length, weight, path)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при поиске пути: {str(e)}")

    def display_results(self, u1, u2, length, weight, path, d, m, prev, steps_log):
        """Отображение результатов поиска пути в журнале"""
        log_text = "\n".join(steps_log)
        
        results_text = "\n" + "=" * 60 + "\n"
        results_text += "РЕЗУЛЬТАТЫ АЛГОРИТМА\n"
        results_text += "=" * 60 + "\n\n"
        
        results_text += f"Начальная вершина: {u1}\n"
        results_text += f"Конечная вершина: {u2}\n\n"

        if length == -1:
            results_text += "ПУТЬ НЕ СУЩЕСТВУЕТ\n"
            self.status_label.setText(f"Путь от {u1} до {u2} не существует")
        elif length == 0:
            results_text += "НАЧАЛЬНАЯ И КОНЕЧНАЯ ВЕРШИНЫ СОВПАДАЮТ\n"
            results_text += f"Вес пути: {weight}\n"
            self.status_label.setText(f"Вершины {u1} и {u2} совпадают")
        else:
            results_text += f"ПУТЬ МИНИМАЛЬНОГО ВЕСА НАЙДЕН\n"
            results_text += f"Длина пути: {length} ребер\n"
            results_text += f"Вес пути: {weight}\n"
            results_text += f"Путь: {' → '.join(map(str, path))}\n"
            
            self.status_label.setText(f"Найден путь от {u1} до {u2}, вес: {weight}")

        results_text += "\n" + "=" * 60
        
        self.algorithm_log.setText(log_text + results_text)

    def display_arrays(self, d, m, prev, u1, u2, length, weight, path):
        """Отображение массивов d, m, prev"""
        if not d or not m or not prev:
            return

        text = "\n"
        text += "МАССИВЫ АЛГОРИТМА ДЕЙКСТРЫ\n"
        text += "=" * 50 + "\n\n"

        if length == -1:
            text += "ПУТЬ НЕ СУЩЕСТВУЕТ\n\n"
        elif length == 0:
            text += "НАЧАЛЬНАЯ И КОНЕЧНАЯ ВЕРШИНЫ СОВПАДАЮТ\n\n"
        else:
            text += f"ПУТЬ МИНИМАЛЬНОГО ВЕСА НАЙДЕН\n"
            text += f"Путь: {' → '.join(map(str, path))}\n\n"

        text += f"{'Вершина':<10} {'d[i]':<15} {'m[i]':<10} {'prev[i]':<10}\n"
        text += "-" * 45 + "\n"

        for i in range(len(d)):
            d_val = f"{d[i]:.1f}" if d[i] < self.graph_ops.GM else "∞"
            prev_val = f"{prev[i] + 1}" if prev[i] != -1 else "-"
            text += f"{i + 1:<10} {d_val:<15} {m[i]:<10} {prev_val:<10}\n"

        self.arrays_text.setText(text)


def main():
    app = QApplication(sys.argv)
    
    # Устанавливаем темную тему для всего приложения
    app.setStyle("Fusion")
    
    # Создаем темную палитру
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(26, 27, 38))
    palette.setColor(QPalette.WindowText, QColor(192, 202, 245))
    palette.setColor(QPalette.Base, QColor(36, 40, 59))
    palette.setColor(QPalette.AlternateBase, QColor(26, 27, 38))
    palette.setColor(QPalette.ToolTipBase, QColor(26, 27, 38))
    palette.setColor(QPalette.ToolTipText, QColor(192, 202, 245))
    palette.setColor(QPalette.Text, QColor(192, 202, 245))
    palette.setColor(QPalette.Button, QColor(36, 40, 59))
    palette.setColor(QPalette.ButtonText, QColor(192, 202, 245))
    palette.setColor(QPalette.BrightText, QColor(255, 255, 255))
    palette.setColor(QPalette.Link, QColor(122, 162, 247))
    palette.setColor(QPalette.Highlight, QColor(122, 162, 247))
    palette.setColor(QPalette.HighlightedText, QColor(26, 27, 38))
    
    app.setPalette(palette)
    
    window = DijkstraApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()