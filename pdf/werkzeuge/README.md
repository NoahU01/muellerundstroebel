# Sichtprüfung der fertigen PDFs

Chrome druckt manche CSS-Effekte anders als am Bildschirm (z. B. weiche Schatten als graue Rechtecke).
Deshalb nach jedem Bau das **echte PDF** prüfen, nicht nur die HTML-Vorlage:

```bash
swiftc -O pdf/werkzeuge/pdfbild.swift -o /tmp/pdfbild
swiftc -O pdf/werkzeuge/uebersicht.swift -o /tmp/uebersicht
mkdir -p /tmp/pdfb && /tmp/pdfbild entwicklung/downloads/business-story-2.pdf /tmp/pdfb   # je Seite ein PNG
/tmp/uebersicht /tmp/ueb.png /tmp/pdfb/pdf-{1..8}.png                                       # Kontaktbogen
```
