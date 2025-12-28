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
                             QSlider, QToolBar, QAction, QStatusBar, QListWidget, QListWidgetItem,
                             QRadioButton, QButtonGroup, QDoubleSpinBox)
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QColor, QBrush, QPalette, QIcon, QKeySequence

INF = 10 ** 9  # "Бесконечность" для отсутствующих ребер


class FloydAlgorithm:
    """Реализация алгоритма Флойда для поиска путей минимальной суммарной длины"""

    def __init__(self, weight_matrix):
        """
        Инициализация алгоритма

        Args:
            weight_matrix: весовая матрица графа (n x n)
        """
        self.n = len(weight_matrix)
        self.W = np.array(weight_matrix, dtype=float)
        self.D = None  # Матрица минимальных весов
        self.P = None  # Матрица предпоследних вершин
        self.success = True  # Успешность выполнения алгоритма
        self.steps_log = []  # Журнал выполнения
        self.iterations_data = []  # Данные по итерациям

    def run(self):
        """
        Выполнение алгоритма Флойда

        Returns:
            tuple: (success, D, P, steps_log, iterations_data)
        """
        self.steps_log = []
        self.iterations_data = []

        # Инициализация
        self.D = self.W.copy()
        self.P = np.zeros((self.n, self.n), dtype=int)

        # Инициализация матрицы P
        for i in range(self.n):
            for j in range(self.n):
                if i != j and self.D[i][j] < INF:
                    self.P[i][j] = i + 1  # 1-based индексы
                else:
                    self.P[i][j] = 0

        self.steps_log.append("=" * 60)
        self.steps_log.append("АЛГОРИТМ ФЛОЙДА - НАЧАЛО РАБОТЫ")
        self.steps_log.append("=" * 60)
        self.steps_log.append(f"Количество вершин: {self.n}")
        self.steps_log.append(f"Исходная матрица весов W (D⁰):")
        self.steps_log.append(self.matrix_to_str(self.D))
        self.steps_log.append(f"Начальная матрица P:")
        self.steps_log.append(self.matrix_to_str(self.P, int_matrix=True))

        # Основной цикл алгоритма Флойда
        for k in range(self.n):
            iteration_log = []
            iteration_log.append(f"\n{'=' * 40}")
            iteration_log.append(f"ИТЕРАЦИЯ m = {k + 1} (промежуточная вершина {k + 1})")
            iteration_log.append(f"{'=' * 40}")

            # Проверка на контур отрицательного веса
            for i in range(self.n):
                if self.D[i][k] + self.D[k][i] < 0:
                    self.steps_log.extend(iteration_log)
                    self.steps_log.append(f"\nОБНАРУЖЕН КОНТУР ОТРИЦАТЕЛЬНОГО ВЕСА!")
                    self.steps_log.append(
                        f"  D[{i + 1}][{k + 1}] + D[{k + 1}][{i + 1}] = {self.D[i][k]} + {self.D[k][i]} = {self.D[i][k] + self.D[k][i]} < 0")
                    self.steps_log.append(f"  Алгоритм прерван. Задача не разрешима.")
                    self.success = False
                    return self.success, self.D, self.P, self.steps_log, self.iterations_data

            # Преобразование матрицы D
            changes_count = 0
            for i in range(self.n):
                for j in range(self.n):
                    if i != j and i != k and j != k:
                        old_value = self.D[i][j]
                        new_value = self.D[i][k] + self.D[k][j]

                        if new_value < old_value:
                            self.D[i][j] = new_value
                            self.P[i][j] = self.P[k][j] if self.P[k][j] != 0 else k + 1
                            changes_count += 1

                            iteration_log.append(
                                f"  D[{i + 1}][{j + 1}] = min({old_value:.1f}, {self.D[i][k]:.1f} + {self.D[k][j]:.1f} = {new_value:.1f}) = {new_value:.1f}")
                            iteration_log.append(f"    P[{i + 1}][{j + 1}] = {self.P[i][j]}")

            # Диагональные элементы остаются нулями
            for i in range(self.n):
                self.D[i][i] = 0

            iteration_log.append(f"\n  Изменений на этой итерации: {changes_count}")
            iteration_log.append(f"  Матрица D после итерации {k + 1}:")
            iteration_log.append(self.matrix_to_str(self.D, indent=4))

            self.steps_log.extend(iteration_log)

            # Сохраняем данные итерации
            self.iterations_data.append({
                'iteration': k + 1,
                'D': self.D.copy(),
                'P': self.P.copy(),
                'changes_count': changes_count
            })

        self.steps_log.append("\n" + "=" * 60)
        self.steps_log.append("АЛГОРИТМ ФЛОЙДА УСПЕШНО ЗАВЕРШЕН")
        self.steps_log.append("=" * 60)
        self.steps_log.append(f"Итоговая матрица минимальных весов D:")
        self.steps_log.append(self.matrix_to_str(self.D))
        self.steps_log.append(f"Итоговая матрица P:")
        self.steps_log.append(self.matrix_to_str(self.P, int_matrix=True))

        self.success = True
        return self.success, self.D, self.P, self.steps_log, self.iterations_data

    def get_path(self, start, end):
        """
        Восстановление пути минимального веса между вершинами

        Args:
            start: начальная вершина (1-based)
            end: конечная вершина (1-based)

        Returns:
            tuple: (path, total_weight, exists)
        """
        if start < 1 or start > self.n or end < 1 or end > self.n:
            return [], 0, False

        # Если путь не существует
        if self.P[start - 1][end - 1] == 0 and start != end:
            return [], INF, False

        # Если начальная и конечная вершины совпадают
        if start == end:
            return [start], 0, True

        # Восстановление пути
        path = []

        # Идем от конца к началу
        current = end
        while current != 0:
            path.insert(0, current)
            if current == start:
                break
            current = self.P[start - 1][current - 1]

        # Проверяем, что путь найден
        if path[0] != start:
            return [], self.D[start - 1][end - 1], False

        total_weight = self.D[start - 1][end - 1]

        return path, total_weight, True

    def matrix_to_str(self, matrix, int_matrix=False, indent=0):
        """Преобразование матрицы в строку для вывода"""
        indent_str = " " * indent
        lines = []

        for i in range(len(matrix)):
            row_str = []
            for j in range(len(matrix[i])):
                if int_matrix:
                    if matrix[i][j] == INF:
                        row_str.append("  ∞")
                    else:
                        row_str.append(f"{int(matrix[i][j]):3d}")
                else:
                    if matrix[i][j] >= INF / 2:
                        row_str.append("    ∞")
                    else:
                        row_str.append(f"{matrix[i][j]:5.1f}")
            lines.append(indent_str + " ".join(row_str))

        return "\n".join(lines)


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
            }
            QHeaderView::section {
                background-color: #24283b;
                color: #7aa2f7;
                padding: 4px;
                border: 1px solid #3b4261;
                font-weight: bold;
            }
            QTableWidget::item:selected {
                background-color: #7aa2f7;
                color: #1a1b26;
            }
        """)

        # Настраиваем заголовки
        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)

    def set_matrix(self, matrix, labels=None, is_weight_matrix=True):
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
                if is_weight_matrix:
                    if matrix[i][j] >= INF / 2:
                        value = "∞"
                    else:
                        value = f"{matrix[i][j]:.1f}"
                else:
                    if matrix[i][j] == 0:
                        value = "0"
                    elif matrix[i][j] >= INF / 2:
                        value = "∞"
                    else:
                        value = str(int(matrix[i][j]))

                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignCenter)

                # Раскрашиваем ячейки в темной теме
                if i == j:
                    item.setBackground(QBrush(QColor('#24283b')))  # Темный для диагонали
                elif is_weight_matrix and matrix[i][j] < INF / 2:
                    # Цветовая кодировка для весов
                    weight = matrix[i][j]
                    if weight < 0:
                        # Красный для отрицательных весов
                        item.setBackground(QBrush(QColor('#f7768e')))
                    elif weight == 0:
                        # Фиолетовый для нулевых весов
                        item.setBackground(QBrush(QColor('#bb9af7')))
                    else:
                        # Синий для положительных весов
                        item.setBackground(QBrush(QColor('#7aa2f7')))
                elif not is_weight_matrix and matrix[i][j] > 0:
                    item.setBackground(QBrush(QColor('#9ece6a')))  # Зеленый для ненулевых P

                self.setItem(i, j, item)

        for i in range(n):
            self.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)
            self.verticalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)


class GraphCanvas(FigureCanvas):
    """Холст для отрисовки взвешенных графов с темной темой"""

    def __init__(self, parent=None, width=5, height=5, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor='#1a1b26')
        self.ax = self.fig.add_subplot(111, facecolor='#1a1b26')
        super().__init__(self.fig)
        self.setParent(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Настраиваем темную тему для холста
        self.setStyleSheet("background-color: #1a1b26; border: 1px solid #3b4261;")

    def draw_weighted_graph(self, G, weight_matrix, path_vertices=None,
                            start_vertex=None, end_vertex=None, title=""):
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
        edge_colors = []
        edge_widths = []
        edge_labels = {}

        for (u, v) in G.edges():
            weight = weight_matrix[u][v]
            if weight < 0:
                edge_colors.append('#f7768e')  # Красный для отрицательных весов
                edge_widths.append(2.5)
            elif weight == 0:
                edge_colors.append('#a9b1d6')  # Серый для нулевых весов
                edge_widths.append(1)
            else:
                edge_colors.append('#7aa2f7')  # Синий для положительных весов
                edge_widths.append(1.5)

            if weight < INF / 2:
                edge_labels[(u, v)] = f"{weight:.1f}"

        nx.draw_networkx_edges(G, pos, ax=self.ax,
                               edge_color=edge_colors,
                               width=edge_widths,
                               alpha=0.7)

        # Рисуем веса ребер
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
                                       width=4,
                                       alpha=0.9,
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
    """Класс для операций со взвешенными графами"""

    def __init__(self, n):
        self.n = n
        self.weight_matrix = None
        self.adj_matrix = None
        self.G_nx = None
        self.allow_negative = False
        self.generate_graph()

    def generate_graph(self, density=0.3, allow_negative=False, max_weight=10):
        """Генерация случайного взвешенного графа"""
        self.allow_negative = allow_negative
        self.weight_matrix = np.full((self.n, self.n), INF, dtype=float)
        self.adj_matrix = np.zeros((self.n, self.n), dtype=int)

        # Диагональные элементы = 0
        for i in range(self.n):
            self.weight_matrix[i][i] = 0

        # Сначала создаем связный остов (дерево) с положительными весами
        for i in range(1, self.n):
            parent = np.random.randint(0, i)
            weight = np.random.uniform(0.5, max_weight)
            self.weight_matrix[i][parent] = weight
            self.weight_matrix[parent][i] = weight
            self.adj_matrix[i][parent] = 1
            self.adj_matrix[parent][i] = 1

        # Добавляем случайные ребра
        total_possible_edges = self.n * (self.n - 1) // 2
        current_edges = self.n - 1
        target_edges = int(total_possible_edges * density)

        while current_edges < target_edges and current_edges < total_possible_edges:
            i = np.random.randint(0, self.n)
            j = np.random.randint(0, self.n)
            if i != j and self.weight_matrix[i][j] == INF:
                if allow_negative and np.random.random() < 0.2:
                    weight = np.random.uniform(-max_weight / 2, -0.5)  # Отрицательный вес
                else:
                    weight = np.random.uniform(0.5, max_weight)  # Положительный вес

                self.weight_matrix[i][j] = weight
                self.weight_matrix[j][i] = weight
                self.adj_matrix[i][j] = 1
                self.adj_matrix[j][i] = 1
                current_edges += 1

        # Создание графа для networkx
        self.create_nx_graph()

        return self.weight_matrix, self.adj_matrix

    def create_nx_graph(self):
        """Создание графа networkx из матрицы весов"""
        self.G_nx = nx.Graph()
        self.G_nx.add_nodes_from(range(self.n))

        for i in range(self.n):
            for j in range(i + 1, self.n):
                if self.weight_matrix[i][j] < INF:
                    self.G_nx.add_edge(i, j, weight=self.weight_matrix[i][j])

    def get_graph_info(self):
        """Получение информации о графе"""
        info = {
            'vertices': self.n,
            'edges': np.sum(self.adj_matrix) // 2,
            'positive_edges': 0,
            'negative_edges': 0,
            'zero_edges': 0,
            'min_weight': INF,
            'max_weight': -INF
        }

        for i in range(self.n):
            for j in range(i + 1, self.n):
                if self.weight_matrix[i][j] < INF:
                    weight = self.weight_matrix[i][j]
                    if weight > 0:
                        info['positive_edges'] += 1
                    elif weight < 0:
                        info['negative_edges'] += 1
                    else:
                        info['zero_edges'] += 1

                    info['min_weight'] = min(info['min_weight'], weight)
                    info['max_weight'] = max(info['max_weight'], weight)

        return info


class FloydAlgorithmApp(QMainWindow):
    """Главное окно приложения с темной темой"""

    def __init__(self):
        super().__init__()
        self.graph_ops = None
        self.floyd_algo = None
        self.current_iteration = 0
        self.total_iterations = 0
        self.init_ui()
        self.generate_graph()

    def init_ui(self):
        """Инициализация интерфейса с темной темой"""
        self.setWindowTitle("Алгоритм Флойда - Пути минимальной суммарной длины")
        self.setGeometry(50, 50, 1800, 900)

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
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(5)
        main_layout.setContentsMargins(5, 5, 5, 5)

        # Заголовок
        title = QLabel("АЛГОРИТМ ФЛОЙДА - ПУТИ МИНИМАЛЬНОЙ СУММАРНОЙ ДЛИНЫ")
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
        control_group = QGroupBox("УПРАВЛЕНИЕ ГРАФОМ И ПАРАМЕТРАМИ АЛГОРИТМА")
        control_group.setFont(QFont("Arial", 10, QFont.Bold))
        control_layout = QGridLayout(control_group)
        control_layout.setSpacing(10)

        # Количество вершин
        control_layout.addWidget(QLabel("Количество вершин (n > 8):"), 0, 0)
        self.n_spinbox = QSpinBox()
        self.n_spinbox.setRange(9, 15)
        self.n_spinbox.setValue(10)
        self.n_spinbox.setFixedWidth(80)
        control_layout.addWidget(self.n_spinbox, 0, 1)

        # Плотность графа
        control_layout.addWidget(QLabel("Плотность графа:"), 0, 2)
        self.density_slider = QSlider(Qt.Horizontal)
        self.density_slider.setRange(10, 50)
        self.density_slider.setValue(30)
        self.density_slider.setFixedWidth(100)
        control_layout.addWidget(self.density_slider, 0, 3)
        self.density_label = QLabel("0.3")
        self.density_label.setFixedWidth(40)
        control_layout.addWidget(self.density_label, 0, 4)
        self.density_slider.valueChanged.connect(self.update_density_label)

        # Максимальный вес
        control_layout.addWidget(QLabel("Максимальный вес:"), 0, 5)
        self.max_weight_spinbox = QDoubleSpinBox()
        self.max_weight_spinbox.setRange(1, 100)
        self.max_weight_spinbox.setValue(10)
        self.max_weight_spinbox.setSingleStep(1)
        self.max_weight_spinbox.setFixedWidth(80)
        control_layout.addWidget(self.max_weight_spinbox, 0, 6)

        # Разрешение отрицательных весов
        self.negative_weights_check = QCheckBox("Разрешить отрицательные веса")
        self.negative_weights_check.setChecked(False)
        control_layout.addWidget(self.negative_weights_check, 0, 7)

        # Начальная вершина для пути
        control_layout.addWidget(QLabel("Начальная вершина:"), 1, 0)
        self.start_spinbox = QSpinBox()
        self.start_spinbox.setRange(1, 15)
        self.start_spinbox.setValue(1)
        self.start_spinbox.setFixedWidth(80)
        control_layout.addWidget(self.start_spinbox, 1, 1)

        # Конечная вершина для пути
        control_layout.addWidget(QLabel("Конечная вершина:"), 1, 2)
        self.end_spinbox = QSpinBox()
        self.end_spinbox.setRange(1, 15)
        self.end_spinbox.setValue(5)
        self.end_spinbox.setFixedWidth(80)
        control_layout.addWidget(self.end_spinbox, 1, 3)

        # Кнопка генерации графа
        self.generate_btn = QPushButton("СГЕНЕРИРОВАТЬ ГРАФ")
        self.generate_btn.clicked.connect(self.generate_graph)
        control_layout.addWidget(self.generate_btn, 1, 4)

        # Кнопка выполнения алгоритма
        self.run_floyd_btn = QPushButton("ВЫПОЛНИТЬ АЛГОРИТМ ФЛОЙДА")
        self.run_floyd_btn.clicked.connect(self.run_floyd_algorithm)
        control_layout.addWidget(self.run_floyd_btn, 1, 5)

        # Кнопка поиска пути
        self.find_path_btn = QPushButton("НАЙТИ ПУТЬ")
        self.find_path_btn.clicked.connect(self.find_path)
        control_layout.addWidget(self.find_path_btn, 1, 6)

        main_layout.addWidget(control_group)

        # Основной сплиттер
        main_splitter = QSplitter(Qt.Horizontal)
        main_splitter.setHandleWidth(3)
        main_splitter.setStyleSheet("QSplitter::handle { background-color: #7aa2f7; }")

        # Левая часть - матрицы и управление итерациями
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(2, 2, 2, 2)

        # Вкладки для левой части
        self.left_tabs = QTabWidget()
        self.left_tabs.setFont(QFont("Arial", 9, QFont.Bold))
        self.left_tabs.currentChanged.connect(self.on_left_tab_changed)

        # Создаем вкладки левой части
        self.create_left_tabs()

        left_layout.addWidget(self.left_tabs)
        main_splitter.addWidget(left_widget)

        # Правая часть - визуализация и результаты
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
        main_splitter.setSizes([800, 1000])
        main_layout.addWidget(main_splitter, 1)

        # Статусная строка
        self.status_label = QLabel("Готов к работе. Сгенерируйте граф и выполните алгоритм Флойда.")
        self.status_label.setFont(QFont("Arial", 9))
        self.status_label.setStyleSheet("color: #c0caf5; padding: 5px;")
        main_layout.addWidget(self.status_label)

    def create_left_tabs(self):
        """Создание вкладок левой части"""
        # Вкладка с весовой матрицей W
        self.weight_table = MatrixTableWidget()

        weight_container = QWidget()
        weight_layout = QVBoxLayout(weight_container)
        weight_layout.setContentsMargins(0, 0, 0, 0)

        weight_label = QLabel("ВЕСОВАЯ МАТРИЦА W (wᵢⱼ = ∞ если ребра нет)")
        weight_label.setFont(QFont("Arial", 10, QFont.Bold))
        weight_label.setStyleSheet("color: #7aa2f7; padding: 5px;")
        weight_label.setAlignment(Qt.AlignCenter)
        weight_layout.addWidget(weight_label)

        weight_hint = QLabel(
            "Цветовая кодировка: синий → положительный вес, красный → отрицательный вес, фиолетовый → нулевой вес")
        weight_hint.setFont(QFont("Arial", 8))
        weight_hint.setStyleSheet("color: #a9b1d6; padding: 2px;")
        weight_hint.setAlignment(Qt.AlignCenter)
        weight_layout.addWidget(weight_hint)

        weight_layout.addWidget(self.weight_table)

        scroll_weight = QScrollArea()
        scroll_weight.setWidget(weight_container)
        scroll_weight.setWidgetResizable(True)
        self.left_tabs.addTab(scroll_weight, "Матрица W")

        # Вкладка с матрицей D (минимальные веса)
        self.distance_table = MatrixTableWidget()

        distance_container = QWidget()
        distance_layout = QVBoxLayout(distance_container)
        distance_layout.setContentsMargins(0, 0, 0, 0)

        distance_label = QLabel("МАТРИЦА МИНИМАЛЬНЫХ ВЕСОВ D")
        distance_label.setFont(QFont("Arial", 10, QFont.Bold))
        distance_label.setStyleSheet("color: #7aa2f7; padding: 5px;")
        distance_label.setAlignment(Qt.AlignCenter)
        distance_layout.addWidget(distance_label)

        self.iteration_label = QLabel("Итерация: 0 из 0")
        self.iteration_label.setFont(QFont("Arial", 9, QFont.Bold))
        self.iteration_label.setStyleSheet("color: #ff9e64; padding: 5px;")
        self.iteration_label.setAlignment(Qt.AlignCenter)
        distance_layout.addWidget(self.iteration_label)

        # Панель управления итерациями
        iteration_control = QWidget()
        iteration_layout = QHBoxLayout(iteration_control)
        iteration_layout.setContentsMargins(10, 5, 10, 5)

        self.prev_iter_btn = QPushButton("ПРЕДЫДУЩАЯ")
        self.prev_iter_btn.setEnabled(False)
        self.prev_iter_btn.clicked.connect(self.prev_iteration)
        iteration_layout.addWidget(self.prev_iter_btn)

        self.next_iter_btn = QPushButton("СЛЕДУЮЩАЯ")
        self.next_iter_btn.setEnabled(False)
        self.next_iter_btn.clicked.connect(self.next_iteration)
        iteration_layout.addWidget(self.next_iter_btn)

        self.first_iter_btn = QPushButton("ПЕРВАЯ")
        self.first_iter_btn.setEnabled(False)
        self.first_iter_btn.clicked.connect(self.first_iteration)
        iteration_layout.addWidget(self.first_iter_btn)

        self.last_iter_btn = QPushButton("ПОСЛЕДНЯЯ")
        self.last_iter_btn.setEnabled(False)
        self.last_iter_btn.clicked.connect(self.last_iteration)
        iteration_layout.addWidget(self.last_iter_btn)

        distance_layout.addWidget(iteration_control)
        distance_layout.addWidget(self.distance_table)

        scroll_distance = QScrollArea()
        scroll_distance.setWidget(distance_container)
        scroll_distance.setWidgetResizable(True)
        self.left_tabs.addTab(scroll_distance, "Матрица D")

        # Вкладка с матрицей P (предыдущие вершины)
        self.predecessor_table = MatrixTableWidget()

        predecessor_container = QWidget()
        predecessor_layout = QVBoxLayout(predecessor_container)
        predecessor_layout.setContentsMargins(0, 0, 0, 0)

        predecessor_label = QLabel("МАТРИЦА ПРЕДЫДУЩИХ ВЕРШИН P (pᵢⱼ = 0 если пути нет)")
        predecessor_label.setFont(QFont("Arial", 10, QFont.Bold))
        predecessor_label.setStyleSheet("color: #7aa2f7; padding: 5px;")
        predecessor_label.setAlignment(Qt.AlignCenter)
        predecessor_layout.addWidget(predecessor_label)

        predecessor_layout.addWidget(self.predecessor_table)

        scroll_predecessor = QScrollArea()
        scroll_predecessor.setWidget(predecessor_container)
        scroll_predecessor.setWidgetResizable(True)
        self.left_tabs.addTab(scroll_predecessor, "Матрица P")

        # Вкладка с информацией о графе
        info_container = QWidget()
        info_layout = QVBoxLayout(info_container)

        info_label = QLabel("ИНФОРМАЦИЯ О ВЗВЕШЕННОМ ГРАФЕ")
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

        viz_label = QLabel("ВИЗУАЛИЗАЦИЯ ВЗВЕШЕННОГО ГРАФА С ПУТЕМ")
        viz_label.setFont(QFont("Arial", 10, QFont.Bold))
        viz_label.setStyleSheet("color: #7aa2f7; padding: 5px;")
        viz_label.setAlignment(Qt.AlignCenter)
        viz_layout.addWidget(viz_label)

        # Легенда
        legend_widget = QWidget()
        legend_layout = QGridLayout(legend_widget)
        legend_layout.setHorizontalSpacing(10)
        legend_layout.setVerticalSpacing(5)

        legend_items = [
            ("Начальная вершина", "#f7768e"),
            ("Конечная вершина", "#9ece6a"),
            ("Вершины пути", "#7aa2f7"),
            ("Обычные вершины", "#24283b"),
            ("Положительный вес", "#7aa2f7"),
            ("Отрицательный вес", "#f7768e"),
            ("Нулевой вес", "#a9b1d6"),
            ("Ребра пути", "#ff9e64")
        ]

        for i, (text, color) in enumerate(legend_items):
            row = i // 2
            col = (i % 2) * 2
            
            color_label = QLabel("■")
            color_label.setStyleSheet(f"color: {color}; font-size: 14px;")
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
        self.right_tabs.addTab(scroll_viz, "Визуализация графа")

        # Вкладка с журналом выполнения алгоритма
        log_container = QWidget()
        log_layout = QVBoxLayout(log_container)

        log_label = QLabel("ЖУРНАЛ ВЫПОЛНЕНИЯ АЛГОРИТМА ФЛОЙДА")
        log_label.setFont(QFont("Arial", 10, QFont.Bold))
        log_label.setStyleSheet("color: #7aa2f7; padding: 10px;")
        log_label.setAlignment(Qt.AlignCenter)
        log_layout.addWidget(log_label)

        self.algorithm_log = QTextEdit()
        self.algorithm_log.setFont(QFont("Courier New", 9))
        self.algorithm_log.setReadOnly(True)
        log_layout.addWidget(self.algorithm_log)

        self.right_tabs.addTab(log_container, "Журнал алгоритма")

        # Вкладка с матричными преобразованиями
        transforms_container = QWidget()
        transforms_layout = QVBoxLayout(transforms_container)

        transforms_label = QLabel("МАТРИЧНЫЕ ПРЕОБРАЗОВАНИЯ ФЛОЙДА")
        transforms_label.setFont(QFont("Arial", 10, QFont.Bold))
        transforms_label.setStyleSheet("color: #7aa2f7; padding: 10px;")
        transforms_label.setAlignment(Qt.AlignCenter)
        transforms_layout.addWidget(transforms_label)

        self.transforms_text = QTextEdit()
        self.transforms_text.setFont(QFont("Courier New", 9))
        self.transforms_text.setReadOnly(True)
        transforms_layout.addWidget(self.transforms_text)

        self.right_tabs.addTab(transforms_container, "Преобразования")

    def update_density_label(self, value):
        """Обновление метки плотности графа"""
        density = value / 100.0
        self.density_label.setText(f"{density:.1f}")

    def generate_graph(self):
        """Генерация нового взвешенного графа"""
        n = self.n_spinbox.value()
        density = self.density_slider.value() / 100.0
        max_weight = self.max_weight_spinbox.value()
        allow_negative = self.negative_weights_check.isChecked()

        # Обновляем диапазоны для вершин
        self.start_spinbox.setRange(1, n)
        self.end_spinbox.setRange(1, n)

        self.graph_ops = GraphOperations(n)
        weight_matrix, adj_matrix = self.graph_ops.generate_graph(density, allow_negative, max_weight)

        # Обновляем таблицы
        self.weight_table.set_matrix(weight_matrix)
        self.distance_table.clear()
        self.predecessor_table.clear()

        # Обновляем информацию о графе
        self.update_graph_info()

        # Очищаем результаты предыдущего выполнения
        self.clear_algorithm_results()

        # Обновляем визуализацию
        self.update_visualization()

        self.status_label.setText(f"Граф сгенерирован. Вершин: {n}, Плотность: {density:.2f}")

    def update_graph_info(self):
        """Обновление информации о графе"""
        if self.graph_ops is None:
            return

        info = self.graph_ops.get_graph_info()

        text = "=" * 50 + "\n"
        text += "ОСНОВНЫЕ ХАРАКТЕРИСТИКИ ВЗВЕШЕННОГО ГРАФА\n"
        text += "=" * 50 + "\n\n"

        text += f"Количество вершин: {info['vertices']}\n"
        text += f"Количество ребер: {info['edges']}\n"
        text += f"Положительных ребер: {info['positive_edges']}\n"
        text += f"Отрицательных ребер: {info['negative_edges']}\n"
        text += f"Нулевых ребер: {info['zero_edges']}\n\n"

        if info['min_weight'] < INF and info['max_weight'] > -INF:
            text += f"Минимальный вес ребра: {info['min_weight']:.2f}\n"
            text += f"Максимальный вес ребра: {info['max_weight']:.2f}\n"

        text += "\n" + "=" * 50

        self.graph_info_text.setText(text)

    def clear_algorithm_results(self):
        """Очистка результатов выполнения алгоритма"""
        self.algorithm_log.clear()
        self.transforms_text.clear()

        # Сбрасываем состояние итераций
        self.current_iteration = 0
        self.total_iterations = 0
        self.iteration_label.setText("Итерация: 0 из 0")
        self.prev_iter_btn.setEnabled(False)
        self.next_iter_btn.setEnabled(False)
        self.first_iter_btn.setEnabled(False)
        self.last_iter_btn.setEnabled(False)

        # Очищаем визуализацию пути
        if self.graph_ops and self.graph_ops.G_nx:
            self.graph_canvas.draw_weighted_graph(
                self.graph_ops.G_nx,
                self.graph_ops.weight_matrix,
                title="Взвешенный граф (алгоритм не выполнен)"
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
                title = f"Путь минимальной длины {start_vertex} → {end_vertex}"
            else:
                title = f"Путь {start_vertex} → {end_vertex} не существует"

        self.graph_canvas.draw_weighted_graph(
            self.graph_ops.G_nx,
            self.graph_ops.weight_matrix,
            path_vertices=path_vertices,
            start_vertex=start_vertex,
            end_vertex=end_vertex,
            title=title
        )

    def run_floyd_algorithm(self):
        """Выполнение алгоритма Флойда"""
        if self.graph_ops is None:
            QMessageBox.warning(self, "Предупреждение", "Сначала сгенерируйте граф!")
            return

        try:
            # Создание и выполнение алгоритма Флойда
            self.floyd_algo = FloydAlgorithm(self.graph_ops.weight_matrix)
            success, D, P, steps_log, iterations_data = self.floyd_algo.run()

            # Отображение результатов
            self.display_algorithm_results(success, D, P, steps_log, iterations_data)

            # Обновление таблиц с итоговыми матрицами
            self.distance_table.set_matrix(D)
            self.predecessor_table.set_matrix(P, is_weight_matrix=False)

            # Настройка управления итерациями
            if iterations_data:
                self.total_iterations = len(iterations_data)
                self.current_iteration = self.total_iterations
                self.update_iteration_controls()
                self.show_iteration_data(self.current_iteration - 1)

            # Прокрутка журнала вверх
            self.algorithm_log.verticalScrollBar().setValue(0)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при выполнении алгоритма Флойда: {str(e)}")

    def display_algorithm_results(self, success, D, P, steps_log, iterations_data):
        """Отображение результатов выполнения алгоритма"""
        # Отображение журнала выполнения
        log_text = "\n".join(steps_log)
        self.algorithm_log.setText(log_text)

        # Отображение матричных преобразований
        self.display_transformations(iterations_data)

        # Обновление статусной строки
        if success:
            self.status_label.setText("Алгоритм Флойда успешно выполнен")
        else:
            self.status_label.setText("Алгоритм прерван: обнаружен контур отрицательного веса")

    def display_transformations(self, iterations_data):
        """Отображение матричных преобразований"""
        if not iterations_data:
            return

        text = "=" * 50 + "\n"
        text += "ПОШАГОВЫЕ ПРЕОБРАЗОВАНИЯ МАТРИЦЫ D\n"
        text += "=" * 50 + "\n\n"

        for i, data in enumerate(iterations_data):
            text += f"ИТЕРАЦИЯ {data['iteration']} (m = {data['iteration']}):\n"
            text += f"Количество изменений: {data['changes_count']}\n"

            if data['changes_count'] > 0:
                text += "Измененные элементы:\n"

                # Находим измененные элементы
                if i > 0:
                    prev_D = iterations_data[i - 1]['D']
                    curr_D = data['D']

                    for row in range(len(curr_D)):
                        for col in range(len(curr_D[row])):
                            if row != col and row != data['iteration'] - 1 and col != data['iteration'] - 1:
                                if abs(curr_D[row][col] - prev_D[row][col]) > 1e-6:
                                    text += f"  D[{row + 1}][{col + 1}] = {curr_D[row][col]:.1f} "
                                    text += f"(было {prev_D[row][col]:.1f})\n"

            text += "\n"

        self.transforms_text.setText(text)

    def find_path(self):
        """Поиск пути между выбранными вершинами"""
        if self.floyd_algo is None:
            QMessageBox.warning(self, "Предупреждение", "Сначала выполните алгоритм Флойда!")
            return

        start = self.start_spinbox.value()
        end = self.end_spinbox.value()
        n = self.graph_ops.n if self.graph_ops else 0

        if start < 1 or start > n or end < 1 or end > n:
            QMessageBox.warning(self, "Ошибка", "Номера вершин должны быть в диапазоне от 1 до n")
            return

        try:
            # Поиск пути с помощью алгоритма Флойда
            path, total_weight, exists = self.floyd_algo.get_path(start, end)

            # Отображение результатов в журнале
            self.display_path_results(start, end, path, total_weight, exists)

            # Обновление визуализации
            self.update_visualization(path)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при поиске пути: {str(e)}")

    def display_path_results(self, start, end, path, total_weight, exists):
        """Отображение результатов поиска пути"""
        text = "\n" + "=" * 60 + "\n"
        text += "РЕЗУЛЬТАТЫ ПОИСКА ПУТИ МИНИМАЛЬНОЙ ДЛИНЫ\n"
        text += "=" * 60 + "\n\n"

        text += f"Начальная вершина: {start}\n"
        text += f"Конечная вершина: {end}\n\n"

        if not exists:
            text += "ПУТЬ НЕ СУЩЕСТВУЕТ\n"
            text += "Между выбранными вершинами нет маршрута.\n"
        elif total_weight >= INF / 2:
            text += "ПУТЬ НЕ СУЩЕСТВУЕТ\n"
            text += "Вес пути равен бесконечности (ребро отсутствует).\n"
        else:
            text += f"ПУТЬ МИНИМАЛЬНОЙ ДЛИНЫ НАЙДЕН\n"
            text += f"Суммарная длина пути: {total_weight:.2f}\n"
            text += f"Количество вершин в пути: {len(path)}\n"
            text += f"Путь минимальной длины: {' → '.join(map(str, path))}\n\n"

            # Детали пути
            if len(path) > 1:
                text += "ДЕТАЛИ ПУТИ:\n"
                for i in range(len(path) - 1):
                    u, v = path[i], path[i + 1]
                    weight = self.floyd_algo.D[u - 1][v - 1] if self.floyd_algo else 0
                    text += f"  Шаг {i + 1}: {u} → {v} (вес: {weight:.2f})\n"

        text += "\n" + "=" * 60

        # Добавляем результаты поиска пути к текущему журналу
        current_log = self.algorithm_log.toPlainText()
        self.algorithm_log.setText(current_log + text)

        # Обновление статусной строки
        if exists and total_weight < INF / 2:
            self.status_label.setText(f"Найден путь от {start} до {end} длиной {total_weight:.2f}")
        else:
            self.status_label.setText(f"Путь от {start} до {end} не существует")

    def update_iteration_controls(self):
        """Обновление элементов управления итерациями"""
        self.iteration_label.setText(f"Итерация: {self.current_iteration} из {self.total_iterations}")

        self.prev_iter_btn.setEnabled(self.current_iteration > 1)
        self.next_iter_btn.setEnabled(self.current_iteration < self.total_iterations)
        self.first_iter_btn.setEnabled(self.current_iteration > 1)
        self.last_iter_btn.setEnabled(self.current_iteration < self.total_iterations)

    def show_iteration_data(self, iteration_idx):
        """Отображение данных конкретной итерации"""
        if not hasattr(self, 'floyd_algo') or not self.floyd_algo:
            return

        if iteration_idx < 0 or iteration_idx >= len(self.floyd_algo.iterations_data):
            return

        data = self.floyd_algo.iterations_data[iteration_idx]
        self.distance_table.set_matrix(data['D'])

    def prev_iteration(self):
        """Переход к предыдущей итерации"""
        if self.current_iteration > 1:
            self.current_iteration -= 1
            self.update_iteration_controls()
            self.show_iteration_data(self.current_iteration - 1)

    def next_iteration(self):
        """Переход к следующей итерации"""
        if self.current_iteration < self.total_iterations:
            self.current_iteration += 1
            self.update_iteration_controls()
            self.show_iteration_data(self.current_iteration - 1)

    def first_iteration(self):
        """Переход к первой итерации"""
        if self.current_iteration > 1:
            self.current_iteration = 1
            self.update_iteration_controls()
            self.show_iteration_data(self.current_iteration - 1)

    def last_iteration(self):
        """Переход к последней итерации"""
        if self.current_iteration < self.total_iterations:
            self.current_iteration = self.total_iterations
            self.update_iteration_controls()
            self.show_iteration_data(self.current_iteration - 1)

    def on_left_tab_changed(self, index):
        """Обработчик изменения вкладки левой части"""
        if index == 1 and hasattr(self, 'floyd_algo') and self.floyd_algo and self.floyd_algo.iterations_data:
            # Если перешли на вкладку матрицы D и есть данные итераций
            self.update_iteration_controls()


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
    
    window = FloydAlgorithmApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()