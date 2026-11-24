import random
import tkinter as tk
from tkinter import messagebox, ttk

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from src.city import City
from src.generations import Generations
from src.map import Map
from src.population import Population


class GAApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("TSP")

        params = ttk.LabelFrame(root, text="Parametry")
        params.grid(row=0, column=0, padx=20, pady=10, sticky="n")

        self.pop_size = tk.IntVar(value=100)
        self.p_cross = tk.DoubleVar(value=0.75)
        self.p_mut = tk.DoubleVar(value=0.001)
        self.gen_count = tk.IntVar(value=200)
        self.seed = tk.StringVar(value="")

        rows = [
            ("Liczebność populacji:", ttk.Entry(params, textvariable=self.pop_size)),
            ("P. krzyżowania:", ttk.Entry(params, textvariable=self.p_cross)),
            ("P. mutacji:", ttk.Entry(params, textvariable=self.p_mut)),
            ("Liczba iteracji:", ttk.Entry(params, textvariable=self.gen_count)),
            ("Ziarno:", ttk.Entry(params, textvariable=self.seed)),
        ]

        for row, (label, widget) in enumerate(rows):
            ttk.Label(params, text=label).grid(row=row, column=0, sticky="w", pady=3)
            widget.grid(row=row, column=1, sticky="ew", pady=3)

        ttk.Button(params, text="Uruchom", command=self.run_ga).grid(
            row=len(rows), column=0, columnspan=2, pady=10, sticky="ew"
        )

        self.result = tk.Text(params, height=4, width=32, state="disabled")
        self.result.grid(row=len(rows) + 1, column=0, columnspan=2)

        plots = ttk.Frame(root)
        plots.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        root.columnconfigure(1, weight=1)
        root.rowconfigure(0, weight=1)

        self.figure = Figure(figsize=(10, 7))
        grid = self.figure.add_gridspec(2, 2)
        self.ax_history = self.figure.add_subplot(grid[0, :])
        self.ax_shortest = self.figure.add_subplot(grid[1, 0])
        self.ax_longest = self.figure.add_subplot(grid[1, 1])
        self.canvas = FigureCanvasTkAgg(self.figure, plots)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.cities = [
            City(1, 2),  # A
            City(8, 8),  # B
            City(5, 6),  # C
            City(0, 8),  # D
            City(2, 7),  # E
            City(4, 7),  # F
            City(3, 3),  # G
            City(9, 5),  # H
            City(6, 4),  # I
            City(7, 1),  # J
        ]

    def run_ga(self):
        try:
            if self.seed.get().strip():
                random.seed(int(self.seed.get()))

            city_map = Map(10, 10)
            city_map.add_city(self.cities)
            population = Population(self.pop_size.get(), city_map)
            generations = Generations(
                population=population,
                p_crossover=self.p_cross.get(),
                p_mutation=self.p_mut.get(),
                generation_count=self.gen_count.get(),
            )
            history = generations.run()

            shortest = generations.best
            longest = min(
                generations.population,
                key=lambda candidate: candidate.get_fitness(),
            )
            self.show_result(shortest)
            self.draw_history(history)
            self.draw_route(self.ax_shortest, shortest, "Najkrótsza trasa", "green")
            self.draw_route(self.ax_longest, longest, "Najdłuższa trasa", "red")
            self.figure.tight_layout()
            self.canvas.draw()
        except (TypeError, ValueError) as error:
            messagebox.showerror("Błąd parametrów", str(error))

    def show_result(self, candidate):
        self.result.configure(state="normal")
        self.result.delete("1.0", tk.END)
        self.result.insert(tk.END, f"Miasta: {len(candidate.representation)}\n")
        self.result.insert(
            tk.END,
            f"Długość najkrótszej trasy: {candidate.get_route_length():.2f}\n",
        )
        self.result.configure(state="disabled")

    def draw_history(self, history):
        self.ax_history.clear()
        generations = range(len(history["max"]))
        self.ax_history.plot(generations, history["min"], label="minimum", color="green")
        self.ax_history.plot(generations, history["avg"], label="średnia", color="blue")
        self.ax_history.plot(generations, history["max"], label="maksimum", color="red")
        self.ax_history.set_title("Długość tras w kolejnych pokoleniach")
        self.ax_history.set_xlabel("Pokolenie")
        self.ax_history.set_ylabel("Długość trasy")
        self.ax_history.legend()
        self.ax_history.grid(True, alpha=0.3)

    def draw_route(self, axis, candidate, title, color):
        axis.clear()
        route = candidate.representation
        x_values = [city.x for city in route] + [route[0].x]
        y_values = [city.y for city in route] + [route[0].y]
        axis.plot(x_values, y_values, "o-", color=color, markersize=4)

        for index, city in enumerate(route, start=1):
            axis.annotate(
                str(index),
                (city.x, city.y),
                xytext=(4, 4),
                textcoords="offset points",
            )

        axis.set_title(f"{title}: {candidate.get_route_length():.2f}")
        axis.set_xlim(-0.5, 9.5)
        axis.set_ylim(-0.5, 9.5)
        axis.set_xticks(range(10))
        axis.set_yticks(range(10))
        axis.set_aspect("equal")
        axis.grid(True, alpha=0.3)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1280x720")
    app = GAApp(root)
    root.mainloop()
