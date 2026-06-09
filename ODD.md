
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