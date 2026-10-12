#!/usr/bin/env python3
"""Marketing › Corporate Design › Geschäftsausstattung (nur Branch daniel).

Baut entwicklung/corporate-design.html (Übersicht) und entwicklung/geschaeftsausstattung.html
(beginnend mit den LinkedIn-Bannern) und exportiert die Banner als PNG nach entwicklung/ga/linkedin/.
Vorbild: empiria-Repo site/projekte/ga-linkedin.html (Schutzzonen, Ansicht wie auf LinkedIn).
Ein Banner ist ein Baustein in cqw-Einheiten: gleiche Gestaltung in der Vorschau und im PNG.

    python3 entwicklung/bs/ga.py
"""
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "pdf"))
import bs2 as b
import bauen as druck

WURZEL = Path(__file__).resolve().parents[2]
ZIEL = WURZEL / "entwicklung"
PNG = ZIEL / "ga" / "linkedin"

FORMATE = {  # Breite, Höhe, Text links ab (cqw), Schutzzone
    "person": (1584, 396, 29.7, "Profilfoto"),
    "firma": (1128, 191, 22.2, "Firmenlogo"),
}
VARIANTEN = [
    ("weiss", "Weiß", "Ruhig wie die Startseite: weiße Fläche, Navy-Schrift, „umsetzen.“ in Taupe, rechts das skizzierte &.",
     {"bg": "#ffffff", "fg": "#082638", "hl": "#998675", "kicker": "#7a6757"}, "/entwicklung/pdf-bs2/ampersand-konstruktion-hell.svg"),
    ("sand", "Weiß auf Sand", "Wie Nr. 1, nur auf der Sandfläche der Startseite: wärmer, gleiche Schrift, gleiches skizziertes &.",
     {"bg": "#f6f3ef", "fg": "#082638", "hl": "#998675", "kicker": "#7a6757"}, "/entwicklung/pdf-bs2/ampersand-konstruktion-hell.svg"),
    ("navy", "Navy mit Anschnitt", "Wie das Deckblatt des PDFs: Navy-Fläche, weiße Schrift, das skizzierte & im Anschnitt.",
     {"bg": "#082638", "fg": "#ffffff", "hl": "#cbbcae", "kicker": "#cbbcae"}, "/pdf/bausteine/ampersand-konstruktion.svg"),
    ("dreiklang", "Der Weg auf Blau", "Unser Vorgehen als Linie mit drei Stationen – Strukturieren, Entscheiden, Umsetzen. Auf dem Blau aus dem Corporate Design, ohne &.",
     {"bg": "#185e8a", "fg": "#ffffff", "hl": "#cbbcae", "kicker": "#d9e6ef"}, ""),
]
KICKER = "Für Führungskräfte in der Versicherungsbranche"
CLAIM = "Komplexe Situationen<br>strukturieren, entscheiden, <i>umsetzen.</i>"


def banner(fmt, var):
    w, h, links, _ = FORMATE[fmt]
    key, _, _, f, amp = var
    hoch = h / w * 100
    if key == "dreiklang":
        gr = (1.05, 3.3) if fmt == "person" else (.95, 3.0)
        return (f'<div class="lb" style="aspect-ratio:{w}/{h};--bg:{f["bg"]};--fg:{f["fg"]};--hl:{f["hl"]};--ki:{f["kicker"]}">'
                f'<div class="lb__text" style="left:{links}cqw;right:5cqw"><p class="lb__kicker" style="font-size:{gr[0]}cqw">{KICKER}</p>'
                f'<ol class="lb__weg" style="font-size:{gr[1]}cqw"><li>Strukturieren</li><li>Entscheiden</li><li class="lb__ziel">Umsetzen.</li></ol></div></div>')
    if fmt == "person":
        txt = f'<div class="lb__text" style="left:{links}cqw"><p class="lb__kicker" style="font-size:1.05cqw">{KICKER}</p><h2 style="font-size:2.9cqw">{CLAIM}</h2></div>'
        amp_stil = {"weiss": "left:80cqw;top:-1.5cqw;width:26cqw", "sand": "left:80cqw;top:-1.5cqw;width:26cqw", "navy": "left:80cqw;top:-1.5cqw;width:26cqw"}.get(key, "")
    else:
        txt = f'<div class="lb__text" style="left:{links}cqw"><p class="lb__kicker" style="font-size:.95cqw">{KICKER}</p><h2 style="font-size:2.55cqw">{CLAIM}</h2></div>'
        amp_stil = {"weiss": "left:82cqw;top:-1cqw;width:18cqw", "sand": "left:82cqw;top:-1cqw;width:18cqw", "navy": "left:82cqw;top:-1cqw;width:18cqw"}.get(key, "")
    return (f'<div class="lb" style="aspect-ratio:{w}/{h};--bg:{f["bg"]};--fg:{f["fg"]};--hl:{f["hl"]};--ki:{f["kicker"]}">'
            f'{txt}<img class="lb__amp" src="{amp}" alt="" style="{amp_stil}"></div>')


def ansicht(fmt, var):
    """Banner so, wie es auf LinkedIn erscheint (Foto bzw. Logo links unten darüber)."""
    if fmt == "person":
        p = b.PERSONEN["daniel"]
        ueber = '<span class="li-foto" style="background-image:url(/assets/daniel-portrait.webp)"></span>'
        info = (f'<div class="li-info"><p class="li-name">{p["name"]}</p><p class="li-rolle">{p["kurz"]}</p>'
                '<div class="li-knoepfe"><span>Vernetzen</span><span>Nachricht</span></div></div>')
    else:
        ueber = '<span class="li-logo"><img src="/assets/favicon.svg" alt="Müller &amp; Ströbel"></span>'
        info = ('<div class="li-info li-info--firma"><p class="li-name">Müller &amp; Ströbel</p><p class="li-rolle">Komplexe Situationen strukturieren, entscheiden, umsetzen.</p>'
                '<div class="li-knoepfe"><span>+ Folgen</span><span>Website ansehen</span></div></div>')
    return f'<div class="li li--{fmt}"><div class="li-banner">{banner(fmt, var)}{ueber}</div>{info}</div>'


def schutzzonen():
    return '''<div class="ga-zwei">
  <figure><div class="lz" style="aspect-ratio:1584/396"><span class="lz-foto" style="left:2.97%;top:44.19%;width:18.94%"></span><span class="lz-text" style="left:23.4%">Profilfoto – hier nichts Wichtiges</span></div><figcaption>Personenprofil · 1584 × 396 px</figcaption></figure>
  <figure><div class="lz" style="aspect-ratio:1128/191"><span class="lz-foto lz-foto--eckig" style="left:2.66%;top:57.59%;width:12.06%"></span><span class="lz-text" style="left:16.8%">Firmenlogo</span></div><figcaption>Unternehmensseite · 1128 × 191 px</figcaption></figure>
</div>'''


def geschaeftsausstattung():
    zeilen = ""
    nummern = {"weiss": "1", "sand": "1b", "navy": "2", "dreiklang": "3"}
    for var in VARIANTEN:
        key, titel, text, _, _ = var
        i = nummern.get(key, "")
        figs = "".join(
            f'<figure>{ansicht(fmt, var)}<figcaption>{"Personenprofil · 1584 × 396 px" if fmt == "person" else "Unternehmensseite · 1128 × 191 px"}'
            f' · <a href="/entwicklung/ga/linkedin/linkedin-{fmt}-{key}.png" download>PNG laden</a></figcaption></figure>' for fmt in ("person", "firma"))
        zeilen += f'<div class="ga-var"><h3>{i} · {titel}</h3><p>{text}</p><div class="ga-zwei">{figs}</div></div>'
    main = f"""
<section class="held held--klein"><div class="wrap">
  <p class="kicker">Corporate Design</p>
  <h1>Geschäftsausstattung</h1>
  <p class="lead">Alles, was Müller &amp; Ströbel im Alltag nach außen zeigt. Wir beginnen mit den LinkedIn-Bannern für Tobias, Daniel und die Unternehmensseite.</p>
</div></section>

<section class="sek sek--sand" id="linkedin"><div class="wrap">
  <p class="kicker">LinkedIn-Banner</p>
  <h2 class="h2">Drei Varianten, Nr. 1 zusätzlich auf Sand – je für das Profil und die Unternehmensseite.</h2>
  <p class="lead">Gezeigt in der Ansicht von LinkedIn. Tobias und Daniel nutzen dasselbe Banner.</p>
  <div class="ga-block"><h3>Wo Foto und Logo liegen</h3><p>LinkedIn legt Profilfoto bzw. Firmenlogo links unten über das Banner. Dort steht deshalb nichts Wichtiges.</p>{schutzzonen()}</div>
  {zeilen}
</div></section>"""
    html = b.seite("Müller &amp; Ströbel – Geschäftsausstattung", "Geschäftsausstattung: LinkedIn-Banner", "ga", "", main)
    return html.replace("</head>", f'<link rel="stylesheet" href="/entwicklung/ga.css?v={b.VERSION}">\n</head>', 1)


def corporate_design():
    main = """
<section class="held held--klein"><div class="wrap">
  <p class="kicker">Marketing</p>
  <h1>Corporate Design</h1>
  <p class="lead">Lora und Poppins, Navy, Blau, Taupe und Sand, Porträts im Kreis mit weißem Rand. Hier liegt alles, was wir daraus gestalten.</p>
</div></section>

<section class="sek sek--sand"><div class="wrap">
  <div class="bsu-karten"><a class="bsu-karte" href="/entwicklung/geschaeftsausstattung.html"><h3>Geschäftsausstattung</h3><p>Beginnend mit den LinkedIn-Bannern für Tobias, Daniel und die Unternehmensseite.</p><span class="bsu-pfeil" aria-hidden="true">&rarr;</span></a></div>
</div></section>"""
    html = b.seite("Müller &amp; Ströbel – Corporate Design", "Corporate Design von Müller & Ströbel", "cd", "", main)
    return html.replace("</head>", f'<link rel="stylesheet" href="/entwicklung/storyboard.css?v={b.VERSION}">\n</head>', 1)


def png_export():
    PNG.mkdir(parents=True, exist_ok=True)
    browser = druck.chrome()
    srv = druck.server_starten()
    time.sleep(.4)
    try:
        for var in VARIANTEN:
            for fmt, (w, h, _, _) in FORMATE.items():
                quelle = ZIEL / "ga" / "_banner.html"
                quelle.write_text(f'''<!DOCTYPE html><html><head><meta charset="utf-8"><link rel="stylesheet" href="/entwicklung/business-story-2.css?v={b.VERSION}"><link rel="stylesheet" href="/entwicklung/ga.css?v={b.VERSION}">
<style>html,body{{margin:0;padding:0;background:#fff;overflow:hidden}}.export{{width:{w}px}}</style></head><body><div class="export">{banner(fmt, var)}</div></body></html>''', encoding="utf-8")
                ziel = PNG / f"linkedin-{fmt}-{var[0]}.png"
                subprocess.run([browser, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size={w},{h}",
                                "--virtual-time-budget=4000", f"--screenshot={ziel}", f"http://127.0.0.1:{druck.PORT}/entwicklung/ga/_banner.html"],
                               capture_output=True)
                print("  PNG", ziel.relative_to(WURZEL))
        quelle.unlink()
    finally:
        srv.shutdown()


if __name__ == "__main__":
    (ZIEL / "geschaeftsausstattung.html").write_text(geschaeftsausstattung(), encoding="utf-8")
    (ZIEL / "corporate-design.html").write_text(corporate_design(), encoding="utf-8")
    print("gebaut: geschaeftsausstattung.html, corporate-design.html")
    if "--ohne-png" not in sys.argv:
        png_export()
