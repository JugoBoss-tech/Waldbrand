import tkinter as tk
import random

# Einstellungen
GRID_SIZE = 100
CELL_SIZE = 6

EMPTY = 0
TREE = 1
FIRE = 2
BURNED = 3

colors = {
    EMPTY: "white",
    TREE: "green",
    FIRE: "blue",
    BURNED: "black"
}

grid = []

# ---------------- SETUP ----------------

def setup():
    global grid

    density = density_slider.get()

    grid = []

    for y in range(GRID_SIZE):
        row = []

        for x in range(GRID_SIZE):

            if random.random() * 100 < density:
                row.append(TREE)
            else:
                row.append(EMPTY)

        grid.append(row)

    # Feuer startet in der Mitte
    start_x = GRID_SIZE // 2
    start_y = GRID_SIZE // 2

    grid[start_y][start_x] = FIRE

    draw_grid()

# ---------------- ZEICHNEN ----------------

def draw_grid():

    canvas.delete("all")

    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):

            color = colors[grid[y][x]]

            canvas.create_rectangle(
                x * CELL_SIZE,
                y * CELL_SIZE,
                (x + 1) * CELL_SIZE,
                (y + 1) * CELL_SIZE,
                fill=color,
                outline=""
            )

# ---------------- SIMULATION ----------------

def step():

    global grid

    new_grid = [row[:] for row in grid]

    # 8 Richtungen
    directions = [
        (-1, -1), (0, -1), (1, -1),
        (-1,  0),          (1,  0),
        (-1,  1), (0,  1), (1,  1)
    ]

    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):

            if grid[y][x] == FIRE:

                new_grid[y][x] = BURNED

                for dx, dy in directions:

                    nx = x + dx
                    ny = y + dy

                    if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:

                        if grid[ny][nx] == TREE:
                            new_grid[ny][nx] = FIRE

    grid = new_grid

    draw_grid()

    # Tickrate aus Slider
    tick_rate = speed_slider.get()

    if any(FIRE in row for row in grid):
        root.after(tick_rate, step)

# ---------------- START ----------------

def start():
    step()

# ---------------- GUI ----------------

root = tk.Tk()
root.title("Waldbrand Simulation")

canvas = tk.Canvas(
    root,
    width=GRID_SIZE * CELL_SIZE,
    height=GRID_SIZE * CELL_SIZE
)

canvas.pack()

controls = tk.Frame(root)
controls.pack()

# Buttons
setup_button = tk.Button(
    controls,
    text="Setup",
    command=setup
)

setup_button.grid(row=0, column=0, padx=10)

start_button = tk.Button(
    controls,
    text="Start",
    command=start
)

start_button.grid(row=0, column=1, padx=10)

# Density Slider
density_label = tk.Label(
    controls,
    text="Density [%]"
)

density_label.grid(row=1, column=0)

density_slider = tk.Scale(
    controls,
    from_=0,
    to=100,
    orient="horizontal"
)

density_slider.set(60)

density_slider.grid(row=1, column=1)

# Tickrate Slider
speed_label = tk.Label(
    controls,
    text="Tick Rate [ms]"
)

speed_label.grid(row=2, column=0)

speed_slider = tk.Scale(
    controls,
    from_=10,
    to=500,
    orient="horizontal"
)

speed_slider.set(80)

speed_slider.grid(row=2, column=1)

setup()

root.mainloop()
