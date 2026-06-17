## 2. Methode

Das Waldbrandmodell wurde in Python als zweidimensionaler zellulärer Automat umgesetzt. Dafür wird ein quadratisches Gitter verwendet, bei dem jede Zelle einen kleinen Bereich des Waldes darstellt. Eine Zelle kann entweder leer sein (EMPTY = 0), einen Baum enthalten (TREE = 1) oder brennen (FIRE = 2). In unserer Simulation hat das Gitter eine Größe von 100 × 100 Zellen. Zu Beginn wird zufällig festgelegt, welche Zellen Bäume enthalten. Mit initial_density = 0.3 sind am Anfang ungefähr 30 % der Zellen bewaldet.

Die Simulation läuft schrittweise ab. In jedem Zeitschritt werden die gleichen Regeln angewendet: Zuerst können auf leeren Zellen neue Bäume wachsen. Danach kann ein Blitz einschlagen und einen Baum entzünden. Anschließend breitet sich das Feuer auf benachbarte Bäume aus, und die Zellen, die vorher gebrannt haben, werden leer. Für das Baumwachstum wurde p_growth = 0.01 verwendet. Die Blitzwahrscheinlichkeit pro Baumzelle beträgt f_lightning = 0.0001. Während ein Brand läuft, pausieren Wachstum und neue Blitzschläge. Das ist zwar eine Vereinfachung, macht es aber leichter, einzelne Brandereignisse getrennt auszuwerten.

Für die technische Umsetzung wurde vor allem numpy verwendet. Das Gitter wird als zweidimensionales Array gespeichert, und auch die Zufallszahlen für Wachstum, Anfangsverteilung und Blitzschlag werden damit erzeugt. Außerdem werden mit numpy Größen wie die Baumdichte oder die Anzahl brennender Zellen berechnet. Für die Darstellung der Simulation und der Ergebnisse wurde matplotlib verwendet. Die Animation zeigt das Gitter während der Simulation, und am Ende werden die wichtigsten Messgrößen als Plots dargestellt. Mit ListedColormap werden die drei Zellzustände farblich unterschieden.

Die Nachbarschaft im Modell ist eine Von-Neumann-Nachbarschaft. Das bedeutet, dass eine Zelle nur ihre direkten Nachbarn oben, unten, links und rechts berücksichtigt. Diagonale Nachbarn zählen nicht dazu. Außerdem gibt es keine periodischen Randbedingungen. Eine Zelle am Rand hat also weniger Nachbarn als eine Zelle im Inneren des Gitters.

```python
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
```

Diese Funktion gibt für eine Zelle alle gültigen Nachbarn zurück. Die if-Abfragen verhindern, dass Zellen außerhalb des Gitters verwendet werden. Dadurch wird gleichzeitig festgelegt, dass das Feuer nicht über den Rand hinaus weiterlaufen kann. Diese Stelle ist wichtig, weil sie die räumliche Struktur des Modells definiert.

Der Start eines Brandes wird über einen zufälligen Blitzschlag modelliert. Dazu werden zuerst alle Baumzellen gesucht. Aus der Anzahl der vorhandenen Bäume wird berechnet, wie wahrscheinlich es ist, dass in diesem Zeitschritt mindestens ein Blitz auftritt.

```python
tree_positions = np.argwhere(new_grid == TREE)
number_of_trees = len(tree_positions)

if number_of_trees > 0:
    probability_at_least_one_lightning = 1 - (1 - f_lightning) ** number_of_trees

    if np.random.random() < probability_at_least_one_lightning:
        random_index = np.random.randint(number_of_trees)
        x, y = tree_positions[random_index]
        new_grid[x, y] = FIRE
```

Der Ausdruck 1 - (1 - f_lightning) ** number_of_trees berechnet die Wahrscheinlichkeit, dass mindestens eine Baumzelle getroffen wird. Wenn dieses Ereignis eintritt, wird eine zufällige Baumzelle ausgewählt und in den Zustand FIRE gesetzt. Pro Zeitschritt kann dadurch maximal ein neuer Brand durch Blitzschlag entstehen.

Die Ausbreitung des Feuers wird über die Nachbarschaftsregel umgesetzt. Dafür werden alle Zellen gesucht, die im aktuellen Gitter brennen. Anschließend werden ihre Nachbarn überprüft. Wenn dort ein Baum steht, wird diese Nachbarzelle im neuen Gitterzustand ebenfalls zu einer Feuerzelle.

```python
current_fires = np.argwhere(grid == FIRE)

for x, y in current_fires:
    for nx, ny in get_neighbors(x, y, grid_size):
        if new_grid[nx, ny] == TREE:
            new_grid[nx, ny] = FIRE
```

In unserem Modell reicht es also aus, wenn ein Baum direkt neben einer brennenden Zelle steht. Dann beginnt er im nächsten Zustand zu brennen. Windrichtung, Feuchtigkeit, Hangneigung oder unterschiedliche Baumarten werden hier nicht berücksichtigt. Die Brandgröße hängt dadurch vor allem davon ab, wie zusammenhängend die Bäume im Gitter verteilt sind.

Nach der Ausbreitung werden alle Zellen, die im vorherigen Zeitschritt gebrannt haben, auf leer gesetzt. Damit brennt jede Feuerzelle genau einen Zeitschritt lang. Während der Simulation werden die Baumdichte, die Anzahl aktiver Feuerzellen, die Dauer einzelner Brände und die betroffene Brandfläche gespeichert. Aus diesen Daten werden nach der Simulation Zeitreihen und Histogramme erstellt.

Wir haben das Modell bewusst einfach gehalten, weil uns vor allem die grundlegende Dynamik aus Wachstum, Zündung, Ausbreitung und Abbrennen interessiert hat. Das Modell soll daher keine realen Waldbrände vorhersagen, sondern zeigen, wie aus einfachen lokalen Regeln und zufälligen Ereignissen größere Brandmuster entstehen können.