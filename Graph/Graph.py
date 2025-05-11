import tkinter as tk
from tkinter import messagebox
from collections import defaultdict
import numpy

class MaxFlow:
    def __init__(self, vertices):
        self.V = vertices  # Количество вершин
        self.graph = defaultdict(lambda: defaultdict(int))  # Граф

    def add_edge(self, u, v, capacity):
        self.graph[u][v] += capacity  # Добавляем ребро с заданной пропускной способностью

    def bfs(self, source, sink, parent):
        visited = set()
        queue = [source]
        visited.add(source)

        while queue:
            u = queue.pop(0)

            for v in self.graph[u]:
                if v not in visited and self.graph[u][v] > 0:  # Если не посещена и есть доступная пропускная способность
                    visited.add(v)
                    parent[v] = u
                    if v == sink:
                        return True
                    queue.append(v)
        return False

    def ford_fulkerson(self, source, sink):
        parent = {}
        max_flow = 0

        while self.bfs(source, sink, parent):
            path_flow = float('Inf')
            s = sink

            while s != source:
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]

            # Обновляем остаточные пропускные способности рёбер
            v = sink
            while v != source:
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]

            max_flow += path_flow

        return max_flow

def draw_graph(edges, num_vertices):
    canvas.delete("all")  # Очистка холста
    node_positions = {}  # Словарь для хранения позиций вершин
    node_radius = 15  # Радиус вершины

    # Определяем позиции для вершин
    for i in range(num_vertices):
        angle = i * (360 / num_vertices)
        x = 200 + 100 * numpy.cos(numpy.radians(angle))
        y = 200 + 100 * numpy.sin(numpy.radians(angle))
        node_positions[i] = (x, y)
        canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius, fill="lightblue")
        canvas.create_text(x, y, text=str(i + 1))  # Вершины начинаются с 1

    # Рисуем рёбра
    for edge in edges:
        u, v, capacity = edge
        x1, y1 = node_positions[u - 1]
        x2, y2 = node_positions[v - 1]

        # Вычисляем направление вектора
        dx = x2 - x1
        dy = y2 - y1
        length = (dx**2 + dy**2)**0.5

        # Нормализуем вектор и добавляем смещение
        if length > 0:
            dx /= length
            dy /= length

        # Смещаем координаты конца стрелок
        x1_end = x1 + dx * node_radius
        y1_end = y1 + dy * node_radius
        x2_end = x2 - dx * node_radius
        y2_end = y2 - dy * node_radius

        # Рисуем линию с стрелкой
        canvas.create_line(x1_end, y1_end, x2_end, y2_end, arrow=tk.LAST)
        mid_x = (x1_end + x2_end) / 2
        mid_y = (y1_end + y2_end) / 2
        canvas.create_text(mid_x, mid_y, text=str(capacity))

def calculate_max_flow():
    try:
        num_vertices = int(vertex_entry.get())
        edges = edge_entry.get("1.0", "end").strip().splitlines()
        edge_list = []

        max_flow_calculator = MaxFlow(num_vertices)

        for edge in edges:
            u, v, capacity = map(int, edge.split())
            max_flow_calculator.add_edge(u - 1, v - 1, capacity)  # Преобразуем в 0-индексацию
            edge_list.append((u, v, capacity))

        source = 0  # Исток (вершина 1)
        sink = num_vertices - 1  # Сток (последняя вершина)
        max_flow = max_flow_calculator.ford_fulkerson(source, sink)

        messagebox.showinfo("Результат", f"Максимальный поток равен: {max_flow}")
        draw_graph(edge_list, num_vertices)  # Передаем количество вершин в draw_graph
    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректные числа!")
    except IndexError:
        messagebox.showerror("Ошибка", "Проверьте вводимые данные о рёбрах!")

# Создание основного окна
root = tk.Tk()
root.title("Максимальный поток")

# Поля для ввода
tk.Label(root, text="Количество вершин:").pack()
vertex_entry = tk.Entry(root)
vertex_entry.pack()

tk.Label(root, text="Рёбра (формат: u v capacity, каждое в новой строке):").pack()
edge_entry = tk.Text(root, height=10, width=50)
edge_entry.pack()

# Кнопка для запуска расчёта
calculate_button = tk.Button(root, text="Рассчитать максимальный поток", command=calculate_max_flow)
calculate_button.pack()

# Создание холста для рисования графа
canvas = tk.Canvas(root, width=400, height=400, bg='white')
canvas.pack()

# Запуск основного цикла
root.mainloop()
