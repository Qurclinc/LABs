import sys
import random
import numpy as np
import networkx as nx
from collections import deque
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit,
                             QVBoxLayout, QHBoxLayout, QMessageBox)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

# --- Hello Kitty Style ---
def set_hello_kitty_style(widget):
    widget.setStyleSheet("""
        QWidget {
            background-color: #ffe4e6;
            color: #ff69b4;
            font-family: 'Comic Sans MS', cursive, sans-serif;
            font-size: 14px;
        }
        QTextEdit {
            background-color: #fff0f5;
            color: #ff1493;
            border: 2px solid #ffb6c1;
            border-radius: 8px;
        }
        QLineEdit {
            background-color: #fff0f5;
            color: #ff1493;
            border: 2px solid #ffb6c1;
            border-radius: 8px;
            padding: 4px;
        }
        QPushButton {
            background-color: #ffb6c1;
            color: #fff;
            font-weight: bold;
            border-radius: 12px;
            padding: 8px;
        }
        QPushButton:hover {
            background-color: #ff69b4;
        }
        QLabel {
            font-weight: bold;
        }
    """)

class GraphAnalyzer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hello Kitty Graph Analyzer")
        self.setGeometry(100, 50, 1400, 900)
        set_hello_kitty_style(self)

        self.n = 9
        self.adj_matrix = None
        self.inc_matrix = None
        self.G = None

        self.init_ui()

        # Загружаем картинку кошки
        self.cat_img = plt.imread("cat_face.png")  # <- положи PNG с мордочкой котика в ту же папку

    def init_ui(self):
        main_layout = QHBoxLayout(self)

        # --- Левый блок ---
        left_frame = QVBoxLayout()
        main_layout.addLayout(left_frame, 2)

        # Параметры
        param_layout = QHBoxLayout()
        lbl_n = QLabel("Порядок графа (n > 8):")
        self.input_n = QLineEdit("9")
        param_layout.addWidget(lbl_n)
        param_layout.addWidget(self.input_n)

        self.btn_generate = QPushButton("Сгенерировать и проанализировать")
        self.btn_generate.clicked.connect(self.generate_and_analyze)

        left_frame.addLayout(param_layout)
        left_frame.addWidget(self.btn_generate)

        # Матрица смежности
        lbl_adj = QLabel("Матрица смежности")
        lbl_adj.setAlignment(Qt.AlignCenter)
        self.adj_text = QTextEdit()
        self.adj_text.setReadOnly(True)
        left_frame.addWidget(lbl_adj)
        left_frame.addWidget(self.adj_text)

        # Матрица инцидентности
        lbl_inc = QLabel("Матрица инцидентности")
        lbl_inc.setAlignment(Qt.AlignCenter)
        self.inc_text = QTextEdit()
        self.inc_text.setReadOnly(True)
        left_frame.addWidget(lbl_inc)
        left_frame.addWidget(self.inc_text)

        # Результаты анализа
        lbl_res = QLabel("Результаты анализа")
        lbl_res.setAlignment(Qt.AlignCenter)
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        left_frame.addWidget(lbl_res)
        left_frame.addWidget(self.results_text)

        # --- Правый блок: граф ---
        right_frame = QVBoxLayout()
        main_layout.addLayout(right_frame, 3)

        lbl_graph = QLabel("Визуализация графа")
        lbl_graph.setAlignment(Qt.AlignCenter)
        right_frame.addWidget(lbl_graph)

        self.fig, self.ax = plt.subplots(figsize=(8, 7))
        self.canvas = FigureCanvas(self.fig)
        right_frame.addWidget(self.canvas)

    # ---------------- Генерация ----------------
    def generate_and_analyze(self):
        try:
            n = int(self.input_n.text())
            if n <= 8:
                QMessageBox.critical(self, "Ошибка", "Порядок графа должен быть > 8")
                return
            self.n = n

            self.adj_matrix = self.generate_adjacency_matrix(n)
            self.inc_matrix = self.adjacency_to_incidence(self.adj_matrix)
            self.G = nx.Graph()
            self.G.add_nodes_from(range(1, n+1))
            for i in range(n):
                for j in range(i+1, n):
                    if self.adj_matrix[i][j] == 1:
                        self.G.add_edge(i+1, j+1)

            self.display_matrices()
            self.draw_graph()
            self.analyze_graph()
        except ValueError:
            QMessageBox.critical(self, "Ошибка", "Введите корректное значение")

    def generate_adjacency_matrix(self, n):
        adj = np.zeros((n, n), dtype=int)
        for i in range(1, n):
            j = random.randint(0, i-1)
            adj[i][j] = adj[j][i] = 1
        for _ in range(n):
            i, j = random.sample(range(n), 2)
            adj[i][j] = adj[j][i] = 1
        return adj

    def adjacency_to_incidence(self, adj):
        n = len(adj)
        edges = [(i, j) for i in range(n) for j in range(i+1, n) if adj[i][j] == 1]
        inc = np.zeros((n, len(edges)), dtype=int)
        for idx, (i, j) in enumerate(edges):
            inc[i][idx] = inc[j][idx] = 1
        return inc

    # ---------------- Матрицы ----------------
    def display_matrices(self):
        header = "   " + " ".join(f"{i+1:2}" for i in range(self.n)) + "\n"
        adj_text = header
        for i, row in enumerate(self.adj_matrix):
            row_str = f"{i+1:2} " + " ".join(f"{x:2}" for x in row) + "\n"
            adj_text += row_str
        self.adj_text.setPlainText(adj_text)

        if len(self.inc_matrix[0]) > 0:
            header = "   " + " ".join(f"{i+1:2}" for i in range(len(self.inc_matrix[0]))) + "\n"
        else:
            header = ""
        inc_text = header
        for i, row in enumerate(self.inc_matrix):
            row_str = f"{i+1:2} " + " ".join(f"{x:2}" for x in row) + "\n"
            inc_text += row_str
        self.inc_text.setPlainText(inc_text)

    # ---------------- Визуализация ----------------
    def draw_graph(self):
        self.ax.clear()
        if self.G:
            pos = nx.spring_layout(self.G, seed=42)

            # Рисуем ребра
            nx.draw_networkx_edges(self.G, pos, ax=self.ax, edge_color='#ff69b4', width=2)

            # Рисуем вершины как мордочки котиков
            for node in self.G.nodes():
                x, y = pos[node]
                im = OffsetImage(self.cat_img, zoom=0.08)
                ab = AnnotationBbox(im, (x, y), frameon=False)
                self.ax.add_artist(ab)

            # Подписи
            for node, (x, y) in pos.items():
                self.ax.text(x, y-0.05, str(node), ha='center', va='top', color='#ff1493', fontweight='bold', fontsize=12)

            self.ax.set_facecolor('#ffe4e6')
            self.ax.set_xticks([])
            self.ax.set_yticks([])
            self.ax.set_title(f"Граф порядка {self.n}", fontsize=16, fontweight='bold', color='#ff1493')
            self.canvas.draw()

    # ---------------- Анализ ----------------
    def find_shortest_paths(self, adj_matrix):
        n = len(adj_matrix)
        distances = np.full((n, n), -1, dtype=int)
        for start in range(n):
            dist = [-1]*n
            dist[start] = 0
            queue = deque([start])
            while queue:
                current = queue.popleft()
                for neighbor in range(n):
                    if adj_matrix[current][neighbor] == 1 and dist[neighbor] == -1:
                        dist[neighbor] = dist[current] + 1
                        queue.append(neighbor)
            distances[start] = dist
        return distances

    def calculate_diameter_radius(self, distances):
        n = len(distances)
        eccentricities = []
        for i in range(n):
            max_dist = max(distances[i])
            if max_dist == -1:
                return None, None, None, None
            eccentricities.append(max_dist)
        diameter = max(eccentricities)
        radius = min(eccentricities)
        central = [i+1 for i, ecc in enumerate(eccentricities) if ecc == radius]
        peripheral = [i+1 for i, ecc in enumerate(eccentricities) if ecc == diameter]
        return diameter, radius, central, peripheral

    def analyze_graph(self):
        if not self.G:
            return

        distances = self.find_shortest_paths(self.adj_matrix)
        diameter, radius, central, peripheral = self.calculate_diameter_radius(distances)
        result = ""

        if diameter is None:
            result += "Граф не связный!\nРадиус и диаметр не вычисляются.\n\n"
        else:
            result += f"Диаметр графа: {diameter}\n"
            result += f"Радиус графа: {radius}\n"
            result += f"Центральные вершины: {central}\n"
            result += f"Периферийные вершины: {peripheral}\n\n"

        degrees = dict(self.G.degree())
        result += "Степени вершин:\n"
        for v, d in degrees.items():
            result += f"Вершина {v}: степень {d}\n"

        result += f"\nИзолированные вершины: {[v for v, d in degrees.items() if d == 0]}\n"
        result += f"Концевые вершины: {[v for v, d in degrees.items() if d == 1]}\n"
        result += f"Доминирующие вершины: {[v for v, d in degrees.items() if d == len(self.G.nodes()) - 1]}\n"

        self.results_text.setPlainText(result)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GraphAnalyzer()
    window.show()
    sys.exit(app.exec_())
