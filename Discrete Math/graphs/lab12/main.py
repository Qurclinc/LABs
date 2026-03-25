import sys
import numpy as np
import heapq
from collections import defaultdict
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
    """Реализация алгоритма Дейкстры для поиска кратчайшего пути"""

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

    def find_shortest_path(self, start, end, excluded_vertices=None):
        """
        Нахождение кратчайшего пути от start до end

        Args:
            start: начальная вершина (0-based)
            end: конечная вершина (0-based)
            excluded_vertices: список вершин для исключения

        Returns:
            tuple: (weight, path) или (GM, []) если путь не найден
        """
        if excluded_vertices is None:
            excluded_vertices = []

        # Создаем копию матрицы с исключенными вершинами
        W_modified = np.copy(self.W)
        for v in excluded_vertices:
            for i in range(self.n):
                W_modified[i][v] = self.GM
                W_modified[v][i] = self.GM

        # Алгоритм Дейкстры
        dist = [self.GM] * self.n
        prev = [-1] * self.n
        visited = [False] * self.n

        dist[start] = 0
        pq = [(0, start)]  # (distance, vertex)

        while pq:
            current_dist, u = heapq.heappop(pq)

            if visited[u]:
                continue

            visited[u] = True

            if u == end:
                break

            for v in range(self.n):
                if not visited[v] and W_modified[u][v] < self.GM:
                    new_dist = current_dist + W_modified[u][v]
                    if new_dist < dist[v]:
                        dist[v] = new_dist
                        prev[v] = u
                        heapq.heappush(pq, (new_dist, v))

        # Восстановление пути
        if dist[end] >= self.GM:
            return self.GM, []

        path = []
        current = end
        while current != -1:
            path.insert(0, current)
            current = prev[current]

        return dist[end], path


class YenAlgorithm:
    """Реализация алгоритма Йена для нахождения K кратчайших путей"""

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
        self.dijkstra = DijkstraAlgorithm(weight_matrix, GM)

    def find_k_shortest_paths(self, u1, u2, K):
        """
        Нахождение K кратчайших путей от u1 до u2

        Args:
            u1: начальная вершина (1-based)
            u2: конечная вершина (1-based)
            K: количество путей для поиска

        Returns:
            tuple: (paths, weights, steps_log)
            paths: список путей (каждый путь - список вершин 1-based)
            weights: список весов путей
            steps_log: журнал выполнения алгоритма
        """
        # Конвертируем в 0-based индексы
        start = u1 - 1
        end = u2 - 1

        steps_log = []
        steps_log.append("=" * 60)
        steps_log.append("АЛГОРИТМ ЙЕНА - НАЧАЛО РАБОТЫ")
        steps_log.append("=" * 60)
        steps_log.append(f"Поиск {K} кратчайших путей от {u1} до {u2}")
        steps_log.append(f"GM (бесконечность): {self.GM}")

        # Шаг 1: Находим первый кратчайший путь
        steps_log.append(f"\nШАГ 1: Поиск первого кратчайшего пути")
        weight1, path1 = self.dijkstra.find_shortest_path(start, end)

        if weight1 >= self.GM:
            steps_log.append(f"Путь от {u1} до {u2} не существует!")
            return [], [], steps_log

        # Конвертируем путь в 1-based индексы
        path1_1based = [v + 1 for v in path1]
        steps_log.append(f"Найден путь 1: {' → '.join(map(str, path1_1based))}")
        steps_log.append(f"Вес пути 1: {weight1}")

        # Инициализация
        A = [(weight1, path1)]  # список найденных путей (0-based)
        B = []  # список кандидатов (0-based)

        paths_1based = [path1_1based]
        weights = [weight1]

        # Массив для хранения длины каждого пути
        lengths = [len(path1_1based) - 1]

        steps_log.append(f"\nШАГ 2: Инициализация")
        steps_log.append(f"Путь P1 добавлен в результирующий список")
        steps_log.append(f"A (найденные пути): {len(A)} путь")
        steps_log.append(f"B (кандидаты): {len(B)} путей")

        for k in range(2, K + 1):
            steps_log.append(f"\n" + "=" * 40)
            steps_log.append(f"ИТЕРАЦИЯ k = {k}: Поиск {k}-го кратчайшего пути")
            steps_log.append(f"=" * 40)

            # Получаем (k-1)-й путь
            prev_weight, prev_path = A[-1]
            L = len(prev_path)  # Количество вершин в пути

            steps_log.append(f"\nP{k - 1}: {' → '.join([str(v + 1) for v in prev_path])}")
            steps_log.append(f"Вес P{k - 1}: {prev_weight}")
            steps_log.append(f"Количество вершин в P{k - 1}: {L}")

            MinW = self.GM
            MinPath = None

            # Перебираем все вершины отклонения i
            for i in range(L - 1):
                steps_log.append(
                    f"\nРассматриваем отклонение в вершине i = {i + 1} (вершина {prev_path[i] + 1})")

                # Шаг 3: Проверка совпадения подпутей
                steps_log.append(f"Проверка подпутей до вершины отклонения")

                match_found = False
                for j, (_, path_j) in enumerate(A):
                    if i < len(path_j):
                        # Проверяем совпадают ли первые i вершин
                        if prev_path[:i + 1] == path_j[:i + 1]:
                            steps_log.append(f"  Подпуть совпадает с путем P{j + 1} до вершины {prev_path[i] + 1}")
                            match_found = True
                            break

                if match_found:
                    steps_log.append(f"  Пропускаем это отклонение (дубликат)")
                    continue

                # Шаг 4-5: Находим кратчайшее ответвление
                root = prev_path[:i + 1]  # Корень (первые i+1 вершин)
                spur_node = prev_path[i]  # Вершина отклонения

                steps_log.append(f"Поиск ответвления от вершины {spur_node + 1}")
                steps_log.append(f"  Корень: {' → '.join([str(v + 1) for v in root])}")
                steps_log.append(f"  Вершина отклонения: {spur_node + 1}")

                # Исключаем вершины корня (кроме вершины отклонения)
                excluded_vertices = root[:-1]  # Все вершины корня кроме последней
                steps_log.append(f"  Исключаемые вершины: {[v + 1 for v in excluded_vertices]}")

                # Находим кратчайший путь от вершины отклонения до конечной
                spur_weight, spur_path = self.dijkstra.find_shortest_path(
                    spur_node, end, excluded_vertices
                )

                if spur_weight < self.GM and len(spur_path) > 0:
                    # Проверяем, что первый элемент spur_path - это spur_node
                    if spur_path[0] != spur_node:
                        spur_path.insert(0, spur_node)

                    # Строим полный путь: корень + ответвление (без дублирования spur_node)
                    total_path = root[:-1] + spur_path
                    total_weight = sum(self.W[total_path[p]][total_path[p + 1]]
                                       for p in range(len(total_path) - 1))

                    steps_log.append(f"  Найдено ответвление: {' → '.join([str(v + 1) for v in spur_path])}")
                    steps_log.append(f"  Вес ответвления: {spur_weight}")
                    steps_log.append(f"  Полный путь: {' → '.join([str(v + 1) for v in total_path])}")
                    steps_log.append(f"  Полный вес: {total_weight}")

                    # Проверяем уникальность пути
                    path_exists = False
                    for _, existing_path in A:
                        if total_path == existing_path:
                            path_exists = True
                            break
                    for _, candidate_path in B:
                        if total_path == candidate_path:
                            path_exists = True
                            break

                    if not path_exists:
                        steps_log.append(f"  Путь уникален - добавляем в кандидаты")
                        B.append((total_weight, total_path))

                        if total_weight < MinW:
                            MinW = total_weight
                            MinPath = total_path
                            steps_log.append(f"  Новый минимальный кандидат! MinW = {MinW}")
                    else:
                        steps_log.append(f"  Путь уже существует - пропускаем")
                else:
                    steps_log.append(f"  Ответвление не найдено (путь от {spur_node + 1} до {u2} не существует)")

            # Шаг 6: Выбираем лучший кандидат
            if B:
                # Находим путь с минимальным весом среди кандидатов
                B.sort(key=lambda x: x[0])
                best_weight, best_path = B.pop(0)

                steps_log.append(f"\nШАГ 6: Выбор лучшего кандидата")
                steps_log.append(f"  Выбран путь с весом {best_weight}")
                steps_log.append(f"  Путь: {' → '.join([str(v + 1) for v in best_path])}")

                # Добавляем в список найденных путей
                A.append((best_weight, best_path))
                paths_1based.append([v + 1 for v in best_path])
                weights.append(best_weight)
                lengths.append(len(best_path) - 1)

                steps_log.append(f"  Путь P{k} добавлен в результирующий список")
            else:
                steps_log.append(f"\nШАГ 6: Кандидатов больше нет")
                steps_log.append(f"  Всего найдено {len(A)} путей")
                break

        # Формируем массивы p и length как в задании
        p = paths_1based
        length = lengths + [-1] * (K - len(lengths))

        steps_log.append(f"\n" + "=" * 60)
        steps_log.append(f"АЛГОРИТМ ЙЕНА ЗАВЕРШЕН")
        steps_log.append(f"Найдено путей: {len(A)} из {K} запрошенных")

        return p, weights, steps_log


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
        header.setSectionResizeMode(QHeaderView.Stretch)

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

        # Оптимизируем размеры колонок
        for i in range(n):
            self.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)
            self.verticalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)


class GraphCanvas(FigureCanvas):
    """Холст для отрисовки взвешенных графов с выделением путей в темной теме"""

    def __init__(self, parent=None, width=5, height=5, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor='#1a1b26')
        self.ax = self.fig.add_subplot(111, facecolor='#1a1b26')
        super().__init__(self.fig)
        self.setParent(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Настраиваем темную тему для холста
        self.setStyleSheet("background-color: #1a1b26; border: 1px solid #3b4261;")

    def draw_weighted_graph_with_paths(self, G, pos=None, paths=None,
                                       start_vertex=None, end_vertex=None,
                                       title="", weight_matrix=None, GM=float('inf'),
                                       current_path_index=0):
        """Отрисовка взвешенного графа с выделением K путей в темной теме"""
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
            if len(G.nodes()) <= 10:
                pos = nx.spring_layout(G, seed=42, k=1.5, iterations=100)
            else:
                pos = nx.circular_layout(G)

        # Определяем цвета вершин в темной теме
        node_colors = []
        node_sizes = []

        for node in G.nodes():
            if node + 1 == start_vertex:
                node_colors.append('#f7768e')  # Красный - начальная
                node_sizes.append(700)
            elif node + 1 == end_vertex:
                node_colors.append('#9ece6a')  # Зеленый - конечная
                node_sizes.append(700)
            else:
                node_colors.append('#24283b')  # Темный - остальные
                node_sizes.append(500)

        # Рисуем все вершины
        nx.draw_networkx_nodes(G, pos, ax=self.ax,
                               node_color=node_colors,
                               node_size=node_sizes,
                               edgecolors='#c0caf5',  # Светлая обводка
                               linewidths=2)

        # Рисуем все ребра в темной теме с весами
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
                               alpha=0.3)

        # Рисуем подписи весов ребер (только если не слишком много)
        if len(G.edges()) <= 20:
            nx.draw_networkx_edge_labels(G, pos, ax=self.ax,
                                         edge_labels=edge_labels,
                                         font_size=8,
                                         font_color='#c0caf5',  # Светлый текст
                                         bbox=dict(facecolor='#1a1b26', edgecolor='#3b4261', alpha=0.9))

        # Рисуем пути разными цветами
        if paths and len(paths) > 0:
            colors = ['#ff9e64', '#7aa2f7', '#bb9af7', '#9ece6a', '#e0af68',
                      '#f7768e', '#2ac3de', '#c0caf5', '#1abc9c', '#8e44ad']

            for idx, path in enumerate(paths):
                if idx >= len(colors):
                    color = colors[-1]
                else:
                    color = colors[idx]

                # Преобразуем путь в 0-based индексы
                path_0based = [v - 1 for v in path]

                # Рисуем ребра пути
                path_edges = []
                for i in range(len(path_0based) - 1):
                    u = path_0based[i]
                    v = path_0based[i + 1]
                    if G.has_edge(u, v):
                        path_edges.append((u, v))

                if path_edges:
                    # Увеличиваем ширину для текущего выбранного пути
                    width = 4 if idx == current_path_index else 2
                    alpha = 0.9 if idx == current_path_index else 0.6

                    nx.draw_networkx_edges(G, pos, ax=self.ax,
                                           edgelist=path_edges,
                                           edge_color=color,
                                           width=width,
                                           alpha=alpha,
                                           style='solid')

        # Рисуем метки вершин
        labels = {node: str(node + 1) for node in G.nodes()}
        nx.draw_networkx_labels(G, pos, ax=self.ax,
                                labels=labels,
                                font_size=9,
                                font_weight='bold',
                                font_color='#c0caf5')  # Светлый текст

        # Настраиваем заголовок
        self.ax.set_title(title, fontsize=11, fontweight='bold', pad=15, color='#7aa2f7')
        
        # Отключаем оси
        self.ax.axis('off')
        
        # Настраиваем границы
        for spine in self.ax.spines.values():
            spine.set_edgecolor('#3b4261')
            
        self.fig.tight_layout()
        self.draw()


class GraphOperations:
    """Класс для операций с взвешенными графами для алгоритма Йена"""

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

    def find_k_shortest_paths(self, u1, u2, K):
        """Нахождение K кратчайших путей алгоритмом Йена"""
        if self.weight_matrix is None:
            return [], [], []

        yen = YenAlgorithm(self.weight_matrix, self.GM)
        paths, weights, steps_log = yen.find_k_shortest_paths(u1, u2, K)

        return paths, weights, steps_log


class YenAlgorithmApp(QMainWindow):
    """Главное окно приложения с темной темой и оптимизированными размерами"""

    def __init__(self):
        super().__init__()
        self.graph_ops = None
        self.current_paths = []
        self.current_weights = []
        self.current_path_index = 0
        self.init_ui()
        self.generate_graph()

    def init_ui(self):
        """Инициализация интерфейса с темной темой"""
        self.setWindowTitle("Алгоритм Йена для поиска K кратчайших путей")
        self.setGeometry(50, 50, 1400, 800)  # Уменьшили размер окна

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
                font-size: 11px;
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
                padding: 6px 12px;
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
                font-size: 11px;
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
            }
            QSplitter::handle:hover {
                background-color: #9ece6a;
            }
        """)

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(3)
        main_layout.setContentsMargins(3, 3, 3, 3)

        # Заголовок
        title = QLabel("АЛГОРИТМ ЙЕНА - K КРАТЧАЙШИХ ПУТЕЙ")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 14, QFont.Bold))
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

        # Панель управления
        control_group = QGroupBox("УПРАВЛЕНИЕ ГРАФОМ И ПАРАМЕТРАМИ АЛГОРИТМА")
        control_group.setFont(QFont("Arial", 9, QFont.Bold))
        control_layout = QGridLayout(control_group)
        control_layout.setSpacing(6)
        control_layout.setContentsMargins(8, 8, 8, 8)

        # Первая строка
        # Количество вершин
        control_layout.addWidget(QLabel("Вершины (n > 3):"), 0, 0)
        self.n_spinbox = QSpinBox()
        self.n_spinbox.setRange(4, 12)  # Уменьшили максимальное количество
        self.n_spinbox.setValue(8)
        self.n_spinbox.setFixedWidth(70)
        control_layout.addWidget(self.n_spinbox, 0, 1)

        # Плотность графа
        control_layout.addWidget(QLabel("Плотность:"), 0, 2)
        self.density_slider = QSlider(Qt.Horizontal)
        self.density_slider.setRange(10, 60)
        self.density_slider.setValue(30)
        self.density_slider.setFixedWidth(80)
        control_layout.addWidget(self.density_slider, 0, 3)
        self.density_label = QLabel("0.3")
        self.density_label.setFixedWidth(35)
        control_layout.addWidget(self.density_label, 0, 4)
        self.density_slider.valueChanged.connect(self.update_density_label)

        # Максимальный вес ребра
        control_layout.addWidget(QLabel("Макс. вес:"), 0, 5)
        self.max_weight_spinbox = QSpinBox()
        self.max_weight_spinbox.setRange(1, 20)
        self.max_weight_spinbox.setValue(10)
        self.max_weight_spinbox.setFixedWidth(70)
        control_layout.addWidget(self.max_weight_spinbox, 0, 6)

        # Значение GM
        control_layout.addWidget(QLabel("GM:"), 0, 7)
        self.gm_spinbox = QDoubleSpinBox()
        self.gm_spinbox.setRange(100, 5000)
        self.gm_spinbox.setValue(1000)
        self.gm_spinbox.setSingleStep(100)
        self.gm_spinbox.setDecimals(0)
        self.gm_spinbox.setFixedWidth(80)
        control_layout.addWidget(self.gm_spinbox, 0, 8)

        # Вторая строка
        # Начальная вершина
        control_layout.addWidget(QLabel("Начальная (u1):"), 1, 0)
        self.start_spinbox = QSpinBox()
        self.start_spinbox.setRange(1, 12)
        self.start_spinbox.setValue(1)
        self.start_spinbox.setFixedWidth(70)
        control_layout.addWidget(self.start_spinbox, 1, 1)

        # Конечная вершина
        control_layout.addWidget(QLabel("Конечная (u2):"), 1, 2)
        self.end_spinbox = QSpinBox()
        self.end_spinbox.setRange(1, 12)
        self.end_spinbox.setValue(5)
        self.end_spinbox.setFixedWidth(70)
        control_layout.addWidget(self.end_spinbox, 1, 3)

        # Количество путей K
        control_layout.addWidget(QLabel("Путей (K):"), 1, 4)
        self.k_spinbox = QSpinBox()
        self.k_spinbox.setRange(1, 8)  # Уменьшили максимальное количество
        self.k_spinbox.setValue(3)
        self.k_spinbox.setFixedWidth(70)
        control_layout.addWidget(self.k_spinbox, 1, 5)

        # Кнопка генерации
        self.generate_btn = QPushButton("СГЕНЕРИРОВАТЬ ГРАФ")
        self.generate_btn.setFixedWidth(140)
        self.generate_btn.clicked.connect(self.generate_graph)
        control_layout.addWidget(self.generate_btn, 0, 9)

        # Кнопка поиска путей
        self.find_paths_btn = QPushButton("НАЙТИ K ПУТЕЙ")
        self.find_paths_btn.setFixedWidth(140)
        self.find_paths_btn.clicked.connect(self.find_k_shortest_paths)
        control_layout.addWidget(self.find_paths_btn, 1, 9)

        main_layout.addWidget(control_group)

        # Основной сплиттер
        main_splitter = QSplitter(Qt.Horizontal)
        main_splitter.setHandleWidth(2)
        main_splitter.setStyleSheet("QSplitter::handle { background-color: #7aa2f7; }")

        # Левая часть - матрицы и информация
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(1, 1, 1, 1)

        # Вкладки для левой части
        self.left_tabs = QTabWidget()
        self.left_tabs.setFont(QFont("Arial", 9, QFont.Bold))
        self.left_tabs.setMaximumWidth(500)  # Ограничиваем ширину

        # Создаем вкладки левой части
        self.create_left_tabs()

        left_layout.addWidget(self.left_tabs)
        main_splitter.addWidget(left_widget)

        # Правая часть - визуализация и журнал
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

        # Устанавливаем начальные размеры (левая часть уже, правая шире)
        main_splitter.setSizes([400, 1000])
        main_layout.addWidget(main_splitter, 1)

        # Статусная строка
        self.status_label = QLabel("Готов к работе. Сгенерируйте граф и найдите K кратчайших путей.")
        self.status_label.setFont(QFont("Arial", 9))
        self.status_label.setStyleSheet("color: #c0caf5; padding: 4px; background-color: #24283b; border-radius: 3px;")
        main_layout.addWidget(self.status_label)

    def create_left_tabs(self):
        """Создание вкладок левой части"""
        # Вкладка с весовой матрицей
        self.weight_table = MatrixTableWidget()

        weight_container = QWidget()
        weight_layout = QVBoxLayout(weight_container)
        weight_layout.setContentsMargins(0, 0, 0, 0)

        weight_label = QLabel("ВЕСОВАЯ МАТРИЦА W")
        weight_label.setFont(QFont("Arial", 10, QFont.Bold))
        weight_label.setStyleSheet("color: #7aa2f7; padding: 5px;")
        weight_label.setAlignment(Qt.AlignCenter)
        weight_layout.addWidget(weight_label)

        weight_hint = QLabel("Цветовая кодировка: зеленый - веса, красный - ∞ (GM), темный - диагональ")
        weight_hint.setFont(QFont("Arial", 8))
        weight_hint.setStyleSheet("color: #a9b1d6; padding: 2px;")
        weight_hint.setAlignment(Qt.AlignCenter)
        weight_layout.addWidget(weight_hint)

        weight_layout.addWidget(self.weight_table)

        scroll_weight = QScrollArea()
        scroll_weight.setWidget(weight_container)
        scroll_weight.setWidgetResizable(True)
        scroll_weight.setMaximumWidth(450)
        self.left_tabs.addTab(scroll_weight, "Матрица W")

        # Вкладка с информацией о графе
        info_container = QWidget()
        info_layout = QVBoxLayout(info_container)

        info_label = QLabel("ИНФОРМАЦИЯ О ГРАФЕ")
        info_label.setFont(QFont("Arial", 10, QFont.Bold))
        info_label.setStyleSheet("color: #7aa2f7; padding: 8px;")
        info_label.setAlignment(Qt.AlignCenter)
        info_layout.addWidget(info_label)

        self.graph_info_text = QTextEdit()
        self.graph_info_text.setFont(QFont("Courier New", 9))
        self.graph_info_text.setReadOnly(True)
        self.graph_info_text.setMaximumHeight(300)
        info_layout.addWidget(self.graph_info_text)

        self.left_tabs.addTab(info_container, "Свойства графа")

    def create_right_tabs(self):
        """Создание вкладок правой части"""
        # Вкладка с визуализацией графа
        self.graph_canvas = GraphCanvas(self, width=5, height=4.5)

        viz_container = QWidget()
        viz_layout = QVBoxLayout(viz_container)
        viz_layout.setContentsMargins(0, 0, 0, 0)

        viz_label = QLabel("ВИЗУАЛИЗАЦИЯ ГРАФА И K ПУТЕЙ")
        viz_label.setFont(QFont("Arial", 10, QFont.Bold))
        viz_label.setStyleSheet("color: #7aa2f7; padding: 5px;")
        viz_label.setAlignment(Qt.AlignCenter)
        viz_layout.addWidget(viz_label)

        # Легенда
        legend_widget = QWidget()
        legend_layout = QGridLayout(legend_widget)
        legend_layout.setHorizontalSpacing(8)
        legend_layout.setVerticalSpacing(4)

        legend_items = [
            ("Начальная", "#f7768e"),
            ("Конечная", "#9ece6a"),
            ("Текущий путь", "#ff9e64"),
            ("Другие пути", "#7aa2f7"),
            ("Обычные ребра", "#3b4261")
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

        log_label = QLabel("ЖУРНАЛ ВЫПОЛНЕНИЯ АЛГОРИТМА ЙЕНА")
        log_label.setFont(QFont("Arial", 10, QFont.Bold))
        log_label.setStyleSheet("color: #7aa2f7; padding: 8px;")
        log_label.setAlignment(Qt.AlignCenter)
        log_layout.addWidget(log_label)

        self.algorithm_log = QTextEdit()
        self.algorithm_log.setFont(QFont("Courier New", 9))
        self.algorithm_log.setReadOnly(True)
        log_layout.addWidget(self.algorithm_log)

        self.right_tabs.addTab(log_container, "Журнал алгоритма")

        # Вкладка со списком найденных путей и навигацией
        paths_container = QWidget()
        paths_layout = QVBoxLayout(paths_container)

        paths_label = QLabel("СПИСОК НАЙДЕННЫХ ПУТЕЙ")
        paths_label.setFont(QFont("Arial", 10, QFont.Bold))
        paths_label.setStyleSheet("color: #7aa2f7; padding: 8px;")
        paths_label.setAlignment(Qt.AlignCenter)
        paths_layout.addWidget(paths_label)

        # Панель навигации
        nav_widget = QWidget()
        nav_layout = QHBoxLayout(nav_widget)
        nav_layout.setSpacing(6)

        self.prev_path_btn = QPushButton("ПРЕДЫДУЩИЙ")
        self.prev_path_btn.setFixedWidth(100)
        self.prev_path_btn.clicked.connect(self.show_previous_path)
        nav_layout.addWidget(self.prev_path_btn)

        self.path_label = QLabel("Путь 1 из 0")
        self.path_label.setAlignment(Qt.AlignCenter)
        self.path_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.path_label.setStyleSheet("color: #ff9e64;")
        nav_layout.addWidget(self.path_label)

        self.next_path_btn = QPushButton("СЛЕДУЮЩИЙ")
        self.next_path_btn.setFixedWidth(100)
        self.next_path_btn.clicked.connect(self.show_next_path)
        nav_layout.addWidget(self.next_path_btn)

        paths_layout.addWidget(nav_widget)

        # Список путей
        self.paths_list = QListWidget()
        self.paths_list.setFont(QFont("Courier New", 9))
        self.paths_list.itemClicked.connect(self.on_path_selected)
        paths_layout.addWidget(self.paths_list)

        # Краткая информация о результатах
        self.results_summary = QTextEdit()
        self.results_summary.setFont(QFont("Courier New", 9))
        self.results_summary.setReadOnly(True)
        self.results_summary.setMaximumHeight(150)
        paths_layout.addWidget(self.results_summary)

        self.right_tabs.addTab(paths_container, "Список путей")

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

        text = "=" * 45 + "\n"
        text += "ХАРАКТЕРИСТИКИ ГРАФА\n"
        text += "=" * 45 + "\n\n"

        text += f"Количество вершин (n): {info['n']}\n"
        text += f"Количество ребер: {info['edges']}\n"
        text += f"Максимально возможное ребер: {info['total_possible_edges']}\n"
        text += f"Плотность графа: {info['density']:.3f}\n"
        text += f"Минимальный вес ребра: {info['min_weight']}\n"
        text += f"Максимальный вес ребра: {info['max_weight']}\n"
        text += f"GM (бесконечность): {self.graph_ops.GM}\n"
        text += f"Связность графа: {'ДА' if info['connected'] else 'НЕТ'}\n\n"

        text += "ИНФОРМАЦИЯ ОБ АЛГОРИТМЕ ЙЕНА:\n"
        text += "  • Находит K кратчайших путей между вершинами u1 и u2\n"
        text += "  • Пути не содержат петель (простые цепи)\n"
        text += "  • Использует алгоритм Дейкстры для поиска отклонений\n"
        text += "  • Исключает дублирующиеся пути через проверку подпутей\n"

        self.graph_info_text.setText(text)

    def clear_path_results(self):
        """Очистка результатов поиска путей"""
        self.algorithm_log.clear()
        self.paths_list.clear()
        self.results_summary.clear()
        self.current_paths = []
        self.current_weights = []
        self.current_path_index = 0
        self.update_navigation()

        # Очищаем визуализацию
        if self.graph_ops and self.graph_ops.G_nx:
            self.graph_canvas.draw_weighted_graph_with_paths(
                self.graph_ops.G_nx,
                weight_matrix=self.graph_ops.weight_matrix,
                GM=self.graph_ops.GM,
                title=f"Граф G ({self.graph_ops.n} вершин)"
            )

    def update_visualization(self, paths=None):
        """Обновление визуализации графа"""
        if self.graph_ops is None or self.graph_ops.G_nx is None:
            return

        u1 = self.start_spinbox.value()
        u2 = self.end_spinbox.value()

        if paths and len(paths) > 0:
            title = f"K кратчайших путей {u1} → {u2} ({len(paths)} найдено)"
        else:
            title = f"Граф G ({self.graph_ops.n} вершин)"

        self.graph_canvas.draw_weighted_graph_with_paths(
            self.graph_ops.G_nx,
            paths=paths,
            start_vertex=u1,
            end_vertex=u2,
            title=title,
            weight_matrix=self.graph_ops.weight_matrix,
            GM=self.graph_ops.GM,
            current_path_index=self.current_path_index
        )

    def find_k_shortest_paths(self):
        """Поиск K кратчайших путей алгоритмом Йена"""
        if self.graph_ops is None:
            QMessageBox.warning(self, "Предупреждение", "Сначала сгенерируйте граф!")
            return

        u1 = self.start_spinbox.value()
        u2 = self.end_spinbox.value()
        K = self.k_spinbox.value()

        if u1 < 1 or u1 > self.graph_ops.n or u2 < 1 or u2 > self.graph_ops.n:
            QMessageBox.warning(self, "Ошибка", "Номера вершин должны быть в диапазоне от 1 до n")
            return

        try:
            # Выполнение алгоритма Йена
            paths, weights, steps_log = self.graph_ops.find_k_shortest_paths(u1, u2, K)

            # Сохраняем результаты
            self.current_paths = paths
            self.current_weights = weights
            self.current_path_index = 0

            # Отображение результатов
            self.display_results(paths, weights, steps_log)

            # Обновление визуализации
            self.update_visualization(paths)

            # Обновление списка путей
            self.update_paths_list()

            # Отображение журнала выполнения
            log_text = "\n".join(steps_log)
            self.algorithm_log.setText(log_text)

            # Прокрутка журнала вверх
            self.algorithm_log.verticalScrollBar().setValue(0)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при поиске путей: {str(e)}")

    def display_results(self, paths, weights, steps_log):
        """Отображение результатов поиска путей"""
        u1 = self.start_spinbox.value()
        u2 = self.end_spinbox.value()
        K = self.k_spinbox.value()

        # Обновляем сводку результатов
        summary_text = "=" * 45 + "\n"
        summary_text += "РЕЗУЛЬТАТЫ АЛГОРИТМА ЙЕНА\n"
        summary_text += "=" * 45 + "\n\n"

        summary_text += f"Начальная вершина (u1): {u1}\n"
        summary_text += f"Конечная вершина (u2): {u2}\n"
        summary_text += f"Запрошено путей (K): {K}\n"
        summary_text += f"Найдено путей: {len(paths)}\n\n"

        if len(paths) == 0:
            summary_text += "ПУТЕЙ НЕ НАЙДЕНО\n"
            summary_text += f"Не существует пути от {u1} до {u2}\n"
            self.status_label.setText(f"Путь от {u1} до {u2} не существует")
        else:
            summary_text += "НАЙДЕННЫЕ ПУТИ (отсортированы по возрастанию веса):\n"
            summary_text += "-" * 45 + "\n"

            for i, (path, weight) in enumerate(zip(paths, weights)):
                summary_text += f"Путь P{i + 1}:\n"
                summary_text += f"  Вес: {weight}\n"
                summary_text += f"  Длина (ребер): {len(path) - 1}\n"
                summary_text += f"  Маршрут: {' → '.join(map(str, path))}\n\n"

            summary_text += f"Самый короткий путь: P1 (вес: {weights[0]})\n"
            self.status_label.setText(f"Найдено {len(paths)} путей от {u1} до {u2}")

        self.results_summary.setText(summary_text)

    def update_paths_list(self):
        """Обновление списка путей"""
        self.paths_list.clear()

        for i, (path, weight) in enumerate(zip(self.current_paths, self.current_weights)):
            item_text = f"Путь {i + 1}: {' → '.join(map(str, path))} (вес: {weight})"
            item = QListWidgetItem(item_text)

            # Цветовое кодирование
            if i == 0:
                item.setForeground(QBrush(QColor("#9ece6a")))  # Зеленый для первого
            elif i == self.current_path_index:
                item.setForeground(QBrush(QColor("#ff9e64")))  # Оранжевый для текущего
            else:
                item.setForeground(QBrush(QColor("#7aa2f7")))  # Синий для остальных

            self.paths_list.addItem(item)

    def update_navigation(self):
        """Обновление навигации по путям"""
        total_paths = len(self.current_paths)
        if total_paths > 0:
            self.path_label.setText(f"Путь {self.current_path_index + 1} из {total_paths}")
            self.prev_path_btn.setEnabled(self.current_path_index > 0)
            self.next_path_btn.setEnabled(self.current_path_index < total_paths - 1)
        else:
            self.path_label.setText("Путей не найдено")
            self.prev_path_btn.setEnabled(False)
            self.next_path_btn.setEnabled(False)

    def show_previous_path(self):
        """Показать предыдущий путь"""
        if self.current_path_index > 0:
            self.current_path_index -= 1
            self.update_navigation()
            self.update_visualization(self.current_paths)
            self.update_paths_list()

    def show_next_path(self):
        """Показать следующий путь"""
        if self.current_path_index < len(self.current_paths) - 1:
            self.current_path_index += 1
            self.update_navigation()
            self.update_visualization(self.current_paths)
            self.update_paths_list()

    def on_path_selected(self, item):
        """Обработчик выбора пути из списка"""
        index = self.paths_list.row(item)
        if 0 <= index < len(self.current_paths):
            self.current_path_index = index
            self.update_navigation()
            self.update_visualization(self.current_paths)


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
    
    window = YenAlgorithmApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()