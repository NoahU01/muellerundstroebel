#!/usr/bin/env python3
"""Elevator Pitch als internes Arbeitsdokument (PDF, A4 hoch) – nur Branch daniel.

Seite 1: der Zusammenhang (Pitch → Fragen → sein Thema) und beide Pitch-Varianten. Seite 2: Gesprächsführung.
Alle Inhalte kommen aus bs2.py (PITCH, PITCH_10, REGELN, LENKUNG, WEG, THEMEN), damit Seite und PDF gleich bleiben.

    python3 entwicklung/bs/pdf_pitch.py
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
QUELLE = WURZEL / "entwicklung" / "pdf-bs2" / "elevator-pitch.html"
ZIEL = WURZEL / "entwicklung" / "downloads" / "elevator-pitch.pdf"
STAND = "11.10.2026"
SCHLUSS = "Kurz gesagt: Wir sind die rechte Hand, die Sie sich für Ihre wichtigsten Themen immer gewünscht haben."


def blatt(nr, gesamt, inhalt):
    return (f'<div class="blatt"><p class="pkopf">Müller &amp; Ströbel · Business Story 2.0 · Elevator Pitch'
            f'<span>Internes Arbeitsdokument · Stand {STAND}</span></p>{inhalt}'
            f'<p class="pfuss"><span>Quelle: Entwicklungsseite „Elevator Pitch“</span><span>Seite {nr} / {gesamt}</span></p></div>')


def fluss():
    """Der Zusammenhang wie auf der Website: Pitch → Fragen → sein Thema."""
    regeln = "".join(f"<li>{t}</li>" for t, _ in b.REGELN)
    themen = "".join(f'<li{" class=passt" if i == 2 else ""}>{t}</li>' for i, (_, t, *_) in enumerate(b.THEMEN))
    return f'''<div class="fluss">
  <div class="stufe stufe--pitch"><b>Pitch</b><div class="dauer"><span>30 Sekunden</span><span>10 Sekunden</span></div><ul class="regeln">{regeln}</ul></div>
  <span class="pfeil"></span>
  <div class="stufe"><b>Fragen</b><p class="zitat">„Wie ist bei Ihnen gerade die Situation?“</p></div>
  <span class="pfeil"></span>
  <div class="stufe"><b>Sein Thema</b><ul class="themen">{themen}</ul></div>
</div>'''


def html():
    woerter = len(" ".join(p[4] for p in b.PITCH).split())
    sek = round(woerter / 2.5 / 5) * 5
    s1 = f'''
<h1>Unsere Story in 30/10 Sekunden</h1>
<p class="intro">Der Pitch öffnet das Gespräch und weckt Interesse. Danach führen Fragen zu seinem Thema.</p>
{fluss()}
<div class="zwei">
  <div><h2>Der Pitch · 30 Sekunden</h2><div class="fliess">{"".join(f"<p>{p[4]}</p>" for p in b.PITCH)}</div>
    <p class="notiz">{woerter} Wörter · gesprochen etwa {sek} Sekunden</p></div>
  <div><h2>Die Kurzfassung · 10 Sekunden</h2><div class="fliess"><p>{b.PITCH_10}</p><p>{SCHLUSS}</p></div>
    <p class="notiz">Für die Vorstellungsrunde oder die Frage „Und was machen Sie?“</p></div>
</div>'''
    lenkung = "".join(f"<tr><td class='frage-l'>{t}</td><td>{x}</td></tr>" for t, x in b.LENKUNG)
    weg = "".join(f"<tr><td><b>{t}</b></td><td>{x}</td></tr>" for t, x in b.WEG)
    s2 = f'''
<h1>Nach dem Pitch: Gesprächsführung</h1>
<p class="intro">Mit Fragen finden wir heraus, was für das Gegenüber wichtig ist, und steuern auf sein Thema zu. Ein Einsatzgebiet bringen wir erst ein, wenn es passt.</p>
<h2>Lenkungsfragen</h2>
<table class="tab tab--zwei tab--fragen">{lenkung}</table>
<h2>Worauf wir hinsteuern, sobald er danach fragt</h2>
<table class="tab tab--zwei">{weg}</table>'''
    seiten = [s1, s2]
    return f'''<!DOCTYPE html>
<html lang="de"><head><meta charset="utf-8"><title>Müller &amp; Ströbel – Elevator Pitch (intern)</title>
<link rel="stylesheet" href="/entwicklung/business-story-2.css?v={b.VERSION}">
<link rel="stylesheet" href="/entwicklung/pdf-bs2/pitch-pdf.css">
</head><body>{"".join(blatt(i, len(seiten), s) for i, s in enumerate(seiten, 1))}</body></html>
'''


def main():
    QUELLE.write_text(html(), encoding="utf-8")
    browser = druck.chrome()
    srv = druck.server_starten()
    time.sleep(.4)
    try:
        subprocess.run([browser, "--headless", "--disable-gpu", "--no-sandbox", "--no-pdf-header-footer", "--print-to-pdf-no-header",
                        "--virtual-time-budget=10000", f"--print-to-pdf={ZIEL}",
                        f"http://127.0.0.1:{druck.PORT}/entwicklung/pdf-bs2/elevator-pitch.html"], capture_output=True)
        print(f"gebaut: {ZIEL.relative_to(WURZEL)} ({ZIEL.stat().st_size // 1024} KB)")
    finally:
        srv.shutdown()


if __name__ == "__main__":
    main()
