# Müller & Ströbel: Nachbau

Statischer Nachbau von https://www.muellerundstroebel.de/ (Original: Webflow).
Kein Framework, kein Build-Schritt, keine externen Requests.

## Struktur

```
├── index.html          Startseite (Nav, Hero, Einsatzgebiete, Ergebnis, Kontakt, Footer, 6 Modals)
├── impressum.html      Impressum
├── datenschutz.html    Datenschutzerklärung
├── styles.css          gesamtes Styling inkl. Breakpoints 991 / 767 / 479
├── script.js           Nav-Linie beim Scrollen, Mobile-Menü, Modals
├── assets/             Logo, Portraits, Icons, "&"-Zeichen, Favicon
└── fonts/              Poppins (300–700) + Lora (variabel), beide SIL Open Font License
```

Alle drei Seiten teilen sich `styles.css` und `script.js`. Die Startseite trägt
`<body class="body">` (Poppins auf Schwarz), die Rechtsseiten laufen auf der
Webflow-Basis (Arial, `#333`), genau wie im Original.

## Lokal ansehen

```bash
python3 -m http.server 8899
# → http://localhost:8899/index.html
```

Für GitHub Pages: Settings → Pages → Branch `main`, Ordner `/ (root)`.

## Abgleich mit dem Original (Stand 18.08.2026)

Verglichen per Headless-Chrome-Screenshot gegen die Live-Seite, jeweils Vollseite
und pixelweise (pixelmatch). Ergebnis überall: **0 abweichende Pixel**.

| | geprüft |
|---|---|
| Breiten | 1920, 1600, 1440, 1280, 1024, 991, 834, 768, 640, 560, 512, 480, 479, 390, 375, 360, 320 (dsf 1–3) |
| Zustände | Grundzustand, Scroll-Positionen (Nav-Linie), offenes Mobile-Menü (375/768/991), alle 6 Modals (1440 und 375) |
| Hover | Buttons, Karten, Navi-Links, Kontaktzeilen, Footer-Links, "Mehr anzeigen", Logo (via CDP `CSS.forcePseudoState`) |
| Rechtsseiten | Impressum und Datenschutz auf 1920, 1280, 991, 768, 480, 375, 320 |

Seitenhöhen identisch: 3404 px (Start @1440), 4749 px (Start @375),
1161 px (Impressum @1440), 6772 px (Datenschutz @1440).

## Bewusste Abweichungen

1. **Burger-Icon**: Original ist eine Lottie-Animation (lottie-web + JSON-Datei).
   Hier als Inline-SVG mit CSS-Transition nachgebaut, auf die gemessenen Maße des
   Originals (Linienbreite, Stärke, Abstand, Farbe `#1d1d1d`).
2. **Burger wird auf allen Seiten zum X.** Im Original ist die Öffnen-Animation
   nur an die Startseite gebunden, auf Impressum und Datenschutz bleiben die drei
   Striche stehen, obwohl das Menü offen ist. Das ist die einzige Stelle, an der
   der Nachbau bewusst vom Original abweicht (192 Pixel im geöffneten Menü).
3. **Seitentitel Impressum**: im Original steht dort `<title>Datenschutz</title>`.
   Hier korrigiert zu "Impressum".
4. **Kein jQuery, kein Webflow-Runtime**: die drei Interaktionen sind rund
   90 Zeilen Vanilla-JS und ersetzen etwa 700 KB JavaScript.
5. **Fonts lokal** statt vom Webflow-CDN.
6. **Zugänglichkeit ergänzt**: `<button>` statt `<div>` für Menü und
   Schließen-Icon, `aria-expanded`, `role="dialog"`, Modal per Escape schließbar,
   "Mehr anzeigen" per Tastatur bedienbar, Fokus kehrt nach dem Schließen zurück.
   Fokusringe erscheinen nur bei Tastaturbedienung (`:focus-visible`), damit sich
   am Mausverhalten optisch nichts ändert.
7. **Semantisches Markup**: `<header>`, `<main>`, `<section>`, `<article>`,
   `<footer>` statt durchgehender `<div>`-Verschachtelung.
8. **Interne Links relativ** (`index.html`, `impressum.html`), damit die Seite
   auch in einem Unterordner läuft, etwa unter GitHub Pages.
