import sys
import random
import numpy as np
import networkx as nx
from collections import deque
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit,
                             QVBoxLayout, QHBoxLayout, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

# --- Tokyo Night Style ---
def set_tokyo_style(widget):
    widget.setStyleSheet("""
        QWidget {
            background-color: #1a1b26;
            color: #c0caf5;
            font-family: 'JetBrains Mono', monospace;
            font-size: 14px;
        }
        QTextEdit {
            background-color: #16161e;
            color: #c0caf5;
            border: 1px solid #414868;
        }
        QLineEdit {
            background-color: #16161e;
            color: #c0caf5;
            border: 1px solid #414868;
            padding: 4px;
        }
        QPushButton {
            background-color: #7aa2f7;
            color: #1a1b26;
            font-weight: bold;
            border-radius: 6px;
            padding: 6px;
        }
        QPushButton:hover {
            background-color: #bb9af7;
        }
        QLabel {
            font-weight: bold;
        }
    """)

class GraphAnalyzer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Анализатор графов")
        self.setGeometry(100, 50, 1400, 900)
        set_tokyo_style(self)

        self.n = 9
        self.adj_matrix = None
        self.inc_matrix = None
        self.G = None

        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self)

        # --- Левый блок: граф ---
        left_frame = QVBoxLayout()
        main_layout.addLayout(left_frame, 3)

        lbl_graph = QLabel("Визуализация графа")
        lbl_graph.setAlignment(Qt.AlignCenter)
        left_frame.addWidget(lbl_graph)

        self.fig, self.ax = plt.subplots(figsize=(8, 7))
        self.canvas = FigureCanvas(self.fig)
        left_frame.addWidget(self.canvas)

        # Сделать Canvas тёмным
        self.fig.patch.set_facecolor('#1a1b26')
        self.ax.set_facecolor('#1a1b26')
        self.ax.axis('off')

        # --- Правый блок: вход и результаты ---
        right_frame = QVBoxLayout()
        main_layout.addLayout(right_frame, 2)

        # Параметры
        param_layout = QHBoxLayout()
        lbl_n = QLabel("Порядок графа (n > 8):")
        self.input_n = QLineEdit("9")
        param_layout.addWidget(lbl_n)
        param_layout.addWidget(self.input_n)

        self.btn_generate = QPushButton("Сгенерировать и проанализировать")
        self.btn_generate.clicked.connect(self.generate_and_analyze)

        right_frame.addLayout(param_layout)
        right_frame.addWidget(self.btn_generate)

        # Матрица смежности
        lbl_adj = QLabel("Матрица смежности")
        lbl_adj.setAlignment(Qt.AlignCenter)
        self.adj_text = QTextEdit()
        self.adj_text.setReadOnly(True)
        right_frame.addWidget(lbl_adj)
        right_frame.addWidget(self.adj_text)

        # Матрица инцидентности
        lbl_inc = QLabel("Матрица инцидентности")
        lbl_inc.setAlignment(Qt.AlignCenter)
        self.inc_text = QTextEdit()
        self.inc_text.setReadOnly(True)
        right_frame.addWidget(lbl_inc)
        right_frame.addWidget(self.inc_text)

        # Результаты анализа
        lbl_res = QLabel("Результаты анализа")
        lbl_res.setAlignment(Qt.AlignCenter)
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        right_frame.addWidget(lbl_res)
        right_frame.addWidget(self.results_text)

    # ---------------- Генерация графа ----------------
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
        self.fig.patch.set_facecolor('#1a1b26')
        self.ax.set_facecolor('#1a1b26')
        self.ax.axis('off')

        if self.G:
            pos = nx.spring_layout(self.G, seed=42)
            nx.draw_networkx_nodes(self.G, pos, ax=self.ax, node_color='#7aa2f7', node_size=800)
            nx.draw_networkx_edges(self.G, pos, ax=self.ax, edge_color='#414868', width=2)
            nx.draw_networkx_labels(self.G, pos, ax=self.ax, font_color='#c0caf5', font_size=14, font_weight='bold')

            self.ax.set_title(f"Граф порядка {self.n}", fontsize=16, fontweight='bold', color='#c0caf5')
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
