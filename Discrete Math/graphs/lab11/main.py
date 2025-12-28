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
    QDoubleSpinBox, QListWidget, QListWidgetItem
)
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QColor, QBrush, QPalette, QIcon, QKeySequence


class KruskalAlgorithm:
    """Реализация алгоритма Краскала для нахождения минимального остовного дерева"""

    def __init__(self, weight_matrix):
        """
        Инициализация алгоритма

        Args:
            weight_matrix: весовая матрица графа (n x n)
        """
        self.W = weight_matrix
        self.n = len(weight_matrix)
        self.edges = []  # Массив ребер: (вес, вершина1, вершина2)
        self.E = []  # Массив ребер: [вершина1, вершина2]
        self.EW = []  # Массив весов ребер
        self.extract_edges()

    def extract_edges(self):
        """Извлечение ребер из весовой матрицы"""
        self.edges = []
        self.E = []
        self.EW = []

        for i in range(self.n):
            for j in range(i + 1, self.n):
                if self.W[i][j] != float('inf') and self.W[i][j] != 0:
                    self.edges.append((self.W[i][j], i, j))
                    self.E.append([i + 1, j + 1])  # 1-based индексы
                    self.EW.append(self.W[i][j])

    def bubble_sort_edges(self):
        """Сортировка ребер по возрастанию веса методом пузырька"""
        m = len(self.edges)
        steps_log = []
        steps_log.append("=== СОРТИРОВКА РЕБЕР ПО ВОЗРАСТАНИЮ ВЕСА ===")
        steps_log.append(f"Количество ребер: {m}")

        # Копируем массив для сортировки
        edges_copy = self.edges.copy()

        for i in range(m - 1):
            steps_log.append(f"\nПРОХОД {i + 1}:")
            swapped = False
            for j in range(m - i - 1):
                if edges_copy[j][0] > edges_copy[j + 1][0]:
                    # Меняем местами
                    edges_copy[j], edges_copy[j + 1] = edges_copy[j + 1], edges_copy[j]
                    swapped = True
                    steps_log.append(f"  Поменяли местами ребра {j + 1} и {j + 2}")

            if not swapped:
                steps_log.append(f"  Перестановок не было - массив отсортирован")
                break

        self.edges = edges_copy
        steps_log.append(f"\nОТСОРТИРОВАННЫЕ РЕБРА:")
        for idx, (weight, u, v) in enumerate(self.edges):
            steps_log.append(f"  Ребро {idx + 1}: {u + 1}-{v + 1}, вес: {weight}")

        return steps_log

    def find_mst(self):
        """Нахождение минимального остовного дерева"""
        steps_log = []
        steps_log.append("=" * 50)
        steps_log.append("АЛГОРИТМ КРАСКАЛА - НАЧАЛО РАБОТЫ")
        steps_log.append("=" * 50)
        steps_log.append(f"Количество вершин: {self.n}")

        # Шаг 1: Сортировка ребер
        sort_log = self.bubble_sort_edges()
        steps_log.extend(sort_log)

        # Шаг 2: Инициализация массива компонент связности
        V = list(range(1, self.n + 1))  # Каждая вершина в своей компоненте
        steps_log.append(f"\n=== ИНИЦИАЛИЗАЦИЯ МАССИВА КОМПОНЕНТ СВЯЗНОСТИ ===")
        steps_log.append(f"V = {V} (каждая вершина в своей компоненте)")

        # Матрица весов остовного дерева
        WO = [[float('inf') for _ in range(self.n)] for _ in range(self.n)]
        for i in range(self.n):
            WO[i][i] = 0

        # Список ребер минимального остовного дерева
        mst_edges = []

        q = self.n - 1  # Количество ребер, которые нужно добавить
        steps_log.append(f"\n=== НАЧАЛО ПОСТРОЕНИЯ МСТ ===")
        steps_log.append(f"Нужно добавить {q} ребер")

        edge_index = 0
        total_weight = 0

        while q > 0 and edge_index < len(self.edges):
            steps_log.append(f"\n--- Рассматриваем ребро {edge_index + 1} ---")
            weight, u, v = self.edges[edge_index]
            u_idx = u  # 0-based
            v_idx = v  # 0-based

            steps_log.append(f"Ребро: {u + 1}-{v + 1}, вес: {weight}")
            steps_log.append(f"Компоненты вершин: V[{u + 1}] = {V[u_idx]}, V[{v + 1}] = {V[v_idx]}")

            if V[u_idx] != V[v_idx]:
                # Вершины в разных компонентах связности
                steps_log.append(f"Вершины в разных компонентах - добавляем ребро в МСТ")

                # Объединяем компоненты связности
                old_component = V[v_idx]
                new_component = V[u_idx]
                steps_log.append(f"Объединяем компоненты: {old_component} -> {new_component}")

                for i in range(self.n):
                    if V[i] == old_component:
                        V[i] = new_component

                steps_log.append(f"Новый массив V: {V}")

                # Добавляем ребро в МСТ
                WO[u_idx][v_idx] = weight
                WO[v_idx][u_idx] = weight
                mst_edges.append((u + 1, v + 1, weight))  # 1-based индексы
                total_weight += weight
                q -= 1

                steps_log.append(f"Добавлено ребро {u + 1}-{v + 1}, вес: {weight}")
                steps_log.append(f"Осталось добавить ребер: {q}")
                steps_log.append(f"Текущий вес МСТ: {total_weight}")
            else:
                steps_log.append(f"Вершины в одной компоненте - пропускаем ребро")

            edge_index += 1

        steps_log.append(f"\n" + "=" * 50)
        steps_log.append(f"АЛГОРИТМ ЗАВЕРШЕН")
        steps_log.append(f"Общий вес минимального остовного дерева: {total_weight}")
        steps_log.append(f"Количество ребер в МСТ: {len(mst_edges)}")
        steps_log.append(f"Ребра МСТ:")

        for i, (u, v, w) in enumerate(mst_edges):
            steps_log.append(f"  Ребро {i + 1}: {u}-{v}, вес: {w}")

        # Проверка связности
        if len(set(V)) > 1:
            steps_log.append(f"\nВНИМАНИЕ: Граф несвязный!")
            steps_log.append(f"Количество компонент связности: {len(set(V))}")
            steps_log.append(f"МСТ включает только ребра из исходных компонент")

        return mst_edges, total_weight, WO, V, steps_log


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
    """Холст для отрисовки взвешенных графов с выделением МСТ в темной теме"""

    def __init__(self, parent=None, width=5, height=5, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor='#1a1b26')
        self.ax = self.fig.add_subplot(111, facecolor='#1a1b26')
        super().__init__(self.fig)
        self.setParent(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Настраиваем темную тему для холста
        self.setStyleSheet("background-color: #1a1b26; border: 1px solid #3b4261;")

    def draw_weighted_graph_with_mst(self, G, pos=None, mst_edges=None,
                                     title="", weight_matrix=None, GM=float('inf')):
        """Отрисовка взвешенного графа с выделением МСТ в темной теме"""
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

        # Определяем цвета вершин
        node_colors = []
        node_sizes = []

        for node in G.nodes():
            node_colors.append('#7aa2f7')  # Синий для всех вершин
            node_sizes.append(500)  # Уменьшенный размер для лучшей визуализации

        # Рисуем все вершины
        nx.draw_networkx_nodes(G, pos, ax=self.ax,
                               node_color=node_colors,
                               node_size=node_sizes,
                               edgecolors='#c0caf5',  # Светлая обводка
                               linewidths=2)

        # Рисуем все ребра с цветами в темной теме
        edge_labels = {}
        all_edges = []
        mst_edge_set = set()

        if mst_edges:
            for u, v, _ in mst_edges:
                mst_edge_set.add((u - 1, v - 1))
                mst_edge_set.add((v - 1, u - 1))

        for u, v in G.edges():
            all_edges.append((u, v))
            if weight_matrix is not None and u < len(weight_matrix) and v < len(weight_matrix):
                weight = weight_matrix[u][v]
                if weight < GM:
                    edge_labels[(u, v)] = f"{weight:.1f}"

        # Рисуем обычные ребра серым цветом
        regular_edges = [e for e in all_edges if e not in mst_edge_set and (e[1], e[0]) not in mst_edge_set]
        if regular_edges:
            nx.draw_networkx_edges(G, pos, ax=self.ax,
                                   edgelist=regular_edges,
                                   edge_color='#3b4261',  # Темно-серый
                                   width=1.5,
                                   alpha=0.3)

        # Рисуем ребра МСТ
        if mst_edges:
            mst_edges_for_draw = []
            for u, v, _ in mst_edges:
                mst_edges_for_draw.append((u - 1, v - 1))

            nx.draw_networkx_edges(G, pos, ax=self.ax,
                                   edgelist=mst_edges_for_draw,
                                   edge_color='#ff9e64',  # Оранжевый для МСТ
                                   width=3,
                                   alpha=0.8,
                                   style='solid')

        # Рисуем подписи весов ребер (только для МСТ для лучшей читаемости)
        mst_edge_labels = {}
        if mst_edges:
            for u, v, weight in mst_edges:
                u0 = u - 1
                v0 = v - 1
                mst_edge_labels[(u0, v0)] = f"{weight:.1f}"
        
        nx.draw_networkx_edge_labels(G, pos, ax=self.ax,
                                     edge_labels=mst_edge_labels,
                                     font_size=8,
                                     font_color='#c0caf5',  # Светлый текст
                                     bbox=dict(facecolor='#1a1b26', edgecolor='#3b4261', alpha=0.9))

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
    """Класс для операций с взвешенными графами для алгоритма Краскала"""

    def __init__(self, n, GM=float('inf')):
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

        # Сначала создаем связный остов (дерево) - гарантируем связность
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
            'connected': nx.is_connected(self.G_nx) if self.G_nx else False
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

    def find_mst_kruskal(self):
        """Нахождение минимального остовного дерева алгоритмом Краскала"""
        if self.weight_matrix is None:
            return [], 0, [], [], []

        kruskal = KruskalAlgorithm(self.weight_matrix)
        mst_edges, total_weight, WO, V, steps_log = kruskal.find_mst()

        return mst_edges, total_weight, WO, V, steps_log


class KruskalApp(QMainWindow):
    """Главное окно приложения с темной темой и оптимизированными размерами"""

    def __init__(self):
        super().__init__()
        self.graph_ops = None
        self.init_ui()
        self.generate_graph()

    def init_ui(self):
        """Инициализация интерфейса с темной темой и оптимизированными размерами"""
        self.setWindowTitle("Алгоритм Краскала для поиска минимального остовного дерева")
        self.setGeometry(50, 50, 1400, 850)  # Уменьшил размер окна для лучшего вписывания в экран

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
                font-size: 10px;
            }
            QGroupBox {
                border: 2px solid #7aa2f7;
                border-radius: 5px;
                margin-top: 8px;
                padding-top: 8px;
                font-weight: bold;
                color: #7aa2f7;
                font-size: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 4px 0 4px;
                color: #7aa2f7;
            }
            QSpinBox, QDoubleSpinBox, QSlider {
                background-color: #24283b;
                color: #c0caf5;
                border: 1px solid #7aa2f7;
                border-radius: 3px;
                padding: 2px;
                font-size: 10px;
                min-height: 20px;
            }
            QSpinBox::up-button, QSpinBox::down-button,
            QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
                background-color: #3b4261;
                border: 1px solid #7aa2f7;
                width: 16px;
            }
            QPushButton {
                background-color: #7aa2f7;
                color: #1a1b26;
                border: 1px solid #7aa2f7;
                border-radius: 4px;
                padding: 6px 12px;
                font-weight: bold;
                font-size: 10px;
                min-height: 25px;
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
                padding: 6px 12px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                border: 1px solid #3b4261;
                border-bottom: none;
                font-size: 10px;
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
                font-size: 10px;
            }
            QCheckBox {
                color: #c0caf5;
                font-size: 10px;
            }
            QCheckBox::indicator {
                width: 12px;
                height: 12px;
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
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #7aa2f7;
                min-height: 20px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #9ece6a;
            }
            QSplitter::handle {
                background-color: #7aa2f7;
                width: 3px;
            }
            QSplitter::handle:hover {
                background-color: #9ece6a;
            }
        """)

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(4)
        main_layout.setContentsMargins(4, 4, 4, 4)

        # Заголовок
        title = QLabel("АЛГОРИТМ КРАСКАЛА - МИНИМАЛЬНОЕ ОСТОВНОЕ ДЕРЕВО")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setStyleSheet("""
            QLabel {
                color: #7aa2f7;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1a1b26, stop:0.5 #24283b, stop:1 #1a1b26);
                padding: 12px;
                border-radius: 6px;
                margin: 2px;
                border: 2px solid #7aa2f7;
            }
        """)
        main_layout.addWidget(title)

        # Панель управления - компактная версия
        control_group = QGroupBox("УПРАВЛЕНИЕ ГРАФОМ И ПАРАМЕТРАМИ АЛГОРИТМА")
        control_group.setFont(QFont("Arial", 9, QFont.Bold))
        control_layout = QGridLayout(control_group)
        control_layout.setSpacing(6)
        control_layout.setContentsMargins(6, 10, 6, 6)

        # Количество вершин
        control_layout.addWidget(QLabel("Вершины (n > 3):"), 0, 0)
        self.n_spinbox = QSpinBox()
        self.n_spinbox.setRange(4, 12)  # Уменьшил максимальное значение для компактности
        self.n_spinbox.setValue(8)
        self.n_spinbox.setFixedWidth(70)
        control_layout.addWidget(self.n_spinbox, 0, 1)

        # Плотность графа
        control_layout.addWidget(QLabel("Плотность:"), 0, 2)
        self.density_slider = QSlider(Qt.Horizontal)
        self.density_slider.setRange(10, 70)
        self.density_slider.setValue(30)
        self.density_slider.setFixedWidth(80)
        control_layout.addWidget(self.density_slider, 0, 3)
        self.density_label = QLabel("0.3")
        self.density_label.setFixedWidth(30)
        control_layout.addWidget(self.density_label, 0, 4)
        self.density_slider.valueChanged.connect(self.update_density_label)

        # Максимальный вес ребра
        control_layout.addWidget(QLabel("Макс. вес:"), 0, 5)
        self.max_weight_spinbox = QSpinBox()
        self.max_weight_spinbox.setRange(1, 50)
        self.max_weight_spinbox.setValue(10)
        self.max_weight_spinbox.setFixedWidth(70)
        control_layout.addWidget(self.max_weight_spinbox, 0, 6)

        # Значение GM (бесконечность)
        control_layout.addWidget(QLabel("GM:"), 1, 0)
        self.gm_spinbox = QDoubleSpinBox()
        self.gm_spinbox.setRange(100, 10000)
        self.gm_spinbox.setValue(1000)
        self.gm_spinbox.setSingleStep(100)
        self.gm_spinbox.setDecimals(0)
        self.gm_spinbox.setFixedWidth(70)
        control_layout.addWidget(self.gm_spinbox, 1, 1)

        # Подсказка для GM
        gm_hint = QLabel("GM >> макс. путь")
        gm_hint.setFont(QFont("Arial", 8))
        gm_hint.setStyleSheet("color: #a9b1d6;")
        control_layout.addWidget(gm_hint, 1, 2)

        # Кнопка генерации
        self.generate_btn = QPushButton("СГЕНЕРИРОВАТЬ ГРАФ")
        self.generate_btn.clicked.connect(self.generate_graph)
        control_layout.addWidget(self.generate_btn, 0, 7, 1, 2)

        # Кнопка поиска МСТ
        self.find_mst_btn = QPushButton("НАЙТИ МИНИМАЛЬНОЕ ОСТОВНОЕ ДЕРЕВО")
        self.find_mst_btn.clicked.connect(self.find_mst)
        control_layout.addWidget(self.find_mst_btn, 1, 5, 1, 4)

        main_layout.addWidget(control_group)

        # Основной сплиттер
        main_splitter = QSplitter(Qt.Horizontal)
        main_splitter.setHandleWidth(3)
        main_splitter.setStyleSheet("QSplitter::handle { background-color: #7aa2f7; }")

        # Левая часть - матрицы и информация (уменьшенная ширина)
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

        # Устанавливаем начальные размеры (уменьшил левую часть)
        main_splitter.setSizes([550, 800])
        main_layout.addWidget(main_splitter, 1)

        # Статусная строка
        self.status_label = QLabel("Готов к работе. Сгенерируйте граф и найдите минимальное остовное дерево.")
        self.status_label.setFont(QFont("Arial", 9))
        self.status_label.setStyleSheet("color: #c0caf5; padding: 4px;")
        main_layout.addWidget(self.status_label)

    def create_left_tabs(self):
        """Создание вкладок левой части"""
        # Вкладка с весовой матрицей
        self.weight_table = MatrixTableWidget()

        weight_container = QWidget()
        weight_layout = QVBoxLayout(weight_container)
        weight_layout.setContentsMargins(0, 0, 0, 0)

        weight_label = QLabel("ВЕСОВАЯ МАТРИЦА W (основа для алгоритма Краскала)")
        weight_label.setFont(QFont("Arial", 9, QFont.Bold))
        weight_label.setStyleSheet("color: #7aa2f7; padding: 4px;")
        weight_label.setAlignment(Qt.AlignCenter)
        weight_layout.addWidget(weight_label)

        weight_hint = QLabel("Зеленый - веса ребер, Красный - ∞ (GM), Темный - диагональ")
        weight_hint.setFont(QFont("Arial", 8))
        weight_hint.setStyleSheet("color: #a9b1d6; padding: 2px;")
        weight_hint.setAlignment(Qt.AlignCenter)
        weight_layout.addWidget(weight_hint)

        weight_layout.addWidget(self.weight_table)

        scroll_weight = QScrollArea()
        scroll_weight.setWidget(weight_container)
        scroll_weight.setWidgetResizable(True)
        self.left_tabs.addTab(scroll_weight, "Матрица W")

        # Вкладка с информацией о графе
        info_container = QWidget()
        info_layout = QVBoxLayout(info_container)

        info_label = QLabel("ИНФОРМАЦИЯ О ВЗВЕШЕННОМ ГРАФЕ")
        info_label.setFont(QFont("Arial", 9, QFont.Bold))
        info_label.setStyleSheet("color: #7aa2f7; padding: 8px;")
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
        self.graph_canvas = GraphCanvas(self, width=5.5, height=5)  # Уменьшил размер холста

        viz_container = QWidget()
        viz_layout = QVBoxLayout(viz_container)
        viz_layout.setContentsMargins(0, 0, 0, 0)

        viz_label = QLabel("ВИЗУАЛИЗАЦИЯ ГРАФА И МИНИМАЛЬНОГО ОСТОВНОГО ДЕРЕВА")
        viz_label.setFont(QFont("Arial", 9, QFont.Bold))
        viz_label.setStyleSheet("color: #7aa2f7; padding: 4px;")
        viz_label.setAlignment(Qt.AlignCenter)
        viz_layout.addWidget(viz_label)

        # Компактная легенда
        legend_widget = QWidget()
        legend_layout = QGridLayout(legend_widget)
        legend_layout.setHorizontalSpacing(8)
        legend_layout.setVerticalSpacing(3)

        legend_items = [
            ("Вершины", "#7aa2f7"),
            ("Ребра МСТ", "#ff9e64"),
            ("Обычные ребра", "#3b4261"),
            ("Веса МСТ", "#c0caf5")
        ]

        for i, (text, color) in enumerate(legend_items):
            row = i // 2
            col = (i % 2) * 2
            
            color_label = QLabel("■")
            color_label.setStyleSheet(f"color: {color}; font-size: 12px;")
            text_label = QLabel(text)
            text_label.setStyleSheet("font-size: 8px; color: #c0caf5;")
            
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

        log_label = QLabel("ЖУРНАЛ ВЫПОЛНЕНИЯ АЛГОРИТМА КРАСКАЛА")
        log_label.setFont(QFont("Arial", 9, QFont.Bold))
        log_label.setStyleSheet("color: #7aa2f7; padding: 8px;")
        log_label.setAlignment(Qt.AlignCenter)
        log_layout.addWidget(log_label)

        self.algorithm_log = QTextEdit()
        self.algorithm_log.setFont(QFont("Courier New", 9))
        self.algorithm_log.setReadOnly(True)
        log_layout.addWidget(self.algorithm_log)

        self.right_tabs.addTab(log_container, "Журнал алгоритма")

        # Вкладка с массивами E, EW, V
        arrays_container = QWidget()
        arrays_layout = QVBoxLayout(arrays_container)

        arrays_label = QLabel("МАССИВЫ АЛГОРИТМА КРАСКАЛА")
        arrays_label.setFont(QFont("Arial", 9, QFont.Bold))
        arrays_label.setStyleSheet("color: #7aa2f7; padding: 8px;")
        arrays_label.setAlignment(Qt.AlignCenter)
        arrays_layout.addWidget(arrays_label)

        # Виджет для отображения массивов
        self.arrays_text = QTextEdit()
        self.arrays_text.setFont(QFont("Courier New", 9))
        self.arrays_text.setReadOnly(True)
        arrays_layout.addWidget(self.arrays_text)

        self.right_tabs.addTab(arrays_container, "Массивы E, EW, V")

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

        # Проверяем, что GM достаточно большое
        max_possible_path = (n - 1) * max_weight
        if GM <= max_possible_path:
            QMessageBox.warning(
                self, 
                "Предупреждение", 
                f"GM ({GM}) должно быть значительно больше максимально возможного пути ({max_possible_path}).\n"
                f"Рекомендуется установить GM не менее {max_possible_path * 10}."
            )

        self.graph_ops = GraphOperations(n, GM)
        self.graph_ops.generate_weighted_graph(density, max_weight)

        # Обновляем весовую матрицу
        self.weight_table.set_weight_matrix(self.graph_ops.weight_matrix, GM=GM)

        # Обновляем информацию о графе
        self.update_graph_info()

        # Очищаем результаты предыдущего поиска
        self.clear_mst_results()

        # Обновляем визуализацию
        self.update_visualization()

        self.status_label.setText(f"Граф сгенерирован. Вершин: {n}, Плотность: {density:.2f}, GM: {GM}")

    def update_graph_info(self):
        """Обновление информации о графе"""
        if self.graph_ops is None:
            return

        info = self.graph_ops.get_graph_info()

        text = "=" * 45 + "\n"
        text += "ХАРАКТЕРИСТИКИ ВЗВЕШЕННОГО ГРАФА\n"
        text += "=" * 45 + "\n\n"

        text += f"Количество вершин (n): {info['n']}\n"
        text += f"Количество ребер: {info['edges']}\n"
        text += f"Максимально возможное ребер: {info['total_possible_edges']}\n"
        text += f"Плотность графа: {info['density']:.3f}\n"
        text += f"Минимальный вес ребра: {info['min_weight']}\n"
        text += f"Максимальный вес ребра: {info['max_weight']}\n"
        text += f"GM (бесконечность): {self.graph_ops.GM}\n"
        text += f"Связность графа: {'ДА' if info['connected'] else 'НЕТ'}\n\n"

        text += "ИНФОРМАЦИЯ ОБ АЛГОРИТМЕ КРАСКАЛА:\n"
        text += "  • E[i] - массив ребер (начальная и конечная вершины)\n"
        text += "  • EW[i] - массив весов ребер\n"
        text += "  • V[i] - компонента связности вершины i\n"
        text += "  • Алгоритм находит минимальное остовное дерево (МСТ)\n"
        text += "  • МСТ содержит n-1 ребер в связном графе\n"
        text += "  • Алгоритм использует сортировку пузырьком\n"

        self.graph_info_text.setText(text)

    def clear_mst_results(self):
        """Очистка результатов поиска МСТ"""
        self.algorithm_log.clear()
        self.arrays_text.clear()

        # Очищаем визуализацию МСТ
        if self.graph_ops and self.graph_ops.G_nx:
            self.graph_canvas.draw_weighted_graph_with_mst(
                self.graph_ops.G_nx,
                weight_matrix=self.graph_ops.weight_matrix,
                GM=self.graph_ops.GM,
                title="Взвешенный граф G (МСТ не найдено)"
            )

    def update_visualization(self, mst_edges=None):
        """Обновление визуализации графа"""
        if self.graph_ops is None or self.graph_ops.G_nx is None:
            return

        title = "Взвешенный граф G"
        if mst_edges:
            if len(mst_edges) > 0:
                title = f"Минимальное остовное дерево ({len(mst_edges)} ребер)"
            else:
                title = "МСТ не найдено"

        self.graph_canvas.draw_weighted_graph_with_mst(
            self.graph_ops.G_nx,
            mst_edges=mst_edges,
            title=title,
            weight_matrix=self.graph_ops.weight_matrix,
            GM=self.graph_ops.GM
        )

    def find_mst(self):
        """Поиск минимального остовного дерева алгоритмом Краскала"""
        if self.graph_ops is None:
            QMessageBox.warning(self, "Предупреждение", "Сначала сгенерируйте граф!")
            return

        try:
            # Выполнение алгоритма Краскала
            mst_edges, total_weight, WO, V, steps_log = self.graph_ops.find_mst_kruskal()

            # Отображение результатов в журнале
            self.display_results_in_log(mst_edges, total_weight, V, steps_log)

            # Обновление визуализации
            self.update_visualization(mst_edges)

            # Отображение массивов E, EW, V
            self.display_arrays(V, WO, mst_edges, total_weight)

            # Прокрутка журнала вверх
            self.algorithm_log.verticalScrollBar().setValue(0)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при поиске МСТ: {str(e)}")

    def display_results_in_log(self, mst_edges, total_weight, V, steps_log):
        """Отображение результатов поиска МСТ в журнале"""
        # Отображение журнала выполнения
        log_text = "\n".join(steps_log)
        
        # Добавляем раздел с итогами
        results_text = "\n" + "=" * 50 + "\n"
        results_text += "ИТОГИ АЛГОРИТМА КРАСКАЛА\n"
        results_text += "=" * 50 + "\n\n"
        
        results_text += f"Общий вес минимального остовного дерева: {total_weight}\n"
        results_text += f"Количество ребер в МСТ: {len(mst_edges)}\n"
        
        if self.graph_ops:
            expected_edges = self.graph_ops.n - 1
            if len(mst_edges) == expected_edges:
                results_text += f"МСТ содержит правильное количество ребер ({expected_edges} для {self.graph_ops.n} вершин)\n"
            else:
                results_text += f"МСТ содержит {len(mst_edges)} ребер вместо ожидаемых {expected_edges}\n"

        results_text += f"\nКомпоненты связности: V = {V}\n"
        unique_components = len(set(V))
        results_text += f"Количество компонент связности: {unique_components}\n\n"

        if unique_components == 1:
            results_text += "Все вершины в одной компоненте связности\n"
        else:
            results_text += "Граф несвязный!\n"

        results_text += f"\nРЕБРА МИНИМАЛЬНОГО ОСТОВНОГО ДЕРЕВА:\n"

        for i, (u, v, w) in enumerate(mst_edges):
            results_text += f"  Ребро {i + 1}: {u}-{v}, вес: {w}\n"

        results_text += f"\nАлгоритм Краскала успешно завершен!\n"
        results_text += "=" * 50
        
        self.algorithm_log.setText(log_text + results_text)
        
        # Обновление статусной строки
        if len(mst_edges) > 0:
            self.status_label.setText(f"Найдено МСТ с весом {total_weight}, ребер: {len(mst_edges)}")
        else:
            self.status_label.setText("МСТ не найдено или граф несвязный")

    def display_arrays(self, V, WO, mst_edges, total_weight):
        """Отображение массивов V и WO"""
        if not V or not WO:
            return

        text = "\n"
        text += "МАССИВЫ АЛГОРИТМА КРАСКАЛА\n"
        text += "=" * 45 + "\n\n"
        
        text += f"ИТОГИ:\n"
        text += f"  Вес МСТ: {total_weight}\n"
        text += f"  Ребер в МСТ: {len(mst_edges)}\n\n"

        # Отображение массива V
        text += "МАССИВ V - КОМПОНЕНТЫ СВЯЗНОСТИ ВЕРШИН:\n"
        text += "V[i] - номер компоненты связности вершины i\n\n"

        text += f"{'Вершина i':<10} {'V[i]':<10}\n"
        text += "-" * 20 + "\n"

        for i in range(len(V)):
            text += f"{i + 1:<10} {V[i]:<10}\n"

        text += f"\nУникальных компонент: {len(set(V))}\n\n"

        # Отображение матрицы WO
        text += "МАТРИЦА ВЕСОВ МИНИМАЛЬНОГО ОСТОВНОГО ДЕРЕВА WO:\n\n"

        n = len(WO)
        # Компактный заголовок
        header = "     "
        for i in range(min(n, 12)):  # Ограничиваем количество столбцов для компактности
            header += f"{i + 1:3}"
        if n > 12:
            header += " ..."
        text += header + "\n"
        text += "    " + "-" * (min(n, 12) * 3) + (" ..." if n > 12 else "") + "\n"

        for i in range(min(n, 12)):  # Ограничиваем количество строк
            row = f"{i + 1:2} | "
            for j in range(min(n, 12)):  # Ограничиваем количество столбцов
                if WO[i][j] == float('inf'):
                    value = " ∞"
                elif WO[i][j] == 0 and i != j:
                    value = " 0"
                else:
                    value = f"{WO[i][j]:2.0f}" if WO[i][j] != float('inf') else " ∞"
                row += value
            if n > 12:
                row += " ..."
            text += row + "\n"
        
        if n > 12:
            text += " ...\n"

        text += "\n"
        text += "ПРИМЕЧАНИЯ:\n"
        text += "  • ∞ означает отсутствие ребра в МСТ\n"
        text += "  • Ненулевые значения - веса ребер МСТ\n"
        text += "  • Диагональ всегда 0 (петли отсутствуют)\n"
        text += "  • Матрица симметрична (неориентированный граф)\n"

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
    
    window = KruskalApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()