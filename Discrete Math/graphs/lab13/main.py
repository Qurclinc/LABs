import sys
import numpy as np
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
    QDoubleSpinBox, QRadioButton, QButtonGroup
)
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QColor, QBrush, QPalette, QIcon, QKeySequence


class GraphConnectivity:
    """Класс для анализа связности графов"""

    @staticmethod
    def vertex_connectivity(adj_matrix):
        """Вычисление вершинной связности графа"""
        n = len(adj_matrix)
        G = nx.Graph()

        # Создаем граф из матрицы смежности
        for i in range(n):
            for j in range(i + 1, n):
                if adj_matrix[i][j] > 0:
                    G.add_edge(i, j)

        if not nx.is_connected(G):
            return 0  # Граф несвязный

        try:
            return nx.node_connectivity(G)
        except:
            # Вычисляем через минимальное количество вершин, удаление которых делает граф несвязным
            return GraphConnectivity._compute_vertex_connectivity(G)

    @staticmethod
    def _compute_vertex_connectivity(G):
        """Вычисление вершинной связности (альтернативная реализация)"""
        if not nx.is_connected(G):
            return 0

        n = len(G.nodes())
        if n <= 1:
            return 0

        min_connectivity = n - 1

        for node in G.nodes():
            H = G.copy()
            H.remove_node(node)
            if not nx.is_connected(H):
                return 1

        # Проверяем пары вершин
        nodes = list(G.nodes())
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                H = G.copy()
                H.remove_node(nodes[i])
                H.remove_node(nodes[j])
                if not nx.is_connected(H):
                    return 2

        return min_connectivity

    @staticmethod
    def edge_connectivity(adj_matrix):
        """Вычисление реберной связности графа"""
        n = len(adj_matrix)
        G = nx.Graph()

        # Создаем граф из матрицы смежности
        for i in range(n):
            for j in range(i + 1, n):
                if adj_matrix[i][j] > 0:
                    G.add_edge(i, j)

        if not nx.is_connected(G):
            return 0  # Граф несвязный

        try:
            return nx.edge_connectivity(G)
        except:
            return GraphConnectivity._compute_edge_connectivity(G)

    @staticmethod
    def _compute_edge_connectivity(G):
        """Вычисление реберной связности (альтернативная реализация)"""
        if not nx.is_connected(G):
            return 0

        min_connectivity = len(G.edges())

        # Простой алгоритм: минимальная степень вершины дает верхнюю границу
        min_degree = min(dict(G.degree()).values())

        return min_degree

    @staticmethod
    def analyze_digraph_connectivity(adj_matrix):
        """Анализ связности ориентированного графа"""
        n = len(adj_matrix)
        DG = nx.DiGraph()

        # Создаем ориентированный граф из матрицы смежности
        for i in range(n):
            for j in range(n):
                if i != j and adj_matrix[i][j] > 0:
                    DG.add_edge(i, j)

        # Слабосвязный (неориентированный вариант связен)
        G = nx.Graph()
        for i in range(n):
            for j in range(n):
                if i != j and (adj_matrix[i][j] > 0 or adj_matrix[j][i] > 0):
                    G.add_edge(i, j)

        weakly_connected = nx.is_connected(G) if len(G.nodes()) > 0 else False

        # Сильносвязный (связный орграф)
        strongly_connected = nx.is_strongly_connected(DG) if len(DG.nodes()) > 0 else False

        # Односторонне связный
        unilaterally_connected = nx.is_weakly_connected(DG) and not strongly_connected
        if not strongly_connected and len(DG.nodes()) > 0:
            # Проверяем одностороннюю связность
            for i in range(n):
                for j in range(n):
                    if i != j:
                        if not (nx.has_path(DG, i, j) or nx.has_path(DG, j, i)):
                            unilaterally_connected = False
                            break
                if not unilaterally_connected:
                    break

        return {
            'strongly_connected': strongly_connected,
            'unilaterally_connected': unilaterally_connected,
            'weakly_connected': weakly_connected,
            'is_digraph_empty': len(DG.nodes()) == 0
        }


class GraphGenerator:
    """Класс для генерации графов"""

    @staticmethod
    def generate_undirected_graph(n, density=0.3, allow_labels=True, max_label=10):
        """Генерация неориентированного помеченного графа"""
        adj_matrix = np.zeros((n, n), dtype=int)

        # Создаем связный остов
        for i in range(1, n):
            parent = np.random.randint(0, i)
            if allow_labels:
                weight = np.random.randint(1, max_label + 1)
            else:
                weight = 1
            adj_matrix[i][parent] = weight
            adj_matrix[parent][i] = weight

        # Добавляем случайные ребра
        total_possible_edges = n * (n - 1) // 2
        current_edges = n - 1
        target_edges = int(total_possible_edges * density)

        while current_edges < target_edges and current_edges < total_possible_edges:
            i = np.random.randint(0, n)
            j = np.random.randint(0, n)
            if i != j and adj_matrix[i][j] == 0:
                if allow_labels:
                    weight = np.random.randint(1, max_label + 1)
                else:
                    weight = 1
                adj_matrix[i][j] = weight
                adj_matrix[j][i] = weight
                current_edges += 1

        return adj_matrix

    @staticmethod
    def generate_directed_graph(n, density=0.3, max_weight=10):
        """Генерация ориентированного графа"""
        adj_matrix = np.zeros((n, n), dtype=int)

        # Создаем сильно связный остов (гарантируем сильную связность)
        # Создаем цикл, проходящий через все вершины
        for i in range(n):
            j = (i + 1) % n
            weight = np.random.randint(1, max_weight + 1)
            adj_matrix[i][j] = weight

        # Добавляем обратные ребра для гарантии сильной связности
        for i in range(1, n):
            j = i - 1
            weight = np.random.randint(1, max_weight + 1)
            adj_matrix[i][j] = weight

        # Добавляем случайные ребра
        total_possible_edges = n * (n - 1)
        current_edges = 2 * n  # Ребра в остове
        target_edges = int(total_possible_edges * density)

        while current_edges < target_edges and current_edges < total_possible_edges:
            i = np.random.randint(0, n)
            j = np.random.randint(0, n)
            if i != j and adj_matrix[i][j] == 0:
                weight = np.random.randint(1, max_weight + 1)
                adj_matrix[i][j] = weight
                current_edges += 1

        return adj_matrix

    @staticmethod
    def get_graph_components(adj_matrix, directed=False):
        """Получение компонент связности графа"""
        n = len(adj_matrix)

        if directed:
            G = nx.DiGraph()
            # Создаем неориентированную версию для поиска слабых компонент
            G_undir = nx.Graph()
        else:
            G = nx.Graph()

        for i in range(n):
            for j in range(n):
                if i != j and adj_matrix[i][j] > 0:
                    if directed:
                        G.add_edge(i, j)
                        G_undir.add_edge(i, j)
                    else:
                        G.add_edge(i, j)

        if directed:
            # Слабые компоненты (неориентированные)
            weak_components = list(nx.weakly_connected_components(G))
            # Сильные компоненты
            strong_components = list(nx.strongly_connected_components(G))

            return {
                'weak_components': weak_components,
                'strong_components': strong_components,
                'weak_count': len(weak_components),
                'strong_count': len(strong_components)
            }
        else:
            components = list(nx.connected_components(G))
            return {
                'components': components,
                'count': len(components)
            }


class MatrixTableWidget(QTableWidget):
    """Виджет таблицы с темной темой"""

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

    def set_adjacency_matrix(self, matrix, labels=None, directed=False):
        """Установка матрицы смежности для отображения"""
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
                value = str(matrix[i][j])

                # Определяем цвет фона
                if i == j:
                    bg_color = QColor('#24283b')  # Темный для диагонали
                    fg_color = QColor('#c0caf5')  # Светлый текст
                elif matrix[i][j] > 0:
                    if directed and matrix[j][i] > 0:
                        bg_color = QColor('#9ece6a')  # Зеленый для двусторонних ребер
                        fg_color = QColor('#1a1b26')  # Темный текст
                    elif directed:
                        bg_color = QColor('#7aa2f7')  # Синий для направленных ребер
                        fg_color = QColor('#1a1b26')  # Темный текст
                    else:
                        bg_color = QColor('#9ece6a')  # Зеленый для ребер
                        fg_color = QColor('#1a1b26')  # Темный текст
                else:
                    bg_color = QColor('#1a1b26')  # Темный для отсутствия ребер
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
    """Холст для отрисовки графов в темной теме"""

    def __init__(self, parent=None, width=4.5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor='#1a1b26')
        self.ax = self.fig.add_subplot(111, facecolor='#1a1b26')
        super().__init__(self.fig)
        self.setParent(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Настраиваем темную тему для холста
        self.setStyleSheet("background-color: #1a1b26; border: 1px solid #3b4261;")

    def draw_graph(self, adj_matrix, directed=False, title="", highlight_components=False):
        """Отрисовка графа"""
        self.ax.clear()
        
        # Устанавливаем темный фон
        self.ax.set_facecolor('#1a1b26')
        self.fig.patch.set_facecolor('#1a1b26')

        if adj_matrix is None or len(adj_matrix) == 0:
            self.ax.text(0.5, 0.5, "Граф не сгенерирован",
                         ha='center', va='center', fontsize=12, color='#c0caf5')
            self.ax.set_xlim(0, 1)
            self.ax.set_ylim(0, 1)
            self.draw()
            return

        n = len(adj_matrix)

        if directed:
            G = nx.DiGraph()
        else:
            G = nx.Graph()

        G.add_nodes_from(range(n))

        # Добавляем ребра
        for i in range(n):
            for j in range(n):
                if i != j and adj_matrix[i][j] > 0:
                    if directed:
                        G.add_edge(i, j, weight=adj_matrix[i][j])
                    elif i < j and adj_matrix[i][j] > 0:
                        G.add_edge(i, j, weight=adj_matrix[i][j])

        if len(G.nodes()) == 0:
            self.ax.text(0.5, 0.5, "Граф пустой",
                         ha='center', va='center', fontsize=12, color='#c0caf5')
            self.ax.set_xlim(0, 1)
            self.ax.set_ylim(0, 1)
            self.draw()
            return

        # Используем spring layout
        pos = nx.spring_layout(G, seed=42, k=1.5, iterations=100)

        # Определяем цвета вершин для компонент
        if highlight_components:
            if directed:
                components = list(nx.weakly_connected_components(G))
            else:
                components = list(nx.connected_components(G))

            node_colors = []
            color_palette = ['#f7768e', '#9ece6a', '#7aa2f7', '#ff9e64',
                             '#bb9af7', '#73daca', '#e0af68', '#c0caf5']

            color_map = {}
            for idx, component in enumerate(components):
                color = color_palette[idx % len(color_palette)]
                for node in component:
                    color_map[node] = color

            for node in G.nodes():
                node_colors.append(color_map.get(node, '#24283b'))
        else:
            node_colors = ['#7aa2f7'] * len(G.nodes())

        # Рисуем вершины (уменьшаем размер для лучшей видимости)
        node_size = 300 if n > 12 else 400
        nx.draw_networkx_nodes(G, pos, ax=self.ax,
                               node_color=node_colors,
                               node_size=node_size,
                               edgecolors='#c0caf5',  # Светлая обводка
                               linewidths=1.5)

        # Рисуем ребра
        if directed:
            nx.draw_networkx_edges(G, pos, ax=self.ax,
                                   arrowstyle='->',
                                   arrowsize=12,  # Уменьшаем стрелки
                                   edge_color='#c0caf5',  # Светлый цвет
                                   width=1.5,
                                   alpha=0.8)
        else:
            nx.draw_networkx_edges(G, pos, ax=self.ax,
                                   edge_color='#c0caf5',  # Светлый цвет
                                   width=1.5,
                                   alpha=0.8)

        # Рисуем метки вершин (уменьшаем шрифт для больших графов)
        font_size = 8 if n > 15 else 10
        labels = {node: str(node + 1) for node in G.nodes()}
        nx.draw_networkx_labels(G, pos, ax=self.ax,
                                labels=labels,
                                font_size=font_size,
                                font_weight='bold',
                                font_color='#c0caf5')  # Светлый текст

        # Рисуем веса ребер (если есть)
        edge_labels = {}
        for (u, v) in G.edges():
            weight = adj_matrix[u][v]
            if weight > 1:  # Показываем только если вес > 1
                edge_labels[(u, v)] = str(weight)

        if edge_labels:
            nx.draw_networkx_edge_labels(G, pos, ax=self.ax,
                                         edge_labels=edge_labels,
                                         font_size=7,
                                         font_color='#ff9e64',  # Оранжевый текст
                                         bbox=dict(facecolor='#1a1b26', edgecolor='#3b4261', alpha=0.9))

        # Настраиваем заголовок
        self.ax.set_title(title, fontsize=11, fontweight='bold', pad=12, color='#7aa2f7')
        
        # Отключаем оси
        self.ax.axis('off')
        
        # Настраиваем границы
        for spine in self.ax.spines.values():
            spine.set_edgecolor('#3b4261')
            
        self.fig.tight_layout(pad=1.0)
        self.draw()


class GraphConnectivityApp(QMainWindow):
    """Главное окно приложения с темной темой"""

    def __init__(self):
        super().__init__()
        self.current_undirected_matrix = None
        self.current_directed_matrix = None
        self.init_ui()
        self.generate_graph()

    def init_ui(self):
        """Инициализация интерфейса с темной темой и адаптивной размерностью"""
        self.setWindowTitle("Анализ связности графов")
        self.setGeometry(50, 50, 1400, 800)  # Уменьшаем размер окна

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
                margin-top: 8px;
                padding-top: 10px;
                font-weight: bold;
                color: #7aa2f7;
                font-size: 10px;
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
                font-size: 10px;
                min-height: 20px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                background-color: #3b4261;
                border: 1px solid #7aa2f7;
                width: 18px;
                height: 10px;
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
                min-height: 20px;
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
                font-size: 9px;
            }
            QRadioButton {
                color: #c0caf5;
                font-size: 10px;
            }
            QRadioButton::indicator {
                width: 12px;
                height: 12px;
                border-radius: 7px;
                border: 2px solid #7aa2f7;
                background-color: #24283b;
            }
            QRadioButton::indicator:checked {
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
        title = QLabel("АНАЛИЗ СВЯЗНОСТИ ГРАФОВ")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setStyleSheet("""
            QLabel {
                color: #7aa2f7;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1a1b26, stop:0.5 #24283b, stop:1 #1a1b26);
                padding: 10px;
                border-radius: 6px;
                margin: 2px;
                border: 2px solid #7aa2f7;
            }
        """)
        main_layout.addWidget(title)

        # Панель управления (компактная)
        control_group = QGroupBox("УПРАВЛЕНИЕ ГЕНЕРАЦИЕЙ ГРАФОВ")
        control_group.setFont(QFont("Arial", 9, QFont.Bold))
        control_layout = QGridLayout(control_group)
        control_layout.setSpacing(6)
        control_layout.setContentsMargins(8, 15, 8, 8)

        # Количество вершин (уменьшаем диапазон для компактности)
        control_layout.addWidget(QLabel("Количество вершин:"), 0, 0)
        self.n_spinbox = QSpinBox()
        self.n_spinbox.setRange(5, 12)  # Уменьшаем максимальное количество
        self.n_spinbox.setValue(8)
        self.n_spinbox.setFixedWidth(70)
        control_layout.addWidget(self.n_spinbox, 0, 1)

        # Плотность графа
        control_layout.addWidget(QLabel("Плотность графа:"), 0, 2)
        self.density_slider = QSlider(Qt.Horizontal)
        self.density_slider.setRange(10, 60)  # Уменьшаем максимальную плотность
        self.density_slider.setValue(30)
        self.density_slider.setFixedWidth(90)
        control_layout.addWidget(self.density_slider, 0, 3)
        self.density_label = QLabel("0.3")
        self.density_label.setFixedWidth(35)
        control_layout.addWidget(self.density_label, 0, 4)
        self.density_slider.valueChanged.connect(self.update_density_label)

        # Максимальная метка ребра
        control_layout.addWidget(QLabel("Макс. метка:"), 0, 5)
        self.max_label_spinbox = QSpinBox()
        self.max_label_spinbox.setRange(1, 10)  # Уменьшаем максимальную метку
        self.max_label_spinbox.setValue(5)
        self.max_label_spinbox.setFixedWidth(70)
        control_layout.addWidget(self.max_label_spinbox, 0, 6)

        # Тип графа
        control_layout.addWidget(QLabel("Тип анализа:"), 1, 0)
        self.graph_type_group = QButtonGroup()

        self.undirected_radio = QRadioButton("Неориентированный")
        self.undirected_radio.setChecked(True)
        self.graph_type_group.addButton(self.undirected_radio)
        control_layout.addWidget(self.undirected_radio, 1, 1, 1, 2)

        self.directed_radio = QRadioButton("Ориентированный")
        self.graph_type_group.addButton(self.directed_radio)
        control_layout.addWidget(self.directed_radio, 1, 3, 1, 2)

        # Кнопки (компактные)
        self.generate_btn = QPushButton("СГЕНЕРИРОВАТЬ ГРАФ")
        self.generate_btn.setFixedHeight(28)
        self.generate_btn.clicked.connect(self.generate_graph)
        control_layout.addWidget(self.generate_btn, 0, 7, 1, 2)

        self.analyze_btn = QPushButton("АНАЛИЗ СВЯЗНОСТИ")
        self.analyze_btn.setFixedHeight(28)
        self.analyze_btn.clicked.connect(self.analyze_connectivity)
        control_layout.addWidget(self.analyze_btn, 1, 7, 1, 2)

        main_layout.addWidget(control_group)

        # Основной сплиттер (меняем пропорции)
        main_splitter = QSplitter(Qt.Horizontal)
        main_splitter.setHandleWidth(2)
        main_splitter.setStyleSheet("QSplitter::handle { background-color: #7aa2f7; }")

        # Левая часть - матрицы (меньше места)
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(1, 1, 1, 1)

        # Вкладки для левой части
        self.left_tabs = QTabWidget()
        self.left_tabs.setFont(QFont("Arial", 9, QFont.Bold))
        self.left_tabs.currentChanged.connect(self.on_tab_changed)

        # Создаем вкладки левой части
        self.create_left_tabs()

        left_layout.addWidget(self.left_tabs)
        main_splitter.addWidget(left_widget)

        # Правая часть - визуализация и анализ (больше места)
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(1, 1, 1, 1)

        # Вкладки для правой части
        self.right_tabs = QTabWidget()
        self.right_tabs.setFont(QFont("Arial", 9, QFont.Bold))

        # Создаем вкладки правой части
        self.create_right_tabs()

        right_layout.addWidget(self.right_tabs)
        main_splitter.addWidget(right_widget)

        # Устанавливаем пропорции сплиттера (40% матрицы, 60% графика)
        main_splitter.setSizes([560, 840])
        main_layout.addWidget(main_splitter, 1)

        # Статусная строка
        self.status_label = QLabel("Готов к работе. Сгенерируйте граф и выполните анализ связности.")
        self.status_label.setFont(QFont("Arial", 9))
        self.status_label.setStyleSheet("color: #c0caf5; padding: 3px;")
        main_layout.addWidget(self.status_label)

    def create_left_tabs(self):
        """Создание вкладок левой части"""
        # Вкладка с матрицей смежности неориентированного графа
        self.undirected_table = MatrixTableWidget()

        undir_container = QWidget()
        undir_layout = QVBoxLayout(undir_container)
        undir_layout.setContentsMargins(0, 0, 0, 0)

        undir_label = QLabel("МАТРИЦА СМЕЖНОСТИ НЕОРИЕНТИРОВАННОГО ГРАФА")
        undir_label.setFont(QFont("Arial", 9, QFont.Bold))
        undir_label.setStyleSheet("color: #7aa2f7; padding: 3px;")
        undir_label.setAlignment(Qt.AlignCenter)
        undir_layout.addWidget(undir_label)

        undir_hint = QLabel("Зеленый - ребра графа, Темный - диагональ")
        undir_hint.setFont(QFont("Arial", 8))
        undir_hint.setStyleSheet("color: #a9b1d6; padding: 2px;")
        undir_hint.setAlignment(Qt.AlignCenter)
        undir_layout.addWidget(undir_hint)

        undir_layout.addWidget(self.undirected_table)

        scroll_undir = QScrollArea()
        scroll_undir.setWidget(undir_container)
        scroll_undir.setWidgetResizable(True)
        self.left_tabs.addTab(scroll_undir, "Неориентированный")

        # Вкладка с матрицей смежности ориентированного графа
        self.directed_table = MatrixTableWidget()

        dir_container = QWidget()
        dir_layout = QVBoxLayout(dir_container)
        dir_layout.setContentsMargins(0, 0, 0, 0)

        dir_label = QLabel("МАТРИЦА СМЕЖНОСТИ ОРИЕНТИРОВАННОГО ГРАФА")
        dir_label.setFont(QFont("Arial", 9, QFont.Bold))
        dir_label.setStyleSheet("color: #7aa2f7; padding: 3px;")
        dir_label.setAlignment(Qt.AlignCenter)
        dir_layout.addWidget(dir_label)

        dir_hint = QLabel("Синий - направленные ребра, Зеленый - двусторонние")
        dir_hint.setFont(QFont("Arial", 8))
        dir_hint.setStyleSheet("color: #a9b1d6; padding: 2px;")
        dir_hint.setAlignment(Qt.AlignCenter)
        dir_layout.addWidget(dir_hint)

        dir_layout.addWidget(self.directed_table)

        scroll_dir = QScrollArea()
        scroll_dir.setWidget(dir_container)
        scroll_dir.setWidgetResizable(True)
        self.left_tabs.addTab(scroll_dir, "Ориентированный")

    def create_right_tabs(self):
        """Создание вкладок правой части (компактные)"""
        # Вкладка с визуализацией неориентированного графа
        self.undirected_canvas = GraphCanvas(self, width=5.5, height=4.5)

        undir_viz_container = QWidget()
        undir_viz_layout = QVBoxLayout(undir_viz_container)
        undir_viz_layout.setContentsMargins(0, 0, 0, 0)
        undir_viz_layout.setSpacing(3)

        undir_viz_label = QLabel("ВИЗУАЛИЗАЦИЯ НЕОРИЕНТИРОВАННОГО ГРАФА")
        undir_viz_label.setFont(QFont("Arial", 9, QFont.Bold))
        undir_viz_label.setStyleSheet("color: #7aa2f7; padding: 3px;")
        undir_viz_label.setAlignment(Qt.AlignCenter)
        undir_viz_layout.addWidget(undir_viz_label)

        # Компактная легенда
        legend_widget = QWidget()
        legend_layout = QGridLayout(legend_widget)
        legend_layout.setHorizontalSpacing(8)
        legend_layout.setVerticalSpacing(3)
        legend_layout.setContentsMargins(5, 2, 5, 2)

        legend_items = [
            ("Вершины", "#7aa2f7"),
            ("Ребра", "#c0caf5"),
            ("Метки ребер", "#ff9e64"),
            ("Компоненты", "Разные цвета")
        ]

        for i, (text, color) in enumerate(legend_items):
            row = i // 2
            col = (i % 2) * 2
            
            color_label = QLabel("■")
            color_label.setStyleSheet(f"color: {color}; font-size: 12px;")
            text_label = QLabel(text)
            text_label.setStyleSheet("font-size: 8px; color: #a9b1d6;")
            
            legend_layout.addWidget(color_label, row, col)
            legend_layout.addWidget(text_label, row, col + 1)

        legend_layout.setColumnStretch(4, 1)
        undir_viz_layout.addWidget(legend_widget)
        undir_viz_layout.addWidget(self.undirected_canvas)

        scroll_undir_viz = QScrollArea()
        scroll_undir_viz.setWidget(undir_viz_container)
        scroll_undir_viz.setWidgetResizable(True)
        self.right_tabs.addTab(scroll_undir_viz, "Визуализация (неор.)")

        # Вкладка с визуализацией ориентированного графа
        self.directed_canvas = GraphCanvas(self, width=5.5, height=4.5)

        dir_viz_container = QWidget()
        dir_viz_layout = QVBoxLayout(dir_viz_container)
        dir_viz_layout.setContentsMargins(0, 0, 0, 0)
        dir_viz_layout.setSpacing(3)

        dir_viz_label = QLabel("ВИЗУАЛИЗАЦИЯ ОРИЕНТИРОВАННОГО ГРАФА")
        dir_viz_label.setFont(QFont("Arial", 9, QFont.Bold))
        dir_viz_label.setStyleSheet("color: #7aa2f7; padding: 3px;")
        dir_viz_label.setAlignment(Qt.AlignCenter)
        dir_viz_layout.addWidget(dir_viz_label)

        # Компактная легенда
        dir_legend_widget = QWidget()
        dir_legend_layout = QGridLayout(dir_legend_widget)
        dir_legend_layout.setHorizontalSpacing(8)
        dir_legend_layout.setVerticalSpacing(3)
        dir_legend_layout.setContentsMargins(5, 2, 5, 2)

        dir_legend_items = [
            ("Вершины", "#7aa2f7"),
            ("Направленные ребра", "#c0caf5"),
            ("Метки ребер", "#ff9e64"),
            ("Стрелки", "→")
        ]

        for i, (text, color) in enumerate(dir_legend_items):
            row = i // 2
            col = (i % 2) * 2
            
            color_label = QLabel("■" if color != "→" else "→")
            color_label.setStyleSheet(f"color: {color if color != '→' else '#c0caf5'}; font-size: 12px;")
            text_label = QLabel(text)
            text_label.setStyleSheet("font-size: 8px; color: #a9b1d6;")
            
            dir_legend_layout.addWidget(color_label, row, col)
            dir_legend_layout.addWidget(text_label, row, col + 1)

        dir_legend_layout.setColumnStretch(4, 1)
        dir_viz_layout.addWidget(dir_legend_widget)
        dir_viz_layout.addWidget(self.directed_canvas)

        scroll_dir_viz = QScrollArea()
        scroll_dir_viz.setWidget(dir_viz_container)
        scroll_dir_viz.setWidgetResizable(True)
        self.right_tabs.addTab(scroll_dir_viz, "Визуализация (ор.)")

        # Вкладка с информацией о графе
        info_container = QWidget()
        info_layout = QVBoxLayout(info_container)
        info_layout.setContentsMargins(5, 5, 5, 5)

        info_label = QLabel("ИНФОРМАЦИЯ О ГРАФЕ И КОМПОНЕНТАХ СВЯЗНОСТИ")
        info_label.setFont(QFont("Arial", 9, QFont.Bold))
        info_label.setStyleSheet("color: #7aa2f7; padding: 8px;")
        info_label.setAlignment(Qt.AlignCenter)
        info_layout.addWidget(info_label)

        self.graph_info_text = QTextEdit()
        self.graph_info_text.setFont(QFont("Courier New", 9))
        self.graph_info_text.setReadOnly(True)
        info_layout.addWidget(self.graph_info_text)

        self.right_tabs.addTab(info_container, "Информация")

        # Вкладка с результатами анализа
        results_container = QWidget()
        results_layout = QVBoxLayout(results_container)
        results_layout.setContentsMargins(5, 5, 5, 5)

        results_label = QLabel("РЕЗУЛЬТАТЫ АНАЛИЗА СВЯЗНОСТИ")
        results_label.setFont(QFont("Arial", 9, QFont.Bold))
        results_label.setStyleSheet("color: #7aa2f7; padding: 8px;")
        results_label.setAlignment(Qt.AlignCenter)
        results_layout.addWidget(results_label)

        self.results_text = QTextEdit()
        self.results_text.setFont(QFont("Courier New", 9))
        self.results_text.setReadOnly(True)
        results_layout.addWidget(self.results_text)

        self.right_tabs.addTab(results_container, "Результаты")

    def update_density_label(self, value):
        """Обновление метки плотности графа"""
        density = value / 100.0
        self.density_label.setText(f"{density:.1f}")

    def on_tab_changed(self, index):
        """Обработчик смены вкладки"""
        if index == 0 and self.current_undirected_matrix is not None:
            self.update_undirected_visualization()
        elif index == 1 and self.current_directed_matrix is not None:
            self.update_directed_visualization()

    def generate_graph(self):
        """Генерация графа"""
        n = self.n_spinbox.value()
        density = self.density_slider.value() / 100.0
        max_label = self.max_label_spinbox.value()

        # Генерация неориентированного графа
        self.current_undirected_matrix = GraphGenerator.generate_undirected_graph(
            n, density, True, max_label
        )

        # Генерация ориентированного графа
        self.current_directed_matrix = GraphGenerator.generate_directed_graph(
            n, density, max_label
        )

        # Обновление таблиц
        self.undirected_table.set_adjacency_matrix(self.current_undirected_matrix, directed=False)
        self.directed_table.set_adjacency_matrix(self.current_directed_matrix, directed=True)

        # Обновление визуализации
        self.update_undirected_visualization()
        self.update_directed_visualization()

        # Обновление информации
        self.update_graph_info()

        # Очистка результатов
        self.results_text.clear()

        self.status_label.setText(f"Графы сгенерированы. Вершин: {n}, Плотность: {density:.2f}")

    def update_undirected_visualization(self, highlight_components=False):
        """Обновление визуализации неориентированного графа"""
        if self.current_undirected_matrix is not None:
            title = f"Неориентированный граф (n={len(self.current_undirected_matrix)})"
            if highlight_components:
                title += " - компоненты связности"

            self.undirected_canvas.draw_graph(
                self.current_undirected_matrix,
                directed=False,
                title=title,
                highlight_components=highlight_components
            )

    def update_directed_visualization(self, highlight_components=False):
        """Обновление визуализации ориентированного графа"""
        if self.current_directed_matrix is not None:
            title = f"Ориентированный граф (n={len(self.current_directed_matrix)})"
            if highlight_components:
                title += " - слабые компоненты"

            self.directed_canvas.draw_graph(
                self.current_directed_matrix,
                directed=True,
                title=title,
                highlight_components=highlight_components
            )

    def update_graph_info(self):
        """Обновление информации о графе"""
        if self.current_undirected_matrix is None or self.current_directed_matrix is None:
            return

        n = len(self.current_undirected_matrix)

        # Информация о неориентированном графе
        undir_edges = 0
        for i in range(n):
            for j in range(i + 1, n):
                if self.current_undirected_matrix[i][j] > 0:
                    undir_edges += 1

        # Информация об ориентированном графе
        dir_edges = 0
        for i in range(n):
            for j in range(n):
                if i != j and self.current_directed_matrix[i][j] > 0:
                    dir_edges += 1

        text = "=" * 45 + "\n"
        text += "ОСНОВНАЯ ИНФОРМАЦИЯ О ГРАФАХ\n"
        text += "=" * 45 + "\n\n"

        text += f"Количество вершин: {n}\n"
        text += f"Плотность генерации: {self.density_slider.value() / 100:.2f}\n"
        text += f"Максимальная метка ребра: {self.max_label_spinbox.value()}\n\n"

        text += "НЕОРИЕНТИРОВАННЫЙ ГРАФ:\n"
        text += f"  • Количество ребер: {undir_edges}\n"
        max_edges = n * (n - 1) // 2
        text += f"  • Максимально возможное: {max_edges}\n"
        text += f"  • Фактическая плотность: {undir_edges / max_edges:.3f}\n\n"

        text += "ОРИЕНТИРОВАННЫЙ ГРАФ:\n"
        text += f"  • Количество дуг: {dir_edges}\n"
        max_dir_edges = n * (n - 1)
        text += f"  • Максимально возможное: {max_dir_edges}\n"
        text += f"  • Фактическая плотность: {dir_edges / max_dir_edges:.3f}\n\n"

        # Компоненты связности
        undir_components = GraphGenerator.get_graph_components(self.current_undirected_matrix, directed=False)
        dir_components = GraphGenerator.get_graph_components(self.current_directed_matrix, directed=True)

        text += "КОМПОНЕНТЫ СВЯЗНОСТИ:\n"
        text += f"  • Неориентированный граф: {undir_components['count']} компонент\n"

        if undir_components['count'] <= 3:
            for idx, component in enumerate(undir_components['components']):
                vertices = [v + 1 for v in component]
                text += f"    Компонента {idx + 1}: {sorted(vertices)}\n"

        text += f"  • Ориентированный граф:\n"
        text += f"    - Слабых компонент: {dir_components['weak_count']}\n"
        text += f"    - Сильных компонент: {dir_components['strong_count']}\n"

        if dir_components['weak_count'] <= 3:
            for idx, component in enumerate(dir_components['weak_components']):
                vertices = [v + 1 for v in component]
                text += f"    Слабая компонента {idx + 1}: {sorted(vertices)}\n"

        self.graph_info_text.setText(text)

    def analyze_connectivity(self):
        """Анализ связности графов"""
        if self.current_undirected_matrix is None or self.current_directed_matrix is None:
            QMessageBox.warning(self, "Предупреждение", "Сначала сгенерируйте граф!")
            return

        try:
            n = len(self.current_undirected_matrix)

            # Анализ неориентированного графа
            vertex_conn = GraphConnectivity.vertex_connectivity(self.current_undirected_matrix)
            edge_conn = GraphConnectivity.edge_connectivity(self.current_undirected_matrix)

            # Анализ ориентированного графа
            digraph_analysis = GraphConnectivity.analyze_digraph_connectivity(self.current_directed_matrix)

            # Отображение результатов
            self.display_results(vertex_conn, edge_conn, digraph_analysis, n)

            # Обновление визуализации с выделением компонент
            self.update_undirected_visualization(highlight_components=True)
            self.update_directed_visualization(highlight_components=True)

            self.status_label.setText("Анализ связности выполнен")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при анализе связности: {str(e)}")

    def display_results(self, vertex_conn, edge_conn, digraph_analysis, n):
        """Отображение результатов анализа"""
        text = "=" * 45 + "\n"
        text += "РЕЗУЛЬТАТЫ АНАЛИЗА СВЯЗНОСТИ\n"
        text += "=" * 45 + "\n\n"

        text += "НЕОРИЕНТИРОВАННЫЙ ГРАФ:\n"
        text += f"  • Вершинная связность: {vertex_conn}\n"
        text += f"  • Реберная связность: {edge_conn}\n"

        if vertex_conn == 0:
            text += "  Граф НЕСВЯЗНЫЙ (вершинная связность = 0)\n"
        elif vertex_conn == 1:
            text += "  Граф связный, но есть шарниры (вершины связности = 1)\n"
        elif vertex_conn >= 2:
            text += f"  Граф {vertex_conn}-связный (вершины связности ≥ 2)\n"

        # Вычисляем минимальную степень
        min_degree = n
        for i in range(n):
            degree = sum(1 for j in range(n) if self.current_undirected_matrix[i][j] > 0)
            if degree < min_degree:
                min_degree = degree

        text += f"\n  • Теорема Уитни: κ(G) ≤ λ(G) ≤ δ(G)\n"
        text += f"    где κ(G)={vertex_conn} - вершинная связность,\n"
        text += f"        λ(G)={edge_conn} - реберная связность,\n"
        text += f"        δ(G)={min_degree} - минимальная степень вершины.\n"

        if vertex_conn <= edge_conn <= min_degree:
            text += "  Неравенство Уитни выполняется\n"
        else:
            text += "  Неравенство Уитни НЕ выполняется\n"

        text += "\n" + "-" * 45 + "\n\n"

        text += "ОРИЕНТИРОВАННЫЙ ГРАФ:\n"

        if digraph_analysis['is_digraph_empty']:
            text += "  Граф пустой (нет дуг)\n"
        else:
            if digraph_analysis['strongly_connected']:
                text += "  СИЛЬНОСВЯЗНЫЙ\n"
                text += "  • Существует путь между ЛЮБЫМИ двумя вершинами в обоих направлениях\n"
                text += "  • Все вершины находятся в одной сильной компоненте\n"
            elif digraph_analysis['unilaterally_connected']:
                text += "  ОДНОСТОРОННЕ СВЯЗНЫЙ\n"
                text += "  • Для любой пары вершин существует путь ХОТЯ БЫ в одном направлении\n"
                text += "  • Нет сильной связности, но есть односторонняя достижимость\n"
            elif digraph_analysis['weakly_connected']:
                text += "  СЛАБОСВЯЗНЫЙ\n"
                text += "  • Неориентированный вариант графа является связным\n"
                text += "  • Существуют пары вершин, не достижимые друг из друга\n"
            else:
                text += "  НЕСВЯЗНЫЙ\n"
                text += "  • Неориентированный вариант графа также несвязный\n"

            # Компоненты
            components_info = GraphGenerator.get_graph_components(self.current_directed_matrix, directed=True)
            text += f"\n  • Количество сильных компонент: {components_info['strong_count']}\n"
            text += f"  • Количество слабых компонент: {components_info['weak_count']}\n"

        text += "\n" + "=" * 45 + "\n\n"

        text += "ВЫВОДЫ:\n"

        if vertex_conn == 0:
            text += "1. Неориентированный граф НЕСВЯЗНЫЙ\n"
        else:
            text += f"1. Неориентированный граф {vertex_conn}-связный\n"

        if digraph_analysis['strongly_connected']:
            text += "2. Ориентированный граф СИЛЬНОСВЯЗНЫЙ (наиболее строгий тип связности)\n"
        elif digraph_analysis['unilaterally_connected']:
            text += "2. Ориентированный граф ОДНОСТОРОННЕ СВЯЗНЫЙ\n"
        elif digraph_analysis['weakly_connected']:
            text += "2. Ориентированный граф СЛАБОСВЯЗНЫЙ (наиболее слабый тип связности)\n"
        else:
            text += "2. Ориентированный граф НЕСВЯЗНЫЙ\n"

        self.results_text.setText(text)


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
    
    window = GraphConnectivityApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()