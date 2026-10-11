#!/usr/bin/env python3
"""Elevator Pitch als internes Arbeitsdokument (PDF, A4 hoch) – nur Branch daniel.

Seite 1: der Pitch (halbe Minute) und die Kurzfassung. Danach, wie wir dorthin gekommen sind:
Zuordnung Satz für Satz, Ausgangsmaterial aus dem Storyboard, Regeln und Weggelassenes.
Alle Inhalte kommen aus bs2.py (PITCH, PITCH_10, STORY, VERDICHTUNG, REGELN, WEG), damit Seite und PDF gleich bleiben.

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
# Welche Leserfrage wo im Pitch landet
VERWENDUNG = {"1": "Kurzfassung", "2": "Satz 1", "3": "Satz 2", "4": "Satz 3 · Kurzfassung", "5": "nicht im Pitch – für das Nachgespräch",
              "6": "Satz 4 · Kurzfassung", "7": "Satz 5", "8": "Satz 6"}


def blatt(nr, gesamt, inhalt):
    return (f'<div class="blatt"><p class="pkopf">Müller &amp; Ströbel · Business Story 2.0 · Elevator Pitch'
            f'<span>Internes Arbeitsdokument · Stand {STAND}</span></p>{inhalt}'
            f'<p class="pfuss"><span>Quelle: Entwicklungsseite „Elevator Pitch“</span><span>Seite {nr} / {gesamt}</span></p></div>')


def fragen():
    alle = {fnr: (frage, punkte) for _, _, fr in b.STORY for fnr, frage, punkte in fr}
    return [(n, *alle[n]) for n in sorted(alle, key=int)]


def frage_block(fnr, frage, punkte):
    pk = "".join(f'<tr><td class="nr">{n}</td><td><b>{t}</b><br>{x}</td></tr>' for n, t, _, x in punkte)
    return (f'<div class="frage"><div class="frage__kopf"><span>F{fnr}</span><b>{frage}</b><em>{VERWENDUNG[fnr]}</em></div>'
            f'<table class="punkte"><tr><th colspan="2">Punkte im Storyboard</th></tr>{pk}</table>'
            f'<p class="verd"><small>Verdichtung</small>{b.VERDICHTUNG[fnr]}</p></div>')


def html():
    woerter = len(" ".join(p[4] for p in b.PITCH).split())
    sek = round(woerter / 2.5 / 5) * 5
    s1 = f'''
<h1>Elevator Pitch</h1>
<p class="intro">Das Ergebnis vorneweg. Danach Regeln und Gesprächsführung (Seiten 2 und 3), ab Seite 4 die Herleitung.</p>
<h2>Der Pitch · gut 30 Sekunden</h2>
<div class="fliess">{"".join(f"<p>{p[4]}</p>" for p in b.PITCH)}</div>
<p class="notiz">{woerter} Wörter · gesprochen etwa {sek} Sekunden (ruhiges Sprechtempo, 2,5 Wörter je Sekunde)</p>
<h2>Die Kurzfassung · gut 10 Sekunden</h2>
<div class="fliess"><p>{b.PITCH_10}</p><p>{SCHLUSS}</p></div>
<p class="notiz">Für die Vorstellungsrunde oder die Frage „Und was machen Sie?“. Danach folgt, wenn Interesse da ist, die lange Fassung.</p>'''
    zeilen = "".join(f'<tr><td class="nr">{n}</td><td><b>{t}</b><br><em>„{fr}“</em></td><td class="satz">{satz}</td>'
                     f'<td>{" · ".join(f"<span class=nw>{x}</span>" for x in q.split(" · "))}</td><td>{w}</td></tr>' for n, t, fr, q, satz, w in b.PITCH)
    s2 = f'''
<h1>Wie wir dorthin gekommen sind</h1>
<p class="intro">Drei Schritte: Im Storyboard haben wir zwölf Punkte als Antworten auf acht Leserfragen gesammelt (Seiten 5 bis 7). Je Leserfrage haben wir die Punkte zu einer Aussage verdichtet. Aus den Verdichtungen sind sechs Bausteine mit je einem gesprochenen Satz geworden (diese Seite). Die Herkunft der Kurzfassung steht auf Seite 8.</p>
<h2>Zuordnung: Satz für Satz</h2>
<table class="tab">
  <tr><th></th><th>Baustein · seine Frage</th><th>Satz im Pitch</th><th>Herkunft im Storyboard</th><th>Warum so</th></tr>{zeilen}
</table>
'''
    f = fragen()
    s3 = '<h1>Ausgangsmaterial: das Storyboard</h1><p class="intro">Die acht Leserfragen mit den Punkten, die wir dazu gesammelt haben, und der Verdichtung je Frage. Rechts oben steht jeweils, wo die Aussage im Pitch landet.</p>' + "".join(frage_block(*x) for x in f[:3])
    fort = '<h1>Ausgangsmaterial: das Storyboard <span class="fort">(Fortsetzung)</span></h1>'
    s4 = fort + "".join(frage_block(*x) for x in f[3:6])
    s4b = fort + "".join(frage_block(*x) for x in f[6:])
    regeln = "".join(f"<tr><td><b>{t}</b></td><td>{x}</td></tr>" for t, x in b.REGELN)
    lenkung = "".join(f"<tr><td class='frage-l'>{t}</td><td>{x}</td></tr>" for t, x in b.LENKUNG)
    weg = "".join(f"<tr><td><b>{t}</b></td><td>{x}</td></tr>" for t, x in b.WEG)
    s_regeln = f'''
<h1>Regeln und Gesprächsführung</h1>
<h2>Vier Regeln für den kurzen Pitch</h2>
<table class="tab tab--zwei">{regeln}</table>
<h2>Nach dem Pitch: Lenkungsfragen</h2>
<p class="intro intro--eng">Der Pitch öffnet das Gespräch. Danach finden wir mit wenigen Fragen heraus, was für das Gegenüber wichtig ist.</p>
<table class="tab tab--zwei tab--fragen">{lenkung}</table>'''
    s_weg = f'''
<h1>Nächste Schritte im Gespräch</h1>
<p class="intro">Worauf wir bewusst hinsteuern, sobald das Gegenüber danach fragt.</p>
<table class="tab tab--zwei">{weg}</table>'''
    kurz_herkunft = (
        "<tr><td><b>Für wen</b></td><td>F1: „Für Führungskräfte in der Versicherungsbranche.“</td></tr>"
        "<tr><td><b>Zwei Beispiele</b></td><td>Aus den Einsatzgebieten: die Vorlage für den Aufsichtsrat und die Überführung der Strategie in den Alltag. Mehr als zwei Beispiele versteht man gesprochen nicht.</td></tr>"
        "<tr><td><b>Das Versprechen</b></td><td>F4 (Punkt 7): „… und liefern das Ergebnis.“</td></tr>"
        "<tr><td><b>Sein Aufwand</b></td><td>F6 (Punkt 9): „Sie brauchen dafür nur kurze Abstimmungen.“</td></tr>"
        "<tr><td><b>Schlusssatz</b></td><td>„Die rechte Hand“: ein Rollenbild, das weder über der Führungskraft steht (Bereichsleiter) noch zu klein ist (Assistenz). Mit einer Leerzeile abgesetzt.</td></tr>")
    s_kurz = f'''
<h1>Herkunft der Kurzfassung</h1>
<p class="intro">Aus welchen Bausteinen die 10-Sekunden-Fassung besteht.</p>
<table class="tab tab--zwei">{kurz_herkunft}</table>'''
    seiten = [s1, s_regeln, s_weg, s2, s3, s4, s4b, s_kurz]
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
