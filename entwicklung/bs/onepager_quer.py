#!/usr/bin/env python3
"""One-Pager A3 quer für Müller & Ströbel (nur Branch daniel).

Nachbau der empiria-Vorlage „Geschäftsausstattung › One-Pager › A3 quer · Inhalt“
(empiria/site/projekte/ga-onepager.html): Headline links oben, Logo rechts oben, drei gleich breite
Spalten, Themenzeile, unten ein dunkles Band mit Ansprechpartnern und Ergebnis.
Maße 1:1 aus der Vorlage (cqw = 1 % der Blattbreite), Farben und Schriften im CD von M&S:
Schwarz → Navy, Gelb → Taupe, Lora + Poppins, Porträts im Kreis mit weißem Rand.

    python3 entwicklung/bs/onepager_quer.py
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
QUELLE = WURZEL / "entwicklung" / "pdf-bs2" / "onepager-quer.html"
ZIEL = WURZEL / "entwicklung" / "downloads" / "onepager-a3-quer.pdf"

LU = {
    "struktur": '<path d="M21 12h-8"/><path d="M21 6H8"/><path d="M21 18h-8"/><path d="M3 6v4c0 1.1.9 2 2 2h3"/><path d="M3 10v6c0 1.1.9 2 2 2h3"/>',
    "leute": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "ergebnis": '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="m9 15 2 2 4-4"/>',
}

LAGE = [("Ihr Team", "Liefert, aber nicht so, wie Sie es brauchen."),
        ("Externe", "Empfehlungen ja. Umsetzen bleibt bei Ihnen."),
        ("Am Ende", "Greifen Sie doch wieder selbst ein.")]
ANSATZ = [("struktur", "Wir strukturieren es.", "Klare Struktur, bevor gearbeitet wird."),
          ("leute", "Wir arbeiten es mit Ihren Leuten aus.", "Ihr Team bringt das Wissen ein, wir führen das Thema."),
          ("ergebnis", "Wir liefern das Ergebnis.", "Fertig für Ihre Entscheidung oder Ihr Gremium.")]
ABLAUF = [("Sie übergeben das Thema", "Und mit ihm die Verantwortung."),
          ("Kurzes Telefonat zwischendurch", "Wenn eine Entscheidung ansteht."),
          ("Sie haben das Ergebnis", "Ohne selbst nacharbeiten zu müssen.")]


def html():
    P = {x[0]: x[4] for x in b.PITCH}
    lage = "".join(f'<li><span class="oi-strich"></span><div><b>{t}</b><p>{x}</p></div></li>' for t, x in LAGE)
    ansatz = "".join(f'<li><span class="oi-ico"><svg viewBox="0 0 24 24">{LU[i]}</svg></span><div><b>{t}</b><p>{x}</p></div></li>' for i, t, x in ANSATZ)
    ablauf = "".join(f'<li><span class="oi-nr">0{n}</span><div><b>{t}</b><p>{x}</p></div></li>' for n, (t, x) in enumerate(ABLAUF, 1))
    themen = "".join(f'<li><b>{t}</b></li>' for _, t, *_ in b.THEMEN[:5])
    personen = "".join(
        f'<div class="oi-person"><div class="kreis"><img src="/assets/{k}-portrait.webp" alt="{p["name"]}"></div>'
        f'<div><b>{p["name"]}</b><span>{p["mail"]}</span><span>{p["tel"]}</span></div></div>' for k, p in b.PERSONEN.items())
    return f'''<!DOCTYPE html>
<html lang="de"><head><meta charset="utf-8"><title>Müller &amp; Ströbel – One-Pager A3 quer</title>
<link rel="stylesheet" href="/entwicklung/business-story-2.css?v={b.VERSION}">
<link rel="stylesheet" href="/entwicklung/pdf-bs2/onepager-quer.css">
</head><body>
<div class="oq">
  <header class="oi-kopf">
    <img class="oi-logo" src="/assets/logo.svg" alt="Müller &amp; Ströbel">
    <div class="oi-titel"><div>
      <p class="op-k">Für Führungskräfte in der Versicherungsbranche</p>
      <h1>Sie müssen alles im Blick haben. Und am Ende zählt <i>nur das Ergebnis.</i></h1>
      <p class="op-lead">Wir übernehmen komplexe Themen, von der Vorlage für den Aufsichtsrat bis zur Strategie für die Bereiche, und liefern das Ergebnis. Sie brauchen dafür nur kurze Abstimmungen.</p>
    </div><span class="oi-zeichen" aria-hidden="true">&amp;</span></div>
  </header>
  <section class="oi-spalten">
    <div class="oi-spalte"><p class="op-k">Ihre Lage</p><h2>{P["2"]}</h2><span></span><ul class="oi-liste">{lage}</ul></div>
    <div class="oi-spalte"><p class="op-k">Unser Ansatz</p><h2>Da setzen wir an. Sie geben uns die Verantwortung für ein Thema, etwa die Vorlage für den Aufsichtsrat.</h2><span></span><ul class="oi-liste">{ansatz}</ul></div>
    <div class="oi-spalte"><p class="op-k">Zusammenarbeit</p><h2>{P["4"]}</h2><span></span><ul class="oi-liste">{ablauf}</ul></div>
  </section>
  <section class="oi-fragen"><p class="op-k">Typische Themen</p>
    <div class="oi-fragen__in"><h3>{P["6"].replace("? ", "?<br>")}</h3><ol>{themen}</ol></div></section>
  <footer class="oi-fuss">{personen}<div class="oi-ergebnis"><p class="op-k">Das Ergebnis</p><p>{P["5"]}</p></div></footer>
</div>
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
                        f"http://127.0.0.1:{druck.PORT}/entwicklung/pdf-bs2/onepager-quer.html"], capture_output=True)
        print(f"gebaut: {ZIEL.relative_to(WURZEL)} ({ZIEL.stat().st_size // 1024} KB)")
    finally:
        srv.shutdown()


if __name__ == "__main__":
    main()
