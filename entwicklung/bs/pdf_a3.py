#!/usr/bin/env python3
"""One-Pager A3 hoch zur Business Story 2.0 (nur Branch daniel).

Die Startseite im Kleinen: Kopf · Ihre Lage · Wendepunkt · So arbeiten wir · Hier setzen wir an ·
Ergebnis und erstes Gespräch. Der Elevator Pitch ist der rote Faden.
Baut entwicklung/pdf-bs2/one-pager-a3.html und druckt entwicklung/downloads/one-pager-a3.pdf.

    python3 entwicklung/bs/pdf_a3.py
"""
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "pdf"))
import bs2 as b
import bauen as druck
from pdf_bs2 import WEGE, ICO, NETZ

WURZEL = Path(__file__).resolve().parents[2]
QUELLE = WURZEL / "entwicklung" / "pdf-bs2" / "one-pager-a3.html"
ZIEL = WURZEL / "entwicklung" / "downloads" / "one-pager-a3.pdf"


def kreis(k, g):
    return f'<div class="kreis" style="width:{g}pt;height:{g}pt"><img src="/assets/{k}-portrait.webp" alt="{b.PERSONEN[k]["name"]}"></div>'


def html():
    farbe = {"sand": "sand", "navy": "navy", "hell": "hell"}
    kaesten = "".join(
        f'<article class="post"><div class="post__bild post__bild--{farbe[f]}"><small>{t}</small><b>{x}</b>{ICO[k]}</div></article>'
        for f, t, x, k, e in WEGE)
    gebiete = "".join(f'<div class="gebiet"><span>{b.icon(k)}</span><div><b>{n}</b><p>{w}</p></div></div>' for k, n, w in b.THEMEN)
    netz = " · ".join(n for n, _ in NETZ)
    personen = "".join(f'<div class="person">{kreis(k, 52)}<div><b>{p["name"]}</b><span class="person__rolle">{p["rolle"]}</span>'
                       f'<span>{p["tel"]}</span><span>{p["mail"]}</span></div></div>' for k, p in b.PERSONEN.items())
    duo = "".join(f'<figure>{kreis(k, 118)}<figcaption>{p["name"]}</figcaption></figure>' for k, p in b.PERSONEN.items())
    return f'''<!DOCTYPE html>
<html lang="de"><head><meta charset="utf-8"><title>Müller &amp; Ströbel – One-Pager A3</title>
<link rel="stylesheet" href="/entwicklung/pdf-bs2/one-pager-a3.css"></head>
<body><section class="blatt">

  <header class="a-kopf">
    <img class="a-kopf__amp" src="/pdf/bausteine/ampersand-konstruktion.svg" alt="">
    <div class="a-kopf__leiste"><img src="/pdf/bausteine/logo-weiss.svg" alt="Müller &amp; Ströbel"><span>www.muellerundstroebel.de</span></div>
    <div class="a-kopf__raster">
      <div><p class="kicker">Für Führungskräfte in der Versicherungsbranche</p>
        <h1>Komplexe Situationen strukturieren, entscheiden, umsetzen.</h1></div>
    </div>
  </header>

  <section class="a-lage">
    <p class="kicker">Ihre Lage</p>
    <h2>Sie müssen alles im Blick haben. Und am Ende zählt nur das Ergebnis.</h2>
    <p class="lead">Ob Sie ein Thema Ihrem Team geben oder Externe holen: Es kommt selten so zurück, wie Sie es brauchen. Am Ende greifen Sie doch wieder selbst ein.</p>
    <div class="posts">{kaesten}</div>
  </section>

  <section class="a-wende">
    <p class="kicker">Da setzen wir an</p>
    <p class="a-wende__satz">Sie geben uns die Verantwortung für ein Thema. Wir liefern das Ergebnis.</p>
  </section>

  <section class="a-mitte">
    <div class="a-arbeit">
      <p class="kicker">So arbeiten wir</p>
      <h2>Die Zusammenarbeit passt in Ihren Kalender.</h2>
      <ol class="ablauf-v">
        <li><b>Kurzer Austausch</b><span>Telefonat, Videokonferenz, Workshop, wenn er sinnvoll ist. Oft reicht ein kurzer Austausch.</span></li>
        <li><b>Wir arbeiten</b><span>Mit Ihren Leuten, selbst und mit Spezialisten aus unserem Netzwerk.</span></li>
        <li><b>Nächster Austausch</b><span>Wir kommen mit einem klaren Bild zurück und setzen eine Stufe höher an.</span></li>
      </ol>
      <p class="a-netz"><b>Unser Netzwerk</b>{netz}</p>
    </div>
    <div class="a-gebiete">
      <p class="kicker">Hier setzen wir an</p>
      <div class="gebiete">{gebiete}</div>
    </div>
  </section>

  <section class="a-ende">
    <div class="a-ende__ergebnis">
      <div><p class="kicker">Ihr Ergebnis</p><h2>Sie haben Ihre Themen im Griff.</h2>
        <p class="lead">Im Gespräch behalten wir das Zielbild im Blick und schaffen Klarheit, wohin es geht. Sie entscheiden.</p></div>
    </div>
    <div class="a-ende__gespraech">
      <div><p class="kicker">Das erste Gespräch</p>
        <ol class="schritte3"><li><b>Sie rufen an</b> oder schreiben uns.</li>
          <li><b>Wir sprechen über Ihr Thema</b> und sagen offen, ob und wie wir es übernehmen.</li>
          <li><b>Sie entscheiden</b>, ob wir loslegen. Kein Pitch, keine Rechnung.</li></ol></div>
      <div class="personen">{personen}</div>
    </div>
  </section>

</section></body></html>
'''


def main():
    QUELLE.write_text(html(), encoding="utf-8")
    browser = druck.chrome()
    srv = druck.server_starten()
    time.sleep(.4)
    try:
        subprocess.run([browser, "--headless", "--disable-gpu", "--no-sandbox", "--no-pdf-header-footer", "--print-to-pdf-no-header",
                        "--virtual-time-budget=10000", f"--print-to-pdf={ZIEL}",
                        f"http://127.0.0.1:{druck.PORT}/entwicklung/pdf-bs2/one-pager-a3.html"], capture_output=True)
        print(f"gebaut: {ZIEL.relative_to(WURZEL)} ({ZIEL.stat().st_size // 1024} KB)")
    finally:
        srv.shutdown()


if __name__ == "__main__":
    main()
