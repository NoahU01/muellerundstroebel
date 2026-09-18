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
| `vorschau.py` | erzeugt die Vorschaubilder für den Download-Kasten |
| `skizze.py` | schneidet eine Grafik aus einer PDF-Seite als SVG heraus |

Maße stehen in Punkt (pt), weil das PDF darin rechnet: A4 ist 595,28 × 841,89 pt,
der Satzspiegel hat 20 mm Rand (56,7 pt). Schriften (`fonts/`), Farben und das
Logo sind dieselben wie auf der Website – Änderungen am Markenauftritt wirken
damit automatisch auch in den PDFs.

## Neues Dokument anlegen

1. Eine bestehende HTML-Datei kopieren und Texte austauschen.
2. In `bauen.py` unter `DOKUMENTE` eintragen: Quelldatei → Zielname.
3. `python3 pdf/bauen.py` laufen lassen.
4. Auf der zugehörigen Seite verlinken (`assets/downloads/<name>.pdf`).

Es gibt zwei Dokumenttypen, beide aus derselben Vorlage:

- **Seminarbeschreibung** (3 Seiten): Deckblatt, „Auf einen Blick" mit zwei
  Spalten, Kontaktseite. Beispiele: die beiden Aufsichtsrats-Dokumente.
- **Themenüberblick** (5 Seiten): Deckblatt, Ausgangslage mit Vorgehen,
  „Im Detail" mit Ergebnisblock, typische Themen, Kontaktseite.

Die Bausteine dafür stehen in `vorlage.css` und sind kommentiert. Was je
Dokument abweicht (Breite des Deckblatt-Textes, Position der Blöcke, die von
der Textlänge abhängen), steht als `style`-Angabe direkt im HTML.

## Vorschaubilder

Die Download-Kästen auf den Themenseiten zeigen Seite 1 und 2 des PDFs:

```bash
python3 pdf/vorschau.py                 # alle
python3 pdf/vorschau.py geschaeftsmodell # einzeln
```

Nach jeder inhaltlichen Änderung an einem dieser PDFs neu erzeugen,
sonst zeigt der Kasten den alten Stand.

## Prüfen gegen ein bestehendes PDF

`bauplan.py` liest aus einem PDF jede Textzeile mit Position, Schriftgröße und
Farbe sowie die gefüllten Flächen:

```bash
python3 pdf/bauplan.py assets/downloads/aufsichtsrat-fit-and-proper.pdf
```

Damit wurde jeder Nachbau gegen sein altes PDF abgeglichen. Anteil der Elemente
innerhalb von 1,5 pt: Fit & Proper 99 %, Strategie im Aufsichtsrat 92 %,
Geschäftsmodell 80 %, Komplexe Themen 79 %, Strategie verankern 74 %.
Die Abweichungen der Themen-Dokumente sind Zeilenumbrüche, die bei etwas
anderer Schriftbreite anders fallen – im Druckbild nicht sichtbar.

## Bewusste Abweichungen vom alten Stand

1. **Dauer Fit & Proper**: „Halber Tag · ca. 3 Stunden" → „1 Tag" (Deckblatt und
   Feld „Dauer").
2. **Graue Linie unter dem Logo** auf den Innenseiten entfernt, in allen fünf
   Dokumenten. Die Linie über dem Impressum auf der Kontaktseite bleibt.
