#!/usr/bin/env python3
"""Vergleicht zwei PDFs Seite für Seite pixelweise.

    python3 pdf/pixelvergleich.py alt.pdf neu.pdf [ausgabeordner]

Für jede Seite wird gemeldet, wie viel Prozent der Pixel abweichen und wo.
Zusätzlich entsteht je Seite ein Differenzbild: das Original blass im
Hintergrund, Abweichungen in Rot. Damit sieht man sofort, welches Element
nicht sitzt - und nicht nur, dass eine Zahl nicht stimmt.

Ohne Fremdbibliotheken: PNG wird direkt dekodiert und geschrieben (zlib).
"""
import re
import struct
import subprocess
import sys
import tempfile
import zlib
from itertools import count
from pathlib import Path

ZAEHLER = count(1)

TOLERANZ = 12        # Helligkeitsunterschied, der noch als gleich gilt (Kantenglättung)
BREITE = 900         # Renderbreite in Pixel


# ----------------------------------------------------------------- PNG lesen
def png_lesen(pfad):
    daten = Path(pfad).read_bytes()
    if daten[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("kein PNG")
    pos = 8
    idat = b""
    breite = hoehe = tiefe = farbtyp = 0
    palette = None
    while pos < len(daten):
        laenge, typ = struct.unpack(">I4s", daten[pos:pos + 8])
        inhalt = daten[pos + 8:pos + 8 + laenge]
        if typ == b"IHDR":
            breite, hoehe, tiefe, farbtyp = struct.unpack(">IIBB", inhalt[:10])
        elif typ == b"PLTE":
            palette = inhalt
        elif typ == b"IDAT":
            idat += inhalt
        elif typ == b"IEND":
            break
        pos += 12 + laenge
    if tiefe != 8:
        raise ValueError(f"nur 8 Bit unterstützt, hier {tiefe}")

    kanaele = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[farbtyp]
    roh = zlib.decompress(idat)
    zeilenlaenge = breite * kanaele
    aus = bytearray(hoehe * zeilenlaenge)
    vorher = bytearray(zeilenlaenge)
    p = 0
    for y in range(hoehe):
        filter_ = roh[p]; p += 1
        zeile = bytearray(roh[p:p + zeilenlaenge]); p += zeilenlaenge
        if filter_ == 1:
            for i in range(kanaele, zeilenlaenge):
                zeile[i] = (zeile[i] + zeile[i - kanaele]) & 255
        elif filter_ == 2:
            for i in range(zeilenlaenge):
                zeile[i] = (zeile[i] + vorher[i]) & 255
        elif filter_ == 3:
            for i in range(zeilenlaenge):
                links = zeile[i - kanaele] if i >= kanaele else 0
                zeile[i] = (zeile[i] + ((links + vorher[i]) >> 1)) & 255
        elif filter_ == 4:
            for i in range(zeilenlaenge):
                a = zeile[i - kanaele] if i >= kanaele else 0
                b = vorher[i]
                c = vorher[i - kanaele] if i >= kanaele else 0
                pp = a + b - c
                pa, pb, pc = abs(pp - a), abs(pp - b), abs(pp - c)
                vor = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                zeile[i] = (zeile[i] + vor) & 255
        aus[y * zeilenlaenge:(y + 1) * zeilenlaenge] = zeile
        vorher = zeile

    # auf Graustufen bringen (Alpha auf Weiß rechnen)
    grau = bytearray(breite * hoehe)
    for i in range(breite * hoehe):
        b = i * kanaele
        if farbtyp == 0:
            g = aus[b]
        elif farbtyp == 4:
            a = aus[b + 1]; g = (aus[b] * a + 255 * (255 - a)) // 255
        elif farbtyp == 3:
            idx = aus[b] * 3
            g = (palette[idx] * 299 + palette[idx + 1] * 587 + palette[idx + 2] * 114) // 1000
        elif farbtyp == 2:
            g = (aus[b] * 299 + aus[b + 1] * 587 + aus[b + 2] * 114) // 1000
        else:
            a = aus[b + 3]
            r = (aus[b] * a + 255 * (255 - a)) // 255
            gg = (aus[b + 1] * a + 255 * (255 - a)) // 255
            bb = (aus[b + 2] * a + 255 * (255 - a)) // 255
            g = (r * 299 + gg * 587 + bb * 114) // 1000
        grau[i] = g
    return breite, hoehe, grau


# --------------------------------------------------------------- PNG schreiben
def png_schreiben(pfad, breite, hoehe, rgb):
    roh = bytearray()
    for y in range(hoehe):
        roh.append(0)
        roh += rgb[y * breite * 3:(y + 1) * breite * 3]
    def chunk(typ, inhalt):
        return (struct.pack(">I", len(inhalt)) + typ + inhalt
                + struct.pack(">I", zlib.crc32(typ + inhalt) & 0xffffffff))
    Path(pfad).write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", breite, hoehe, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(bytes(roh), 6))
        + chunk(b"IEND", b""))


# ------------------------------------------------------------- Seite rendern
def einzelseite(quelle, ziel, nummer):
    """Eine Seite als eigenes PDF (inkrementelles Update auf den Seitenbaum)."""
    import shutil
    shutil.copy(quelle, ziel)
    d = Path(ziel).read_bytes()
    objs = {}
    for m in re.finditer(rb"(\d+)\s+0\s+obj(.*?)endobj", d, re.S):
        objs[int(m.group(1))] = (m.group(2), m.start())
    baum = None
    for num, (o, _) in objs.items():
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
    off = len(aus)
    aus += b"%d 0 obj" % num + neu + b"endobj\n"
    xp = len(aus)
    aus += b"xref\n%d 1\n%010d 00000 n \n" % (num, off)
    aus += b"trailer\n<</Size %d\n/Root %s\n/Prev %d>>\nstartxref\n%d\n%%%%EOF\n" % (
        size, root, alt, xp)
    Path(ziel).write_bytes(bytes(aus))


def rendern(pdf, seite, arbeit, name):
    """qlmanage merkt sich Vorschauen am Dateinamen - deshalb bekommt jeder
    Aufruf einen eigenen, noch nie verwendeten Namen."""
    marke = f"{name}-{seite}-{next(ZAEHLER)}"
    einzel = arbeit / f"{marke}.pdf"
    einzelseite(pdf, einzel, seite)
    subprocess.run(["qlmanage", "-t", "-s", str(BREITE), "-o", str(arbeit), str(einzel)],
                   capture_output=True)
    quelle = arbeit / f"{marke}.pdf.png"
    if not quelle.exists():
        return None
    return png_lesen(quelle)


def seitenzahl(pdf):
    d = Path(pdf).read_bytes()
    return len(re.findall(rb"/Type\s*/Page[^s]", d))


def main():
    alt_pdf, neu_pdf = sys.argv[1], sys.argv[2]
    ausgabe = Path(sys.argv[3]) if len(sys.argv) > 3 else Path("pdf-vergleich")
    ausgabe.mkdir(parents=True, exist_ok=True)
    arbeit = Path(tempfile.mkdtemp(prefix="pixelvgl-"))

    n = min(seitenzahl(alt_pdf), seitenzahl(neu_pdf))
    if seitenzahl(alt_pdf) != seitenzahl(neu_pdf):
        print(f"ACHTUNG: {seitenzahl(alt_pdf)} gegen {seitenzahl(neu_pdf)} Seiten")

    gesamt = []
    for seite in range(1, n + 1):
        a = rendern(alt_pdf, seite, arbeit, "a")
        b = rendern(neu_pdf, seite, arbeit, "b")
        if not a or not b:
            print(f"  Seite {seite}: konnte nicht gerendert werden"); continue
        (bw, bh, ga), (nw, nh, gb) = a, b
        if (bw, bh) != (nw, nh):
            print(f"  Seite {seite}: unterschiedliche Größe {bw}x{bh} / {nw}x{nh}"); continue

        rgb = bytearray(bw * bh * 3)
        anders = 0
        strukturell = 0
        minx, miny, maxx, maxy = bw, bh, -1, -1
        for i in range(bw * bh):
            d = ga[i] - gb[i]
            if d < 0: d = -d
            if d > TOLERANZ:
                anders += 1
                # strukturell nur, wenn auch die Nachbarschaft nicht passt: so
                # zaehlen Haarlinien-Versaetze eines Buchstabens nicht mit
                x, y = i % bw, i // bw
                treffer = False
                for ny in range(max(0, y-1), min(bh, y+2)):
                    for nx in range(max(0, x-1), min(bw, x+2)):
                        e = ga[i] - gb[ny*bw+nx]
                        if -TOLERANZ <= e <= TOLERANZ:
                            treffer = True; break
                    if treffer: break
                if not treffer:
                    strukturell += 1
                rgb[i*3] = 220; rgb[i*3+1] = 30; rgb[i*3+2] = 40
                x, y = i % bw, i // bw
                if x < minx: minx = x
                if x > maxx: maxx = x
                if y < miny: miny = y
                if y > maxy: maxy = y
            else:
                hell = 200 + ga[i] // 5
                rgb[i*3] = rgb[i*3+1] = rgb[i*3+2] = min(255, hell)
        anteil = anders * 100.0 / (bw * bh)
        anteil_s = strukturell * 100.0 / (bw * bh)
        gesamt.append(anteil)
        png_schreiben(ausgabe / f"seite{seite}.png", bw, bh, rgb)
        ort = (f"  Bereich x {minx}-{maxx}, y {miny}-{maxy}" if maxx >= 0 else "")
        print(f"  Seite {seite}: {anteil:6.3f} % abweichend, davon {anteil_s:6.3f} % "
              f"strukturell{ort}")

    if gesamt:
        print(f"\n  Schnitt: {sum(gesamt)/len(gesamt):.3f} %  |  "
              f"schlechteste Seite: {max(gesamt):.3f} %")
        print(f"  Differenzbilder in {ausgabe}/")
    import shutil
    shutil.rmtree(arbeit, ignore_errors=True)


if __name__ == "__main__":
    main()
