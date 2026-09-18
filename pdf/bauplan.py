"""Liest aus einem Chrome-gedruckten PDF den Layout-Bauplan:
Textzeilen mit Position/Größe/Farbe, gefüllte Flächen, Bilder."""
import re, zlib, sys, json
from collections import defaultdict


def mul(m, n):
    a, b, c, d, e, f = m
    A, B, C, D, E, F = n
    return (a*A + b*C, a*B + b*D, c*A + d*C, c*B + d*D, e*A + f*C + E, e*B + f*D + F)


def apply(m, x, y):
    a, b, c, d, e, f = m
    return (a*x + c*y + e, b*x + d*y + f)


def load(path):
    """Objekte des PDFs. Folgt der xref-Kette, damit bei inkrementell
    aktualisierten Dateien die neueste Fassung eines Objekts gilt."""
    data = open(path, "rb").read()
    objs = {}
    for m in re.finditer(rb"(\d+)\s+0\s+obj(.*?)endobj", data, re.S):
        objs[int(m.group(1))] = m.group(2)

    try:
        pos = int(re.findall(rb"startxref\s+(\d+)", data)[-1])
    except IndexError:
        return objs
    gesehen = set()
    aktuell = {}
    while pos and pos not in gesehen:
        gesehen.add(pos)
        if data[pos:pos + 4] != b"xref":
            break
        i = pos + 4
        while True:
            m = re.match(rb"\s*(\d+)\s+(\d+)\s*\n", data[i:i + 40])
            if not m:
                break
            start, anzahl = int(m.group(1)), int(m.group(2))
            i += m.end()
            for k in range(anzahl):
                em = re.match(rb"(\d{10}) (\d{5}) ([nf])", data[i:i + 20])
                i += 20
                if em and em.group(3) == b"n":
                    aktuell.setdefault(start + k, int(em.group(1)))
        tm = re.search(rb"trailer\s*<<(.*?)>>", data[i:i + 2000], re.S)
        prev = re.search(rb"/Prev\s+(\d+)", tm.group(1)) if tm else None
        pos = int(prev.group(1)) if prev else None

    for num, off in aktuell.items():
        m = re.match(rb"\s*\d+\s+0\s+obj", data[off:off + 40])
        if m:
            ende = data.find(b"endobj", off)
            if ende > off:
                objs[num] = data[off + m.end():ende]
    return objs


def stream_of(body):
    m = re.search(rb"stream\r?\n(.*?)\r?\nendstream", body, re.S)
    if not m:
        return None
    try:
        return zlib.decompress(m.group(1)) if b"FlateDecode" in body else m.group(1)
    except Exception:
        return None


def cmaps(objs):
    out = {}
    for num, body in objs.items():
        s = stream_of(body)
        if not s or (b"beginbfchar" not in s and b"beginbfrange" not in s):
            continue
        mp = {}
        for mm in re.finditer(rb"beginbfchar(.*?)endbfchar", s, re.S):
            for a, b in re.findall(rb"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>", mm.group(1)):
                mp[int(a, 16)] = bytes.fromhex(b.decode()).decode("utf-16-be", "replace")
        for mm in re.finditer(rb"beginbfrange(.*?)endbfrange", s, re.S):
            for a, b, c in re.findall(rb"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>", mm.group(1)):
                lo, hi, dst = int(a, 16), int(b, 16), int(c, 16)
                for i in range(lo, hi + 1):
                    mp[i] = chr(dst + (i - lo))
        if mp:
            out[num] = mp
    return out


def font_info(objs, cm):
    info = {}
    for num, body in objs.items():
        m = re.search(rb"/ToUnicode\s+(\d+)\s+0\s+R", body)
        if not m or int(m.group(1)) not in cm:
            continue
        name = re.search(rb"/BaseFont\s*/([A-Za-z0-9+\-,_]+)", body)
        info[num] = {"cmap": cm[int(m.group(1))],
                     "name": name.group(1).decode() if name else "?"}
    return info


TOKEN = re.compile(rb"""
    (?P<num>-?\d*\.?\d+)\s
  | (?P<name>/[A-Za-z0-9#+\-.]+)
  | (?P<hex><[0-9A-Fa-f\s]*>)
  | (?P<op>[A-Za-z'"*]+)
""", re.X)


def parse_page(objs, fonts, page_obj, page_height=842.0, mit_glyphen=False):
    body = objs[page_obj]
    res = {n.decode(): int(r) for n, r in re.findall(rb"/(F\d+)\s+(\d+)\s+0\s+R", body)}
    xobj = {n.decode(): int(r) for n, r in re.findall(rb"/(X\d+)\s+(\d+)\s+0\s+R", body)}
    glyphs, rects, images = [], [], []

    for cnum in re.findall(rb"/Contents\s+(\d+)\s+0\s+R", body):
        s = stream_of(objs.get(int(cnum), b"")) or b""
        ctm = (1, 0, 0, 1, 0, 0)
        stack = []
        stackops = []
        fill = (0, 0, 0)
        cur_font = None
        cur_size = 0
        pending = []
        offen = None
        tm = tlm = (1, 0, 0, 1, 0, 0)
        leading = 0.0

        for t in TOKEN.finditer(s):
            if t.group("num"):
                pending.append(float(t.group("num")))
                continue
            if t.group("name"):
                pending.append(t.group("name")[1:].decode())
                continue
            if t.group("hex"):
                pending.append(("hex", re.sub(rb"\s", b"", t.group("hex")[1:-1])))
                continue
            op = t.group("op").decode()

            if op == "q":
                stack.append(ctm); stackops.append(fill)
            elif op == "Q":
                if stack: ctm = stack.pop(); fill = stackops.pop()
            elif op == "cm" and len(pending) >= 6:
                ctm = mul(tuple(pending[-6:]), ctm)
            elif op in ("rg", "sc", "scn") and len(pending) >= 3:
                fill = tuple(round(v, 4) for v in pending[-3:])
            elif op == "g" and len(pending) >= 1:
                v = pending[-1]; fill = (v, v, v)
            elif op == "Tf" and len(pending) >= 2:
                cur_font = res.get(pending[-2]); cur_size = pending[-1]
            elif op == "BT":
                tm = tlm = (1, 0, 0, 1, 0, 0)
            elif op == "Tm" and len(pending) >= 6:
                tm = tlm = tuple(pending[-6:])
            elif op == "TL" and pending:
                leading = pending[-1]
            elif op in ("Td", "TD") and len(pending) >= 2:
                if op == "TD":
                    leading = -pending[-1]
                tlm = mul((1, 0, 0, 1, pending[-2], pending[-1]), tlm)
                tm = tlm
            elif op == "T*":
                tlm = mul((1, 0, 0, 1, 0, -leading), tlm)
                tm = tlm
            elif op == "re" and len(pending) >= 4:
                x, y, w, h = pending[-4:]
                p0 = apply(ctm, x, y); p1 = apply(ctm, x + w, y + h)
                pending = []
                offen = {"x": round(min(p0[0], p1[0]), 2),
                         "y_top": round(page_height - max(p0[1], p1[1]), 2),
                         "w": round(abs(p1[0] - p0[0]), 2),
                         "h": round(abs(p1[1] - p0[1]), 2)}
                continue
            elif op in ("f", "f*", "B", "B*") and offen:
                offen["farbe"] = fill
                offen["art"] = "fuellung"
                rects.append(offen); offen = None
            elif op in ("W", "W*", "n", "S", "s"):
                offen = None   # Clip-Pfad, verworfen oder nur Kontur: keine Flaeche
            elif op == "Do" and pending:
                px, py = apply(ctm, 0, 0)
                sx, sy = apply(ctm, 1, 1)
                images.append({"name": pending[-1], "x": round(px, 2),
                               "y_top": round(page_height - py, 2),
                               "w": round(abs(sx - px), 2), "h": round(abs(sy - py), 2)})
            elif op in ("Tj", "TJ"):
                txt = ""
                cmp_ = fonts.get(cur_font, {}).get("cmap", {})
                for item in pending:
                    if isinstance(item, tuple) and item[0] == "hex":
                        h = item[1]
                        for i in range(0, len(h), 4):
                            txt += cmp_.get(int(h[i:i + 4], 16), "")
                if txt:
                    full = mul(tm, ctm)
                    px, py = apply(full, 0, 0)
                    scale = abs(full[3]) or 1
                    glyphs.append({"t": txt, "x": round(px, 2),
                                   "y_top": round(page_height - py, 2),
                                   "size": round(cur_size * scale, 2),
                                   "font": fonts.get(cur_font, {}).get("name", "?"),
                                   "farbe": fill})
            if op not in ("re",):
                pending = []

    # Glyphen zu Zeilen gruppieren, dabei getrennte Bloecke auf gleicher Hoehe trennen
    lines = defaultdict(list)
    for g in glyphs:
        lines[(round(g["y_top"], 1), g["size"], g["font"], g["farbe"])].append(g)
    out = []
    for (y, size, font, farbe), gs in lines.items():
        gs.sort(key=lambda g: g["x"])
        gaps = sorted(b["x"] - a["x"] for a, b in zip(gs, gs[1:]))
        # Median der Buchstabenabstaende als Massstab: Wortabstaende liegen klar darueber
        med = gaps[len(gaps) // 2] if gaps else size * 0.5
        med = med if med > 0.1 else size * 0.5
        wort = med * 1.55
        block = max(med * 3.5, size * 1.2)
        blocks, cur = [], [gs[0]]
        for prev, g in zip(gs, gs[1:]):
            if g["x"] - prev["x"] > block:
                blocks.append(cur); cur = [g]
            else:
                cur.append(g)
        blocks.append(cur)
        for b in blocks:
            text = b[0]["t"]
            for prev, g in zip(b, b[1:]):
                if g["x"] - prev["x"] > wort and not text.endswith(" ") and g["t"] != " ":
                    text += " "
                text += g["t"]
            out.append({"y_top": y, "x": round(b[0]["x"], 2),
                        "x_ende": round(b[-1]["x"], 2),
                        "size": size, "font": font, "farbe": farbe,
                        "text": re.sub(r"\s+", " ", text).strip()})
    out.sort(key=lambda r: (r["y_top"], r["x"]))
    if mit_glyphen:
        return out, rects, images, glyphs
    return out, rects, images


def main(path):
    objs = load(path)
    fonts = font_info(objs, cmaps(objs))
    pages = sorted(n for n, b in objs.items() if re.search(rb"/Type\s*/Page[^s]", b))
    doc = []
    for i, p in enumerate(pages, 1):
        lines, rects, images = parse_page(objs, fonts, p)
        doc.append({"seite": i, "zeilen": lines, "flaechen": rects, "bilder": images})
    return doc


if __name__ == "__main__":
    doc = main(sys.argv[1])
    if len(sys.argv) > 2 and sys.argv[2] == "--json":
        print(json.dumps(doc, ensure_ascii=False, indent=1))
    else:
        for p in doc:
            print(f"\n{'='*70}\nSEITE {p['seite']}  ({len(p['zeilen'])} Zeilen, "
                  f"{len(p['flaechen'])} Flächen, {len(p['bilder'])} Bilder)\n{'='*70}")
            for r in p["zeilen"]:
                c = "#%02x%02x%02x" % tuple(int(v * 255) for v in r["farbe"])
                print(f"  y={r['y_top']:7.1f} x={r['x']:6.1f}–{r['x_ende']:6.1f} "
                      f"{r['size']:5.1f}pt {c} {r['font'][:18]:18} {r['text'][:70]}")
            for f in p["flaechen"]:
                c = "#%02x%02x%02x" % tuple(int(v * 255) for v in f["farbe"])
                print(f"  FLÄCHE y={f['y_top']:7.1f} x={f['x']:6.1f} {f['w']:6.1f}×{f['h']:6.1f} {c}")
            for im in p["bilder"]:
                print(f"  BILD   y={im['y_top']:7.1f} x={im['x']:6.1f} {im['w']:6.1f}×{im['h']:6.1f} {im['name']}")
