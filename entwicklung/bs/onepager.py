#!/usr/bin/env python3
"""One-Pager zur Business Story 2.0 (nur Branch daniel) – gebaut aus den Bausteinen der Startseite.

Grundsatz: Ein One-Pager ist die Landingpage in kurz. Gleiches CSS (entwicklung/business-story-2.css),
gleiche Schriftgrößen, Abstände, Kästen und Flächen. Nur drei Abschnitte je Variante; nichts wird zum
Einpassen verkleinert. Blattgröße A3 hoch (1123 × 1587 px = 297 × 420 mm), damit die Desktop-Gestaltung greift.

    python3 entwicklung/bs/onepager.py
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
QUELLE = WURZEL / "entwicklung" / "pdf-bs2" / "onepager.html"
ZIEL = WURZEL / "entwicklung" / "downloads" / "onepager-a3.pdf"

ICO = {
    "team": '<svg class="ico" viewBox="0 0 24 24"><circle cx="9" cy="8" r="3.2"/><path d="M3.5 19.5c.6-3.3 2.7-5 5.5-5s4.9 1.7 5.5 5"/><circle cx="17" cy="9" r="2.5"/><path d="M16 14.6c2.4.1 4 1.6 4.5 4.4"/></svg>',
    "extern": '<svg class="ico" viewBox="0 0 24 24"><rect x="3" y="7.5" width="18" height="12.5" rx="2"/><path d="M8.5 7.5V5.8A1.8 1.8 0 0 1 10.3 4h3.4a1.8 1.8 0 0 1 1.8 1.8v1.7M3 12.5h18"/></svg>',
    "workshop": '<svg class="ico" viewBox="0 0 24 24"><rect x="3.5" y="5" width="17" height="15.5" rx="2"/><path d="M3.5 9.5h17M8 3v4M16 3v4M7.5 13.5h3M13.5 13.5h3M7.5 17h3"/></svg>',
}
KAESTEN = [("sand", "Ihr Team", "Liefert, aber nicht so, wie Sie es brauchen.", "team",
            "Typisch bei der Vorlage für den Aufsichtsrat oder dem Konzept für die Bereiche. Am Ende greifen Sie wieder selbst ein."),
           ("navy", "Externe", "Empfehlungen ja. Umsetzen bleibt bei Ihnen.", "extern",
            "Strategieberater, Projektmanager, Spezialisten: Die Koordination und die Verantwortung für das Ergebnis bleiben bei Ihnen."),
           ("hell", "Nur Workshops", "Zwei Tage im Kalender. Dann wochenlang Stillstand.", "workshop",
            "Große Themen werden zur Hürde. Es geht erst weiter, wenn wieder Zeit im Kalender ist.")]
VERSPRECHEN = "Sie geben uns die Verantwortung für ein Thema. Wir liefern das Ergebnis."
KOPF_TEXT = ("Die Vorlage für den Aufsichtsrat, die Strategie für die Bereiche, die Kennzahlen, die steuern sollen: "
             "Wir übernehmen Ihr Thema und sorgen dafür, dass es vorankommt. Mit wenig Aufwand für Sie.")


def kaesten():
    return '<div class="pks">' + "".join(
        f'<article class="pk"><div class="pk__bild pk__bild--{f}"><small>{t}</small><b>{x}</b>{ICO[k]}</div>'
        f'</article>' for f, t, x, k, e in KAESTEN) + "</div>"


def duo():
    return '<div class="duo duo--gleich">' + "".join(
        f'<figure><div class="kreis"><img src="/assets/{k}-portrait.webp" alt="{p["name"]}"></div><figcaption><b>{p["name"]}</b></figcaption></figure>'
        for k, p in b.PERSONEN.items()) + "</div>"


def personen():
    return '<div class="op-personen">' + "".join(
        f'<article class="kp"><div class="kreis"><img src="/assets/{k}-portrait.webp" alt="{p["name"]}"></div>'
        f'<div><h3>{p["name"]}</h3><p class="kp__themen">{p["rolle"]}</p><p class="kp__wege"><span>{p["mail"]}</span><span>{p["tel"]}</span></p></div></article>'
        for k, p in b.PERSONEN.items()) + "</div>"


def logo(hell=False):
    return f'<div class="op-logo"><img src="{"/pdf/bausteine/logo-weiss.svg" if hell else "/assets/logo.svg"}" alt="Müller &amp; Ströbel"><span>www.muellerundstroebel.de</span></div>'


def blatt(name, inhalt):
    return f'<section class="op" aria-label="{name}"><span class="op-name">{name}</span>{inhalt}</section>'


def seiten():
    v1 = blatt("Variante 1 · Die Startseite in kurz", f'''
  <div class="held op-held"><div class="wrap">{logo()}
    <div class="held__raster"><div>
      <p class="kicker">Für Führungskräfte in der Versicherungsbranche</p>
      <h1>Komplexe Situationen strukturieren, entscheiden, umsetzen.</h1>
      <p class="lead">{KOPF_TEXT}</p></div>{duo()}</div></div></div>
  <div class="sek sek--sand"><div class="wrap">
    <p class="kicker">Ihre Lage</p><h2 class="h2">„Es ging schon wieder nichts voran.“</h2>
    <p class="lead">Alles läuft über Ihren Tisch. Und die üblichen Wege helfen nur halb.</p>{kaesten()}</div></div>
  <div class="sek sek--navy op-ende"><div class="wrap">
    <p class="kicker">Kontakt</p><h2 class="h2">{VERSPRECHEN}</h2>
    <p class="lead">Erzählen Sie uns, was ansteht. Das erste Gespräch schafft Klarheit. Kein Pitch, keine Rechnung.</p>{personen()}</div></div>''')

    v2 = blatt("Variante 2 · Vom Problem zum Versprechen", f'''
  <div class="held op-held"><div class="wrap">{logo()}
    <p class="kicker">Für Führungskräfte in der Versicherungsbranche</p>
    <h1 class="op-h1-breit">„Es ging schon wieder nichts voran.“</h1>
    <p class="lead">Ob Sie ein Thema Ihrem Team geben oder Externe holen: Es kommt selten so zurück, wie Sie es brauchen.</p>
    {kaesten()}</div></div>
  <div class="sek sek--navy lp-ergebnis op-wende"><div class="wrap lp-ergebnis__raster">
    <div><p class="kicker">Da setzen wir an</p><h2 class="h2">{VERSPRECHEN}</h2>
      <p class="lead">Wir strukturieren Ihr Thema, arbeiten es mit Ihren Leuten aus und holen Spezialisten dazu. Von Ihnen brauchen wir meist nur ein kurzes Telefonat zwischendurch.</p></div>
    {b.trio_szene("compass", "circle-check", "target")}</div></div>
  <div class="sek sek--sand op-ende op-ende--hell"><div class="wrap">
    <p class="kicker">Kontakt</p><h2 class="h2">Liegt gerade so ein Thema auf Ihrem Tisch?</h2>{personen()}</div></div>''')

    v3 = blatt("Variante 3 · Das Ergebnis zuerst", f'''
  <div class="sek sek--navy op-held op-held--dunkel"><div class="wrap">{logo(True)}
    <div class="lp-ergebnis__raster"><div>
      <p class="kicker">Für Führungskräfte in der Versicherungsbranche</p>
      <h1>Sie haben Ihre Themen im Griff.</h1>
      <p class="lead">Wir übernehmen komplexe Themen, von der Vorlage für den Aufsichtsrat bis zur Strategie für die Bereiche, und sorgen dafür, dass sie vorankommen. Sie entscheiden.</p></div>
      {b.trio_szene("compass", "circle-check", "target")}</div></div></div>
  <div class="sek sek--sand"><div class="wrap">
    <p class="kicker">Heute</p><h2 class="h2">Die üblichen Wege helfen nur halb.</h2>{kaesten()}</div></div>
  <div class="sek op-ende op-ende--hell"><div class="wrap">
    <p class="kicker">Unser Versprechen</p><h2 class="h2">{VERSPRECHEN}</h2>{personen()}</div></div>''')
    return [v1, v2, v3]


def html():
    return f'''<!DOCTYPE html>
<html lang="de"><head><meta charset="utf-8"><title>Müller &amp; Ströbel – One-Pager</title>
<link rel="stylesheet" href="/entwicklung/business-story-2.css?v={b.VERSION}">
<link rel="stylesheet" href="/entwicklung/pdf-bs2/onepager.css">
</head><body>
{"".join(seiten())}
</body></html>
'''


def main():
    QUELLE.write_text(html(), encoding="utf-8")
    browser = druck.chrome()
    srv = druck.server_starten()
    time.sleep(.4)
    try:
        subprocess.run([browser, "--headless", "--disable-gpu", "--no-sandbox", "--no-pdf-header-footer", "--print-to-pdf-no-header",
                        "--virtual-time-budget=10000", f"--print-to-pdf={ZIEL}",
                        f"http://127.0.0.1:{druck.PORT}/entwicklung/pdf-bs2/onepager.html"], capture_output=True)
        print(f"gebaut: {ZIEL.relative_to(WURZEL)} ({ZIEL.stat().st_size // 1024} KB)")
    finally:
        srv.shutdown()


if __name__ == "__main__":
    main()
