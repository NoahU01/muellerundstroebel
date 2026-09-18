#!/usr/bin/env python3
"""Erzeugt die Vorschaubilder für den Download-Kasten aus den fertigen PDFs.

    python3 pdf/vorschau.py                 # alle Dokumente mit Download-Kasten
    python3 pdf/vorschau.py geschaeftsmodell

Je Dokument entstehen <name>-1.webp (Seite 1) und <name>-2.webp (Seite 2),
520 × 736 px, in assets/downloads/.

Ablauf: Die gewünschte Seite wird als eigenes einseitiges PDF geschrieben
(inkrementelles Update auf den Seitenbaum), von qlmanage gerendert und von
Chrome über ein Canvas als WebP kodiert - sips kann WebP nur lesen.
"""
import base64
import http.server
import re
import shutil
import socketserver
import subprocess
import sys
import tempfile
import threading
from pathlib import Path

PDF_ORDNER = Path(__file__).resolve().parent
WURZEL = PDF_ORDNER.parent
DOWNLOADS = WURZEL / "assets" / "downloads"
PORT = 8801
BREITE, HOEHE = 520, 736

DOKUMENTE = ["geschaeftsmodell", "komplexe-themen", "strategie-verankern"]

CHROME_PFADE = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
]

KODIERER = """<!doctype html><meta charset="utf-8"><body><pre id="out">…</pre>
<script>
var img = new Image();
img.onload = function () {
  var c = document.createElement('canvas');
  c.width = %d; c.height = %d;
  var x = c.getContext('2d');
  x.fillStyle = '#fff'; x.fillRect(0, 0, c.width, c.height);
  x.drawImage(img, 0, 0, c.width, c.height);
  document.getElementById('out').textContent =
    'START' + c.toDataURL('image/webp', 0.86).split(',')[1] + 'ENDE';
};
img.src = 'quelle.png?' + Math.random();
</script>""" % (BREITE, HOEHE)


def chrome():
    for p in CHROME_PFADE:
        if Path(p).exists():
            return p
    sys.exit("Chrome nicht gefunden.")


def xref_karte(d):
    karte, pos, gesehen = {}, int(re.findall(rb"startxref\s+(\d+)", d)[-1]), set()
    while pos and pos not in gesehen:
        gesehen.add(pos)
        if d[pos:pos + 4] != b"xref":
            break
        i = pos + 4
        while True:
            m = re.match(rb"\s*(\d+)\s+(\d+)\s*\n", d[i:i + 40])
            if not m:
                break
            start, anzahl = int(m.group(1)), int(m.group(2))
            i += m.end()
            for k in range(anzahl):
                em = re.match(rb"(\d{10}) (\d{5}) ([nf])", d[i:i + 20]); i += 20
                if em and em.group(3) == b"n":
                    karte.setdefault(start + k, int(em.group(1)))
        tm = re.search(rb"trailer\s*<<(.*?)>>", d[i:i + 2000], re.S)
        prev = re.search(rb"/Prev\s+(\d+)", tm.group(1)) if tm else None
        pos = int(prev.group(1)) if prev else None
    return karte


def einzelseite(quelle, ziel, nummer):
    shutil.copy(quelle, ziel)
    d = open(ziel, "rb").read()
    karte = xref_karte(d)
    baum = None
    for num, off in karte.items():
        m = re.match(rb"\s*\d+\s+0\s+obj", d[off:off + 40])
        if not m:
            continue
        o = d[off + m.end():d.find(b"endobj", off)]
        if re.search(rb"/Type\s*/Pages", o) and b"/Kids" in o:
            baum = (num, o)
    num, o = baum
    refs = re.findall(rb"\d+\s+0\s+R", re.search(rb"/Kids\s*\[(.*?)\]", o, re.S).group(1))
    neu = re.sub(rb"/Kids\s*\[.*?\]", b"/Kids [" + refs[nummer - 1] + b"]", o, flags=re.S)
    neu = re.sub(rb"/Count\s+\d+", b"/Count 1", neu)

    alt = int(re.findall(rb"startxref\s+(\d+)", d)[-1])
    tr = re.findall(rb"trailer\s*<<(.*?)>>", d, re.S)[-1]
    size = int(re.search(rb"/Size\s+(\d+)", tr).group(1))
    root = re.search(rb"/Root\s+(\d+\s+\d+\s+R)", tr).group(1)

    aus = bytearray(d)
    if not aus.endswith(b"\n"):
        aus += b"\n"
    off_neu = len(aus)
    aus += b"%d 0 obj" % num + neu + b"endobj\n"
    xref_pos = len(aus)
    aus += b"xref\n%d 1\n%010d 00000 n \n" % (num, off_neu)
    aus += b"trailer\n<</Size %d\n/Root %s\n/Prev %d>>\nstartxref\n%d\n%%%%EOF\n" % (
        size, root, alt, xref_pos)
    open(ziel, "wb").write(bytes(aus))


def main():
    filter_ = sys.argv[1] if len(sys.argv) > 1 else ""
    browser = chrome()
    arbeit = Path(tempfile.mkdtemp(prefix="vorschau-"))
    handler = lambda *a, **k: http.server.SimpleHTTPRequestHandler(*a, directory=str(arbeit), **k)
    socketserver.TCPServer.allow_reuse_address = True
    srv = socketserver.TCPServer(("127.0.0.1", PORT), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    (arbeit / "kodiere.html").write_text(KODIERER, encoding="utf-8")

    try:
        for dok in DOKUMENTE:
            if filter_ and filter_ not in dok:
                continue
            pdf = DOWNLOADS / f"{dok}.pdf"
            if not pdf.exists():
                print(f"  {dok}: PDF fehlt, übersprungen")
                continue
            for seite in (1, 2):
                einzelseite(pdf, arbeit / "e.pdf", seite)
                for rest in arbeit.glob("*.png"):
                    rest.unlink()
                subprocess.run(["qlmanage", "-t", "-s", str(HOEHE), "-o", str(arbeit),
                                str(arbeit / "e.pdf")], capture_output=True)
                (arbeit / "e.pdf.png").rename(arbeit / "quelle.png")
                dom = subprocess.run(
                    [browser, "--headless", "--disable-gpu", "--no-sandbox",
                     "--virtual-time-budget=8000", "--dump-dom",
                     f"http://127.0.0.1:{PORT}/kodiere.html"],
                    capture_output=True, text=True).stdout
                m = re.search(r"START([A-Za-z0-9+/=]+)ENDE", dom)
                if not m:
                    sys.exit(f"FEHLER: keine WebP-Daten für {dok} Seite {seite}")
                ziel = DOWNLOADS / f"{dok}-{seite}.webp"
                ziel.write_bytes(base64.b64decode(m.group(1)))
                print(f"  {ziel.name}  ({ziel.stat().st_size // 1024} KB)")
    finally:
        srv.shutdown()
        shutil.rmtree(arbeit, ignore_errors=True)


if __name__ == "__main__":
    main()
