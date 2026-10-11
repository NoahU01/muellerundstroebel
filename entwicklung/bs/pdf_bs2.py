#!/usr/bin/env python3
"""PDF „Was wir tun und wofür wir stehen“ zur Business Story 2.0 (nur Branch daniel).

Baut entwicklung/pdf-bs2/business-story-2.html aus denselben Inhalten wie die Landingpage
(entwicklung/bs/bs2.py), druckt daraus entwicklung/downloads/business-story-2.pdf und legt
Vorschaubilder für den Download-Kasten an (Seite 1 und 2 als PNG).

    python3 entwicklung/bs/pdf_bs2.py
"""
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "pdf"))
import bs2 as b          # Inhalte der Landingpage
import bauen as druck    # Chrome-Druck und lokaler Server aus pdf/bauen.py

WURZEL = Path(__file__).resolve().parents[2]
QUELLE = WURZEL / "entwicklung" / "pdf-bs2" / "business-story-2.html"
ZIEL = WURZEL / "entwicklung" / "downloads" / "business-story-2.pdf"
LOGO, LOGO_WEISS = "/assets/logo.svg", "/pdf/bausteine/logo-weiss.svg"
DOKUMENT = "Was wir tun und wofür wir stehen"
KONTAKT_TEXT = ("Erzählen Sie uns, was ansteht. Wir sagen offen, ob und wie wir es gemeinsam mit Ihnen umsetzen, "
                "und geben direkt unsere Meinung. Kein Pitch, keine Rechnung.")
VERSPRECHEN = "Sie geben uns ein Thema und die Verantwortung dafür. Wir liefern das Ergebnis."
HAKEN = '<svg viewBox="0 0 20 20"><path d="M4.5 10.5l3.5 3.5 7.5-8"/></svg>'
ICO = {  # dünne Strich-Icons wie auf der Landingpage
    "team": '<svg viewBox="0 0 24 24"><circle cx="9" cy="8" r="3.2"/><path d="M3.5 19.5c.6-3.3 2.7-5 5.5-5s4.9 1.7 5.5 5"/><circle cx="17" cy="9" r="2.5"/><path d="M16 14.6c2.4.1 4 1.6 4.5 4.4"/></svg>',
    "extern": '<svg viewBox="0 0 24 24"><rect x="3" y="7.5" width="18" height="12.5" rx="2"/><path d="M8.5 7.5V5.8A1.8 1.8 0 0 1 10.3 4h3.4a1.8 1.8 0 0 1 1.8 1.8v1.7M3 12.5h18"/></svg>',
    "workshop": '<svg viewBox="0 0 24 24"><rect x="3.5" y="5" width="17" height="15.5" rx="2"/><path d="M3.5 9.5h17M8 3v4M16 3v4M7.5 13.5h3M13.5 13.5h3M7.5 17h3"/></svg>',
}
NETZ = [  # (Name, Pfad) – wie auf der Landingpage
    ("Ehemalige Vorstände", '<path d="M3 9.5 12 4l9 5.5"/><path d="M5 10v8M9.5 10v8M14.5 10v8M19 10v8"/><path d="M3 20.5h18"/>'),
    ("Aufsichtsräte", '<circle cx="12" cy="6.5" r="2.3"/><circle cx="5.5" cy="11" r="2"/><circle cx="18.5" cy="11" r="2"/><path d="M3 20h18M6 20v-3.5h12V20"/>'),
    ("IT- und Prozess-Spezialisten", '<rect x="3" y="4.5" width="18" height="12" rx="1.5"/><path d="M9 20h6M12 16.5V20M7.5 10.5h3l1.5-2 1.5 4 1.5-2h1.5"/>'),
    ("Entwickler", '<path d="M8.5 7.5 4 12l4.5 4.5M15.5 7.5 20 12l-4.5 4.5M13.5 5l-3 14"/>'),
    ("Marketingexperten", '<path d="M4 10v4h3l6 4V6L7 10H4Z"/><path d="M16.5 9a4 4 0 0 1 0 6M19 6.5a7.5 7.5 0 0 1 0 11"/>'),
    ("Grafiker", '<path d="M4 20l1.2-4.2L15.5 5.5a2 2 0 0 1 2.8 0l.2.2a2 2 0 0 1 0 2.8L8.2 18.8 4 20Z"/><path d="M13.5 7.5l3 3"/>'),
]
WEGE = [  # Ihre Lage: (Farbe, Bezeichnung, Aussage, Icon, Ergänzung) – wie Landingpage Variante 2
    ("sand", "Ihr Team", "Liefert, aber nicht so, wie Sie es brauchen.", "team",
     "Typisch bei der Vorlage für den Aufsichtsrat oder dem Konzept für die Bereiche. Am Ende greifen Sie wieder selbst ein."),
    ("navy", "Externe", "Empfehlungen ja. Umsetzen bleibt bei Ihnen.", "extern",
     "Strategieberater, Projektmanager, Spezialisten: Die Koordination und die Verantwortung für das Ergebnis bleiben bei Ihnen."),
    ("hell", "Nur Workshops", "Zwei Tage im Kalender. Dann wochenlang Stillstand.", "workshop",
     "Große Themen werden zur Hürde. Es geht erst weiter, wenn wieder Zeit im Kalender ist."),
]
ABLAUF = [("Kurzer Austausch", "Telefonat, Videokonferenz, Workshop, wenn er sinnvoll ist. Oft reicht ein kurzer Austausch."),
          ("Wir arbeiten", "Mit Ihren Leuten, selbst und mit Spezialisten aus unserem Netzwerk."),
          ("Nächster Austausch", "Wir kommen mit einem klaren Bild zurück und setzen eine Stufe höher an.")]


def leiste(label, dunkel=False):
    return f'<div class="leiste"><img src="{LOGO_WEISS if dunkel else LOGO}" alt="Müller &amp; Ströbel"><span>{label}</span></div>'


def fuss(nr, gesamt):
    return f'<div class="fuss"><span>Müller &amp; Ströbel · {DOKUMENT}</span><span>Seite {nr} / {gesamt}</span></div>'


def posts(klein=False):
    return '<div class="posts">' + "".join(
        f'<article class="post"><div class="post__bild post__bild--{f}"><small>{t}</small><b>{x}</b>{ICO[k]}</div>'
        f'{"" if klein else f"<p class=post__text>{e}</p>"}</article>' for f, t, x, k, e in WEGE) + '</div>'


def ablauf():
    return '<ol class="ablauf">' + "".join(f"<li><b>{t}</b><span>{x}</span></li>" for t, x in ABLAUF) + "</ol>"


def kreis(k, gross=112):
    return f'<div class="kreis" style="width:{gross}pt;height:{gross}pt"><img src="/assets/{k}-portrait.webp" alt=""></div>'


def op_person(k):
    p = b.PERSONEN[k]
    return f'<div class="op-person">{kreis(k, 44)}<div><b>{p["name"]}</b><span>{p["rolle"]}<br>{p["mail"]}<br>{p["tel"]}</span></div></div>'


def gebiet_detail(k):
    t = b.thema_detail(k)
    desc = re.search(r"</h3>\s*<p>(.*?)</p>", t, re.S).group(1)
    tun = re.findall(r"<li>(.*?)</li>", t)
    erg = re.search(r"Ihr Ergebnis</h4>\s*<p>(.*?)</p>", t, re.S).group(1)
    return desc, tun, erg


def kreismodell():
    t = (WURZEL / "pdf" / "wer-wir-sind.html").read_text(encoding="utf-8")
    abschnitt = t[t.index("Seite 7: Das Geschäftsmodell"):]
    return re.search(r"<svg viewBox=\"0 0 520 520\".*?</svg>", abschnitt, re.S).group(0)


def seiten():
    S = []
    # 1 Deckblatt
    S.append(("navy deck", f'''{leiste(DOKUMENT, True)}
  <img class="deck__amp" src="/pdf/bausteine/ampersand-konstruktion.svg" alt="">
  <div class="deck__text">
    <p class="kicker">Für Führungskräfte in der Versicherungsbranche</p>
    <h1>Komplexe Situationen strukturieren, entscheiden, umsetzen.</h1>
    <p class="unter">Die Vorlage für den Aufsichtsrat, die Strategie für die Bereiche, die Kennzahlen, die steuern sollen: Wir übernehmen Ihr Thema und sorgen dafür, dass es vorankommt. Mit wenig Aufwand für Sie.</p>
  </div>''', False))
    # 2 Ihre Lage
    S.append(("sand", f'''{leiste("Ihre Lage")}
  <p class="kicker">Ihre Lage</p>
  <h2>„Es ging schon wieder nichts voran.“</h2>
  <p class="unter">Die Vorlage für den Aufsichtsrat, die Strategie für die Bereiche, das Projekt, das seit Monaten hängt: Alles läuft über Ihren Tisch. Und die üblichen Wege helfen nur halb.</p>
  <div class="block">{posts()}</div>
  <div class="kern"><p class="kicker">Was Sie brauchen</p><p>Jemanden, der Ihr Thema versteht, es strukturiert, die Bearbeitung übernimmt und das Ergebnis liefert. Mit wenig Aufwand für Sie.</p></div>''', True))
    # 3 So arbeiten wir
    netz = "".join(f'<li><svg viewBox="0 0 24 24">{p}</svg>{n}</li>' for n, p in NETZ)
    S.append(("", f'''{leiste("So arbeiten wir")}
  <p class="kicker">So arbeiten wir</p>
  <h2>Die Zusammenarbeit passt in Ihren Kalender.</h2>
  <div class="text unter">
    <p>Wir bleiben im regelmäßigen, kurzen Austausch. Meist reicht ein Telefonat zwischen zwei Terminen oder auf der Fahrt. Wenn es ein Thema braucht, nehmen wir uns eine längere Videokonferenz, und wenn es sinnvoll ist, einen Workshop.</p>
    <p><b>So bleibt Ihr Thema präsent, auch wenn Sie gerade im Tagesgeschäft stecken.</b></p>
  </div>
  <div class="block">{ablauf()}</div>
  <div class="block netz"><p class="kicker">Unser Netzwerk</p><h3>Wenn ein Thema mehr braucht, holen wir die passenden Leute dazu.</h3>
    <p>Sie behalten einen Ansprechpartner. Die Koordination liegt bei uns.</p><ul>{netz}</ul></div>''', True))
    # 4 Ihr Ergebnis
    S.append(("navy ergebnis", f'''{leiste("Ihr Ergebnis", True)}
  <div class="ergebnis__szene">{b.trio_szene("compass", "circle-check", "target")}</div>
  <div class="ergebnis__text">
    <p class="kicker">Ihr Ergebnis</p>
    <h2>Sie haben Ihre Themen im Griff.</h2>
    <p class="unter">Im Gespräch behalten wir das Zielbild im Blick und schaffen Klarheit, wohin es geht. Sie entscheiden und konzentrieren sich auf die richtigen Dinge.</p>
    <ul class="haken">
      <li>{HAKEN}Sie wissen jederzeit, wo Ihr Thema steht und wie das Zielbild aussieht.</li>
      <li>{HAKEN}Ihre Vorhaben laufen weiter, während Sie im Tagesgeschäft sind.</li>
      <li>{HAKEN}Sie verwalten keinen Mangel mehr. Sie steuern.</li>
    </ul>
  </div>''', True))
    # 5 Einsatzgebiete – Überblick
    weiss_ico = {k: b.icon(k).replace('stroke="currentColor"', 'stroke="#ffffff"') for k, _, _ in b.THEMEN}
    gebiete = "".join(f'<div class="gebiet"><span class="gebiet__ico">{weiss_ico[k]}</span>'
                      f'<span class="gebiet__nr">0{i}</span><h3>{n}</h3><p>{w}</p></div>' for i, (k, n, w) in enumerate(b.THEMEN, 1))
    S.append(("", f'''{leiste("Einsatzgebiete")}
  <p class="kicker">Einsatzgebiete</p>
  <h2>Hier setzen wir an.</h2>
  <p class="unter">Sechs Felder, in denen Führungskräfte uns typischerweise dazuholen. Auf den folgenden Seiten: was wir jeweils konkret tun und was Sie davon haben.</p>
  <div class="block gebiete">{gebiete}</div>''', True))
    # 6–7 Einsatzgebiete im Detail
    for teil in (b.THEMEN[:2], b.THEMEN[2:4], b.THEMEN[4:]):
        bloecke = ""
        for k, n, w in teil:
            i = [x[0] for x in b.THEMEN].index(k) + 1
            desc, tun, erg = gebiet_detail(k)
            bloecke += (f'<div class="detail"><div><span class="detail__nr">0{i}</span><h3>{n}</h3><p class="detail__wenn">{w}</p></div>'
                        f'<div class="detail__text"><p>{desc}</p><h4>Was wir konkret tun</h4><ul>{"".join(f"<li>{x}</li>" for x in tun)}</ul>'
                        f'<p class="detail__ergebnis"><small>Ihr Ergebnis</small>{erg}</p></div></div>')
        S.append(("", f'''{leiste("Einsatzgebiete im Detail")}
  <p class="kicker">Einsatzgebiete im Detail</p>
  <h2>Was wir konkret tun.</h2>
  <div class="block">{bloecke}</div>''', True))
    # 8 Wer wir sind
    zusatz = {"tobias": "Mitglied in zwei Aufsichtsräten", "daniel": "Geschäftsführer der empiria GmbH"}
    personen = ""
    for k, p in b.PERSONEN.items():
        personen += (f'<div class="person">{kreis(k)}<div><p class="kicker">Partner · {zusatz[k]}</p><h3>{p["name"]}</h3>'
                     f'<p class="person__rolle">{p["rolle"]}</p><div class="chips">{"".join(f"<span>{x}</span>" for x in p["schwerpunkte"])}</div>'
                     f'<p class="person__werdegang">{p["werdegang"]}</p>'
                     f'<p class="person__kontakt"><span>{p["mail"]}</span><span>{p["tel"]}</span></p></div></div>')
    S.append(("sand", f'''{leiste("Wer wir sind")}
  <p class="kicker">Wer wir sind</p>
  <h2>Unser Team. Unser Netzwerk.</h2>
  <p class="unter">Zwei Partner mit eigener Führungserfahrung in der Versicherungswirtschaft, dazu ein Netzwerk erfahrener Spezialisten. Im Projekt arbeiten wir beide selbst mit.</p>
  <div class="block">{personen}</div>''', True))
    # 9 Das Geschäftsmodell in seiner Gänze
    S.append(("weiss", f'''{leiste("Was uns verbindet")}
  <p class="kicker">Was uns verbindet</p>
  <h2>Das Geschäftsmodell Versicherung. In seiner Gänze.</h2>
  <p class="unter">Wir verstehen, wie die Teile zusammenhängen: wie Strategie in Kennzahlen sichtbar wird, wie Gremien entscheiden und was davon im Vertrieb ankommt.</p>
  <div class="block gaenze">
    <ul class="haken" style="margin-top:0">
      <li>{HAKEN}Wir wissen, wie Erfolg im Unternehmen entsteht.</li>
      <li>{HAKEN}Wir kennen Entscheidungswege und wer eingebunden werden muss.</li>
      <li>{HAKEN}Wir sprechen die Sprache von Vorstand, Aufsichtsrat und Fachbereich.</li>
      <li>{HAKEN}Sechs Felder, ein Geschäftsmodell: Wir bringen sie in Ihrem Projekt zusammen.</li>
    </ul>
    {kreismodell()}
  </div>''', True))
    # 10 Abschluss
    pers = "".join(f'<div>{kreis(k, 96)}<h3>{p["name"]}</h3><p>{p["rolle"]}</p><div class="wege">{p["mail"]}<br>{p["tel"]}</div></div>'
                   for k, p in b.PERSONEN.items())
    S.append(("navy ende", f'''<img class="ende__logo" src="{LOGO_WEISS}" alt="Müller &amp; Ströbel">
  <div class="ende__kern"><p class="kicker">Kontakt</p><h2>{VERSPRECHEN}</h2><p class="unter">{KONTAKT_TEXT}</p></div>
  <div class="ende__personen">{pers}</div>
  <p class="ende__web">www.muellerundstroebel.de</p>
  <div class="impressum">
    <div><b>Impressum</b>empiria GmbH<br>Kapellengasse 6<br>74564 Crailsheim</div>
    <div><b>Register</b>Handelsregister: HRB 750146<br>Registergericht: Amtsgericht Ulm<br>Vertreten durch: Daniel Ströbel</div>
    <div><b>Stand</b>Oktober 2026<br>Müller &amp; Ströbel<br>www.muellerundstroebel.de</div>
  </div>''', False))
    # 11–14 One-Pager
    S.append(("opa", f'''<span class="op-kennung">One-Pager · Variante A</span>{leiste("Für Führungskräfte in der Versicherungsbranche")}
  <h1>Komplexe Situationen strukturieren, entscheiden, umsetzen.</h1>
  <p class="unter">Wir übernehmen Ihr Thema, von der Vorlage für den Aufsichtsrat bis zur Strategie für die Bereiche, und sorgen dafür, dass es vorankommt. Mit wenig Aufwand für Sie.</p>
  <p class="zwischen">Ihre Lage: Die üblichen Wege helfen nur halb</p>{posts(klein=True)}
  <p class="zwischen">So arbeiten wir: Die Zusammenarbeit passt in Ihren Kalender</p>{ablauf()}
  <div class="opa__band dunkel"><p class="kicker">Ihr Ergebnis</p><h2>Sie haben Ihre Themen im Griff.</h2>
    <p class="unter">{VERSPRECHEN}</p><div class="opa__kontakt">{op_person("tobias")}{op_person("daniel")}</div></div>''', False))
    S.append(("opb", f'''<div class="opb__links"><img src="{LOGO_WEISS}" alt="Müller &amp; Ströbel"><span class="op-kennung" style="right:auto;left:24pt">One-Pager · Variante B</span>
    <h1>Komplexe Situationen strukturieren, entscheiden, umsetzen.</h1>
    <p class="unter">Für Führungskräfte in der Versicherungsbranche.</p>
    <p class="opb__versprechen">{VERSPRECHEN}</p>
    <div class="opb__kontakt dunkel">{op_person("tobias")}{op_person("daniel")}</div></div>
  <div class="opb__rechts">
    <div class="opb__abschnitt"><p class="kicker">Ihre Lage</p><h2>„Es ging schon wieder nichts voran.“</h2>
      <ul class="opb__liste" style="margin-top:10pt">{"".join(f"<li><b>{t}</b>{x}</li>" for _, t, x, _, _ in WEGE)}</ul></div>
    <div class="opb__abschnitt"><p class="kicker">So arbeiten wir</p><h2>Die Zusammenarbeit passt in Ihren Kalender.</h2>
      <ul class="opb__liste" style="margin-top:10pt">{"".join(f"<li><b>{t}</b>{x}</li>" for t, x in ABLAUF)}</ul></div>
    <div class="opb__abschnitt"><p class="kicker">Unser Netzwerk</p><p>Ehemalige Vorstände, Aufsichtsräte, IT- und Prozess-Spezialisten, Entwickler, Marketingexperten, Grafiker. Sie behalten einen Ansprechpartner.</p></div>
    <div class="opb__abschnitt"><p class="kicker">Ihr Ergebnis</p><h2>Sie haben Ihre Themen im Griff.</h2>
      <p>Im Gespräch behalten wir das Zielbild im Blick und schaffen Klarheit, wohin es geht. Sie entscheiden und konzentrieren sich auf die richtigen Dinge.</p></div>
  </div>''', False))
    kacheln = [
        ("navy", "Für Führungskräfte in der Versicherungsbranche", "Komplexe Situationen strukturieren, entscheiden, umsetzen.", ""),
        ("sand", "Ihre Lage", "„Es ging schon wieder nichts voran.“", "Die Vorlage für den Aufsichtsrat, die Strategie für die Bereiche: Alles läuft über Ihren Tisch."),
        ("", "Die üblichen Wege", "Team, Externe, Workshops helfen nur halb.", "Das Ergebnis kommt nicht so zurück, wie Sie es brauchen."),
        ("", "So arbeiten wir", "Die Zusammenarbeit passt in Ihren Kalender.", "Kurz abstimmen, oft reicht ein Telefonat. Die Arbeit dazwischen machen wir."),
        ("sand", "Unser Netzwerk", "Die passenden Leute, ein Ansprechpartner.", "Ehemalige Vorstände, Aufsichtsräte, IT-Spezialisten, Entwickler, Grafiker."),
        ("navy", "Ihr Ergebnis", "Sie haben Ihre Themen im Griff.", "Zielbild im Blick, Klarheit, wohin es geht. Sie entscheiden."),
    ]
    k_html = "".join(f'<div class="kachel{" kachel--" + f if f else ""}"><small>{t}</small><b>{x}</b><p>{e}</p></div>' for f, t, x, e in kacheln)
    S.append(("opc", f'''<span class="op-kennung">One-Pager · Variante C</span>{leiste("Was wir tun und wofür wir stehen")}
  <p class="kicker">Auf einen Blick</p>
  <h1>Sie geben uns ein Thema. Wir liefern das Ergebnis.</h1>
  <div class="kacheln">{k_html}</div>
  <div class="opc__kontakt"><p>Das erste Gespräch schafft Klarheit. Kein Pitch, keine Rechnung.</p>{op_person("tobias")}{op_person("daniel")}</div>''', False))
    S.append(("navy opd", f'''<span class="op-kennung">One-Pager · Variante D</span>{leiste("Für Führungskräfte in der Versicherungsbranche", True)}
  <h1>„Es ging schon wieder nichts voran.“</h1>
  <p class="unter">Die Vorlage für den Aufsichtsrat, die Strategie für die Bereiche, das Projekt, das seit Monaten hängt: Genau hier setzen wir an.</p>
  <div class="opd__drei">
    <div><small>01</small><h3>Strukturieren</h3><p>Wir verstehen Ihr Thema und arbeiten den Kern heraus. Sie müssen nichts vorbereiten.</p></div>
    <div><small>02</small><h3>Entscheiden</h3><p>Im kurzen, regelmäßigen Austausch behalten wir das Zielbild im Blick. Sie entscheiden.</p></div>
    <div><small>03</small><h3>Umsetzen</h3><p>Wir arbeiten mit Ihren Leuten, selbst und mit Spezialisten aus unserem Netzwerk.</p></div>
  </div>
  <p class="opd__versprechen">{VERSPRECHEN}</p>
  <div class="opd__kontakt dunkel">{op_person("tobias")}{op_person("daniel")}</div>''', False))
    return S


def html():
    S = seiten()
    n = len(S)
    body = ""
    for i, (klasse, inhalt, mit_fuss) in enumerate(S, 1):
        kl = " ".join(f"seite--{k}" if k in ("navy", "sand", "weiss") else k for k in klasse.split())
        body += f'<section class="seite {kl}">\n  {inhalt}\n  {fuss(i, n) if mit_fuss else ""}\n</section>\n'
    return f'''<!DOCTYPE html>
<html lang="de"><head><meta charset="utf-8"><title>Müller &amp; Ströbel – {DOKUMENT}</title>
<link rel="stylesheet" href="/entwicklung/pdf-bs2/bs2-pdf.css"></head>
<body>
{body}</body></html>
'''


def vorschau(browser):
    """Seite 1 und 2 als PNG für den Download-Kasten (Bildschirmdarstellung der HTML-Quelle)."""
    for nr in (1, 2):
        ziel = WURZEL / "entwicklung" / "downloads" / f"business-story-2-{nr}.png"
        url = f"http://127.0.0.1:{druck.PORT}/entwicklung/pdf-bs2/business-story-2.html#s{nr}"
        hilfe = WURZEL / "entwicklung" / "pdf-bs2" / f"_vorschau{nr}.html"
        hilfe.write_text(f'''<html><body style="margin:0;overflow:hidden"><iframe src="/entwicklung/pdf-bs2/business-story-2.html" style="border:0;width:794px;height:{1123*nr}px;margin-top:-{1123*(nr-1)+0}px" scrolling="no"></iframe>
<style>iframe{{display:block}}</style></body></html>''', encoding="utf-8")
        subprocess.run([browser, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--window-size=794,1123",
                        "--virtual-time-budget=6000", f"--screenshot={ziel}", f"http://127.0.0.1:{druck.PORT}/entwicklung/pdf-bs2/_vorschau{nr}.html"],
                       capture_output=True)
        hilfe.unlink()
        print(f"  Vorschau {ziel.name}")


def main():
    QUELLE.parent.mkdir(parents=True, exist_ok=True)
    ZIEL.parent.mkdir(parents=True, exist_ok=True)
    QUELLE.write_text(html(), encoding="utf-8")
    browser = druck.chrome()
    srv = druck.server_starten()
    time.sleep(.4)
    try:
        befehl = [browser, "--headless", "--disable-gpu", "--no-sandbox", "--no-pdf-header-footer", "--print-to-pdf-no-header",
                  "--virtual-time-budget=10000", f"--print-to-pdf={ZIEL}", f"http://127.0.0.1:{druck.PORT}/entwicklung/pdf-bs2/business-story-2.html"]
        subprocess.run(befehl, capture_output=True, text=True)
        print(f"gebaut: {ZIEL.relative_to(WURZEL)} ({ZIEL.stat().st_size // 1024} KB)")
        vorschau(browser)
    finally:
        srv.shutdown()


if __name__ == "__main__":
    main()
