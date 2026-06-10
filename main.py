import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


# -----------------------------
# Zellzustände
# -----------------------------
EMPTY = 0
TREE = 1
FIRE = 2


# -----------------------------
# Hilfsfunktion: Nachbarn
# -----------------------------
def get_neighbors(x, y, size):
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


# -----------------------------
# Simulation
# -----------------------------
def run_simulation(
    grid_size=100,
    initial_density=0.4,
    p_growth=0.01,
    f_lightning=0.0001,
    steps=200,
    animate=True,
    animation_interval=1,
    tick_rate=30,
    seed=None
):
    if seed is not None:
        np.random.seed(seed)

    # -----------------------------
    # Anfangswald erzeugen
    # -----------------------------
    grid = np.zeros((grid_size, grid_size), dtype=int)

    random_grid = np.random.random((grid_size, grid_size))
    initial_trees = random_grid < initial_density
    grid[initial_trees] = TREE

    # Datenlisten
    tree_densities = []
    active_fire_cells = []

    fire_durations = []
    fire_areas = []

    # Aktuelles Brandereignis
    fire_active = False
    current_fire_duration = 0
    current_burned_cells = set()

    # Visualisierung vorbereiten
    if animate:
        cmap = ListedColormap(["black", "green", "red"])

        plt.ion()
        fig, ax = plt.subplots(figsize=(7, 7))
        img = ax.imshow(grid, cmap=cmap, vmin=0, vmax=2)

        ax.set_title("Waldbrandmodell")
        ax.set_xticks([])
        ax.set_yticks([])

    # -----------------------------
    # Hauptsimulation
    # -----------------------------
    for step in range(steps):

        new_grid = grid.copy()

        # -----------------------------
        # 1. Baumwachstum
        # -----------------------------
        # Wachstum findet nur statt, wenn gerade kein Brand aktiv ist.
        if not fire_active:
            empty_cells = (grid == EMPTY)
            growth_random = np.random.random((grid_size, grid_size))
            new_trees = (growth_random < p_growth) & empty_cells

            new_grid[new_trees] = TREE

        # -----------------------------
        # 2. Blitzschlag
        # -----------------------------
        # Ein neuer Blitz darf nur einschlagen, wenn gerade kein Brand aktiv ist.
        if not fire_active:

            tree_positions = np.argwhere(new_grid == TREE)
            number_of_trees = len(tree_positions)

            if number_of_trees > 0:
                # Wahrscheinlichkeit, dass in diesem Zeitschritt mindestens ein Blitz auftritt.
                # Es wird aber maximal ein Baum getroffen.
                probability_at_least_one_lightning = 1 - (1 - f_lightning) ** number_of_trees

                if np.random.random() < probability_at_least_one_lightning:
                    random_index = np.random.randint(number_of_trees)
                    x, y = tree_positions[random_index]
                    new_grid[x, y] = FIRE

        # -----------------------------
        # 3. Feuerausbreitung
        # -----------------------------
        current_fires = np.argwhere(grid == FIRE)

        for x, y in current_fires:
            for nx, ny in get_neighbors(x, y, grid_size):
                if new_grid[nx, ny] == TREE:
                    new_grid[nx, ny] = FIRE

        # -----------------------------
        # 4. Abbrennen alter Feuerzellen
        # -----------------------------
        new_grid[grid == FIRE] = EMPTY

        # -----------------------------
        # Brandereignis messen
        # -----------------------------
        fires = np.argwhere(new_grid == FIRE)
        number_of_fire_cells = len(fires)

        if number_of_fire_cells > 0:

            # Neuer Brand beginnt
            if not fire_active:
                fire_active = True
                current_fire_duration = 0
                current_burned_cells = set()

            # Brand läuft weiter
            current_fire_duration += 1

            # Betroffene Fläche speichern
            for x, y in fires:
                current_burned_cells.add((x, y))

        else:

            # Brand endet
            if fire_active:
                fire_durations.append(current_fire_duration)
                fire_areas.append(len(current_burned_cells))

                fire_active = False
                current_fire_duration = 0
                current_burned_cells = set()

        # -----------------------------
        # Baumdichte erfassen
        # -----------------------------
        density = np.sum(new_grid == TREE) / (grid_size * grid_size)
        tree_densities.append(density)

        active_fire_cells.append(number_of_fire_cells)

        # Grid aktualisieren
        grid = new_grid

        # -----------------------------
        # Animation
        # -----------------------------
        if animate and step % animation_interval == 0:
            img.set_data(grid)
            ax.set_title(f"Waldbrandmodell - Schritt {step}")

            if tick_rate > 0:
                plt.pause(1 / tick_rate)
            else:
                plt.pause(0.001)

    # Falls am Simulationsende noch ein Brand aktiv ist
    if fire_active:
        fire_durations.append(current_fire_duration)
        fire_areas.append(len(current_burned_cells))

    if animate:
        plt.ioff()

    results = {
        "tree_densities": tree_densities,
        "active_fire_cells": active_fire_cells,
        "fire_durations": fire_durations,
        "fire_areas": fire_areas,
        "parameters": {
            "grid_size": grid_size,
            "initial_density": initial_density,
            "p_growth": p_growth,
            "f_lightning": f_lightning,
            "steps": steps,
            "tick_rate": tick_rate
        }
    }

    return results


# -----------------------------
# Analyseplots
# -----------------------------
def plot_results(results):
    tree_densities = results["tree_densities"]
    active_fire_cells = results["active_fire_cells"]
    fire_durations = results["fire_durations"]
    fire_areas = results["fire_areas"]

    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    # Baumdichte über Zeit
    axes[0, 0].plot(tree_densities)
    axes[0, 0].set_title("Baumdichte über Zeit")
    axes[0, 0].set_xlabel("Zeitschritt")
    axes[0, 0].set_ylabel("Baumdichte")

    # Aktive Feuerzellen über Zeit
    axes[0, 1].plot(active_fire_cells)
    axes[0, 1].set_title("Aktiv brennende Zellen über Zeit")
    axes[0, 1].set_xlabel("Zeitschritt")
    axes[0, 1].set_ylabel("Anzahl Feuerzellen")

    # Branddauer
    axes[1, 0].hist(fire_durations, bins=30)
    axes[1, 0].set_title("Verteilung der Branddauer")
    axes[1, 0].set_xlabel("Branddauer in Zeitschritten")
    axes[1, 0].set_ylabel("Häufigkeit")

    # Brandfläche
    axes[1, 1].hist(fire_areas, bins=30)
    axes[1, 1].set_title("Verteilung der Brandflächen")
    axes[1, 1].set_xlabel("Brandfläche")
    axes[1, 1].set_ylabel("Häufigkeit")

    plt.tight_layout()
    plt.show()


# -----------------------------
# Kennwerte ausgeben
# -----------------------------
def print_summary(results):
    fire_durations = results["fire_durations"]
    fire_areas = results["fire_areas"]
    tree_densities = results["tree_densities"]

    print("Parameter:")
    for key, value in results["parameters"].items():
        print(f"{key}: {value}")

    print("\nBaumdichte:")
    print(f"Start-Baumdichte nach erstem Schritt: {tree_densities[0]:.3f}")
    print(f"Mittlere Baumdichte: {np.mean(tree_densities):.3f}")
    print(f"Maximale Baumdichte: {np.max(tree_densities):.3f}")

    print("\nBrandereignisse:")
    print(f"Anzahl der Brandereignisse: {len(fire_areas)}")

    if len(fire_areas) > 0:
        print(f"Mittlere Brandfläche: {np.mean(fire_areas):.2f}")
        print(f"Maximale Brandfläche: {np.max(fire_areas)}")
        print(f"Mittlere Branddauer: {np.mean(fire_durations):.2f}")
        print(f"Maximale Branddauer: {np.max(fire_durations)}")
    else:
        print("Keine Brandereignisse gefunden.")


# -----------------------------
# Simulation starten
# -----------------------------
results = run_simulation(
    grid_size=100,
    initial_density=0.3,
    p_growth=0.01,
    f_lightning=0.0001,
    steps=2000,
    animate=True,
    animation_interval=1,
    tick_rate=20,
    seed=42
)

plot_results(results)
print_summary(results)