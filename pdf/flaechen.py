#!/usr/bin/env python3
"""Listet alle gefüllten Flächen und Rahmen einer PDF-Seite.

    python3 pdf/flaechen.py <pdf> <seite> [mindestbreite]

bauplan.py zeigt nur Text und achsenparallele Rechtecke. Panels mit runden Ecken
sind Pfade aus Kurven und fehlen dort - genau die waren beim ersten Nachbau
übersehen worden. Dieses Werkzeug erfasst sie.
"""
import re
import sys
import zlib
from pathlib import Path


def mul(m, n):
    a, b, c, d, e, f = m
    A, B, C, D, E, F = n
    return (a*A + b*C, a*B + b*D, c*A + d*C, c*B + d*D, e*A + f*C + E, e*B + f*D + F)


def apply(m, x, y):
    a, b, c, d, e, f = m
    return (a*x + c*y + e, b*x + d*y + f)


TOKEN = re.compile(rb"(?P<num>-?\d*\.?\d+)\s|(?P<name>/[A-Za-z0-9#+\-.]+)|"
                   rb"(?P<arr>\[[^\]]*\])|(?P<op>[A-Za-z'\"*]+)")


def flaechen(pdf, seite, mindest=8.0, hoehe=841.89):
    daten = Path(pdf).read_bytes()
    objs = {int(m.group(1)): m.group(2)
            for m in re.finditer(rb"(\d+)\s+0\s+obj(.*?)endobj", daten, re.S)}
    seiten = sorted(n for n, b in objs.items() if re.search(rb"/Type\s*/Page[^s]", b))
    body = objs[seiten[seite - 1]]
    gefunden = []
    for cn in re.findall(rb"/Contents\s+(\d+)\s+0\s+R", body):
        o = objs[int(cn)]
        m = re.search(rb"stream\r?\n(.*)\r?\nendstream", o, re.S)
        if not m:
            continue
        try:
            s = zlib.decompress(m.group(1))
        except Exception:
            continue
        ctm = (1, 0, 0, 1, 0, 0)
        stack, pend, pts = [], [], []
        fill = strich = (0, 0, 0)
        for t in TOKEN.finditer(s):
            if t.group("num"):
                pend.append(float(t.group("num"))); continue
            if t.group("name") or t.group("arr"):
                pend.append("x"); continue
            op = t.group("op").decode()
            if op == "q":
                stack.append((ctm, fill, strich))
            elif op == "Q":
                if stack: ctm, fill, strich = stack.pop()
            elif op == "cm" and len(pend) >= 6:
                ctm = mul(tuple(pend[-6:]), ctm)
            elif op == "rg" and len(pend) >= 3:
                fill = tuple(pend[-3:])
            elif op == "RG" and len(pend) >= 3:
                strich = tuple(pend[-3:])
            elif op in ("m", "l") and len(pend) >= 2:
                pts.append(apply(ctm, pend[-2], pend[-1]))
            elif op == "c" and len(pend) >= 6:
                for i in (0, 2, 4):
                    pts.append(apply(ctm, pend[-6 + i], pend[-6 + i + 1]))
            elif op == "re" and len(pend) >= 4:
                x, y, w, h = pend[-4:]
                for px, py in ((x, y), (x + w, y), (x + w, y + h), (x, y + h)):
                    pts.append(apply(ctm, px, py))
            elif op in ("f", "f*", "S", "B", "B*"):
                if pts:
                    xs = [p[0] for p in pts]; ys = [hoehe - p[1] for p in pts]
                    b = (min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys))
                    if b[2] >= mindest and b[3] >= 3:
                        farbe = fill if op in ("f", "f*", "B", "B*") else strich
                        gefunden.append((round(b[0], 1), round(b[1], 1), round(b[2], 1),
                                         round(b[3], 1),
                                         "#%02x%02x%02x" % tuple(round(v * 255) for v in farbe),
                                         "Füllung" if op in ("f", "f*", "B", "B*") else "Rahmen"))
                pts = []
            elif op == "n":
                pts = []
            pend = []
    return sorted(set(gefunden), key=lambda t: (t[1], t[0]))


if __name__ == "__main__":
    pdf, seite = sys.argv[1], int(sys.argv[2])
    mindest = float(sys.argv[3]) if len(sys.argv) > 3 else 8.0
    print(f"Flächen auf Seite {seite} (ab {mindest} pt Breite):")
    for x, y, w, h, farbe, art in flaechen(pdf, seite, mindest):
        print(f"   x={x:6.1f} y={y:6.1f}  {w:6.1f} × {h:6.1f}  {farbe}  {art}")
