# Waldbrandmodell

## Abstract

In diesem Projekt wird ein vereinfachtes Waldbrand-System als zellulärer Automat auf einem zweidimensionalen Raster modelliert. Untersucht wird, wie Baumwachstum, Anfangsdichte und Blitzwahrscheinlichkeit die Häufigkeit und Größe von Brandereignissen beeinflussen. Das Modell arbeitet mit drei Zellzuständen: leer, Baum und Feuer. Bäume wachsen zufällig nach, Blitze entzünden einzelne Baumzellen, Feuer breitet sich lokal auf direkte Nachbarn aus und abgebrannte Zellen werden leer. Die Ergebnisse zeigen, dass hohe Baumdichte und seltene Zündungen größere Brandflächen begünstigen, während häufige Blitze eher viele kleinere Brandereignisse erzeugen. Die wichtigste Einschränkung ist, dass reale Einflussfaktoren wie Wind, Feuchtigkeit, Topographie, Baumarten und Löschmaßnahmen nicht berücksichtigt werden.

## 1. Introduction

Waldbrände sind räumliche Störungsereignisse, bei denen lokale Prozesse zu großflächigen Mustern führen können. Ob ein Brand klein bleibt oder sich stark ausbreitet, hängt wesentlich davon ab, wie viel brennbares Material vorhanden ist, wie dieses Material räumlich verteilt ist und wie häufig Zündereignisse auftreten.

Das Projekt orientiert sich an einfachen zellulären Automaten für Waldbrände. Dabei wird ein Wald als zweidimensionales Raster dargestellt. Jede Zelle besitzt genau einen Zustand: leer, Baum oder Feuer. Die Dynamik entsteht durch wenige Regeln: Bäume wachsen auf leeren Zellen nach, Blitze können Baumzellen entzünden, Feuer breitet sich auf benachbarte Baumzellen aus, und brennende Zellen werden anschließend leer.

Die Forschungsfrage lautet:
Wie beeinflussen Baumwachstum, Anfangsdichte und Blitzwahrscheinlichkeit die Häufigkeit und Größe von Waldbränden in einem Rastermodell?

Diese Frage ist mit dem Modell direkt untersuchbar, weil Baumwachstum, Anfangsdichte und Blitzwahrscheinlichkeit als Parameter variiert werden. Die Ergebnisse werden über Kennzahlen wie mittlere Baumdichte, Anzahl der Brandereignisse, mittlere Brandfläche und maximale Brandfläche ausgewertet. Dadurch kann untersucht werden, unter welchen Bedingungen viele kleine Brände oder wenige große Brandereignisse entstehen.

Ziel des Modells ist nicht die reale Vorhersage einzelner Waldbrände, sondern die Analyse grundlegender Systemmuster. Das Modell ist bewusst vereinfacht: Wind, Feuchtigkeit, Topographie, Baumarten, Altersstruktur und Löschmaßnahmen werden nicht berücksichtigt. Die Ergebnisse beschreiben daher Modellverhalten und keine reale Waldbrandprognose.

## 2. Method

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

In unserem Modell reicht es also aus, wenn ein Baum direkt neben einer brennenden Zelle steht. Dann beginnt er im nächsten Zustand zu brennen. Windrichtung oder unterschiedliche Baumarten werden hier nicht berücksichtigt. Die Brandgröße hängt dadurch vor allem davon ab, wie zusammenhängend die Bäume im Gitter verteilt sind.

Nach der Ausbreitung werden alle Zellen, die im vorherigen Zeitschritt gebrannt haben, auf leer gesetzt. Damit brennt jede Feuerzelle genau einen Zeitschritt lang. Während der Simulation werden die Baumdichte, die Anzahl aktiver Feuerzellen, die Dauer einzelner Brände und die betroffene Brandfläche gespeichert. Aus diesen Daten werden nach der Simulation Zeitreihen und Histogramme erstellt.

Wir haben das Modell bewusst einfach gehalten, weil uns vor allem die grundlegende Dynamik aus Wachstum, Zündung, Ausbreitung und Abbrennen interessiert hat. Das Modell soll daher keine realen Waldbrände vorhersagen, sondern zeigen, wie aus einfachen lokalen Regeln und zufälligen Ereignissen größere Brandmuster entstehen können.

## 3. Results

Die Parameterstudie zeigt deutliche Unterschiede zwischen den einzelnen Modellläufen. Die mittlere Baumdichte liegt in den meisten Szenarien zwischen etwa 0,3 und 0,4. Besonders niedrige Werte treten bei sehr häufigen Blitzen, lückigem Wald und im Grenzfall mit fast keinem Wald auf. Der Grenzfall mit extrem dichtem Wald zeigt dagegen eine künstlich hohe Baumdichte und ist daher nur eingeschränkt realistisch interpretierbar.
![Vergleich der mittleren Baumdichte](Bilder\mittlere_Bumdichte.png)

Die Anzahl der Brandereignisse nimmt vor allem mit der Blitzwahrscheinlichkeit zu. Besonders viele Brandereignisse entstehen bei lückigem Wald mit häufigen Blitzen sowie bei der vertauschten Größenordnung. Sehr seltene Blitze führen dagegen zu deutlich weniger Brandereignissen, weil Zündungen nur selten auftreten.
![Vergleich der Anzahl der Brandereignisse](Bilder\Brandereignisse.png)

Die mittlere Brandfläche bleibt in den meisten Läufen relativ klein. Auffällig sind jedoch einzelne Szenarien mit deutlich größeren mittleren Brandflächen, insbesondere dichter Wald mit seltenen Blitzen und der Grenzfall mit extrem dichtem Wald. 
![Vergleich der mittleren Brandflächen](Bilder\mittlere_Brandfläche.png)

Bei den maximalen Brandflächen treten die stärksten Unterschiede zwischen den Läufen auf. Besonders hohe Maximalwerte entstehen bei hoher Anfangsdichte, dichtem Wald mit seltenen Blitzen und im Grenzfall mit extrem dichtem Wald. Sehr häufige Blitze erzeugen dagegen viele kleinere Ereignisse.
![Vergleich der maximalen Brandflächen](Bilder\max_Brandfläche.png)

## 4. Discussion, Conclusion and Limitations

Die Forschungsfrage unseres Projekts besagt im Wesentlichen, unter welchen Bedingungen in einem einfachen Waldbrandmodell große Brandereignisse entstehen und welche Muster sich aus der Wechselwirkung von Baumwachstum, zufälliger Zündung und lokaler Feuerausbreitung ergeben. Die Simulationsergebnisse zeigen, dass bereits wenige einfache Regeln ausreichen, um eine komplexe Dynamik hervorzubringen. Es traten dabei viele kleine Brandereignisse auf, während große Brände deutlich seltener waren. Dieses Muster entspricht qualitativen Beobachtungen aus der Literatur zu sich selbst organisierten Systemen und deutet darauf hin, dass die räumliche Struktur des Waldes einen entscheidenden Einfluss auf die Brandgröße hat. 

Die Ergebnisse legen nahe, dass die Baumdichte eine zentrale Rolle für die Entstehung großer Brände spielt. Nach längeren brandfreien Phasen kann sich eine hohe Dichte zusammenhängender Baumcluster entwickeln. Wird ein solcher Cluster durch einen Blitz entzündet, kann sich das Feuer über viele Zeitschritte hinweg ausbreiten und sich über große Fläche ausbreiten. Sind allerdings nur kleine oder voneinander getrennte Baumgruppen vorhanden, bleiben Brandereignisse meist lokal begrenzt. Die beobachteten Schwankungen der Baumdichte spiegeln daher das Zusammenspiel von Regeneration und Zerstörung wider.

Die Forschungsfrage kann somit dahingehend beantwortet werden, dass große Waldbrände im Modell vor allem dann entstehen, wenn ausreichend große zusammenhängende Baumstrukturen vorhanden sind. Die Kombination aus kontinuierlichem Wachstum und seltenen Zündungen führt zu einer Dynamik, in der sich über längere Zeiträume Brennmaterial ansammelt und anschließend durch einzelne Ereignisse wieder reduziert wird. Unser Modell macht deutlich, wie komplexe Systemmuster ohne zentrale Steuerung allein durch lokale Interaktionen und stochastische Prozesse entstehen können.

Gleichzeitig müssen die Ergebnisse mit Vorsicht interpretiert werden. Unser Modell stellt keine realistische Vorhersage tatsächlicher Waldbrände dar, sondern eine stark vereinfachte Abstraktion. Alle Bäume sind von ihren Eigenschaften her ident und unterscheiden sich weder hinsichtlich ihrer Art noch ihres Alters oder ihrer Feuchtigkeit. Ebenso werden wichtige Einflussfaktoren wie Wind, Niederschlag, Geländeform oder unterschiedliche Vegetationstypen gänzlich vernachlässigt. Diese Faktoren beeinflussen reale Brandverläufe jedoch maßgeblich. 

Eine weitere Einschränkung besteht in der von uns verwendeten Von-Neumann-Nachbarschaft. Ein Feuer kann sich dort ausschließlich auf die vier direkten Nachbarzellen ausbreiten. Diagonale Ausbreitung ist nicht möglich, wodurch die räumliche Dynamik künstlich eingeschränkt wird. Darüber hinaus brennt jede Feuerzelle exakt einen Zeitschritt lang und wird anschließend unmittelbar zu einer leeren, schwarzen Zelle. In der Realität unterscheiden sich Brandintensität und Brenndauer jedoch deutlich zwischen verschiedenen Bereichen eines Waldes.
Auch die Annahme, dass während eines aktiven Brandes weder neues Baumwachstum noch weitere Blitzschläge auftreten können, vereinfacht die Prozesse erheblich. Diese Entscheidung haben wir bewusst getroffen, um einzelne Brandereignisse klar voneinander abzugrenzen und ihre Dauer sowie Fläche eindeutig bestimmen zu können. Gleichzeitig beeinflusst diese Modellierungsentscheidung die beobachteten Ergebnisse und sollte bei der Interpretation berücksichtigt werden.
Zusammenfassend greift unser Modell auf, dass einfache Regeln ausreichen, um typische Merkmale von Waldbranddynamiken hervorzubringen. Besonders die ungleiche Verteilung von Brandgrößen sowie die Wechselwirkung zwischen Aufbau und Abbau von Biomasse konnten nachvollzogen werden. Unser Modell eignet sich daher gut als Werkzeug, um grundlegende Mechanismen komplexer Systeme zu untersuchen und Konzepte wie Emergenz und Selbstorganisation zu veranschaulichen.
Für zukünftige Arbeiten könnte man verschiedene Erweiterungen realitätsnaher gestalten. Anbieten würden sich hier Faktoren wie Windrichtung und Windstärke, unterschiedliche Brennbarkeiten in Abhängigkeit von Feuchtigkeit oder Baumarten, periodische Randbedingungen, menschliche Eingriffe wie Löschmaßnahmen oder sowie anpassungsfähige Strategien zur Brandbekämpfung. Darüber hinaus könnten systematische Parameter-Sweeps durchgeführt werden, um den Einfluss von Wachstums- und Blitzwahrscheinlichkeiten quantitativ zu analysieren. Solche Erweiterungen könnten die Aussagekraft unseres Modells verbessern. Gleichzeitig würden sie das Modell jedoch komplexer machen und einen höheren Aufwand bei der empirischen Überprüfung und Validierung erfordern.

## References

Bak, P., Chen, K., & Tang, C. (1990). A forest-fire model and some thoughts on turbulence. Physics Letters A, 147(5–6), 297–300.

Drossel, B., & Schwabl, F. (1992). Self-organized critical forest-fire model. Physical Review Letters, 69(11), 1629–1632.







## Appendix A: ODD


## 1. Purpose Patterns

Ziel des Modells ist es, die Dynamik eines einfachen Waldbrand-Systems auf einem zweidimensionalen Gitter zu untersuchen. Das Modell beschreibt, wie Bäume zufällig nachwachsen, durch seltene Blitzereignisse entzündet werden und sich Feuer lokal über benachbarte Baumzellen ausbreitet.

Während eines aktiven Brandereignisses findet kein neues Baumwachstum statt und es kann kein neuer Blitzschlag ausgelöst werden. Dadurch wird jedes Brandereignis klar von der Regenerationsphase getrennt.

Das Modell eignet sich zur Untersuchung folgender Muster:

- Entwicklung der Baumdichte über die Zeit
- Anzahl aktiver Feuerzellen pro Zeitschritt
- Dauer einzelner Brandereignisse
- Größe beziehungsweise Fläche einzelner Brände
- Auftreten vieler kleiner und weniger großer Brände
- selbstorganisierte Dynamik durch lokale Interaktionen und stochastische Ereignisse

Das Modell orientiert sich an einem zellulären Automaten für Waldbrände. Es untersucht nicht einzelne reale Waldbrände im Detail, sondern abstrahierte Systemmuster, die durch Wachstum, Zündung, Ausbreitung und Abbrennen entstehen.

---

## 2. Entities, State Variables, Scales

### Entities

Die einzigen Entitäten des Modells sind Gitterzellen. Jede Zelle repräsentiert einen kleinen Bereich des Waldes.

### Zustandsvariablen der Zellen

Jede Zelle kann genau einen von drei Zuständen annehmen:

- `EMPTY = 0`: leere Zelle
- `TREE = 1`: Zelle enthält einen Baum
- `FIRE = 2`: Zelle brennt

### Globale Modellparameter

Die wichtigsten Parameter des Modells sind:

- `grid_size`: Seitenlänge des quadratischen Gitters
- `initial_density`: anfänglicher Anteil an Baumzellen
- `p_growth`: Wahrscheinlichkeit für Baumwachstum in einer leeren Zelle pro Zeitschritt
- `f_lightning`: Blitzwahrscheinlichkeit pro Baumzelle
- `steps`: Anzahl der Simulationsschritte
- `animate`: steuert die Animation der Simulation
- `animation_interval`: Intervall, in dem die Animation aktualisiert wird
- `tick_rate`: Geschwindigkeit der Animation
- `seed`: Startwert für den Zufallszahlengenerator

Im ausgeführten Modell werden folgende Werte verwendet:

- `grid_size = 100`
- `initial_density = 0.3`
- `p_growth = 0.01`
- `f_lightning = 0.0001`
- `steps = 2000`
- `animate = True`
- `animation_interval = 1`
- `tick_rate = 20`
- `seed = 42`

### Räumliche Skala

Das Modell verwendet ein quadratisches Gitter der Größe `grid_size × grid_size`. Im ausgeführten Beispiel besteht das Modell aus `100 × 100 = 10 000` Zellen.

### Zeitliche Skala

Die Simulation läuft in diskreten Zeitschritten. Im ausgeführten Beispiel werden 2000 Zeitschritte simuliert.

### Randbedingungen

Die Ränder des Gitters sind begrenzt. Es gibt keine periodischen Randbedingungen. Zellen am Rand haben daher weniger Nachbarn als Zellen im Inneren.

### Nachbarschaft

Das Modell verwendet eine Von-Neumann-Nachbarschaft. Eine Zelle interagiert nur mit ihren direkten Nachbarn oben, unten, links und rechts. Diagonale Nachbarn werden nicht berücksichtigt.

---

## 3. Prozessübersicht und Ablauf

In jedem Zeitschritt wird das Gitter synchron aktualisiert. Dazu wird zunächst eine Kopie des aktuellen Gitters erstellt. Auf dieser Kopie werden die Änderungen des aktuellen Zeitschritts gesammelt. Erst am Ende des Zeitschritts wird das alte Gitter durch das neue Gitter ersetzt.

Der Ablauf eines Zeitschritts ist:

1. Baumwachstum
2. Blitzschlag
3. Feuerausbreitung
4. Abbrennen brennender Zellen
5. Messung des aktuellen Brandereignisses
6. Speicherung der Beobachtungsgrößen
7. Aktualisierung des Gitters
8. optionale Animation

### 1. Baumwachstum

Leere Zellen können mit der Wahrscheinlichkeit `p_growth` zu Baumzellen werden. Baumwachstum findet nur statt, wenn gerade kein Brand aktiv ist.

Das bedeutet:

- Wenn kein Feuerereignis läuft, können leere Zellen zu Bäumen werden.
- Wenn ein Feuerereignis läuft, bleibt das Wachstum vollständig pausiert.

Diese Regel trennt die Wachstumsphase klar von der Brandphase.

### 2. Blitzschlag

Ein Blitz kann nur auftreten, wenn kein Brand aktiv ist. Dafür werden alle aktuellen Baumzellen gesucht. Aus der Anzahl der Baumzellen wird berechnet, wie wahrscheinlich es ist, dass mindestens ein Blitzereignis in diesem Zeitschritt auftritt.

Die verwendete Wahrscheinlichkeit lautet:

`1 - (1 - f_lightning) ** number_of_trees`

Tritt ein Blitz auf, wird genau eine zufällig ausgewählte Baumzelle entzündet. Es können also nicht mehrere neue Blitzschläge im gleichen Zeitschritt entstehen.

### 3. Feuerausbreitung

Alle Zellen, die im alten Gitterzustand brennen, übertragen das Feuer auf ihre direkten Nachbarzellen, sofern diese im neuen Gitterzustand Bäume sind.

Die Ausbreitung erfolgt lokal über die Von-Neumann-Nachbarschaft:

- oben
- unten
- links
- rechts

Diagonale Ausbreitung findet nicht statt.

### 4. Abbrennen brennender Zellen

Alle Zellen, die im vorherigen Zeitschritt gebrannt haben, werden im neuen Zustand leer. Eine Feuerzelle brennt also genau einen Zeitschritt lang und wird danach zu einer leeren Zelle.

### 5. Messung von Brandereignissen

Nach der Ausbreitung und dem Abbrennen wird geprüft, ob im neuen Gitter noch Feuerzellen vorhanden sind.

Wenn Feuerzellen vorhanden sind:

- Falls zuvor kein Brand aktiv war, beginnt ein neues Brandereignis.
- Die Branddauer wird um einen Zeitschritt erhöht.
- Die aktuell brennenden Zellen werden zur Menge der betroffenen Brandfläche hinzugefügt.

Wenn keine Feuerzellen vorhanden sind:

- Falls zuvor ein Brand aktiv war, endet das Brandereignis.
- Die Dauer des Brandes wird gespeichert.
- Die Anzahl der betroffenen Zellen wird als Brandfläche gespeichert.
- Die Variablen für das aktuelle Brandereignis werden zurückgesetzt.

Am Ende der Simulation wird ein noch aktiver Brand ebenfalls gespeichert.

---

## 4. Design Concepts

### Basic Principles

Das Modell basiert auf lokalen Zellinteraktionen. Globale Muster wie große Brandereignisse oder Veränderungen der Baumdichte entstehen aus einfachen lokalen Regeln:

- zufälliges Baumwachstum
- zufällige Zündung durch Blitz
- lokale Feuerausbreitung
- Abbrennen brennender Zellen

Es gibt keine zentrale Steuerung des Systems.

### Emergence

Emergente Muster entstehen durch die Kombination aus Wachstum, Zündung und Ausbreitung. Besonders relevant sind:

- zeitliche Schwankungen der Baumdichte
- Brandereignisse unterschiedlicher Größe
- seltene große Brände bei zusammenhängenden Baumclustern
- viele kleine Brände, wenn nur wenige zusammenhängende Baumzellen betroffen sind

Die Verteilung der Brandflächen ergibt sich aus der räumlichen Struktur des Waldes und der zufälligen Zündung.

### Adaptation

Die Zellen passen ihr Verhalten nicht aktiv an. Es gibt keine individuelle Strategie und keine Reaktion auf vergangene Ereignisse.

### Objectives

Die einzelnen Zellen besitzen keine Ziele. Das Modell verfolgt keine Optimierung, sondern simuliert Zustandsänderungen nach festen Regeln.

### Learning

Im Modell findet kein Lernen statt. Parameter und Regeln bleiben über die gesamte Simulation konstant.

### Prediction

Die Zellen oder das System treffen keine Vorhersagen. Die weitere Entwicklung ergibt sich ausschließlich aus dem aktuellen Zustand, den lokalen Regeln und Zufallsprozessen.

### Sensing

Eine Zelle nimmt nur den Zustand ihrer direkten Nachbarzellen wahr, wenn Feuer übertragen wird. Die Wahrnehmung ist lokal auf die Von-Neumann-Nachbarschaft beschränkt.

### Interaction

Die wichtigste Interaktion ist die Feuerausbreitung von brennenden Zellen auf benachbarte Baumzellen. Baumwachstum und Blitzschlag sind stochastische Prozesse.

### Stochasticity

Zufall spielt eine zentrale Rolle im Modell:

- Die anfängliche Baumverteilung wird zufällig erzeugt.
- Baumwachstum erfolgt zufällig mit Wahrscheinlichkeit `p_growth`.
- Blitzereignisse treten zufällig in Abhängigkeit von `f_lightning` und der Anzahl der Baumzellen auf.
- Wird ein Blitz ausgelöst, wird die getroffene Baumzelle zufällig ausgewählt.

Durch den Parameter `seed` kann die Simulation reproduzierbar gemacht werden.

### Collectives

Zusammenhängende Gruppen von Baumzellen bilden Baumcluster. Diese Cluster sind keine expliziten Agenten, beeinflussen aber die Brandgröße stark. Je größer und dichter ein Cluster ist, desto größer kann ein Brandereignis werden.

### Observation

Das Modell beobachtet und speichert folgende Größen:

- Baumdichte pro Zeitschritt
- Anzahl aktiver Feuerzellen pro Zeitschritt
- Dauer einzelner Brandereignisse
- Fläche einzelner Brandereignisse
- Parameter der Simulation

Zusätzlich werden Analyseplots erstellt:

1. Baumdichte über Zeit
2. aktive Feuerzellen über Zeit
3. Histogramm der Branddauer
4. Histogramm der Brandflächen

Außerdem werden zusammenfassende Kennwerte ausgegeben, zum Beispiel mittlere Baumdichte, maximale Baumdichte, Anzahl der Brandereignisse, mittlere Brandfläche und maximale Branddauer.

---

## 5. Initialisation

Zu Beginn wird ein quadratisches Gitter mit `grid_size × grid_size` Zellen erzeugt. Alle Zellen starten zunächst im Zustand `EMPTY`.

Anschließend wird für jede Zelle eine Zufallszahl gezogen. Ist diese kleiner als `initial_density`, wird die Zelle als Baumzelle initialisiert.

Im ausgeführten Beispiel gelten folgende Startwerte:

- Gittergröße: `100 × 100`
- anfängliche Baumdichte: `0.3`
- Baumwachstumswahrscheinlichkeit: `0.01`
- Blitzwahrscheinlichkeit: `0.0001`
- Anzahl der Zeitschritte: `2000`
- Zufallsseed: `42`

Durch den Seed ist die Simulation bei gleichen Parametern reproduzierbar.

---

## 6. Input Data

Das Modell verwendet keine externen Eingangsdaten. Alle Anfangszustände werden über Zufallszahlen erzeugt. Die Dynamik wird vollständig durch die im Code festgelegten Parameter und Regeln bestimmt.

---

## 7. Submodels

### 7.1 Nachbarschaftsmodell

Die Funktion `get_neighbors(x, y, size)` bestimmt die gültigen Nachbarn einer Zelle. Berücksichtigt werden nur direkte horizontale und vertikale Nachbarn. Randzellen besitzen entsprechend weniger Nachbarn.

Regeln:

- Wenn `x > 0`, existiert ein oberer Nachbar.
- Wenn `x < size - 1`, existiert ein unterer Nachbar.
- Wenn `y > 0`, existiert ein linker Nachbar.
- Wenn `y < size - 1`, existiert ein rechter Nachbar.

Es gibt keine diagonale Nachbarschaft und keine Verbindung über den Gitterrand hinweg.

### 7.2 Baumwachstum

Wenn kein Brand aktiv ist, werden alle leeren Zellen betrachtet. Für jede leere Zelle wird eine Zufallszahl gezogen. Ist diese kleiner als `p_growth`, wird die Zelle zu einem Baum.

Formal:

- Bedingung: Zelle ist leer und kein Brand ist aktiv.
- Übergang: `EMPTY → TREE`
- Wahrscheinlichkeit: `p_growth`

Während aktiver Brände findet kein Baumwachstum statt.

### 7.3 Blitzschlag

Wenn kein Brand aktiv ist, kann ein neuer Blitz auftreten. Dazu wird zunächst die Anzahl aller Baumzellen bestimmt. Aus dieser Anzahl wird die Wahrscheinlichkeit berechnet, dass mindestens ein Blitz auftritt:

`1 - (1 - f_lightning) ** number_of_trees`

Wenn ein Blitzereignis eintritt, wird genau eine Baumzelle zufällig ausgewählt und entzündet.

Formal:

- Bedingung: mindestens ein Baum vorhanden und kein Brand aktiv
- Übergang: `TREE → FIRE`
- maximal ein neu entzündeter Baum pro Zeitschritt

Während aktiver Brände können keine neuen Blitzschläge auftreten.

### 7.4 Feuerausbreitung

Für alle Zellen, die im alten Gitterzustand brennen, werden die direkten Nachbarn geprüft. Wenn ein Nachbar im neuen Gitterzustand ein Baum ist, wird er entzündet.

Formal:

- Bedingung: Nachbarzelle ist `TREE`
- Übergang: `TREE → FIRE`
- Ausbreitung nur über direkte Nachbarn

### 7.5 Abbrennen

Alle Zellen, die im alten Gitterzustand gebrannt haben, werden im neuen Zustand leer.

Formal:

- Übergang: `FIRE → EMPTY`
- Dauer einer einzelnen Feuerzelle: ein Zeitschritt

### 7.6 Brandereignis-Erfassung

Ein Brandereignis beginnt, sobald nach einem Zeitschritt mindestens eine Feuerzelle vorhanden ist und vorher kein Brand aktiv war.

Während des Brandes werden gezählt:

- die Dauer des Brandes in Zeitschritten
- die Menge aller Zellen, die während des Brandes gebrannt haben

Ein Brandereignis endet, sobald keine Feuerzellen mehr vorhanden sind. Danach werden Branddauer und Brandfläche gespeichert.

### 7.7 Beobachtungs- und Auswertungsmodell

Nach jedem Zeitschritt werden die Baumdichte und die Anzahl aktiver Feuerzellen gespeichert.

Nach Ende der Simulation werden zusätzlich folgende Auswertungen durchgeführt:

- Zeitreihe der Baumdichte
- Zeitreihe der aktiven Feuerzellen
- Histogramm der Branddauern
- Histogramm der Brandflächen
- textuelle Zusammenfassung der wichtigsten Kennwerte

---

## 8. Zentrale Annahmen und Vereinfachungen

Das Modell enthält mehrere Vereinfachungen gegenüber realen Waldbränden:

- Alle Bäume sind gleich brennbar.
- Wind, Topographie und Feuchtigkeit werden nicht berücksichtigt.
- Feuer breitet sich nur in vier Richtungen aus.
- Eine brennende Zelle brennt genau einen Zeitschritt.
- Während eines aktiven Brandes wachsen keine neuen Bäume.
- Während eines aktiven Brandes kann kein neuer Blitz auftreten.
- Pro Zeitschritt kann maximal ein neuer Blitz eine Baumzelle entzünden.
- Es gibt keine Löschmaßnahmen.
- Es gibt keine unterschiedlichen Baumarten oder Altersstrukturen.
- Das Modell nutzt begrenzte Ränder ohne periodische Fortsetzung.

---

## 9. Mögliche Erweiterungen

Mögliche Erweiterungen des Modells wären:

- Einführung von Windrichtung und Windstärke
- unterschiedliche Brennwahrscheinlichkeiten je nach Feuchtigkeit
- diagonale Feuerausbreitung durch Moore-Nachbarschaft
- periodische Randbedingungen
- verschiedene Baumarten
- Alter der Bäume als zusätzliche Zustandsvariable
- Löschmaßnahmen oder Brandschneisen
- menschliche Eingriffe
- KI-gestützte Strategien zur Verhinderung oder Verlangsamung der Ausbreitung
- Untersuchung verschiedener Parameterkombinationen für `p_growth` und `f_lightning`