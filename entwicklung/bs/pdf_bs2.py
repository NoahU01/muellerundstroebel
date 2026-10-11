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
  </div>''', "haupt"))
    # 2 Ihre Lage
    S.append(("sand", f'''{leiste("Ihre Lage")}
  <p class="kicker">Ihre Lage</p>
  <h2>„Es ging schon wieder nichts voran.“</h2>
  <p class="unter">Die Vorlage für den Aufsichtsrat, die Strategie für die Bereiche, das Projekt, das seit Monaten hängt: Alles läuft über Ihren Tisch. Und die üblichen Wege helfen nur halb.</p>
  <div class="block">{posts()}</div>
  <div class="kern"><p class="kicker">Was Sie brauchen</p><p>Jemanden, der Ihr Thema versteht, es strukturiert, die Bearbeitung übernimmt und das Ergebnis liefert. Mit wenig Aufwand für Sie.</p></div>''', "haupt"))
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
    <p>Sie behalten einen Ansprechpartner. Die Koordination liegt bei uns.</p><ul>{netz}</ul></div>''', "haupt"))
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
  </div>''', "haupt"))
    # 5 Einsatzgebiete – Überblick
    weiss_ico = {k: b.icon(k).replace('stroke="currentColor"', 'stroke="#ffffff"') for k, _, _ in b.THEMEN}
    gebiete = "".join(f'<div class="gebiet"><span class="gebiet__ico">{weiss_ico[k]}</span>'
                      f'<span class="gebiet__nr">0{i}</span><h3>{n}</h3><p>{w}</p></div>' for i, (k, n, w) in enumerate(b.THEMEN, 1))
    S.append(("", f'''{leiste("Einsatzgebiete")}
  <p class="kicker">Einsatzgebiete</p>
  <h2>Hier setzen wir an.</h2>
  <p class="unter">Sechs Felder, in denen Führungskräfte uns typischerweise dazuholen. Auf den folgenden Seiten: was wir jeweils konkret tun und was Sie davon haben.</p>
  <div class="block gebiete">{gebiete}</div>''', "haupt"))
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
  <div class="block">{bloecke}</div>''', "haupt"))
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
  <div class="block">{personen}</div>''', "haupt"))
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
  </div>''', "haupt"))
    # 10 Abschluss – drei ruhige Varianten (gleiche Seitenzahl 10, Auswahl durch Daniel)
    impressum = '''<div><b>Impressum</b>empiria GmbH<br>Kapellengasse 6<br>74564 Crailsheim</div>
    <div><b>Register</b>Handelsregister: HRB 750146<br>Registergericht: Amtsgericht Ulm<br>Vertreten durch: Daniel Ströbel</div>
    <div><b>Stand</b>Oktober 2026<br>www.muellerundstroebel.de</div>'''
    kontakt_zeilen = "".join(f'<div class="ab-person">{kreis(k, 58)}<div><b>{p["name"]}</b><span>{p["rolle"]}</span>'
                             f'<span>{p["mail"]}</span><span>{p["tel"]}</span></div></div>' for k, p in b.PERSONEN.items())
    S.append(("ab ab2n", f'''{leiste("Kontakt")}
  <img class="ab2n__amp" src="/entwicklung/pdf-bs2/ampersand-blau.svg" alt="">
  <div class="ab2n__unten dunkel">
    <div class="ab2n__text">
      <p class="kicker">Kontakt</p>
      <h2>Sie geben uns die Verantwortung für ein Thema. Wir liefern das Ergebnis.</h2>
      <p class="unter">{KONTAKT_TEXT}</p>
    </div>
    <div class="ab-personen ab-personen--ohne ab-personen--hell">{kontakt_zeilen}</div>
    <div class="ab4__impressum">
      <p><b>Müller &amp; Ströbel</b> · empiria GmbH · Kapellengasse 6 · 74564 Crailsheim · www.muellerundstroebel.de</p>
      <p>Vertreten durch Daniel Ströbel · Amtsgericht Ulm HRB 750146 · USt-IdNr. DE 281217286 · Stand Oktober 2026</p>
    </div>
  </div>''', "ende"))
    # ===================== One-Pager „Der Pitch als Text“: fortlaufend erzählt, nur der Kernsatz hervorgehoben =====================
    kontakt_brief = "".join(f'<div class="o4-person">{kreis(k, 52)}<div><b>{p["name"]}</b><span>{p["rolle"]}</span><span>{p["tel"]}</span><span>{p["mail"]}</span></div></div>'
                            for k, p in b.PERSONEN.items())
    fuss_pers = "".join(f'<div class="o4-p">{kreis(k, 42)}<div><b>{p["name"]}</b><span>{p["tel"]}</span><span>{p["mail"]}</span></div></div>'
                        for k, p in b.PERSONEN.items())
    S.append(("o4", f'''<span class="op-kennung op-kennung--hell">One-Pager · Der Pitch als Text</span>
  <header class="o4-kopf dunkel">
    <img class="o4-kopf__amp" src="/pdf/bausteine/ampersand-konstruktion.svg" alt="">
    <img class="o4-kopf__logo" src="{LOGO_WEISS}" alt="Müller &amp; Ströbel">
    <div class="o4-kopf__text"><p class="kicker">Für Führungskräfte in der Versicherungsbranche</p>
      <h1>Komplexe Situationen strukturieren, entscheiden, umsetzen.</h1></div>
  </header>
  <main class="o4-story">
    <div class="o4-schritt"><p class="o4-gross">Sie müssen alles im Blick haben. Und am Ende zählt nur das Ergebnis.</p></div>
    <div class="o4-schritt"><p>Ob Sie ein Thema Ihrem Team geben oder Externe holen: Es kommt selten so zurück, wie Sie es brauchen. Am Ende greifen Sie doch wieder selbst ein.</p></div>
    <div class="o4-schritt o4-schritt--kern"><p class="o4-kernsatz"><span>Da setzen wir an.</span> Sie geben uns die Verantwortung für ein Thema. Wir liefern das Ergebnis.</p></div>
    <div class="o4-schritt"><p>Etwa die Vorlage für den Aufsichtsrat oder die Strategie für die Bereiche. Wir strukturieren Ihr Thema, arbeiten es mit Ihren Leuten aus und holen Spezialisten dazu, wo es sie braucht.</p></div>
    <div class="o4-schritt o4-schritt--ende"><p>Von Ihnen brauchen wir dafür meist nur ein kurzes Telefonat zwischendurch. <b>So haben Sie Ihre Themen im Griff.</b></p></div>
  </main>
  <footer class="o4-fuss dunkel">
    <p class="o4-fuss__satz">Liegt gerade so ein Thema auf Ihrem Tisch? Lassen Sie uns kurz sprechen.</p>
    <div class="o4-fuss__pers">{fuss_pers}</div>
  </footer>''', "op"))

    # ===================== One-Pager mit Visualisierung: gleicher Kopf und Fuß, Mitte erzählt den Pitch mit Bild =====================
    def o5_rahmen(label, klasse, mitte):
        return (klasse, f'''<span class="op-kennung op-kennung--hell">One-Pager · {label}</span>
  <header class="o4-kopf dunkel">
    <img class="o4-kopf__amp" src="/pdf/bausteine/ampersand-konstruktion.svg" alt="">
    <img class="o4-kopf__logo" src="{LOGO_WEISS}" alt="Müller &amp; Ströbel">
    <div class="o4-kopf__text"><p class="kicker">Für Führungskräfte in der Versicherungsbranche</p>
      <h1>Komplexe Situationen strukturieren, entscheiden, umsetzen.</h1></div>
  </header>
  <main class="o5-mitte">{mitte}</main>
  <footer class="o4-fuss dunkel">
    <p class="o4-fuss__satz">Liegt gerade so ein Thema auf Ihrem Tisch? Lassen Sie uns kurz sprechen.</p>
    <div class="o4-fuss__pers">{fuss_pers}</div>
  </footer>''', "op")

    N, T, TH, SA = "#082638", "#998675", "#cbbcae", "#ebe4dc"
    def svg(inhalt, w=150, h=70):
        return f'<svg viewBox="0 0 {w} {h}" class="o5-svg" font-family="Poppins, sans-serif">{inhalt}</svg>'
    def pill(x, y, w, h, text, fill=N, farbe="#fff", rand=None):
        r = f' stroke="{rand}" stroke-width="1.2"' if rand else ""
        return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="{fill}"{r}/>'
                f'<text x="{x+w/2}" y="{y+h/2+3}" font-size="8" font-weight="600" fill="{farbe}" text-anchor="middle">{text}</text>')
    pfeil_def = f'<defs><marker id="pf" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0l8 4-8 4z" fill="{T}"/></marker></defs>'

    # --- Variante 1: Text mit Bild am Rand
    bilder = [
        svg("".join(f'<rect x="{x}" y="{y}" width="40" height="15" rx="4" fill="{f}" stroke="{TH}" stroke-width=".8"/>' for x, y, f in
                    [(8, 8, "#fff"), (56, 4, SA), (104, 10, "#fff"), (20, 30, SA), (68, 26, "#fff"), (96, 46, SA), (40, 50, "#fff")])),
        svg(pfeil_def + pill(4, 26, 34, 18, "Sie") + f'<path d="M40 35 H70" stroke="{T}" stroke-width="1.2" marker-end="url(#pf)"/>'
            + pill(72, 26, 72, 18, "Team · Externe", "#fff", N, TH)
            + f'<path d="M108 46 C108 66 22 66 22 47" fill="none" stroke="{T}" stroke-width="1.2" stroke-dasharray="3 3" marker-end="url(#pf)"/>'),
        svg(pfeil_def + pill(4, 26, 34, 18, "Sie", "#fff", N, TH) + f'<path d="M40 35 H74" stroke="{N}" stroke-width="1.6" marker-end="url(#pf)"/>'
            + pill(76, 24, 70, 22, "Müller &amp; Ströbel")),
        svg(pill(56, 4, 58, 18, "Ihr Thema") + f'<path d="M85 22 L31 46 M85 22 L85 46 M85 22 L139 46" stroke="{TH}" stroke-width="1"/>'
            + pill(1, 46, 60, 18, "Strukturieren", "#fff", N, TH) + pill(63, 46, 44, 18, "Ihre Leute", "#fff", N, TH) + pill(109, 46, 60, 18, "Spezialisten", "#fff", N, TH), 170, 70),
        svg(f'<circle cx="28" cy="35" r="20" fill="none" stroke="{N}" stroke-width="1.4"/><path d="M28 23v12l8 5" fill="none" stroke="{N}" stroke-width="1.4" stroke-linecap="round"/>'
            f'<path d="M58 35 H86" stroke="{TH}" stroke-width="1.2"/><circle cx="112" cy="35" r="20" fill="{N}"/>'
            f'<path d="M103 35l6 6 12-13" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'),
    ]
    zeilen1 = [
        ("Sie müssen alles im Blick haben. Und am Ende zählt nur das Ergebnis.", "gross"),
        ("Ob Sie ein Thema Ihrem Team geben oder Externe holen: Es kommt selten so zurück, wie Sie es brauchen. Am Ende greifen Sie doch wieder selbst ein.", ""),
        ("Sie geben uns die Verantwortung für ein Thema. Wir liefern das Ergebnis.", "kern"),
        ("Etwa die Vorlage für den Aufsichtsrat. Wir strukturieren es, arbeiten es mit Ihren Leuten aus und holen Spezialisten dazu.", ""),
        ("Von Ihnen brauchen wir meist nur ein kurzes Telefonat zwischendurch. So haben Sie Ihre Themen im Griff.", ""),
    ]
    m1 = "".join(f'<div class="o5a-zeile o5a-zeile--{art}"><p>{t}</p>{bild}</div>' for (t, art), bild in zip(zeilen1, bilder))
    S.append(o5_rahmen("Variante 1 · Text mit Bild", "o5 o5a", m1))

    # --- Variante 2: Bisher und mit uns
    bisher = svg(pfeil_def + pill(55, 4, 70, 20, "Ihr Thema", "#fff", N, TH)
                 + f'<path d="M90 24 L52 52 M90 24 L128 52" stroke="{T}" stroke-width="1.2" marker-end="url(#pf)"/>'
                 + pill(14, 54, 72, 20, "Ihr Team", "#fff", N, TH) + pill(94, 54, 72, 20, "Externe", "#fff", N, TH)
                 + f'<path d="M50 74 L84 104 M130 74 L96 104" stroke="{T}" stroke-width="1.2" marker-end="url(#pf)"/>'
                 + pill(50, 106, 80, 22, "Sie greifen ein")
                 + f'<path d="M132 117 C172 117 172 14 128 14" fill="none" stroke="{T}" stroke-width="1.2" stroke-dasharray="3 3" marker-end="url(#pf)"/>', 180, 134)
    mit = svg(pfeil_def + pill(55, 4, 70, 20, "Ihr Thema", "#fff", N)
              + f'<path d="M90 24 V48" stroke="{TH}" stroke-width="1.4" marker-end="url(#pf)"/>'
              + pill(40, 50, 100, 24, "Müller &amp; Ströbel", TH, N)
              + f'<path d="M90 74 V100" stroke="{TH}" stroke-width="1.4" marker-end="url(#pf)"/>'
              + pill(50, 104, 80, 24, "Ihr Ergebnis", "#fff", N), 180, 134)
    m2 = f'''<p class="o5-einstieg">Sie müssen alles im Blick haben. Und am Ende zählt nur das Ergebnis.</p>
    <div class="o5b-zwei">
      <div class="o5b-feld"><p class="kicker">Bisher</p>{bisher}<p>Ob Sie ein Thema Ihrem Team geben oder Externe holen: Es kommt selten so zurück, wie Sie es brauchen.</p></div>
      <div class="o5b-feld o5b-feld--dunkel dunkel"><p class="kicker">Mit uns</p>{mit}<p>Sie geben uns die Verantwortung für ein Thema. Wir liefern das Ergebnis, etwa die Vorlage für den Aufsichtsrat.</p></div>
    </div>
    <p class="o5-schluss">Von Ihnen brauchen wir meist nur ein kurzes Telefonat zwischendurch. <b>So haben Sie Ihre Themen im Griff.</b></p>'''
    S.append(o5_rahmen("Variante 2 · Bisher und mit uns", "o5 o5b", m2))

    # --- Variante 3: Die Übergabe
    m3 = f'''<p class="o5-einstieg">Sie müssen alles im Blick haben. Und am Ende zählt nur das Ergebnis. Ob Team oder Externe: Es kommt selten so zurück, wie Sie es brauchen.</p>
    <div class="o5c-tausch">
      <div class="o5c-seite"><p class="kicker">Bei Ihnen bleibt</p><ul><li>Die Richtung vorgeben</li><li>Entscheiden</li><li>Ein kurzes Telefonat zwischendurch</li></ul></div>
      <div class="o5c-mitte">
        <div class="o5c-pfeil"><span>Verantwortung für ein Thema</span><svg viewBox="0 0 100 12"><path d="M2 6H96M90 1l6 5-6 5" fill="none" stroke="{N}" stroke-width="1.6"/></svg></div>
        <div class="o5c-pfeil o5c-pfeil--zurueck"><svg viewBox="0 0 100 12"><path d="M98 6H4M10 1L4 6l6 5" fill="none" stroke="{T}" stroke-width="1.6"/></svg><span>Das Ergebnis</span></div>
      </div>
      <div class="o5c-seite o5c-seite--wir dunkel"><p class="kicker">Bei uns liegt</p><ul><li>Das Thema strukturieren</li><li>Mit Ihren Leuten ausarbeiten</li><li>Spezialisten dazuholen</li><li>Das Ergebnis liefern, etwa die Vorlage für den Aufsichtsrat</li></ul></div>
    </div>
    <p class="o5-schluss"><b>So haben Sie Ihre Themen im Griff.</b></p>'''
    S.append(o5_rahmen("Variante 3 · Die Übergabe", "o5 o5c", m3))
    return S


def html():
    S = seiten()
    gesamt = sum(1 for _, _, art in S if art == "haupt") + 1   # + Abschlussseite
    body, nr = "", 0
    for klasse, inhalt, art in S:
        if art == "haupt":
            nr += 1
        kl = " ".join(f"seite--{k}" if k in ("navy", "sand", "weiss") else k for k in klasse.split())
        f = fuss(nr, gesamt) if (art == "haupt" and nr > 1) else ""
        body += f'<section class="seite {kl}">\n  {inhalt}\n  {f}\n</section>\n'
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
