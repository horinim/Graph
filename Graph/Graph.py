import tkinter as tk
from tkinter import messagebox
from collections import defaultdict
import numpy
import random


#Основное окно программы
def main_window():
    hello.destroy()

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
                    if v not in visited and self.graph[u][
                        v] > 0:
                        visited.add(v)
                        parent[v] = u
                        if v == sink:
                            return True
                        queue.append(v)
            return False
#Алгоритм Форда-Фалкерсона
        def ford_fulkerson(self, source, sink):
            parent = {}
            max_flow = 0
            max_flow_path = []

            while self.bfs(source, sink, parent):
                path_flow = float('Inf')
                s = sink


                current_path = []

                while s != source:
                    current_path.append((parent[s], s))
                    path_flow = min(path_flow, self.graph[parent[s]][s])
                    s = parent[s]


                v = sink
                while v != source:
                    u = parent[v]
                    self.graph[u][v] -= path_flow
                    self.graph[v][u] += path_flow
                    v = parent[v]

                max_flow += path_flow
                max_flow_path = current_path

            return max_flow, max_flow_path
#Визуализация графа
    def draw_graph(edges, num_vertices, max_flow_path=None):
        canvas.delete("all")
        node_positions = {}
        node_radius = 15
        offset_range = 35


        for i in range(num_vertices):
            angle = i * (360 / num_vertices)
            x = 200 + 100 * numpy.cos(numpy.radians(angle)) + random.uniform(-offset_range, offset_range)
            y = 200 + 100 * numpy.sin(numpy.radians(angle)) + random.uniform(-offset_range, offset_range)
            node_positions[i] = (x, y)
            canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius, fill="lightblue")
            canvas.create_text(x, y, text=str(i + 1))

        # Рисуем рёбра
        for edge in edges:
            u, v, capacity = edge
            x1, y1 = node_positions[u - 1]
            x2, y2 = node_positions[v - 1]

            dx = x2 - x1
            dy = y2 - y1
            length = (dx ** 2 + dy ** 2) ** 0.5

            if length > 0:
                dx /= length
                dy /= length


            x1_end = x1 + dx * node_radius
            y1_end = y1 + dy * node_radius
            x2_end = x2 - dx * node_radius
            y2_end = y2 - dy * node_radius


            if max_flow_path and (u - 1, v - 1) in max_flow_path:
                color = "red"
            else:
                color = "black"

            canvas.create_line(x1_end, y1_end, x2_end, y2_end, arrow=tk.LAST, fill=color)
            mid_x = (x1_end + x2_end) / 2
            mid_y = (y1_end + y2_end) / 2

            text_offset = 10
            angle = numpy.arctan2(dy, dx)

            if angle < numpy.pi / 2 and angle > -numpy.pi / 2:
                mid_y -= text_offset
            else:
                mid_y += text_offset

            canvas.create_text(mid_x, mid_y, text=str(capacity))
#Расчет максимального потока
    def calculate_max_flow():
        try:
            num_vertices = int(vertex_entry.get())
            edges = edge_entry.get("1.0", "end").strip().splitlines()
            edge_list = []

            max_flow_calculator = MaxFlow(num_vertices)

            for edge in edges:
                u, v, capacity = map(int, edge.split())
                max_flow_calculator.add_edge(u - 1, v - 1, capacity)
                edge_list.append((u, v, capacity))

            source = 0
            sink = num_vertices - 1
            max_flow, max_flow_path = max_flow_calculator.ford_fulkerson(source, sink)

            messagebox.showinfo("Результат", f"Максимальный поток равен: {max_flow}")
            draw_graph(edge_list, num_vertices, max_flow_path)
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные числа!")
        except IndexError:
            messagebox.showerror("Ошибка", "Проверьте вводимые данные о рёбрах!")
#Инструкция
    def show_instructions():
        instructions = (
            "Инструкция по использованию:\n\n"
            "1. Введите количество вершин графа.\n"
            "2. Введите рёбра в формате 'начальная вершина - конечная вершина - значение потока(пропускная способность)',\n"
            "   Каждое ребро вводится с новой строки.\n"
            "3. Нажмите кнопку 'Рассчитать максимальный поток'.\n"
            "4. Результат будет отображён в виде сообщения.\nМаксимальный поток будет выделен красным цветом\n"
            "5. Граф будет нарисован на экране.\n"
            "6. Вы можете нажать расчитать поток повторно чтобы граф перерисовался."

        )
        messagebox.showinfo("Инструкция", instructions)

    root = tk.Tk()
    root.title("Максимальный поток")
    root.geometry('600x800')

    tk.Label(root, text="Количество вершин:", font=("Helvetica", 16), wraplength=500).pack()
    vertex_entry = tk.Entry(root, font=("Helvetica", 16))
    vertex_entry.pack()

    tk.Label(root, text="Рёбра (формат: Нач.вер - Кон.вер - Проп.способ, каждое в новой строке):",
             font=("Helvetica", 16), wraplength=500).pack()
    edge_entry = tk.Text(root, height=10, width=50, font=("Helvetica", 12))
    edge_entry.pack()

    calculate_button = tk.Button(root, text="Рассчитать максимальный поток", command=calculate_max_flow,
                                 font=("Helvetica", 16, "bold"), fg="green")
    calculate_button.pack()

    instruction_button = tk.Button(root, text="Инструкция", command=show_instructions,
                                   font=("Helvetica", 16, "bold"), fg="black")
    instruction_button.pack()

    canvas = tk.Canvas(root, width=400, height=400, bg='white')
    canvas.pack()

    root.mainloop()


# Приветственное окно
hello = tk.Tk()
hello.title("Программа по расчету максимального потока в графе")
hello.geometry("600x450")

header = tk.Label(hello, text="\nПроект курса 2:\n\n", font=("Helvetica", 24, "bold"), fg="blue")
header.pack()

description = tk.Label(
    hello,
    text="Эта программа предназначена для нахождения максимального потока в графе "
         "с использованием эффективного алгоритма Форда-Фалкерсона. "
         "Вы сможете визуализировать процесс и понять, как работает данный алгоритм.\n\n"
         "ПМИ-231: Жиров Артем, Луценко Даниил",
    font=("Helvetica", 16),
    wraplength=500,
    justify="left"
)
description.pack(pady=20)

start_button = tk.Button(hello, text='Начать', command=main_window, font=("Helvetica", 14), bg="lightgreen")
start_button.pack(pady=10)

hello.mainloop()