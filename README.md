# Müller & Ströbel: Nachbau

Statischer Nachbau von https://www.muellerundstroebel.de/ (Original: Webflow).
Kein Framework, kein Build-Schritt, keine externen Requests.

## Struktur

```
├── index.html          Startseite (Nav, Hero, Einsatzgebiete, Ergebnis, Kontakt, Footer, 6 Modals)
├── vercel.json         cleanUrls: /impressum statt /impressum.html
├── impressum.html      Impressum
├── datenschutz.html    Datenschutzerklärung
├── robots.txt          Freigabe inkl. KI-Crawler, Sitemap-Verweis
├── sitemap.xml         die drei kanonischen URLs
├── llms.txt            Positionierung in Klartext für KI-Systeme
├── styles.css          gesamtes Styling inkl. Breakpoints 991 / 767 / 479
├── script.js           Nav-Linie beim Scrollen, Mobile-Menü, Modals
├── tracking.js         GA4-Events, Modul-Tracking, Cookie-Einstellungen
├── assets/             Logo, Portraits, Icons, "&"-Zeichen, Favicon
└── fonts/              Poppins (300–700) + Lora (variabel), beide SIL Open Font License

Portraits liegen als WebP vor (493 KB als PNG, 38 KB als WebP). Das og-image
bleibt bewusst PNG, weil Social-Media-Crawler bei WebP unzuverlässig sind.
```

Alle drei Seiten teilen sich `styles.css` und `script.js`. Die Startseite trägt
`<body class="body">` (Poppins auf Schwarz), die Rechtsseiten laufen auf der
Webflow-Basis (Arial, `#333`), genau wie im Original.

## URLs

`vercel.json` setzt `cleanUrls`, damit die Adressen die der alten Webflow-Seite
bleiben:

| URL | liefert |
|---|---|
| `/` | Startseite |
| `/impressum` | Impressum |
| `/datenschutz` | Datenschutz |

`/impressum.html` leitet per 308 auf `/impressum` um. Interne Links und
Asset-Pfade sind absolut (`/styles.css`, `/assets/…`), damit sie unter jeder
dieser Adressen stimmen.

## Lokal ansehen

```bash
npx serve .          # kennt cleanUrls, verhält sich wie Vercel
# → http://localhost:3000
```

`python3 -m http.server` funktioniert auch, dort sind die Rechtsseiten aber nur
unter `/impressum.html` erreichbar.

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

Die Rechtsseiten wurden nach dem Abgleich auf Wunsch linksbündig gestellt (siehe
Punkt 3 unten). Der Nachweis oben bezieht sich auf den Stand davor.

## Ankernavigation

Klicks auf die Navigation und die CTA-Buttons gleiten zum Ziel statt zu
springen (`scroll-behavior: smooth`). Unter `prefers-reduced-motion: reduce`
bleibt der harte Sprung.

`section[id]` trägt ein `scroll-margin-top` in Höhe der fixen Navigation
(92 px, ab 991 px dann 80 px). Ohne das schnitt die Navigation auf 375 px die
Zielüberschrift um 16 px an.

## Tracking

Cookiebot als erstes Script im `<head>`, danach Consent Mode v2 mit allen
Kategorien auf `denied`, erst dann `gtag.js`. Google-Tag und eigene Skripte
tragen `data-cookieconsent="ignore"`, sonst blockiert Cookiebots Auto-Blocking
den Tag und der Consent Mode läuft nie an.

Vor der Einwilligung: `/g/collect` antwortet **204**, `page.cookies()` ist leer.

| Event | löst aus bei | Parameter |
|---|---|---|
| `kontakt_email` | Klick auf eine E-Mail-Adresse | `person`, `ziel` |
| `kontakt_telefon` | Klick auf eine Telefonnummer | `person`, `ziel` |
| `kontakt_linkedin` | Klick auf ein LinkedIn-Profil | `person`, `ziel` |
| `cta_klick` | Klick auf einen Button | `cta_label`, `cta_bereich` |
| `einsatzgebiet_geoeffnet` | Öffnen eines Modals | `thema` |
| `section_view_<id>` | Abschnitt wird sichtbar | `page`, `page_location` |
| `section_time_<id>` | Verweildauer je Abschnitt in Sekunden, gesendet bei Tab-Wechsel und Verlassen | `value`, `page`, `page_location` |

Die Seite hat kein Formular. Echte Conversions sind die Kontaktklicks, alles
andere sind Interessens-Signale. Die Sektion steckt im Event-Namen, das erspart
in GA4 die Anlage einer Custom Dimension.

Verweildauer: GA4 summiert `value` in der Metrik `eventValue`. Durchschnitt je
Sektion = `eventValue` geteilt durch die Anzahl der `section_view`-Events. Die
Uhr läuft nur bei sichtbarem Tab, Deckel 600 s, unter 1 s wird nichts gesendet.
Event-Namen und Parameter sind identisch mit admemory.de, damit dessen
Report-Skript ohne Umbau auch hier läuft.

## Bewusste Abweichungen

1. **Burger-Icon**: Original ist eine Lottie-Animation (lottie-web + JSON-Datei).
   Hier als Inline-SVG mit CSS-Transition nachgebaut, auf die gemessenen Maße des
   Originals (Linienbreite, Stärke, Abstand, Farbe `#1d1d1d`).
2. **Burger wird auf allen Seiten zum X.** Im Original ist die Öffnen-Animation
   nur an die Startseite gebunden, auf Impressum und Datenschutz bleiben die drei
   Striche stehen, obwohl das Menü offen ist. Hier wird der Burger überall zum X
   (betrifft 192 Pixel im geöffneten Menü der beiden Rechtsseiten).
3. **Impressum und Datenschutz linksbündig.** Im Original sitzt der Textblock
   mittig auf der Seite, mit großer Leerfläche rechts. Hier steht er auf derselben
   linken Kante wie Logo und Footer (x = 80 px bei 1440, x = 40 px ab 991, x = 20 px
   ab 767). Die Textbreite bleibt bei 48 rem, damit alle Zeilenumbrüche des
   Originals erhalten bleiben. Unterhalb von 768 px ändert sich nichts, dort war
   der Block ohnehin randbündig.
4. **Seitentitel Impressum**: im Original steht dort `<title>Datenschutz</title>`.
   Hier korrigiert zu "Impressum".
5. **Kein jQuery, kein Webflow-Runtime**: die drei Interaktionen sind rund
   90 Zeilen Vanilla-JS und ersetzen etwa 700 KB JavaScript.
6. **Fonts lokal** statt vom Webflow-CDN.
7. **Zugänglichkeit ergänzt**: `<button>` statt `<div>` für Menü und
   Schließen-Icon, `aria-expanded`, `role="dialog"`, Modal per Escape schließbar,
   "Mehr anzeigen" per Tastatur bedienbar, Fokus kehrt nach dem Schließen zurück.
   Fokusringe erscheinen nur bei Tastaturbedienung (`:focus-visible`), damit sich
   am Mausverhalten optisch nichts ändert.
8. **Semantisches Markup**: `<header>`, `<main>`, `<section>`, `<article>`,
   `<footer>` statt durchgehender `<div>`-Verschachtelung.
9. **URL-Struktur wie im Original** (`/impressum` statt `/impressum.html`),
   damit bereits indexierte Links und Lesezeichen weiter funktionieren.
