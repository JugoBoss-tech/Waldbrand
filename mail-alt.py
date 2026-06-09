
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from collections import deque


# -----------------------------
# Parameter
# -----------------------------
GRID_SIZE = 100          # Größe des Gitters
P_GROWTH = 0.01          # Wahrscheinlichkeit für Baumwachstum
F_LIGHTNING = 0.0001     # Wahrscheinlichkeit für Blitzschlag
STEPS = 300            # Anzahl der Simulationsschritte
ANIMATION_INTERVAL = 1  # Aktualisierung der Anzeige


# -----------------------------
# Zellzustände
# -----------------------------
EMPTY = 0
TREE = 1
FIRE = 2


# -----------------------------
# Hilfsfunktionen
# -----------------------------
def get_neighbors(x, y, size):
    """
    Liefert die direkten Nachbarn (oben, unten, links, rechts).
    """
    neighbors = []

    if x > 0:
        neighbors.append((x - 1, y))
    if x < size - 1:
        neighbors.append((x + 1, y))
    if y > 0:
        neighbors.append((x, y - 1))
    if y < size - 1:
        neighbors.append((x, y + 1))
        

    return neighbors


def count_fire_size(grid, fire_positions):
    """
    Bestimmt die Größe eines zusammenhängenden Brandes.
    """
    visited = set()
    total = 0

    queue = deque(fire_positions)

    while queue:
        x, y = queue.popleft()

        if (x, y) in visited:
            continue

        visited.add((x, y))
        total += 1

        for nx, ny in get_neighbors(x, y, grid.shape[0]):
            if grid[nx, ny] == FIRE and (nx, ny) not in visited:
                queue.append((nx, ny))

    return total


# -----------------------------
# Initialisierung
# -----------------------------
grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)

fire_sizes = []
tree_densities = []


# -----------------------------
# Visualisierung vorbereiten
# -----------------------------
cmap = ListedColormap([
    "black",   # leer
    "green",   # Baum
    "red"      # Feuer
])

plt.ion()

fig, ax = plt.subplots(figsize=(7, 7))
img = ax.imshow(grid, cmap=cmap, vmin=0, vmax=2)

ax.set_title("Waldbrandmodell")
ax.set_xticks([])
ax.set_yticks([])


# -----------------------------
# Hauptsimulation
# -----------------------------
for step in range(STEPS):

    new_grid = grid.copy()

    # -----------------------------------
    # 1. Baumwachstum
    # -----------------------------------
    empty_cells = (grid == EMPTY)

    growth_random = np.random.random((GRID_SIZE, GRID_SIZE))
    new_trees = (growth_random < P_GROWTH) & empty_cells

    new_grid[new_trees] = TREE

    # -----------------------------------
    # 2. Blitzschlag
    # -----------------------------------
    tree_cells = (new_grid == TREE)

    lightning_random = np.random.random((GRID_SIZE, GRID_SIZE))
    lightning = (lightning_random < F_LIGHTNING) & tree_cells

    new_grid[lightning] = FIRE

    # -----------------------------------
    # 3. Feuerausbreitung
    # -----------------------------------
    current_fires = np.argwhere(grid == FIRE)

    for x, y in current_fires:

        for nx, ny in get_neighbors(x, y, GRID_SIZE):

            if new_grid[nx, ny] == TREE:
                new_grid[nx, ny] = FIRE

    # -----------------------------------
    # 4. Abbrennen
    # -----------------------------------
    new_grid[grid == FIRE] = EMPTY

    # -----------------------------------
    # Brandgröße erfassen
    # -----------------------------------
    fires = np.argwhere(new_grid == FIRE)

    if len(fires) > 0:
        fire_size = len(fires)
        fire_sizes.append(fire_size)

    # -----------------------------------
    # Baumdichte erfassen
    # -----------------------------------
    density = np.sum(new_grid == TREE) / (GRID_SIZE * GRID_SIZE)
    tree_densities.append(density)

    # Grid aktualisieren
    grid = new_grid

    # -----------------------------------
    # Visualisierung
    # -----------------------------------
    if step % ANIMATION_INTERVAL == 0:
        img.set_data(grid)
        ax.set_title(f"Waldbrandmodell - Schritt {step}")
        plt.pause(0.001)


# -----------------------------
# Simulation beendet
# -----------------------------
plt.ioff()

# -----------------------------------
# Analyseplots
# -----------------------------------
fig2, axes = plt.subplots(1, 2, figsize=(12, 5))

# Brandgrößenverteilung
axes[0].hist(
    fire_sizes,
    bins=50,
    log=True
)

axes[0].set_title("Verteilung der Brandgrößen")
axes[0].set_xlabel("Brandgröße")
axes[0].set_ylabel("Häufigkeit (log)")

# Baumdichte
axes[1].plot(tree_densities)

axes[1].set_title("Baumdichte über Zeit")
axes[1].set_xlabel("Zeitschritt")
axes[1].set_ylabel("Baumdichte")

plt.tight_layout()
plt.show()