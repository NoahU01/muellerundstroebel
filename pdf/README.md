# PDF-Quellen

Die PDFs unter `assets/downloads/` werden hier gebaut. Vorher lagen sie nur als
fertige Datei im Repo, ohne Quelle – eine Änderung wie „halber Tag" → „1 Tag"
hätte bedeutet, das Dokument neu zu bauen.

## Bauen

```bash
python3 pdf/bauen.py                 # alle Dokumente
python3 pdf/bauen.py fit-and-proper  # nur passende
```

Gedruckt wird mit Google Chrome im Headless-Modus über einen kurzlebigen
lokalen Server (Chrome lädt Schriften und Bilder nicht von `file://`).
Das Ergebnis landet direkt in `assets/downloads/`.

## Aufbau

| | |
|---|---|
| `vorlage.css` | gemeinsames Layout: Seitenformat, Typografie, Farben, Bausteine |
| `<dokument>.html` | Inhalt eines Dokuments, nur Text und Struktur |
| `bausteine/` | Grafiken, die nur in den PDFs vorkommen |
| `bauen.py` | Druckskript, enthält die Liste der Dokumente |
| `bauplan.py` | Prüfwerkzeug, siehe unten |

Maße stehen in Punkt (pt), weil das PDF darin rechnet: A4 ist 595,28 × 841,89 pt,
der Satzspiegel hat 20 mm Rand (56,7 pt). Schriften (`fonts/`), Farben und das
Logo sind dieselben wie auf der Website – Änderungen am Markenauftritt wirken
damit automatisch auch in den PDFs.

## Neues Dokument anlegen

1. Eine bestehende HTML-Datei kopieren und Texte austauschen.
2. In `bauen.py` unter `DOKUMENTE` eintragen: Quelldatei → Zielname.
3. `python3 pdf/bauen.py` laufen lassen.
4. Auf der zugehörigen Seite verlinken (`assets/downloads/<name>.pdf`).

Ein Dokument besteht aus drei Seiten: Deckblatt (`seite--navy`), Innenseite
(zwei Spalten) und Kontaktseite. Die Bausteine dafür stehen in `vorlage.css`
und sind kommentiert.

## Prüfen gegen ein bestehendes PDF

`bauplan.py` liest aus einem PDF jede Textzeile mit Position, Schriftgröße und
Farbe sowie die gefüllten Flächen:

```bash
python3 pdf/bauplan.py assets/downloads/aufsichtsrat-fit-and-proper.pdf
```

Damit wurde der Nachbau gegen das alte PDF abgeglichen: 105 von 119 Elementen
liegen innerhalb von 1,5 pt, die übrigen sind die bewusste Inhaltsänderung
(Dauer) und Rundungen.

## Bewusste Abweichungen vom alten Stand

1. **Dauer Fit & Proper**: „Halber Tag · ca. 3 Stunden" → „1 Tag" (Deckblatt und
   Feld „Dauer").
2. **Graue Linie unter dem Logo** auf den Innenseiten entfernt.
