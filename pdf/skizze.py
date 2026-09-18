#!/usr/bin/env python3
"""Schneidet einen Bereich einer PDF-Seite als SVG heraus.

    python3 pdf/skizze.py <pdf> <seite> <x> <y> <breite> <hoehe> <ziel.svg>

Koordinaten in Punkt, gemessen von der linken oberen Ecke der Seite (so wie
bauplan.py sie ausgibt). Übernommen werden alle Vektorpfade, deren Mittelpunkt
im Bereich liegt - Text bleibt außen vor, der gehört ins HTML.

Damit lassen sich die Skizzen aus den alten PDFs übernehmen, statt sie
nachzuzeichnen.
"""
import re
import sys
import zlib


def mul(m, n):
    a, b, c, d, e, f = m
    A, B, C, D, E, F = n
    return (a*A + b*C, a*B + b*D, c*A + d*C, c*B + d*D, e*A + f*C + E, e*B + f*D + F)


def apply(m, x, y):
    a, b, c, d, e, f = m
    return (a*x + c*y + e, b*x + d*y + f)


TOKEN = re.compile(rb"(?P<num>-?\d*\.?\d+)\s|(?P<name>/[A-Za-z0-9#+\-.]+)|"
                   rb"(?P<arr>\[[^\]]*\])|(?P<op>[A-Za-z'\"*]+)")


def hexcol(c):
    return "#%02x%02x%02x" % tuple(max(0, min(255, round(v * 255))) for v in c)


def stream_of(body):
    m = re.search(rb"stream\r?\n(.*)\r?\nendstream", body, re.S)
    if not m:
        return None
    try:
        return zlib.decompress(m.group(1)) if b"FlateDecode" in body else m.group(1)
    except Exception:
        return None


class Sammler:
    def __init__(self, objs, bereich, seitenhoehe=841.89):
        self.objs = objs
        self.bereich = bereich          # (x, y_top, breite, hoehe)
        self.h = seitenhoehe
        self.pfade = []
        self.gs = {}
        self.kasten = None   # Umriss aller uebernommenen Pfade

    def alpha(self, num):
        if num not in self.gs:
            b = self.objs.get(num, b"")
            d = {}
            for k in (b"CA", b"ca", b"LW"):
                m = re.search(rb"/" + k + rb"\s+([\d.]+)", b)
                if m:
                    d[k.decode()] = float(m.group(1))
            self.gs[num] = d
        return self.gs[num]

    def drin(self, punkte):
        """Pfad gehoert zum Ausschnitt, wenn sein Mittelpunkt darin liegt - und er
        nicht wesentlich groesser ist als der Ausschnitt selbst. Ohne die zweite
        Bedingung rutscht die Hintergrundflaeche der Seite mit hinein."""
        x, y, w, h = self.bereich
        xs = [p[0] for p in punkte]; ys = [self.h - p[1] for p in punkte]
        cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
        if not (x <= cx <= x + w and y <= cy <= y + h):
            return False
        return (max(xs) - min(xs)) <= w * 1.08 and (max(ys) - min(ys)) <= h * 1.08

    def lauf(self, stream, body, ctm, st, tiefe=0):
        if tiefe > 6:
            return
        xrefs = {n.decode(): int(r) for n, r in re.findall(rb"/(X\d+)\s+(\d+)\s+0\s+R", body)}
        grefs = {n.decode(): int(r) for n, r in re.findall(rb"/(G\d+)\s+(\d+)\s+0\s+R", body)}
        stack, pend, punkte, teile = [], [], [], []
        st = dict(st)
        cur = None

        def ablegen(modus):
            nonlocal teile, punkte
            if teile and self.drin(punkte):
                a = [f'd="{" ".join(teile)}"']
                if modus == "S":
                    a += ['fill="none"', f'stroke="{hexcol(st["stroke"])}"',
                          f'stroke-width="{round(st["lw"], 2)}"']
                    if st["alpha_s"] < 1:
                        a.append(f'stroke-opacity="{round(st["alpha_s"], 3)}"')
                    if st["dash"]:
                        a.append(f'stroke-dasharray="{st["dash"]}"')
                else:
                    a += [f'fill="{hexcol(st["fill"])}"', 'stroke="none"']
                    if st["alpha_f"] < 1:
                        a.append(f'fill-opacity="{round(st["alpha_f"], 3)}"')
                self.pfade.append("<path " + " ".join(a) + "/>")
                xs = [q[0] for q in punkte]; ys = [self.h - q[1] for q in punkte]
                k = (min(xs), min(ys), max(xs), max(ys))
                self.kasten = k if self.kasten is None else (
                    min(self.kasten[0], k[0]), min(self.kasten[1], k[1]),
                    max(self.kasten[2], k[2]), max(self.kasten[3], k[3]))
            teile, punkte = [], []

        for t in TOKEN.finditer(stream):
            if t.group("num"):
                pend.append(float(t.group("num"))); continue
            if t.group("name"):
                pend.append(t.group("name")[1:].decode()); continue
            if t.group("arr"):
                pend.append(t.group("arr").decode()); continue
            op = t.group("op").decode()

            if op == "q":
                stack.append((ctm, dict(st)))
            elif op == "Q":
                if stack:
                    ctm, st = stack.pop(); st = dict(st)
            elif op == "cm" and len(pend) >= 6:
                ctm = mul(tuple(pend[-6:]), ctm)
            elif op == "RG" and len(pend) >= 3:
                st["stroke"] = tuple(pend[-3:])
            elif op == "rg" and len(pend) >= 3:
                st["fill"] = tuple(pend[-3:])
            elif op == "G" and pend:
                st["stroke"] = (pend[-1],) * 3
            elif op == "g" and pend:
                st["fill"] = (pend[-1],) * 3
            elif op == "w" and pend:
                st["lw"] = pend[-1] * abs(ctm[0] or 1)
            elif op == "d" and pend:
                arr = [p for p in pend if isinstance(p, str) and p.startswith("[")]
                if arr:
                    nums = [float(v) * abs(ctm[0] or 1) for v in arr[-1].strip("[]").split()]
                    st["dash"] = " ".join(str(round(n, 2)) for n in nums) if nums else ""
            elif op == "gs" and pend:
                g = self.alpha(grefs.get(pend[-1], -1))
                if "CA" in g: st["alpha_s"] = g["CA"]
                if "ca" in g: st["alpha_f"] = g["ca"]
                if "LW" in g: st["lw"] = g["LW"] * abs(ctm[0] or 1)
            elif op == "m" and len(pend) >= 2:
                p = apply(ctm, pend[-2], pend[-1])
                teile.append(f"M{round(p[0],2)} {round(self.h-p[1],2)}")
                punkte.append(p); cur = p
            elif op == "l" and len(pend) >= 2:
                p = apply(ctm, pend[-2], pend[-1])
                teile.append(f"L{round(p[0],2)} {round(self.h-p[1],2)}")
                punkte.append(p); cur = p
            elif op == "c" and len(pend) >= 6:
                q = pend[-6:]
                a1 = apply(ctm, q[0], q[1]); a2 = apply(ctm, q[2], q[3]); a3 = apply(ctm, q[4], q[5])
                teile.append("C%s %s %s %s %s %s" % (
                    round(a1[0], 2), round(self.h - a1[1], 2), round(a2[0], 2),
                    round(self.h - a2[1], 2), round(a3[0], 2), round(self.h - a3[1], 2)))
                punkte += [a1, a2, a3]; cur = a3
            elif op in ("v", "y") and len(pend) >= 4:
                q = pend[-4:]
                a1 = apply(ctm, q[0], q[1]); a2 = apply(ctm, q[2], q[3])
                s0 = cur or a1
                teile.append("C%s %s %s %s %s %s" % (
                    round(s0[0], 2), round(self.h - s0[1], 2), round(a1[0], 2),
                    round(self.h - a1[1], 2), round(a2[0], 2), round(self.h - a2[1], 2)))
                punkte += [a1, a2]; cur = a2
            elif op == "re" and len(pend) >= 4:
                x, y, w, h = pend[-4:]
                ps = [apply(ctm, x, y), apply(ctm, x + w, y),
                      apply(ctm, x + w, y + h), apply(ctm, x, y + h)]
                teile.append("M%s %sL%s %sL%s %sL%s %sZ" % tuple(
                    v for p in ps for v in (round(p[0], 2), round(self.h - p[1], 2))))
                punkte += ps
            elif op == "h":
                teile.append("Z")
            elif op in ("S", "s"):
                ablegen("S")
            elif op in ("f", "f*", "F"):
                ablegen("f")
            elif op in ("B", "B*", "b", "b*"):
                merk, mp = list(teile), list(punkte)
                ablegen("f"); teile, punkte = merk, mp; ablegen("S")
            elif op == "n":
                teile, punkte = [], []
            elif op == "Do" and pend:
                num = xrefs.get(pend[-1])
                if num and num in self.objs:
                    sub = self.objs[num]
                    sm = re.search(rb"/Matrix\s*\[([^\]]*)\]", sub)
                    base = tuple(float(v) for v in sm.group(1).split()) if sm else (1, 0, 0, 1, 0, 0)
                    s2 = stream_of(sub)
                    if s2:
                        self.lauf(s2, sub, mul(base, ctm), st, tiefe + 1)
            pend = []


def beschriftung(pdf, seite, bereich, hoehe=841.89, kasten=None):
    """Textzeilen im Bereich als SVG-<text>-Elemente."""
    sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
    from bauplan import load, cmaps, font_info, parse_page
    objs = load(pdf)
    fonts = font_info(objs, cmaps(objs))
    seiten = sorted(n for n, b in objs.items() if re.search(rb"/Type\s*/Page[^s]", b))
    _, _, _, glyphen = parse_page(objs, fonts, seiten[seite - 1], mit_glyphen=True)
    x, y, w, h = bereich
    if kasten:                      # eng am tatsaechlichen Umriss der Grafik
        x = max(x, kasten[0] - 6); y = max(y, kasten[1] - 8)
        w = min(x + w, kasten[2] + 6) - x; h = min(y + h, kasten[3] + 8) - y
    out = []
    for g in glyphen:
        if not (x <= g["x"] <= x + w and y - 4 <= g["y_top"] <= y + h + 2):
            continue
        farbe = "#%02x%02x%02x" % tuple(round(v * 255) for v in g["farbe"])
        fett = ' font-weight="600"' if "Sem" in g["font"] or "Bold" in g["font"] else ""
        serif = ("Lora, Georgia, serif" if "Lora" in g["font"] or g["font"] == "?"
                 else "Poppins, Arial, sans-serif")
        zeichen = (g["t"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
        if not zeichen.strip():
            continue
        out.append(f'<text x="{g["x"]}" y="{g["y_top"]}" font-family="{serif}" '
                   f'font-size="{g["size"]}" fill="{farbe}"{fett}>{zeichen}</text>')
    return out


def main():
    pdf, seite = sys.argv[1], int(sys.argv[2])
    x, y, w, h = (float(v) for v in sys.argv[3:7])
    ziel = sys.argv[7]

    daten = open(pdf, "rb").read()
    objs = {int(m.group(1)): m.group(2)
            for m in re.finditer(rb"(\d+)\s+0\s+obj(.*?)endobj", daten, re.S)}
    seiten = sorted(n for n, b in objs.items() if re.search(rb"/Type\s*/Page[^s]", b))
    body = objs[seiten[seite - 1]]

    s = Sammler(objs, (x, y, w, h))
    st = {"stroke": (0, 0, 0), "fill": (0, 0, 0), "lw": 1.0, "dash": "",
          "alpha_s": 1.0, "alpha_f": 1.0}
    for cn in re.findall(rb"/Contents\s+(\d+)\s+0\s+R", body):
        strom = stream_of(objs[int(cn)])
        if strom:
            s.lauf(strom, body, (1, 0, 0, 1, 0, 0), st)

    texte = beschriftung(pdf, seite, (x, y, w, h), kasten=s.kasten)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x} {y} {w} {h}" fill="none">\n'
           + "\n".join(s.pfade + texte) + "\n</svg>\n")
    open(ziel, "w").write(svg)
    print(f"  {ziel.split('/')[-1]}: {len(s.pfade)} Pfade, {len(texte)} Beschriftungen")


if __name__ == "__main__":
    main()
