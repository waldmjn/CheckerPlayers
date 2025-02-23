# CheckerPlayers

## Kurzfassung
Beschreibung: Der Checkers Player ist ein KI-Programm, das entwickelt wurde, um das Spiel Dame zu spielen. Funktionsweise: Diese Programme verwenden Suchalgorithmen und Heuristiken, um optimale Züge zu berechnen. Oft wird ein Minimax-Algorithmus genutzt, der die möglichen Züge und deren Konsequenzen bewertet, um den besten Zug auszuwählen. Es wurde sich ebenfalls an einem MCTS-Algorithmus probiert.


## Überblick
Das Projekt handelt von der Implementierung eines klassichen Dame-Spiels mit einer grafischen Benutzeroberfläche, sowie mit zwei verwendete Algorithmen, die die Spielzüge für den "Gegner" berechnen:
- Minimax-Algorithmus mit Alpha-Beta-Pruning
- Monte Carlo Tree Search (MCTS) (nicht erfolgreich)

Die GUI basiert auf Tkinter, während die Spiellogik in einer separaten Klasse ist. Der Spieler kann ziwschen zwei Schwierigkeitsstufen wählen, die aufgrund der Suchtiefe des Minimax basieren. 

## Projekstruktur
- main.py: Startet die GUI und lädt das Spiel
- checkers_gui.py: Verwaltet die grafische Benutzeroberfläche und gibt das traditionelle Damebrett wieder.
- checker_games.py: Beinhaltet die Spielmechanik und die jeweiligen Algorithmen.

## Algorithmen
1. Minimax mit Alpha-Beta-Pruning:
    - Bewertet verschiedene Spielzüge bis zu einer bestimmten Tiefe.
    - Maximiert die eigenen Vorteile und minimiert die Chancen des Gegners.
2. Monte Carlo Tree Search (MCTS) (Fehlgeschlagen!):
    - MCTS simuliert zufällige Partien, um die besten Züge zu bestimmen.
    - Nach einer gewissen Zeit stürzt das Programm jedoch ab, was auf Probleme mit der Rekursionstiefe oder der Speichernutzung hindeutet.


