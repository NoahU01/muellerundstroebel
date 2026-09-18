#!/usr/bin/env python3
"""Baut die PDFs aus den HTML-Quellen in diesem Ordner.

    python3 pdf/bauen.py              # alle Dokumente
    python3 pdf/bauen.py fit-and-proper   # nur passende

Gedruckt wird mit Chrome im Headless-Modus. Die Seiten werden über einen
kurzlebigen lokalen Server ausgeliefert, weil Chrome Schriften und Bilder
sonst nicht von file:// nachlädt.
"""
import http.server
import shutil
import socketserver
import subprocess
import sys
import threading
import time
from pathlib import Path

PDF_ORDNER = Path(__file__).resolve().parent
WURZEL = PDF_ORDNER.parent
ZIEL = WURZEL / "assets" / "downloads"
PORT = 8799

# Quelldatei -> fertiges PDF
DOKUMENTE = {
    "aufsichtsrat-fit-and-proper.html": "aufsichtsrat-fit-and-proper.pdf",
    "aufsichtsrat-strategie.html": "aufsichtsrat-strategie.pdf",
}

CHROME_PFADE = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    shutil.which("google-chrome") or "",
    shutil.which("chromium") or "",
]


def chrome():
    for p in CHROME_PFADE:
        if p and Path(p).exists():
            return p
    sys.exit("Chrome nicht gefunden – bitte Google Chrome installieren.")


def server_starten():
    handler = lambda *a, **k: http.server.SimpleHTTPRequestHandler(*a, directory=str(WURZEL), **k)
    socketserver.TCPServer.allow_reuse_address = True
    srv = socketserver.TCPServer(("127.0.0.1", PORT), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def bauen(quelle, ziel, browser):
    url = f"http://127.0.0.1:{PORT}/pdf/{quelle}"
    ZIEL.mkdir(parents=True, exist_ok=True)
    ausgabe = ZIEL / ziel
    befehl = [
        browser, "--headless", "--disable-gpu", "--no-sandbox",
        "--no-pdf-header-footer", "--print-to-pdf-no-header",
        "--virtual-time-budget=10000",
        f"--print-to-pdf={ausgabe}", url,
    ]
    ergebnis = subprocess.run(befehl, capture_output=True, text=True)
    if not ausgabe.exists() or ausgabe.stat().st_size < 10_000:
        print(ergebnis.stderr[-800:])
        sys.exit(f"FEHLER: {ziel} wurde nicht erzeugt.")
    print(f"  {ziel}  ({ausgabe.stat().st_size // 1024} KB)")


def main():
    filter_ = sys.argv[1] if len(sys.argv) > 1 else ""
    browser = chrome()
    srv = server_starten()
    time.sleep(0.4)
    print("Baue PDFs nach assets/downloads/:")
    try:
        for quelle, ziel in DOKUMENTE.items():
            if filter_ and filter_ not in quelle:
                continue
            bauen(quelle, ziel, browser)
    finally:
        srv.shutdown()


if __name__ == "__main__":
    main()
