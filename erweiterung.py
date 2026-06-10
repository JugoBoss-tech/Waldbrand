import tkinter as tk
import random

# Einstellungen
GRID_SIZE = 100
CELL_SIZE = 6

EMPTY = 0

TREE_1 = 1
TREE_2 = 2
TREE_3 = 3

FIRE_1 = 4
FIRE_2 = 5
FIRE_3 = 6

BURNED_1 = 7
BURNED_2 = 8
BURNED_3 = 9

RIVER = 10

colors = {
    EMPTY: "white",

    TREE_1: "green",
    TREE_2: "darkgreen",
    TREE_3: "olive",

    FIRE_1: "blue",
    FIRE_2: "blue",
    FIRE_3: "blue",

    BURNED_1: "black",
    BURNED_2: "black",
    BURNED_3: "black",

    RIVER: "lightblue"
}

grid = []

initial_tree_cells = 0
initial_tree_1_cells = 0
initial_tree_2_cells = 0
initial_tree_3_cells = 0

# ---------------- SETUP ----------------

def setup():
    global grid
    global initial_tree_cells
    global initial_tree_1_cells
    global initial_tree_2_cells
    global initial_tree_3_cells

    density = density_slider.get()

    grid = []

    initial_tree_cells = 0
    initial_tree_1_cells = 0
    initial_tree_2_cells = 0
    initial_tree_3_cells = 0

    for y in range(GRID_SIZE):
        row = []

        for x in range(GRID_SIZE):

            if random.random() * 100 < density:

                tree_type = random.choice([TREE_1, TREE_2, TREE_3])
                row.append(tree_type)

            else:
                row.append(EMPTY)

        grid.append(row)

    create_river()

    initial_tree_cells = 0
    initial_tree_1_cells = 0
    initial_tree_2_cells = 0
    initial_tree_3_cells = 0

    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):

            if grid[y][x] == TREE_1:
                initial_tree_cells += 1
                initial_tree_1_cells += 1

            elif grid[y][x] == TREE_2:
                initial_tree_cells += 1
                initial_tree_2_cells += 1

            elif grid[y][x] == TREE_3:
                initial_tree_cells += 1
                initial_tree_3_cells += 1

    # Feuer startet an einem zufaelligen Baum
    tree_positions = []

    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if is_tree(grid[y][x]):
                tree_positions.append((x, y))

    if tree_positions:
        start_x, start_y = random.choice(tree_positions)
        grid[start_y][start_x] = get_fire_state(grid[start_y][start_x])

    draw_grid()
    update_stats()

# ---------------- FLUSS ----------------

def create_river():

    river_x = GRID_SIZE // 3
    river_width = 3

    for y in range(GRID_SIZE):

        river_x += random.choice([-1, 0, 1])

        if river_x < 10:
            river_x = 10

        if river_x > GRID_SIZE - 10:
            river_x = GRID_SIZE - 10

        for w in range(-river_width // 2, river_width // 2 + 1):

            x = river_x + w

            if 0 <= x < GRID_SIZE:
                grid[y][x] = RIVER

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

# ---------------- STATISTIK ----------------

def update_stats():

    total_cells = GRID_SIZE * GRID_SIZE

    empty_cells = 0
    river_cells = 0

    tree_1_cells = 0
    tree_2_cells = 0
    tree_3_cells = 0

    fire_1_cells = 0
    fire_2_cells = 0
    fire_3_cells = 0

    burned_1_cells = 0
    burned_2_cells = 0
    burned_3_cells = 0

    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):

            if grid[y][x] == EMPTY:
                empty_cells += 1

            elif grid[y][x] == RIVER:
                river_cells += 1

            elif grid[y][x] == TREE_1:
                tree_1_cells += 1

            elif grid[y][x] == TREE_2:
                tree_2_cells += 1

            elif grid[y][x] == TREE_3:
                tree_3_cells += 1

            elif grid[y][x] == FIRE_1:
                fire_1_cells += 1

            elif grid[y][x] == FIRE_2:
                fire_2_cells += 1

            elif grid[y][x] == FIRE_3:
                fire_3_cells += 1

            elif grid[y][x] == BURNED_1:
                burned_1_cells += 1

            elif grid[y][x] == BURNED_2:
                burned_2_cells += 1

            elif grid[y][x] == BURNED_3:
                burned_3_cells += 1

    burned_total = burned_1_cells + burned_2_cells + burned_3_cells
    not_burned_total = (
        tree_1_cells + tree_2_cells + tree_3_cells +
        fire_1_cells + fire_2_cells + fire_3_cells
    )

    if initial_tree_cells > 0:
        burned_percent = burned_total / initial_tree_cells * 100
        not_burned_percent = not_burned_total / initial_tree_cells * 100
    else:
        burned_percent = 0
        not_burned_percent = 0

    if initial_tree_1_cells > 0:
        burned_tree_1_percent = burned_1_cells / initial_tree_1_cells * 100
    else:
        burned_tree_1_percent = 0

    if initial_tree_2_cells > 0:
        burned_tree_2_percent = burned_2_cells / initial_tree_2_cells * 100
    else:
        burned_tree_2_percent = 0

    if initial_tree_3_cells > 0:
        burned_tree_3_percent = burned_3_cells / initial_tree_3_cells * 100
    else:
        burned_tree_3_percent = 0

    empty_percent = empty_cells / total_cells * 100
    river_percent = river_cells / total_cells * 100

    stats_label.config(
        text=
        f"Abgebrannte Bäume gesamt: {burned_percent:.2f}%\n"
        f"Nicht abgebrannte Bäume gesamt: {not_burned_percent:.2f}%\n"
        f"Baumart 1 abgebrannt: {burned_tree_1_percent:.2f}%\n"
        f"Baumart 2 abgebrannt: {burned_tree_2_percent:.2f}%\n"
        f"Baumart 3 abgebrannt: {burned_tree_3_percent:.2f}%\n"
        f"Leer / kein Baum: {empty_percent:.2f}%\n"
        f"Fluss: {river_percent:.2f}%"
    )

# ---------------- HILFSFUNKTIONEN ----------------

def is_tree(cell):
    return cell == TREE_1 or cell == TREE_2 or cell == TREE_3

def is_fire(cell):
    return cell == FIRE_1 or cell == FIRE_2 or cell == FIRE_3

def get_fire_state(tree_type):

    if tree_type == TREE_1:
        return FIRE_1

    elif tree_type == TREE_2:
        return FIRE_2

    elif tree_type == TREE_3:
        return FIRE_3

def get_burned_state(fire_type):

    if fire_type == FIRE_1:
        return BURNED_1

    elif fire_type == FIRE_2:
        return BURNED_2

    elif fire_type == FIRE_3:
        return BURNED_3

def get_burn_probability(tree_type):

    if tree_type == TREE_1:
        return tree_1_slider.get()

    elif tree_type == TREE_2:
        return tree_2_slider.get()

    elif tree_type == TREE_3:
        return tree_3_slider.get()

    return 0

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

    river_cross_probability = river_slider.get()

    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):

            if is_fire(grid[y][x]):

                new_grid[y][x] = get_burned_state(grid[y][x])

                for dx, dy in directions:

                    nx = x + dx
                    ny = y + dy

                    if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:

                        if is_tree(grid[ny][nx]):

                            burn_probability = get_burn_probability(grid[ny][nx])

                            if random.random() * 100 < burn_probability:
                                new_grid[ny][nx] = get_fire_state(grid[ny][nx])

                        elif grid[ny][nx] == RIVER:

                            rx = nx
                            ry = ny

                            while 0 <= rx < GRID_SIZE and 0 <= ry < GRID_SIZE and grid[ry][rx] == RIVER:
                                rx += dx
                                ry += dy

                            if 0 <= rx < GRID_SIZE and 0 <= ry < GRID_SIZE:

                                if is_tree(grid[ry][rx]):

                                    burn_probability = get_burn_probability(grid[ry][rx])

                                    total_probability = river_cross_probability * burn_probability / 100

                                    if random.random() * 100 < total_probability:
                                        new_grid[ry][rx] = get_fire_state(grid[ry][rx])

    grid = new_grid

    draw_grid()
    update_stats()

    # Tickrate aus Slider
    tick_rate = speed_slider.get()

    fire_exists = False

    for row in grid:
        for cell in row:
            if is_fire(cell):
                fire_exists = True

    if fire_exists:
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

# ---------------- SCROLLBAR FÜR REGLER ----------------

controls_container = tk.Frame(root)
controls_container.pack(fill="both", expand=True)

controls_canvas = tk.Canvas(
    controls_container,
    height=320
)

controls_scrollbar = tk.Scrollbar(
    controls_container,
    orient="vertical",
    command=controls_canvas.yview
)

controls = tk.Frame(controls_canvas)

controls.bind(
    "<Configure>",
    lambda event: controls_canvas.configure(
        scrollregion=controls_canvas.bbox("all")
    )
)

controls_canvas.create_window(
    (0, 0),
    window=controls,
    anchor="nw"
)

controls_canvas.configure(
    yscrollcommand=controls_scrollbar.set
)

controls_canvas.pack(
    side="left",
    fill="both",
    expand=True
)

controls_scrollbar.pack(
    side="right",
    fill="y"
)

def on_mousewheel(event):
    controls_canvas.yview_scroll(
        int(-1 * (event.delta / 120)),
        "units"
    )

controls_canvas.bind_all("<MouseWheel>", on_mousewheel)

# ---------------- BUTTONS ----------------

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

# ---------------- DENSITY SLIDER ----------------

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

# ---------------- TICKRATE SLIDER ----------------

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

# ---------------- RIVER CROSSING SLIDER ----------------

river_label = tk.Label(
    controls,
    text="River Crossing Probability [%]"
)

river_label.grid(row=3, column=0)

river_slider = tk.Scale(
    controls,
    from_=0,
    to=100,
    orient="horizontal"
)

river_slider.set(5)

river_slider.grid(row=3, column=1)

# ---------------- TREE 1 SLIDER ----------------

tree_1_label = tk.Label(
    controls,
    text="Baumart 1 Brennwahrscheinlichkeit [%]"
)

tree_1_label.grid(row=4, column=0)

tree_1_slider = tk.Scale(
    controls,
    from_=0,
    to=100,
    orient="horizontal"
)

tree_1_slider.set(90)

tree_1_slider.grid(row=4, column=1)

# ---------------- TREE 2 SLIDER ----------------

tree_2_label = tk.Label(
    controls,
    text="Baumart 2 Brennwahrscheinlichkeit [%]"
)

tree_2_label.grid(row=5, column=0)

tree_2_slider = tk.Scale(
    controls,
    from_=0,
    to=100,
    orient="horizontal"
)

tree_2_slider.set(60)

tree_2_slider.grid(row=5, column=1)

# ---------------- TREE 3 SLIDER ----------------

tree_3_label = tk.Label(
    controls,
    text="Baumart 3 Brennwahrscheinlichkeit [%]"
)

tree_3_label.grid(row=6, column=0)

tree_3_slider = tk.Scale(
    controls,
    from_=0,
    to=100,
    orient="horizontal"
)

tree_3_slider.set(30)

tree_3_slider.grid(row=6, column=1)

# ---------------- STATISTIK LABEL ----------------

stats_label = tk.Label(
    controls,
    text=
    "Abgebrannte Bäume gesamt: 0.00%\n"
    "Nicht abgebrannte Bäume gesamt: 0.00%\n"
    "Baumart 1 abgebrannt: 0.00%\n"
    "Baumart 2 abgebrannt: 0.00%\n"
    "Baumart 3 abgebrannt: 0.00%\n"
    "Leer / kein Baum: 0.00%\n"
    "Fluss: 0.00%",
    justify="left"
)

stats_label.grid(row=7, column=0, columnspan=2, pady=10)

setup()

root.mainloop()
