 
 # 1. Purpose Patterns

Ziel des Modells ist es, das Verhalten realer Waldbrände zu simulieren. 
Auf einem Gitter wachsen Bäume mit einer gewissen Wahrscheinlichkeit nach, ein zufälliger Blitz zündet mit kleiner Wahrscheinlichkeit eine Zelle und das Feuer breitet sich auf benachbarte Bäume aus.
Stark schiefe Größenverteilung - viele kleine und wenig extrem große Brände. (Potenzgesetz-Verteilung)
Erreichen eines kritischen Zustands ohne externe Feinabstimmung (Self-Organized Critically) - Parameter müssen nicht exakt eingestellt werden um einen Zustand zu erreichen.


# 2. Entities, State Variables, Scales


Entities:
Gitterzellen

Zustandsvariablen:
Leer
Baum
Feuer

Wahrscheinlichkeit für Baumwachstum pro Zeitschritt p
Wahrscheinlichkeit für Blitzschlag f

Scales:
Zeitschritte
Gittergröße/Zellengröße

# 3. Prozessübersicht und Ablauf

In jedem Zeitschritt werden folgende Prozesse ausgeführt:

Baumwachstum:
Leere Zellen werden mit Wahrscheinlichkeit p zu Bäumen.
Blitzschlag:
Jede Baumzelle wird mit Wahrscheinlichkeit f entzündet.
Feuerausbreitung:
Brennende Zellen setzen benachbarte Baumzellen in Brand.
Abbrennen:
Brennende Zellen werden im nächsten Schritt leer.

# 4. Design Concepts

Basic Principles
Lokale Interaktionen führen zu globalen Mustern.
Keine zentrale Steuerung → emergentes Verhalten.
Selbstorganisation in einen kritischen Zustand (Self-Organised Criticality)

Emergence
Auftreten von Potenzgesetz-Verteilungen der Brandgrößen
Große Brände entstehen selten, kleine häufig 
Kein globaler Mechanismus steuert diese Verteilung 


Adaptation
Keine aktive Anpassung einzelner Entitäten.

Objectives
Keine individuellen Ziele

Learning
Kein Lernen im Modell

Prediction
Keine explizite Vorhersage durch Agenten

Sensing
Zellen „erkennen“ nur den Zustand ihrer Nachbarn

Interaction
Feuer breitet sich lokal von Zelle zu Zelle aus

Stochasticity
Baumwachstum und Blitzschläge mit gewisser Wahrscheinlichkeit
Zufälligkeit ist zentral für die Dynamik

Collectives
(Cluster von Bäumen bilden zusammenhängende Strukturen, die als „Brennstoff“ für Großbrände dienen)

Observation
Größe einzelner Brände
Verteilung der Brandgrößen
Dichte von Bäumen


# 5. Initialisierung

Gitter startet leer oder mit zufälliger Verteilung von Bäumen
Parameter p (Baumwachstum) und f (Blitzschlag) definieren die Dynamik


# 6. Input Data

Keine externen Daten notwendig

# 7. Submodelle

Baumwachstum:
Für jede leere Zelle mit Wahrscheinlichkeit p → Baum

Blitzschlag:
Für jede Baumzelle mit Wahrscheinlichkeit f → brennend

Feuerausbreitung:
Wenn eine Zelle brennt: Alle benachbarten Baumzellen → brennend

Abbrennen:
Brennende Zellen → leer im nächsten Zeitschritt


# TD
Ränder (wie sehen diese aus? begrenzt?), Art der Nachbarschaft (Von Neumann etc...), Purpose (konkrete Forschungsfrage/Aussage - was wollen wir untersuchen), Gitter- und Zellengröße konkret festlegen, Modellerweiterung mit KI überlegen (Maßnahmen die Ausbreitung verhindern/verlangsamen), synchron/asynchron?