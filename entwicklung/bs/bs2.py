#!/usr/bin/env python3
"""Business Story 2.0 (nur Branch daniel – entwicklung/ geht nie auf main).

Baut entwicklung/business-story-2.html (Startseite) und entwicklung/business-story-2-ueber-uns.html.
Gestaltung: entwicklung/business-story-2.css. Inhalte, die es schon gibt, kommen aus den Live-Seiten:
Einsatzgebiete (Icons + Details) aus index.html, Werdegang und Stationen aus ueber-uns.html.
Das Entwicklungsmenü wird aus index.html übernommen.

    python3 entwicklung/bs/bs2.py
"""
import re
from pathlib import Path

WURZEL = Path(__file__).resolve().parents[2]
ZIEL = WURZEL / "entwicklung"
INDEX = (WURZEL / "index.html").read_text(encoding="utf-8")
UEBER = (WURZEL / "ueber-uns.html").read_text(encoding="utf-8")
DEV = re.search(r"<!-- ENTWICKLUNG:START.*?<!-- ENTWICKLUNG:END -->", INDEX, re.S).group(0)
VERSION = 34

MAIL_BEIDE = "mailto:daniel@muellerundstroebel.de,tobias@muellerundstroebel.de?subject=Thema%20besprechen"
PERSONEN = {
    "tobias": dict(name="Tobias Müller", rolle="Governance, Gremien &amp; Risiko", kurz="Partner · Mitglied in zwei Aufsichtsräten",
                   tel="+49 176 2152 9798", tel_roh="+4917621529798", mail="tobias@muellerundstroebel.de",
                   linkedin="https://www.linkedin.com/in/tobias-m%C3%BCller-b5606b24/",
                   schwerpunkte=["Governance &amp; Gremienlogik", "Aufsichtsrats- &amp; Vorstandssicht", "Risiko &amp; Rechnungslegung"],
                   werdegang="Tobias Müller kommt aus der Rückversicherung: Nach Stationen bei SCOR und als Underwriter bei Hannover Re führte er über zwölf Jahre die Müller Unternehmensberatung für Versicherer und Rückversicherer. Heute ist er Mitglied der Aufsichtsräte von Gartenbau-Versicherung und Grundeigentümer-Versicherung."),
    "daniel": dict(name="Daniel Ströbel", rolle="Strategie, Führung &amp; Vertrieb", kurz="Partner · Geschäftsführer der empiria GmbH",
                   tel="+49 176 3134 7217", tel_roh="+4917631347217", mail="daniel@muellerundstroebel.de",
                   linkedin="https://www.linkedin.com/in/daniel-stroebel/",
                   schwerpunkte=["Strategie &amp; Geschäftsmodell", "Struktur &amp; Führung", "Vertrieb &amp; Stakeholderfokus"],
                   werdegang="Daniel Ströbel verantwortete bei der SV SparkassenVersicherung Konzernstrategie und Risikomanagement, baute das Inhouse-Consulting Leben auf und leitete eine Abteilung mit rund 40 Mitarbeitenden. Seit 2012 führt er die empiria GmbH – mit über 300 Projekten für die Versicherungsbranche."),
}
THEMEN = [  # Schlüssel der Live-Einsatzgebiete, Titel, „Wenn …“-Satz
    ("strategie", "Strategie &amp; Geschäftsmodell", "Wenn die Richtung klar sein muss und im Alltag ankommen soll."),
    ("kennzahlen", "Kennzahlen &amp; Steuerung", "Wenn Zahlen da sind, aber nicht steuern."),
    ("gremien", "Entscheidungen &amp; Gremien", "Wenn Themen seit Monaten „in Bearbeitung“ sind."),
    ("vertrieb", "Vertrieb &amp; Wachstum", "Wenn Potenziale im Markt liegen bleiben."),
    ("ki", "KI-Transformation", "Wenn KI das Geschäftsmodell verändern soll, nicht nur Prozesse."),
    ("resilienz", "Resilienz", "Wenn Unsicherheit zur dauerhaften Managementaufgabe wird."),
]
NETZWERK = ["Ehemalige Vorstände", "Aufsichtsräte", "IT-Spezialisten", "Prozess-Spezialisten", "Entwickler", "Marketingexperten", "Grafiker"]

ICONS = """<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="i-weiter" viewBox="0 0 16 16"><path d="M3 8h10M9 4l4 4-4 4"/></symbol>
  <symbol id="i-extern" viewBox="0 0 16 16"><path d="M6 3.5H3.5v9h9V10M9 3h4v4M13 3 7.5 8.5"/></symbol>
  <symbol id="i-uhr" viewBox="0 0 24 24"><circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/></symbol>
  <symbol id="i-haken" viewBox="0 0 20 20"><path d="M4.5 10.5l3.5 3.5 7.5-8"/></symbol>
  <symbol id="i-minus" viewBox="0 0 20 20"><path d="M5 10h10"/></symbol>
  <symbol id="i-zu" viewBox="0 0 24 24"><path d="M6 6l12 12M18 6 6 18"/></symbol>
</svg>"""


def icon(key):
    return re.search(rf'data-modal="{key}".*?<span class="v-ico">(<svg.*?</svg>)', INDEX, re.S).group(1)


def thema_detail(key):
    """Inhalt der Live-Einsatzgebiet-Vorlage (Was wir konkret tun, Ihr Ergebnis) ohne Kicker."""
    t = re.search(rf'<template id="m-{key}">(.*?)</template>', INDEX, re.S).group(1)
    return re.sub(r'<p class="v-kicker">.*?</p>', "", t, 1)


def stationen(key):
    return re.search(rf'<template id="m-cv-{key}">.*?(<ol class="v-cv">.*?</ol>)</template>', UEBER, re.S).group(1)


def kopfzeile(aktiv):
    start = "/entwicklung/business-story-2.html"
    links = [(f"{start}#lage", "Ihre Lage"), (f"{start}#arbeitsweise", "So arbeiten wir"),
             ("/entwicklung/business-story-2-ueber-uns.html", "Über uns")]
    akt = ' aria-current="page"'
    nav = "".join(f'<a class="nav__anker" href="{h}"{akt if n == aktiv else ""}>{n}</a>' for h, n in links)
    seiten = "".join(f'<a href="{h}">{n}</a>' for h, n in links) + '<a href="/entwicklung/business-story-2.html#kontakt">Thema besprechen</a>'
    dev = DEV.replace('<p class="dev-dd-note">', f'<div class="menu-seiten">{seiten}</div><p class="dev-dd-note">', 1)
    return f'''<header class="kopf"><div class="wrap">
  <a class="marke" href="{start}" aria-label="Müller &amp; Ströbel – Startseite"><img src="/assets/logo.svg" alt="Müller &amp; Ströbel"></a>
  <nav class="nav" aria-label="Hauptmenü">{nav}
{dev}
    <a class="knopf" href="#kontakt">Thema besprechen</a>
  </nav>
</div></header>'''


def kontakt(titel, text):
    personen = "".join(f'''<article class="person"><div class="kreis"><img src="/assets/{k}-portrait.webp" alt="{p['name']}"></div><div>
      <h3>{p['name']}</h3><p class="person__kurz">{p['kurz']}</p>
      <div class="wege">
        <a href="tel:{p['tel_roh']}">{p['tel']}</a>
        <a href="mailto:{p['mail']}">{p['mail']}</a>
        <a href="{p['linkedin']}" target="_blank" rel="noopener">LinkedIn</a>
      </div></div></article>''' for k, p in PERSONEN.items())
    return f'''<section class="sek sek--sand kontakt" id="kontakt"><div class="wrap">
  <h2>{titel}</h2>
  <p class="lead">{text}</p>
  <div class="personen">{personen}</div>
  <div class="knoepfe"><a class="knopf" href="{MAIL_BEIDE}">Thema per E-Mail schicken <svg class="ico" aria-hidden="true"><use href="#i-weiter"/></svg></a></div>
</div></section>'''


def seite(titel, beschreibung, variante, aktiv, main, skript=""):
    return f'''<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titel}</title>
<meta name="description" content="{beschreibung}">
<meta name="robots" content="noindex, nofollow">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/entwicklung/business-story-2.css?v={VERSION}">
</head>
<body data-variante="{variante}">
{ICONS}
{kopfzeile(aktiv)}
<main>
{main}
</main>
<footer class="fuss"><div class="wrap">
  <img src="/pdf/bausteine/logo-weiss.svg" alt="Müller &amp; Ströbel">
  <nav><a href="/entwicklung/business-story-2-ueber-uns.html">Über uns</a><a href="/impressum.html">Impressum</a><a href="/datenschutz.html">Datenschutz</a></nav>
</div></footer>
{skript}
<script>/* Menü schließt nach Klick auf einen Eintrag (Tablet/Handy) */
document.querySelectorAll('#dev-dd .dev-dd-panel a').forEach(function (a) {{ a.addEventListener('click', function () {{ var d = document.getElementById('dev-dd'); d.classList.remove('is-open'); d.querySelector('.dev-dd-toggle').setAttribute('aria-expanded', 'false'); }}); }});
</script>
</body>
</html>
'''


# ------------------------------------------------------------------ Startseite
def platz(punkt, titel, hinweis, status="offen", klein=False):
    """Sichtbar markierter Platzhalter für einen noch offenen Punkt aus dem Storyboard."""
    return (f'<div class="platz platz--{status}{" platz--klein" if klein else ""}"><span class="platz__tag">{punkt} · {STATUS[status]}</span>'
            f'<b>{titel}</b><p>{hinweis}</p></div>')


# Lucide Icons (https://lucide.dev, ISC-Lizenz) – Icon-Szene „Trio“ nach dem System der empiria-Kopfbilder:
# eine Familie, gleiche Strichstärke, nur Linien, genau ein Icon in Akzentfarbe.
LUCIDE = {'compass': '<circle cx="12" cy="12" r="10" /> <path d="m16.24 7.76-1.804 5.411a2 2 0 0 1-1.265 1.265L7.76 16.24l1.804-5.411a2 2 0 0 1 1.265-1.265z" />', 'circle-check': '<circle cx="12" cy="12" r="10" /> <path d="m16 9-5.5 5.5L8 12" />', 'target': '<circle cx="12" cy="12" r="10" /> <circle cx="12" cy="12" r="6" /> <circle cx="12" cy="12" r="2" />'}


def trio_szene(kern, akzent, neben, farbe="#ffffff", akzentfarbe="#cbbcae", strich=5.2):
    def icon(n, x, y, g, f):
        return (f'<g transform="translate({x} {y}) scale({g/24:.4f})" fill="none" stroke="{f}" stroke-width="{strich*24/g:.3f}" '
                f'stroke-linecap="round" stroke-linejoin="round">{LUCIDE[n]}</g>')
    return ('<svg class="szene" viewBox="0 0 440 400" role="img" aria-label="Zielbild, Entscheidung, Fokus">'
            + icon(kern, 40, 104, 196, farbe) + icon(akzent, 316, 104, 84, akzentfarbe) + icon(neben, 316, 216, 84, farbe) + '</svg>')


def startseite():
    """Startseite nach Storyboard: Kopf C · Ihre Lage C · So arbeiten wir Vis. 2 · 4.1 Ergebnis C · 4.2 Kontakt C."""
    duo = "".join(f'<figure><div class="kreis"><img src="/assets/{k}-portrait.webp" alt="{p["name"]}"></div><figcaption><b>{p["name"]}</b>{p["kurz"]}</figcaption></figure>'
                  for k, p in PERSONEN.items())
    wege = [("weiss", "Ihr Team", "Liefert, aber nicht so, wie Sie es brauchen.", "team",
             "<h3>Ihr Team</h3><p>Ihr Team liefert, aber nicht so, wie Sie es brauchen. Sie greifen wieder selbst ein.</p>"
             "<h4>Typisch bei</h4><ul><li>der Vorlage für den Aufsichtsrat</li><li>der Analyse, die eine Entscheidung tragen soll</li><li>dem Konzept, das in den Bereichen umgesetzt werden muss</li></ul>"),
            ("navy", "Externe", "Empfehlungen ja. Umsetzen bleibt bei Ihnen.", "extern",
             "<h3>Externe</h3><p>Strategieberater, Projektmanager, Spezialisten: jeweils einzeln beauftragt. Die Verbindung, die Koordination und die Verantwortung für das Ergebnis bleiben bei Ihnen.</p>"),
            ("weiss", "Nur Workshops", "Zwei Tage im Kalender. Dann wochenlang Stillstand.", "workshop",
             "<h3>Nur Workshops</h3><p>Große Themen werden zur Hürde: erst ein Termin für den großen Workshop, danach tut sich wenig, bis wieder Zeit im Kalender ist.</p>")]
    ico = {
        "team": '<svg class="ico" viewBox="0 0 24 24"><circle cx="9" cy="8" r="3.2"/><path d="M3.5 19.5c.6-3.3 2.7-5 5.5-5s4.9 1.7 5.5 5"/><circle cx="17" cy="9" r="2.5"/><path d="M16 14.6c2.4.1 4 1.6 4.5 4.4"/></svg>',
        "extern": '<svg class="ico" viewBox="0 0 24 24"><rect x="3" y="7.5" width="18" height="12.5" rx="2"/><path d="M8.5 7.5V5.8A1.8 1.8 0 0 1 10.3 4h3.4a1.8 1.8 0 0 1 1.8 1.8v1.7M3 12.5h18"/></svg>',
        "workshop": '<svg class="ico" viewBox="0 0 24 24"><rect x="3.5" y="5" width="17" height="15.5" rx="2"/><path d="M3.5 9.5h17M8 3v4M16 3v4M7.5 13.5h3M13.5 13.5h3M7.5 17h3"/></svg>',
    }
    lang = {"team": "Liefert, aber nicht so, wie Sie es brauchen. Sie greifen wieder selbst ein.",
            "extern": "Liefern Empfehlungen. Umsetzen und koordinieren bleibt bei Ihnen.",
            "workshop": "Zwei Tage im Kalender. Danach tut sich wochenlang nichts."}
    # Variante 2: Aufbau wie die Social-Media-Kästen: weißer Rahmen, farbiges Quadrat mit Aussage und Icon, Text darunter
    farben = {"team": "sand", "extern": "navy", "workshop": "hell"}
    ergaenzung = {"team": "Typisch bei der Vorlage für den Aufsichtsrat oder dem Konzept für die Bereiche. Am Ende greifen Sie wieder selbst ein.",
                  "extern": "Strategieberater, Projektmanager, Spezialisten: Die Koordination und die Verantwortung für das Ergebnis bleiben bei Ihnen.",
                  "workshop": "Große Themen werden zur Hürde. Es geht erst weiter, wenn wieder Zeit im Kalender ist."}
    karten2 = "".join(f'<article class="pk"><div class="pk__bild pk__bild--{farben[k]}"><small>{t}</small><b>{x}</b>{ico[k]}</div>'
                      f'<div class="pk__text"><p>{ergaenzung[k]}</p><button class="pk__mehr" type="button" data-thema="{k}">Mehr</button></div></article>'
                      for f, t, x, k, _ in wege)
    karten = f'<div class="pks">{karten2}</div>'
    vorlagen = "".join(f'<template id="t-{k}">{d}</template>' for _, _, _, k, d in wege)
    schritte = "".join(f'<li class="lp-schritt"><span class="lp-schritt__ico">{ic}</span><h3>{t}</h3><p>{x}</p></li>' for ic, t, x in [
        (ICO_GESPRAECH, "Kurzer Austausch", "Telefonat, Videokonferenz, Workshop, wenn er sinnvoll ist. Oft reicht ein kurzer Austausch."),
        (ICO_ARBEIT, "Wir arbeiten", "Mit Ihren Leuten, selbst und mit Spezialisten aus unserem Netzwerk."),
        (ICO_KREIS, "Nächster Austausch", "Wir kommen mit einem klaren Bild zurück und setzen eine Stufe höher an.")])
    netz_ico = [
        ("Ehemalige Vorstände", '<path d="M3 9.5 12 4l9 5.5"/><path d="M5 10v8M9.5 10v8M14.5 10v8M19 10v8"/><path d="M3 20.5h18"/>'),
        ("Aufsichtsräte", '<circle cx="12" cy="6.5" r="2.3"/><circle cx="5.5" cy="11" r="2"/><circle cx="18.5" cy="11" r="2"/><path d="M3 20h18M6 20v-3.5h12V20"/>'),
        ("IT- und Prozess-Spezialisten", '<rect x="3" y="4.5" width="18" height="12" rx="1.5"/><path d="M9 20h6M12 16.5V20M7.5 10.5h3l1.5-2 1.5 4 1.5-2h1.5"/>'),
        ("Entwickler", '<path d="M8.5 7.5 4 12l4.5 4.5M15.5 7.5 20 12l-4.5 4.5M13.5 5l-3 14"/>'),
        ("Marketingexperten", '<path d="M4 10v4h3l6 4V6L7 10H4Z"/><path d="M16.5 9a4 4 0 0 1 0 6M19 6.5a7.5 7.5 0 0 1 0 11"/>'),
        ("Grafiker", '<path d="M4 20l1.2-4.2L15.5 5.5a2 2 0 0 1 2.8 0l.2.2a2 2 0 0 1 0 2.8L8.2 18.8 4 20Z"/><path d="M13.5 7.5l3 3"/>'),
    ]
    netz = "".join(f'<li><svg class="ico" viewBox="0 0 24 24" aria-hidden="true">{p}</svg>{n}</li>' for n, p in netz_ico)
    kontakte = "".join(f'''<article class="kp"><div class="kreis"><img src="/assets/{k}-portrait.webp" alt="{p['name']}"></div>
      <h3>{p['name']}</h3><p class="kp__themen">{p['rolle']}</p>
      <p class="kp__wege"><a href="mailto:{p['mail']}">{p['mail']}</a><a href="tel:{p['tel_roh']}">{p['tel']}</a><a class="kp__li" href="{p['linkedin']}" target="_blank" rel="noopener">LinkedIn-Profil <svg viewBox="0 0 16 16" aria-hidden="true"><path d="M6 3.5H3.5v9h9V10M9 3h4v4M13 3 7.5 8.5"/></svg></a></p>
    </article>''' for k, p in PERSONEN.items())
    main = f"""

<!-- 1 Kopf -->
<section class="held lp-held"><div class="wrap held__raster">
  <div>
    <p class="kicker">Für Führungskräfte in der Versicherungsbranche</p>
    <div class="wahl" data-gruppe="kopf"><span>Überschrift</span><button type="button" aria-pressed="true">1</button><button type="button" aria-pressed="false">2</button></div>
    <h1 data-gruppe="kopf" data-variante="1">Komplexe Situationen <span class="wort" aria-hidden="true"><span class="ist">strukturieren.</span><span>entscheiden.</span><span>umsetzen.</span></span><span class="nur-lesen">strukturieren, entscheiden, umsetzen.</span></h1>
    <div data-gruppe="kopf" data-variante="2" hidden><p class="lp-vorzeile">Komplexe Situationen</p><h1>Strukturieren. Entscheiden. Umsetzen.</h1></div>
    <p class="lead">Die Vorlage für den Aufsichtsrat, die Strategie für die Bereiche, die Kennzahlen, die steuern sollen: Wir übernehmen Ihr Thema und sorgen dafür, dass es vorankommt. Mit wenig Aufwand für Sie.</p>
    <div class="knoepfe"><a class="knopf" href="#kontakt">Gespräch vereinbaren <svg class="ico" aria-hidden="true"><use href="#i-weiter"/></svg></a><a class="knopf knopf--rand" href="#lage">Ihre Lage</a></div>
  </div>
  <div class="duo duo--gleich">{duo}</div>
</div></section>

<!-- 2 Ihre Lage -->
<section class="sek sek--sand" id="lage"><div class="wrap">
  <div class="kopfteil">
    <p class="kicker">Ihre Lage</p>
    <h2 class="h2">„Es ging schon wieder nichts voran.“</h2>
    <p class="lead">Die Vorlage für den Aufsichtsrat, die Strategie für die Bereiche, das Projekt, das seit Monaten hängt: Alles läuft über Ihren Tisch. Und die üblichen Wege helfen nur halb.</p>
  </div>
  {karten}
</div></section>

<!-- 3 So arbeiten wir -->
<section class="sek" id="arbeitsweise"><div class="wrap">
  <p class="kicker">So arbeiten wir</p>
  <div class="wahl" data-gruppe="arbeit"><span>Darstellung</span><button type="button" aria-pressed="true">1</button><button type="button" aria-pressed="false">2</button><button type="button" aria-pressed="false">3</button></div>
  <div class="lp-arbeit">
    <div>
      <h2 class="h2">Die Zusammenarbeit passt in Ihren Kalender.</h2>
      <div class="lp-arbeit__text" data-gruppe="arbeit-text" data-variante="lang">
        <p>Wir bleiben im regelmäßigen, kurzen Austausch. Meist reicht ein Telefonat zwischen zwei Terminen oder auf der Fahrt. Wenn es ein Thema braucht, nehmen wir uns eine längere Videokonferenz, und wenn es sinnvoll ist, einen Workshop.</p>
        <p>Dazwischen arbeiten wir: Wir sprechen mit Ihren Leuten, erarbeiten selbst und holen Spezialisten dazu, wo es sie braucht. Beim nächsten Austausch steigen wir eine Stufe höher ein.</p>
        <p><b>So bleibt Ihr Thema präsent, auch wenn Sie gerade im Tagesgeschäft stecken.</b></p>
      </div>
      <div class="lp-arbeit__text" data-gruppe="arbeit-text" data-variante="kurz" hidden>
        <p>Sie müssen nichts vorbereiten und keinen ganzen Tag blocken. Wir stimmen uns kurz ab, die Arbeit dazwischen machen wir.</p>
        <p><b>So bleibt Ihr Thema präsent, auch wenn Sie gerade im Tagesgeschäft stecken.</b></p>
      </div>
    </div>
    <aside class="lp-netz">
      <p class="kicker">Unser Netzwerk</p>
      <h3>Wenn ein Thema mehr braucht, holen wir die passenden Leute dazu.</h3>
      <p>Sie behalten einen Ansprechpartner. Die Koordination liegt bei uns.</p>
      <ul>{netz}</ul>
    </aside>
  </div>
  <ol class="lp-schritte" data-gruppe="arbeit" data-variante="2" hidden>{schritte}</ol>
  <ol class="lp-ablauf" data-gruppe="arbeit" data-variante="3" hidden>
    <li><b>Kurzer Austausch</b><span>Telefonat, Videokonferenz, Workshop, wenn er sinnvoll ist. Oft reicht ein kurzer Austausch.</span></li>
    <li><b>Wir arbeiten</b><span>Mit Ihren Leuten, selbst und mit Spezialisten aus unserem Netzwerk.</span></li>
    <li><b>Nächster Austausch</b><span>Wir kommen mit einem klaren Bild zurück und setzen eine Stufe höher an.</span></li>
  </ol>
</div></section>

<!-- 4.1 Ergebnis -->
<section class="sek sek--navy lp-ergebnis"><div class="wrap lp-ergebnis__raster">
  <div>
    <p class="kicker">Ihr Ergebnis</p>
    <h2 class="h2 lp-gross">Sie haben Ihre Themen im Griff.</h2>
    <p class="lead">Im Gespräch behalten wir das Zielbild im Blick und schaffen Klarheit, wohin es geht. Sie entscheiden und konzentrieren sich auf die richtigen Dinge.</p>
  </div>
  {trio_szene("compass", "circle-check", "target")}
</div></section>

<!-- 4.2 Kontakt -->
<section class="sek lp-kontakt" id="kontakt"><div class="wrap">
  <div class="lp-kontakt__raster">
    <div>
      <p class="kicker">Kontakt</p>
      <h2 class="h2">Sie geben uns ein Thema und die Verantwortung dafür. Wir liefern das Ergebnis.</h2>
      <p class="lead">Erzählen Sie uns, was ansteht. Wir sagen offen, ob und wie wir es gemeinsam mit Ihnen umsetzen, und geben direkt unsere Meinung. Das erste Gespräch schafft Klarheit. Kein Pitch, keine Rechnung.</p>
      <div class="knoepfe"><a class="knopf" href="{MAIL_BEIDE}">Gespräch vereinbaren <svg class="ico" aria-hidden="true"><use href="#i-weiter"/></svg></a></div>
    </div>
    <div class="lp-kontakt__personen">{kontakte}</div>
  </div>
  <div class="lp-dl">
    <div class="lp-dl__bild" aria-hidden="true"><img class="lp-dl__seite lp-dl__seite--hinten" src="/entwicklung/downloads/business-story-2-2.png" alt="" loading="lazy"><img class="lp-dl__seite lp-dl__seite--vorn" src="/entwicklung/downloads/business-story-2-1.png" alt="" loading="lazy"></div>
    <div class="lp-dl__text">
      <p class="kicker">Download</p>
      <h3>Was wir tun und wofür wir stehen.</h3>
      <p>Unsere Einsatzgebiete, unser Vorgehen und wer wir sind. Zum Nachlesen und Weitergeben im Vorstand oder im Team.</p>
      <div class="lp-dl__meta"><span>PDF</span><span>12 Seiten</span><span>1,3 MB</span></div>
      <a class="knopf knopf--hell" href="/entwicklung/downloads/business-story-2.pdf" target="_blank" rel="noopener">PDF herunterladen <svg class="ico" aria-hidden="true"><use href="#i-weiter"/></svg></a>
    </div>
  </div>
</div></section>

<dialog class="fenster" id="fenster" aria-labelledby="fenster-titel"><div class="fenster__inhalt"></div><button class="fenster__zu" type="button" aria-label="Schließen"><svg class="ico" aria-hidden="true"><use href="#i-zu"/></svg></button></dialog>
{vorlagen}"""
    skript = """<script>
/* Variantenwahl (nur Entwurf) */
document.querySelectorAll('.wahl').forEach(function (w) {
  var g = w.getAttribute('data-gruppe');
  w.querySelectorAll('button').forEach(function (b) {
    b.addEventListener('click', function () {
      var v = b.textContent.trim();
      w.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
      document.querySelectorAll('[data-gruppe="' + g + '"][data-variante]').forEach(function (el) { el.hidden = el.getAttribute('data-variante') !== v; });
      if (g === 'arbeit') document.querySelectorAll('[data-gruppe="arbeit-text"]').forEach(function (el) { el.hidden = el.getAttribute('data-variante') !== (v === '3' ? 'kurz' : 'lang'); });
    });
  });
});
/* Wechselndes Wort in der Überschrift, im Takt mit der Zeile der drei Schritte */
(function () {
  var woerter = document.querySelectorAll('.wort > span'), schritte = document.querySelectorAll('.lp-drei li');
  if (!woerter.length || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var i = 0;
  setInterval(function () {
    i = (i + 1) % woerter.length;
    woerter.forEach(function (w, n) { w.classList.toggle('ist', n === i); });
    schritte.forEach(function (s, n) { s.classList.toggle('ist', n === i); });
  }, 2600);
})();
(function () {
  var f = document.getElementById('fenster'), inh = f.querySelector('.fenster__inhalt');
  document.querySelectorAll('[data-thema]').forEach(function (b) {
    b.addEventListener('click', function () {
      inh.innerHTML = document.getElementById('t-' + b.getAttribute('data-thema')).innerHTML;
      var h = inh.querySelector('h3'); if (h) h.id = 'fenster-titel';
      f.showModal();
    });
  });
  f.querySelector('.fenster__zu').addEventListener('click', function () { f.close(); });
  f.addEventListener('click', function (e) { if (e.target === f) f.close(); });
})();
</script>"""
    return seite("Müller &amp; Ströbel – Business Story 2.0 (Entwurf)", "Entwurf der Startseite: Business Story 2.0", "bs2", "", main, skript)


# ------------------------------------------------------------------ Über uns
def kontakt_neu(titel, text):
    """Kontakt wie auf der Startseite: Personen frei nebeneinander, darunter der Download."""
    kontakte = "".join(f'''<article class="kp"><div class="kreis"><img src="/assets/{k}-portrait.webp" alt="{p['name']}"></div>
      <h3>{p['name']}</h3><p class="kp__themen">{p['rolle']}</p>
      <p class="kp__wege"><a href="mailto:{p['mail']}">{p['mail']}</a><a href="tel:{p['tel_roh']}">{p['tel']}</a><a class="kp__li" href="{p['linkedin']}" target="_blank" rel="noopener">LinkedIn-Profil <svg viewBox="0 0 16 16" aria-hidden="true"><path d="M6 3.5H3.5v9h9V10M9 3h4v4M13 3 7.5 8.5"/></svg></a></p>
    </article>''' for k, p in PERSONEN.items())
    return f'''<section class="sek lp-kontakt" id="kontakt"><div class="wrap">
  <div class="lp-kontakt__raster">
    <div>
      <p class="kicker">Kontakt</p>
      <h2 class="h2">{titel}</h2>
      <p class="lead">{text}</p>
      <div class="knoepfe"><a class="knopf" href="{MAIL_BEIDE}">Gespräch vereinbaren <svg class="ico" aria-hidden="true"><use href="#i-weiter"/></svg></a></div>
    </div>
    <div class="lp-kontakt__personen">{kontakte}</div>
  </div>
  <div class="lp-dl">
    <div class="lp-dl__bild" aria-hidden="true"><img class="lp-dl__seite lp-dl__seite--hinten" src="/entwicklung/downloads/business-story-2-2.png" alt="" loading="lazy"><img class="lp-dl__seite lp-dl__seite--vorn" src="/entwicklung/downloads/business-story-2-1.png" alt="" loading="lazy"></div>
    <div class="lp-dl__text">
      <p class="kicker">Download</p>
      <h3>Was wir tun und wofür wir stehen.</h3>
      <p>Unsere Einsatzgebiete, unser Vorgehen und wer wir sind. Zum Nachlesen und Weitergeben im Vorstand oder im Team.</p>
      <div class="lp-dl__meta"><span>PDF</span><span>12 Seiten</span><span>1,3 MB</span></div>
      <a class="knopf knopf--hell" href="/entwicklung/downloads/business-story-2.pdf" target="_blank" rel="noopener">PDF herunterladen <svg class="ico" aria-hidden="true"><use href="#i-weiter"/></svg></a>
    </div>
  </div>
</div></section>'''


SKRIPT_WAHL_FENSTER = """<script>
document.querySelectorAll('.wahl').forEach(function (w) {
  var g = w.getAttribute('data-gruppe');
  w.querySelectorAll('button').forEach(function (b) {
    b.addEventListener('click', function () {
      var v = b.textContent.trim();
      w.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
      document.querySelectorAll('[data-gruppe="' + g + '"][data-variante]').forEach(function (el) { el.hidden = el.getAttribute('data-variante') !== v; });
    });
  });
});
(function () {
  var f = document.getElementById('fenster'); if (!f) return;
  var inh = f.querySelector('.fenster__inhalt');
  document.querySelectorAll('[data-thema]').forEach(function (b) {
    b.addEventListener('click', function () {
      inh.innerHTML = document.getElementById('t-' + b.getAttribute('data-thema')).innerHTML;
      var h = inh.querySelector('h3'); if (h) h.id = 'fenster-titel';
      f.showModal();
    });
  });
  f.querySelector('.fenster__zu').addEventListener('click', function () { f.close(); });
  f.addEventListener('click', function (e) { if (e.target === f) f.close(); });
})();
</script>"""

FENSTER = '<dialog class="fenster" id="fenster" aria-labelledby="fenster-titel"><div class="fenster__inhalt"></div><button class="fenster__zu" type="button" aria-label="Schließen"><svg class="ico" aria-hidden="true"><use href="#i-zu"/></svg></button></dialog>'


def ueber_uns():
    duo = "".join(f'<figure><div class="kreis"><img src="/assets/{k}-portrait.webp" alt="{p["name"]}"></div><figcaption><b>{p["name"]}</b></figcaption></figure>'
                  for k, p in PERSONEN.items())
    zusatz = {"tobias": '<p class="pp__fakt">Mitglied in zwei Aufsichtsräten</p>', "daniel": ""}
    personen = ""
    for i, (k, p) in enumerate(PERSONEN.items()):
        chips = "".join(f"<span>{x}</span>" for x in p["schwerpunkte"])
        personen += f'''<article class="pp{" pp--rechts" if i else ""}">
    <div class="pp__bild"><div class="kreis"><img src="/assets/{k}-portrait.webp" alt="{p['name']}"></div></div>
    <div class="pp__inhalt">
      <p class="kicker">Partner</p><h2 class="pp__name">{p['name']}</h2><p class="pp__rolle">{p['rolle']}</p>
      <div class="pp__spalten">
        <div><h4>Schwerpunkte</h4><div class="pp__chips">{chips}</div>{zusatz[k]}</div>
        <div><h4>Werdegang</h4><p>{p['werdegang']}</p>
          <button class="pp__mehr" type="button" data-thema="cv-{k}">Stationen im Lebenslauf <svg class="ico" aria-hidden="true"><use href="#i-weiter"/></svg></button>
          <h4>Kontakt</h4><p class="pp__wege"><a href="mailto:{p['mail']}">{p['mail']}</a><a href="tel:{p['tel_roh']}">{p['tel']}</a><a class="kp__li" href="{p['linkedin']}" target="_blank" rel="noopener">LinkedIn-Profil <svg viewBox="0 0 16 16" aria-hidden="true"><path d="M6 3.5H3.5v9h9V10M9 3h4v4M13 3 7.5 8.5"/></svg></a></p></div>
      </div>
    </div>
  </article>'''
    cv_vorlagen = "".join(f'<template id="t-cv-{k}"><h3>{p["name"]}</h3><p>Stationen im Lebenslauf</p><div class="stationen">{stationen(k)}</div></template>'
                          for k, p in PERSONEN.items())
    gebiete = "".join(f'<button class="gebiet" type="button" data-thema="{k}"><span class="gebiet__ico">{icon(k)}</span><b>{n}</b><span class="gebiet__wenn">{w}</span></button>'
                      for k, n, w in THEMEN)
    gebiet_vorlagen = "".join(f'<template id="t-{k}">{thema_detail(k)}</template>' for k, _, _ in THEMEN)
    netz = "".join(f"<span>{n}</span>" for n in NETZWERK)
    main = f"""
<section class="held lp-held"><div class="wrap held__raster">
  <div>
    <p class="kicker">Über uns</p>
    <div class="wahl" data-gruppe="ukopf"><span>Überschrift</span><button type="button" aria-pressed="true">1</button><button type="button" aria-pressed="false">2</button></div>
    <h1 data-gruppe="ukopf" data-variante="1">Unser Team. Unser Netzwerk.</h1>
    <h1 data-gruppe="ukopf" data-variante="2" hidden>Wir kennen die Branche von innen.</h1>
    <p class="lead">Zwei Partner mit eigener Führungserfahrung in der Versicherungswirtschaft, dazu ein Netzwerk erfahrener Spezialisten. Sie haben einen Ansprechpartner, wir bringen die passenden Leute zusammen. Im Projekt arbeiten wir beide selbst mit.</p>
  </div>
  <div class="duo duo--gleich">{duo}</div>
</div></section>

<section class="sek sek--sand"><div class="wrap pp-liste">{personen}</div></section>

<section class="sek sek--navy" id="gebiete"><div class="wrap">
  <div class="ergebnis">
    <div>
      <p class="kicker">Was uns verbindet</p>
      <h2 class="h2">Das Geschäftsmodell Versicherung. In seiner Gänze.</h2>
      <p class="lead">Wir verstehen, wie die Teile zusammenhängen: wie Strategie in Kennzahlen sichtbar wird, wie Gremien entscheiden und was davon im Vertrieb ankommt.</p>
    </div>
    <ul class="ergebnis__liste">
      <li><svg aria-hidden="true"><use href="#i-haken"/></svg>Wir wissen, wie Erfolg im Unternehmen entsteht.</li>
      <li><svg aria-hidden="true"><use href="#i-haken"/></svg>Wir kennen Entscheidungswege und wer eingebunden werden muss.</li>
      <li><svg aria-hidden="true"><use href="#i-haken"/></svg>Wir sprechen die Sprache von Vorstand, Aufsichtsrat und Fachbereich.</li>
    </ul>
  </div>
  <p class="gebiete__titel">Hier setzen wir an: unsere Einsatzgebiete</p>
  <div class="gebiete">{gebiete}</div>
</div></section>

<section class="sek"><div class="wrap netzwerk">
  <div><p class="kicker">Unser Netzwerk</p><h2 class="h2">Wenn ein Thema mehr braucht, holen wir die passenden Leute dazu.</h2></div>
  <div class="netzwerk__liste">{netz}</div>
</div></section>

{kontakt_neu("Sie geben uns ein Thema und die Verantwortung dafür. Wir liefern das Ergebnis.", "Erzählen Sie uns, was ansteht. Wir sagen offen, ob und wie wir es gemeinsam mit Ihnen umsetzen, und geben direkt unsere Meinung. Das erste Gespräch schafft Klarheit. Kein Pitch, keine Rechnung.")}

{FENSTER}
{cv_vorlagen}{gebiet_vorlagen}"""
    return seite("Müller &amp; Ströbel – Über uns (Entwurf Business Story 2.0)", "Entwurf: Über uns zur Business Story 2.0", "bs2-ueber", "Über uns", main, SKRIPT_WAHL_FENSTER)


# ------------------------------------------------------------------ Storyboard
# 12 Punkte (Interview) -> 8 Fragen des Lesers -> 4 Abschnitte der Landingpage. Status: da / teil / offen.
STORY = [
    ("Kopf", "Der Leser weiß sofort: Ich bin richtig, und das bekomme ich.", [
        ("1", "Bin ich hier richtig?", [
            ("1", "Welche Rollen genau", "da", "Vorstände und Geschäftsführer, Hauptabteilungs- und Bereichsleiter."),
            ("2", "Welche Unternehmen genau", "da", "Versicherungsbranche: Versicherer und Rückversicherer vom Konzern bis zum Versicherungsverein, Makler und Rückversicherungsmakler. Auf der Seite steht nur das Wort Versicherungsbranche.")]),
        ("4", "Was ist eure Antwort?", [
            ("7", "Das Versprechen im Wortlaut", "zuletzt", "Wir verstehen das Gegenüber. Wir strukturieren das Thema. Wir sorgen für die Abarbeitung und liefern das Ergebnis. Und wir belasten die Führungskraft dabei nur minimal.")]),
    ]),
    ("Ihre Lage", "Der Leser nickt: Genau so ist es bei mir, und darum hat es bisher nicht geklappt.", [
        ("2", "Verstehen die mein Problem?", [
            ("3", "Der Moment, in dem man euch anruft", "teil", "Ich muss alles im Blick haben. Ich will ein Ergebnis zurückbekommen, weil nur das zählt. Und das geht nicht."),
            ("4", "Das Problem in einem Satz", "teil", "Es ging schon wieder nichts voran.")]),
        ("3", "Warum hat das bisher keiner gelöst?", [
            ("5", "Was die Person vorher probiert hat", "teil", "Ich gebe es meinem eigenen Team. Oder ich hole Externe. Oder wir planen den großen Workshop über ein, zwei Tage."),
            ("6", "Warum das nicht gereicht hat", "teil", "Ich bekomme das Ergebnis nicht so zurück, wie ich es brauche, und muss immer noch mit reingreifen.")]),
    ]),
    ("So arbeiten wir", "Der Leser glaubt es und sieht, wie wenig Aufwand es ihn kostet.", [
        ("5", "Warum soll ich euch das glauben?", [
            ("8", "Der eine Beleg, der euch glaubwürdig macht", "teil", "Die Zusammenarbeit beim HÖV")]),
        ("6", "Wie läuft das ab, und was kostet es mich?", [
            ("9", "Der Zeitaufwand für den Kunden, konkret", "teil", "Wir setzen Formate gezielt ein: kurzer Austausch am Telefon, längere Videokonferenz, Workshop, wenn er sinnvoll ist. Oft reicht ein kurzer Austausch. Entscheidend ist der regelmäßige Kontakt: So bleibt das Thema präsent, und Sie haben es im Griff."),
            ("10", "Was ihr zwischen den Gesprächen liefert", "teil", "Ideen, Optionen, Entwürfe")]),
    ]),
    ("Ergebnis + Kontakt", "Der Leser weiß, was er davon hat, und greift zum Telefon.", [
        ("7", "Was habe ich am Ende davon?", [
            ("11", "Was am Ende anders ist, konkret", "teil", "Sie haben Ihre Themen im Griff und konzentrieren sich auf die richtigen Dinge. Im Gespräch behalten wir das Zielbild im Blick und schaffen Klarheit, wohin es geht. Darüber entscheiden Sie.")]),
        ("8", "Was ist der nächste Schritt?", [
            ("12", "Was im ersten Anruf passiert", "teil", "Sie erzählen uns, was ansteht. Wir stellen Fragen, sagen offen, ob und wie wir es gemeinsam mit Ihnen umsetzen können, und geben direkt unsere Meinung. Kein Pitch, keine Rechnung. Schon das erste Gespräch schafft Klarheit.")]),
    ]),
]
# Hintergrund je Punkt: Aussagen, die zum Kasten geführt haben (aufklappbar im Storyboard)
HINTERGRUND = {
    "1": ["„Die Zielgruppe sind Vorstände, Hauptabteilungsleiter, erfahrene Manager von Versicherungsunternehmen oder Rückversicherungsunternehmen.“ (09.10.)",
          "Ausarbeitung: Vorstand, Hauptabteilungsleiter, Bereichsleiter – das Problem gilt unabhängig von der Hierarchieebene.",
          "Euer eigener Fall: Tobias war Geschäftsführer beim HÖV.",
          "Bewusst nicht aufgenommen: Abteilungsleiter, Aufsichtsrat. Freigegeben am 11.10."],
    "2": ["„Wir sprechen immer von der Versicherungsbranche, um eben niemanden auszuschließen.“ (11.10.)",
          "Dazu gehören auch Makler und Rückversicherungsmakler.",
          "Versicherer und Rückversicherer (09.10.); Spanne vom Konzern bis zum Versicherungsverein: HÖV, Tobias’ Aufsichtsratsmandate, Daniels Zeit im Konzern.",
          "Festlegung: Auf der Seite steht nur das Wort Versicherungsbranche."],
    "3": ["Daniel, 11.10.: „Das bedeutet ja, dass er alles im Blick haben muss. Oder sie.“",
          "„Ich will ein Ergebnis zurückbekommen. Das brauche ich, weil nur das zählt. Und das geht nicht.“"],
    "4": ["Entwurf bisher: „Es ging schon wieder nichts voran.“",
          "Zu prüfen gegen Daniels Kern: „Ich will ein Ergebnis zurückbekommen, weil nur das zählt. Und das geht nicht.“"],
    "5": ["„Egal, ob ich es meinem eigenen Team oder einem Externen gebe …“ (11.10.)",
          "Der große Workshop: „Oh Gott, da brauche ich jetzt wieder einen riesen Workshop über ein, zwei Tage.“"],
    "6": ["Grenze 1 – Verstehen: „Ich habe diesen Komplex. Ich muss ihn verstehen, strukturieren, priorisieren. Da brauche ich am besten einen Sparringspartner auf Augenhöhe, der es aber wirklich bis in die Tiefe kapiert. Und auch die Logiken darin sieht und auch Lösungen erkennt.“",
          "Grenze 2 – Abarbeiten: „Egal, ob ich es meinem eigenen Team oder einem Externen gebe, ich bekomme das Ergebnis nicht so zurück, wie ich es brauche und muss da immer noch mit reingreifen. Das ist meine nächste Limitierung.“",
          "Workshop: „Der Workshop alleine hilft nichts, weil danach tut sich wieder ewig nichts, bis man dann irgendwann wieder im Kalender Zeit findet für den Riesen-Workshop.“"],
    "7": ["„Wir verstehen das Gegenüber.“",
          "„Wir strukturieren das Thema.“",
          "Sinngemäß: „Wir sorgen aber auch für die Abarbeitung und liefern das Ergebnis.“",
          "„Wir belasten die Führungskraft nur minimal, das ist der Kern.“",
          "Wird als Management Summary zum Schluss festgelegt."],
    "8": ["Euer Fall beim HÖV: Tobias als Geschäftsführer, Daniel hat ihn begleitet.",
          "Sinngemäß: Er konnte über jedes Thema sprechen; wo Daniel sich auskannte, dachte er direkt mit, wo nicht, sagte er es offen und wusste trotzdem, wie man das Thema angeht.",
          "Sinngemäß: Daniel hat das Projektmanagement übernommen, mit den Leuten gesprochen, dafür gesorgt, dass es weiterläuft, und selbst angepackt.",
          "Auf der Seite ohne Namen: „aus eigener Erfahrung“."],
    "9": ["„Wir haben verschiedene Formate, die wir gezielt einsetzen. Natürlich haben wir auch mal eine längere Videokonferenz. Und wenn es Sinn macht, dann gibt es auch mal einen Workshop.“ (11.10.)",
          "„Oftmals reicht ein kurzer Austausch.“ – zum Beispiel eine halbe Stunde am Telefon, wenn Sie ohnehin im Auto sitzen.",
          "„Wir wollen sicherstellen, dass wir im regelmäßigen kurzen Austausch bleiben, weil so bleibt das Thema präsent und unser Auftraggeber hat auch permanent das Thema im Griff.“",
          "Ähnlich wie das 1:1-Sparring für Führungskräfte bei empiria.",
          "Kern: Wir belasten die Führungskraft nur minimal."],
    "10": ["„Zwischen diesen Gesprächen arbeiten wir, an mehreren Ebenen gleichzeitig.“", "„Wir entwickeln Ideen, Optionen und Entwürfe, professionell aufbereitet.“",
           "„Beim nächsten Gespräch steigen wir eine Stufe höher ein, und du kannst entscheiden.“", "„Wir sind Referent, Analyseabteilung und Projektleitung in einem.“",
           "Netzwerk: ehemalige Vorstände und Aufsichtsräte, IT- und Prozess-Spezialisten, Entwickler, Marketingexperten, Grafiker."],
    "12": ["„Wir wollen mit den Personen sprechen. Sprechen wir über ihr Thema. Erzählen sie uns, was ansteht.“",
           "„Wir sagen ihnen offen, ob und wie wir es gemeinsam mit ihnen umsetzen können.“",
           "„Wir liefern direkt unseren Input und unsere Meinungen zu dem Thema. Wir halten da nichts zurück.“",
           "„Schon das erste Gespräch wird Klarheit schaffen, und da stellen wir auch gar keine Rechnung. Wir pitchen auch nichts.“",
           "„Unser Kunde kann direkt über seine Situation sprechen. Wir verstehen ihn. Wir stellen Fragen. Wir geben unsere Meinung ganz offen. Das ist schon allein ein Mehrwert.“"],
    "11": ["„Es geht über Entscheiden und Managen, Themen im Griff haben und sich auf die richtigen Dinge fokussieren.“ (11.10.)",
           "„Das Tolle ist, dass wir im Gespräch immer wieder das Zukunftsbild im Blick haben und Klarheit schaffen, wo es hingehen soll. Und darüber entschieden wird.“",
           "Es darf nicht nach Unterlagen und großen Dokumenten klingen. Kein Wort „Vorlagen“ an dieser Stelle.",
           "„Du verwaltest keinen Mangel mehr.“ (Grundstory)"],
}
# Verdichtung: der Satz für den Leser je Frage (Entwurf, gestrichelt bis zur Freigabe)
VERDICHTUNG = {
    "1": "Für Führungskräfte in der Versicherungsbranche.",
    "2": "Sie müssen alles im Blick haben. Und am Ende zählt nur das Ergebnis.",
    "3": "Ob eigenes Team oder Externe: Das Ergebnis kommt nicht so zurück, wie Sie es brauchen. Sie greifen doch wieder selbst ein. Und nach dem großen Workshop tut sich wochenlang nichts.",
    "4": "Wir verstehen Sie, strukturieren das Thema, sorgen für die Abarbeitung und liefern das Ergebnis. Und belasten Sie dabei nur minimal.",
    "5": "Aus eigener Erfahrung: Wir haben eine Führungskraft genau so begleitet. Mitgedacht, die Bearbeitung übernommen und dort selbst angepackt, wo wir die Fachkompetenz hatten.",
    "6": "Die Zusammenarbeit passt in Ihren Kalender: regelmäßig und kurz im Austausch, oft reicht ein Telefonat. Die Arbeit dazwischen machen wir.",
    "7": "Sie haben Ihre Themen im Griff und konzentrieren sich auf die richtigen Dinge. Im Gespräch behalten wir das Zielbild im Blick und schaffen Klarheit, wohin es geht. Darüber entscheiden Sie.",
    "8": "Rufen Sie an. Schon das erste Gespräch schafft Klarheit. Kein Pitch, keine Rechnung.",
}
ICO_GESPRAECH = '<svg class="ico" viewBox="0 0 24 24"><path d="M3.5 5.5h11a1.5 1.5 0 0 1 1.5 1.5v6a1.5 1.5 0 0 1-1.5 1.5H8l-3.5 3v-3h-1A1.5 1.5 0 0 1 2 13V7a1.5 1.5 0 0 1 1.5-1.5Z"/><path d="M16 9h4.5A1.5 1.5 0 0 1 22 10.5v6a1.5 1.5 0 0 1-1.5 1.5h-1v3l-3.5-3h-4"/></svg>'
ICO_ARBEIT = '<svg class="ico" viewBox="0 0 24 24"><path d="M14 3H6.5A1.5 1.5 0 0 0 5 4.5v15A1.5 1.5 0 0 0 6.5 21h11a1.5 1.5 0 0 0 1.5-1.5V8z"/><path d="M14 3v5h5M8.5 12.5h7M8.5 16h7M8.5 9h3"/></svg>'
ICO_ENTSCHEID = '<svg class="ico" viewBox="0 0 24 24"><circle cx="12" cy="12" r="8.5"/><path d="M8.2 12.3l2.6 2.6 5-5.4"/></svg>'
ICO_KREIS = '<svg class="ico" viewBox="0 0 24 24"><path d="M20 12a8 8 0 1 1-2.34-5.66"/><path d="M20 4v4.5h-4.5"/></svg>'
SCHRITTE_HTML = ('<ol class="lp-schritte">'
    f'<li class="lp-schritt"><span class="lp-schritt__ico">{ICO_GESPRAECH}</span><h3>Kurzer Austausch</h3><p>Telefonat, Videokonferenz, Workshop, wenn er sinnvoll ist. Oft reicht ein kurzer Austausch.</p></li>'
    f'<li class="lp-schritt"><span class="lp-schritt__ico">{ICO_ARBEIT}</span><h3>Wir arbeiten</h3><p>Mit Ihren Leuten, selbst und mit Spezialisten aus unserem Netzwerk.</p></li>'
    f'<li class="lp-schritt"><span class="lp-schritt__ico">{ICO_KREIS}</span><h3>Nächster Austausch</h3><p>Wir kommen mit einem klaren Bild zurück und setzen eine Stufe höher an.</p></li></ol>')
VORSCHAU_3_1 = ('<p class="kicker">So arbeiten wir</p><h2 class="h2">Die Zusammenarbeit passt in Ihren Kalender.</h2>'
    '<p class="lead">Wir bleiben im regelmäßigen, kurzen Austausch, oft reicht ein Telefonat. Die Arbeit dazwischen machen wir.</p>'
    + SCHRITTE_HTML +
    '<div class="vs-netz"><b>Wenn es Spezialwissen braucht, kommt es aus unserem Netzwerk</b><div><span>Ehemalige Vorstände</span><span>Aufsichtsräte</span><span>IT-Spezialisten</span><span>Prozess-Spezialisten</span><span>Entwickler</span><span>Grafiker</span></div></div>')
VORSCHAU_3_2 = ('<div class="vs-zwei"><div><p class="kicker">So arbeiten wir</p><h2 class="h2">Die Zusammenarbeit passt in Ihren Kalender.</h2>'
    '<p class="lead">Wir sprechen mit Ihren Leuten, arbeiten selbst mit und holen Spezialisten aus unserem Netzwerk dazu. Mit Ihnen bleiben wir im regelmäßigen, kurzen Austausch: So bleibt das Thema präsent, und Sie haben es im Griff.</p></div>'
    '<blockquote class="vs-erfahrung"><small>Aus eigener Erfahrung</small><p>Ein Geschäftsführer konnte mit uns über jedes Thema sprechen. Wir haben die Projekte übernommen, mit den Leuten gesprochen und selbst angepackt.</p></blockquote></div>'
    + SCHRITTE_HTML +
    f'<p class="lp-takt">{ICO_KREIS}Regelmäßig, bis das Ergebnis steht. So bleibt Ihr Thema präsent.</p>')

# Skizze der Landingpage je Abschnitt: zwei konkrete Fassungen (A/B), jede Zeile mit Quelle im Material
SKIZZE = [
    ("weiss", [
        ("A", [("Zeile", "Für Führungskräfte in der Versicherungsbranche", "Punkte 1–2"),
               ("H1", "Sie geben uns ein Thema und die Verantwortung dafür. Wir liefern das Ergebnis.", "Punkt 7 · zum Schluss"),
               ("Text", "Die Vorlage für den Aufsichtsrat, die Strategie, die in den Bereichen ankommen soll, die Kennzahlen, die steuern sollen: Wir verstehen Ihr Thema, strukturieren es und sorgen für die Umsetzung. Mit wenig Aufwand für Sie.", "Aufsichtsrat: Aussage 8 · Bereiche: Aussage 9 · Kennzahlen: Einsatzgebiet · Kern: Punkt 7"),
               ("Element", "Tobias und Daniel im Kreis · Knopf „Direkt anrufen“", "Punkt 12")]),
        ("B", [("Zeile", "Für Führungskräfte in der Versicherungsbranche", "Punkte 1–2"),
               ("H1", "Die Vorlage für den Aufsichtsrat. Die Strategie für die Bereiche. Das Projekt, das seit Monaten hängt. Geben Sie es uns.", "Aussagen 8, 9 · „seit Monaten in Bearbeitung“: Einsatzgebiet"),
               ("Text", "Wir verstehen Ihr Thema, strukturieren es und liefern Konzept, Analyse und Entscheidungsvorlage. Sie entscheiden.", "Kern: Punkt 7 · Konzepte, Analysen: Ausarbeitung 3.3"),
               ("Element", "Tobias und Daniel im Kreis · Knopf „Direkt anrufen“", "Punkt 12")]),
        ("C", [("Zeile", "Für Führungskräfte in der Versicherungsbranche", "Punkte 1–2"),
               ("H1", "Komplexe Situationen strukturieren, entscheiden, umsetzen.", "aus A"),
               ("Text", "Die Vorlage für den Aufsichtsrat, die Strategie, die in den Bereichen ankommen soll, die Kennzahlen, die steuern sollen: Wir machen Ihr Thema entscheidbar, mit Konzept, Analyse und Entscheidungsvorlage. Und wir sorgen für die Umsetzung, mit wenig Aufwand für Sie.", "Beispiele zuerst (A) · „entscheidbar machen“ (B) · Leistung und Umsetzung (A, B) · wenig Aufwand: Kern Punkt 7"),
               ("Element", "Tobias und Daniel im Kreis · Knopf „Direkt anrufen“", "Punkt 12"),
               ("Hinweis", "Das Versprechen (Punkt 7) wandert als Überschrift in den Kontakt am Ende.", "Vorschlag")]),
    ]),
    ("sand", [
        ("A", [("H2", "Die Vorlage für den Aufsichtsrat, die Strategie, die in den Bereichen ankommen soll, das Projekt, das seit Monaten hängt. Alles läuft über Ihren Tisch.", "Aussagen 8, 9 · Einsatzgebiet · Punkt 3"),
               ("Karte", "Ihr Team: liefert, aber nicht so, wie Sie es brauchen. Sie greifen wieder selbst ein.", "Punkt 6, Grenze 2"),
               ("Karte", "Externe: Der Berater liefert Empfehlungen. Umsetzen und koordinieren bleibt bei Ihnen.", "Aussagen 15, 18"),
               ("Karte", "Nur Workshops: zwei Tage im Kalender. Danach tut sich wochenlang nichts, bis wieder Zeit für den nächsten ist.", "Aussagen 22, 26")]),
        ("B", [("H2", "„Es ging schon wieder nichts voran. Jetzt muss ich mich doch selbst darum kümmern.“", "Dein Satz im Chat, Aussage 25"),
               ("Element", "Themen als Leiste: Aufsichtsrat · Strategie in die Bereiche · Kennzahlen · Vertrieb · KI-Vorhaben", "Aussagen 8, 9 · Einsatzgebiete"),
               ("Karte", "Ihr Team und Externe: Das Ergebnis kommt nicht so zurück, wie Sie es brauchen.", "Punkt 6"),
               ("Karte", "Nur Workshops: zwei Tage im Kalender, danach wochenlang Stillstand.", "Aussagen 22, 26")]),
        ("C", [("H2", "„Es ging schon wieder nichts voran.“", "Dein Satz im Chat, Aussage 25"),
               ("Text", "Die Vorlage für den Aufsichtsrat, die Strategie für die Bereiche, das Projekt, das seit Monaten hängt: Alles läuft über Ihren Tisch. Und die üblichen Wege helfen nur halb.", "Aussagen 8, 9 · Einsatzgebiet · Punkt 3 · Punkt 5"),
               ("Element", "Drei Karten nebeneinander, je ein kurzer Satz, darunter „Mehr“ zum Aufklappen", "Gestaltung"),
               ("Karte", "Ihr Team: liefert, aber nicht so, wie Sie es brauchen. Sie greifen wieder selbst ein.", "Punkt 6, Grenze 2"),
               ("Aufklappen", "Typisch bei: der Vorlage für den Aufsichtsrat · der Analyse, die eine Entscheidung tragen soll · dem Konzept, das in den Bereichen umgesetzt werden muss.", "Aussagen 8, 9 · Ausarbeitung 3.3"),
               ("Karte", "Externe: liefern Empfehlungen. Umsetzen und koordinieren bleibt bei Ihnen.", "Aussagen 15, 18"),
               ("Aufklappen", "Strategieberater, Projektmanager, Spezialisten: jeweils einzeln beauftragt. Die Verbindung, die Koordination und die Verantwortung für das Ergebnis bleiben bei Ihnen.", "Aussage 15"),
               ("Karte", "Nur Workshops: zwei Tage im Kalender, danach wochenlang Stillstand.", "Aussagen 22, 26"),
               ("Aufklappen", "Große Themen werden zur Hürde: erst ein Termin für den großen Workshop, danach tut sich wenig, bis wieder Zeit im Kalender ist.", "Aussagen 22, 26"),
               ("Zeile", "Darunter, als Brücke zu Abschnitt 3: Das Ergebnis kommt nicht so zurück, wie Sie es brauchen.", "Punkt 6")]),
    ]),
    ("weiss", [
        ("A", [("H2", "Wir arbeiten. Sie entscheiden.", "Punkte 9, 10"),
               ("Text", "Wir bleiben im regelmäßigen, kurzen Austausch, oft reicht ein Telefonat. Danach liegen Optionen, Entwürfe und Entscheidungsvorlagen auf Ihrem Tisch, professionell aufbereitet.", "Punkt 9 · Punkt 10 · Entscheidungsvorlagen: Einsatzgebiet Gremien"),
               ("Element", "Formate je nach Bedarf: kurzes Telefonat · längere Videokonferenz · Workshop, wenn sinnvoll", "Punkt 9"),
               ("Element", "Drei Schritt-Karten: Kurzer Austausch → Wir arbeiten → Sie entscheiden · darunter: regelmäßig, bis das Ergebnis steht", "Punkte 9, 10"),
               ("Element", "Netzwerk: ehemalige Vorstände, Aufsichtsräte, IT- und Prozess-Spezialisten, Entwickler, Grafiker", "Netzwerk-Hinweis")]),
        ("B", [("H2", "Zwischen zwei Telefonaten entstehen Konzept, Analyse und Entscheidungsvorlage.", "Punkt 10 · Ausarbeitung 3.3"),
               ("Text", "Wir sprechen mit Ihren Leuten, arbeiten selbst mit und holen Spezialisten aus unserem Netzwerk dazu. Mit Ihnen bleiben wir im regelmäßigen, kurzen Austausch: So bleibt das Thema präsent, und Sie haben es im Griff.", "Ausarbeitung 3.2, 3.3 · Punkt 9"),
               ("Element", "Drei Schritt-Karten: Kurzer Austausch → Wir arbeiten → Sie entscheiden", "Punkte 9, 10"),
               ("Kasten", "Aus eigener Erfahrung: Ein Geschäftsführer konnte mit uns über jedes Thema sprechen. Wir haben die Projekte übernommen, mit den Leuten gesprochen und selbst angepackt.", "Punkt 8, Fall HÖV, ohne Namen")]),
        ("Visualisierung 1", [("Vorschau", VORSCHAU_3_1, "Überschrift neu: Einfachheit der Zusammenarbeit · drei Schritt-Karten · Netzwerk als Leiste")]),
        ("Visualisierung 2", [("Vorschau", VORSCHAU_3_2, "Überschrift neu: Einfachheit der Zusammenarbeit · Erfahrung als Kasten rechts · drei Schritt-Karten · Takt-Zeile")]),
    ]),
    ("navy", [
        ("A", [("H2", "Sie verwalten keinen Mangel mehr. Sie entscheiden über fertige Vorlagen.", "Punkt 11"),
               ("Text", "Themen kommen so aufbereitet auf Ihren Tisch, dass Sie damit arbeiten können.", "Punkt 11")]),
        ("B", [("H2", "„Einmal mit Profis arbeiten.“", "Punkt 11, Aussage 27"),
               ("Text", "Sie entscheiden über Vorlagen, Zielbild und Fahrplan und sehen, wie es vorangeht.", "Punkt 11 · Zielbild: Grundstory")]),
        ("C", [("H2", "Sie haben Ihre Themen im Griff.", "Punkt 11"),
               ("Text", "Im Gespräch behalten wir das Zielbild im Blick und schaffen Klarheit, wohin es geht. Sie entscheiden und konzentrieren sich auf die richtigen Dinge.", "Punkt 11, Daniel 11.10.")]),
    ], "4.1 · Ergebnis", [
        ("4.2 · Kontakt", "sand", [
            ("C", [("H2", "Sie geben uns ein Thema und die Verantwortung dafür. Wir liefern das Ergebnis.", "Punkt 7 · zum Schluss"),
                   ("Text", "Das erste Gespräch schafft Klarheit. Kein Pitch, keine Rechnung.", "Punkt 12")]),
        ]),
    ]),
]
STATUS = {"da": "vorhanden", "teil": "teilweise", "offen": "offen", "zuletzt": "zum Schluss"}
SLOTS = [  # Abschnitt der Seite -> Bausteine mit Herkunft
    ("1", "Kopf", [("Zeile über der Überschrift", "F1 · Punkte 1–2"), ("Überschrift", "F4 · Punkt 7"),
                   ("Ein Satz darunter: für wen und welche Lage", "F1 · Punkte 1–2"), ("Knopf „Anrufen“", "F8 · Punkt 12")]),
    ("2", "Ihre Lage", [("Überschrift", "F2 · Punkt 4"), ("Szene aus dem Alltag", "F2 · Punkt 3"),
                        ("Gegensatz: übliche Wege und warum sie nicht reichen", "F3 · Punkte 5–6")]),
    ("3", "So arbeiten wir", [("Überschrift", "F6 · Punkt 9"), ("Bild: kurze Gespräche, dazwischen liefern wir", "F6 · Punkte 9–10"),
                              ("Beleg: ein erzählter Fall", "F5 · Punkt 8")]),
    ("4", "Ergebnis + Kontakt", [("Überschrift", "F7 · Punkt 11"), ("Was im ersten Anruf passiert", "F8 · Punkt 12"),
                                 ("Tobias und Daniel mit Telefon", "F8")]),
]


def storyboard():
    sprite = """<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="s-antwort" viewBox="0 0 24 24"><path d="M4 5.5h16v10H9l-5 4z"/><path d="M8 9.5h8M8 12.5h5"/></symbol>
  <symbol id="s-leser" viewBox="0 0 24 24"><circle cx="12" cy="8" r="3.5"/><path d="M5 20c.8-3.6 3.6-5.5 7-5.5s6.2 1.9 7 5.5"/></symbol>
  <symbol id="s-seite" viewBox="0 0 24 24"><rect x="4" y="3.5" width="16" height="17" rx="2"/><path d="M4 8h16M7.5 11.5h9M7.5 14.5h6"/></symbol>
  <symbol id="s-eins" viewBox="0 0 24 24"><path d="M4 12h16"/><path d="M4 7h10M4 17h7"/></symbol>
  <symbol id="s-wort" viewBox="0 0 24 24"><path d="M6 7.5h4.5v4.5c0 2.5-1.3 4-3.5 4.5M13.5 7.5H18v4.5c0 2.5-1.3 4-3.5 4.5"/></symbol>
  <symbol id="s-test" viewBox="0 0 24 24"><path d="M5 6.5l1.5 1.5 3-3M5 12.5l1.5 1.5 3-3M5 18.5l1.5 1.5 3-3M12.5 7h7M12.5 13h7M12.5 19h7"/></symbol>
  <symbol id="s-frei" viewBox="0 0 24 24"><circle cx="12" cy="12" r="8.5"/><path d="M8.2 12.3l2.6 2.6 5-5.4"/></symbol>
  <symbol id="s-pfeil" viewBox="0 0 24 24"><path d="M4 12h16M14 6l6 6-6 6"/></symbol>
</svg>"""

    def punkt(nr, txt, st, zit):
        q = f'<q>{zit}</q>' if zit else ""
        art = "Festlegung" if nr in ("1", "2") else "Wortlaut"
        info = ('<button class="sb-info" type="button" aria-label="Hinweis zu Punkt 7">i<span role="tooltip"><b>Management Summary</b>'
                'Das Versprechen fasst alles zusammen, was die übrigen Punkte ergeben. Deshalb legen wir es als Letztes fest.</span></button>') if nr == "7" else ""
        hg = HINTERGRUND.get(nr)
        mehr = (f'<details class="sb-mehr"><summary>Hintergrund</summary><ul>{"".join(f"<li>{x}</li>" for x in hg)}</ul></details>') if hg else ""
        return f'<li class="sb-p sb-p--{st}"><div><small>Punkt {nr} · {art}{info}</small><b>{txt}</b>{q}{mehr}</div></li>'

    baum = ""
    for i, (abschnitt, wirkung, fragen) in enumerate(STORY, 1):
        zeilen = ""
        for fnr, frage, punkte in fragen:
            pk = "".join(punkt(*p) for p in punkte)
            zeilen += (f'<div class="sb-t-zeile"><ul class="sb-t-punkte">{pk}</ul>'
                       f'<div class="sb-t-frage"><span class="sb-f">F{fnr}</span><b>{frage}</b>'
                       f'<p class="sb-verdichtung"><small>Verdichtung</small>{VERDICHTUNG[fnr]}</p></div></div>')
        eintrag = SKIZZE[i - 1]
        art, varianten = eintrag[0], eintrag[1]
        streifen_titel = eintrag[2] if len(eintrag) > 2 else ""
        weitere = eintrag[3] if len(eintrag) > 3 else []

        def vars_html(varianten):
            out = ""
            for v, teile in varianten:
                zeilen_sk = "".join(
                    (f'<div class="sk-vorschau"><div class="sk-vorschau__innen">{x}</div></div><span class="sk-vorschau__quelle">{q}</span>' if t == "Vorschau"
                     else f'<div class="sk-teil sk-teil--{t.lower()}"><em>{t}</em><p>{x}</p><span>{q}</span></div>') for t, x, q in teile)
                out += f'<div class="sk-var"><b class="sk-var__kopf">{"Fassung " + v if len(v) == 1 else v}</b>{zeilen_sk}</div>'
            return out

        if weitere:  # gleichrangige Sektionen (z. B. 4.1 Ergebnis, 4.2 Kontakt): je ein eigener Kasten
            kaesten = [(streifen_titel, art, varianten)] + list(weitere)
            skizze_html = '<div class="sk-stapel">' + "".join(
                f'<div class="sk sk--{a2}"><div class="sk__kopf">Abschnitt {t2}</div><div class="sk__vars">{vars_html(v2)}</div></div>'
                for t2, a2, v2 in kaesten) + '</div>'
        else:
            skizze_html = f'<div class="sk sk--{art}"><div class="sk__kopf">Abschnitt {i} · {abschnitt}</div><div class="sk__vars">{vars_html(varianten)}</div></div>'
        baum += (f'<div class="sb-t-gruppe"><div class="sb-t-zeilen">{zeilen}</div>'
                 f'<div class="sb-t-abschnitt"><span>0{i}</span><b>{abschnitt}</b><p>{wirkung}</p></div>'
                 f'{skizze_html}</div>\n')

    fragen_alle = sorted((int(f), t) for _, _, fr in STORY for f, t, _ in fr)
    punkte_alle = sorted((int(p[0]), p[1]) for _, _, fr in STORY for _, _, ps in fr for p in ps)
    logik_fragen = "".join(f'<li><span>F{n}</span>{t}</li>' for n, t in fragen_alle)
    logik_punkte = "".join(f'<li><span>{n}</span>{t}</li>' for n, t in punkte_alle)

    regeln = [("s-eins", "Eine Aussage je Frage", "Acht Fragen, acht Sätze. Mehr kommt nicht auf die erste Ebene."),
              ("s-wort", "Ihr Wortlaut", "Ich kürze und ordne Ihre Antworten. Wo etwas fehlt, frage ich nach."),
              ("s-test", "Drei Tests je Satz", "Könnte das jede Beratung schreiben? Steckt Führungsalltag drin? Gibt es eine echte Situation dahinter?"),
              ("s-frei", "Freigabe als Liste", "Sie sehen die acht Sätze untereinander, bevor eine Seite entsteht.")]
    karten = "".join(f'<div class="sb-karte"><span class="sb-karte__ico"><svg class="ico"><use href="#{ic}"/></svg></span><h3>{t}</h3><p>{x}</p></div>'
                     for ic, t, x in regeln)

    legende = "".join(f'<li><span class="sb-nr">{n}</span><div><b>{t}</b><p>{" · ".join(f"{a} <em>{h}</em>" for a, h in bs)}</p></div></li>'
                      for n, t, bs in SLOTS)

    main = f"""{sprite}
<section class="held sb-held"><div class="wrap">
  <p class="kicker">Storyboard</p>
  <h1>So entsteht die Landingpage.</h1>
  <p class="lead">Sie beantworten enge Punkte. Daraus werden die Antworten auf die Fragen, die sich der Leser stellt. Und daraus die Seite. <b>Festlegung</b> heißt: steuert den Text, steht nicht wörtlich da. <b>Wortlaut</b> heißt: kommt so oder fast so auf die Seite.</p>
  <ol class="sb-weg">
    <li><span class="sb-weg__ico"><svg class="ico"><use href="#s-antwort"/></svg></span><b>12 Punkte</b><h2>Ihre Antworten</h2><p>Enge Fragen, je eine klare Antwort.</p></li>
    <li class="sb-weg__pfeil" aria-hidden="true"><svg class="ico"><use href="#s-pfeil"/></svg></li>
    <li><span class="sb-weg__ico"><svg class="ico"><use href="#s-leser"/></svg></span><b>8 Fragen</b><h2>Die Gedanken des Lesers</h2><p>In der Reihenfolge, in der er sie sich stellt.</p></li>
    <li class="sb-weg__pfeil" aria-hidden="true"><svg class="ico"><use href="#s-pfeil"/></svg></li>
    <li class="sb-weg--ziel"><span class="sb-weg__ico"><svg class="ico"><use href="#s-seite"/></svg></span><b>4 Abschnitte</b><h2>Die Landingpage</h2><p>Je zwei Fragen ergeben einen Abschnitt.</p></li>
  </ol>
</div></section>

<section class="sb-logik"><div class="wrap">
  <div class="sb-logik__kopf"><p class="kicker">Die Logik dahinter</p>
    <p>Der Leser stellt sich acht Fragen, immer in dieser Reihenfolge. Um sie zu beantworten, klären wir zwölf Punkte. Wie beides zusammenhängt, zeigt die Zuordnung darunter.</p></div>
  <div class="sb-logik__listen">
    <div><h2>Die 8 Fragen des Lesers</h2><ol class="sb-liste">{logik_fragen}</ol></div>
    <div><h2>Die 12 Punkte, die wir klären</h2><ol class="sb-liste">{logik_punkte}</ol></div>
  </div>
</div></section>

<section class="sek sek--sand"><div class="wrap">
  <div class="sb-titel"><div><p class="kicker">Zuordnung</p><h2 class="h2">Jeder Punkt hat genau einen Platz.</h2></div></div>
  <p class="sb-schieben">Arbeitsfläche: mit dem Trackpad nach rechts schieben bis zur Skizze der Landingpage →</p>
</div>
<div class="sb-flaeche"><div class="sb-flaeche__innen">
  <div class="sb-t-kopf"><span><i>1</i>Ihre Antworten<small>12 Punkte</small></span><span><i>2</i>Fragen des Lesers<small>8 Fragen · Verdichtung</small></span><span><i>3</i>Abschnitt<small>4</small></span><span><i>4</i>Landingpage-Skizze<small>Headline · Text · Elemente</small></span></div>
  <div class="sb-t">{baum}</div>
</div></div>
<div class="wrap">
</div></section>

<section class="sek"><div class="wrap">
  <p class="kicker">Aus Punkten werden Aussagen</p>
  <h2 class="h2">Vier Regeln, bevor ein Satz auf die Seite kommt.</h2>
  <div class="sb-karten">{karten}</div>
</div></section>

<section class="sek sek--navy"><div class="wrap sb-bau">
  <div>
    <p class="kicker">Aus Aussagen wird die Seite</p>
    <h2 class="h2">Jeder Baustein hat genau eine Herkunft.</h2>
    <ol class="sb-bau__liste">{legende}</ol>
  </div>
  <div class="sb-mock" aria-label="Aufbau der Landingpage">
    <div class="sb-mock__leiste"><i></i><i></i><i></i></div>
    <div class="sb-mock__a sb-mock__a--1"><span class="sb-tag">F1 · Für wen</span><b class="sb-bar sb-bar--h1"></b><span class="sb-tag sb-tag--n">F4 · Versprechen</span><b class="sb-bar"></b><span class="sb-knopf">F8 · Anrufen</span><em class="sb-kreise"><i></i><i></i></em></div>
    <div class="sb-mock__a sb-mock__a--2"><span class="sb-tag">F2 · Ihre Lage</span><b class="sb-bar sb-bar--h2"></b><div class="sb-zwei"><span>Szene aus dem Alltag</span><span>F3 · Übliche Wege vs. wir</span></div></div>
    <div class="sb-mock__a sb-mock__a--3"><span class="sb-tag sb-tag--h">F6 · Ablauf</span><b class="sb-bar sb-bar--h2"></b><div class="sb-drei"><i></i><i></i><i></i></div><span class="sb-tag sb-tag--h">F5 · Beleg</span></div>
    <div class="sb-mock__a sb-mock__a--4"><span class="sb-tag">F7 · Ergebnis</span><b class="sb-bar sb-bar--h2"></b><em class="sb-kreise sb-kreise--klein"><i></i><i></i></em><span class="sb-knopf">F8 · Anrufen</span></div>
  </div>
</div></section>"""
    html = seite("Müller &amp; Ströbel – Storyboard Business Story 2.0", "Storyboard: von den Antworten zur Landingpage", "bs2-story", "", main)
    return html.replace("</head>", f'<link rel="stylesheet" href="/entwicklung/storyboard.css?v={VERSION}">\n</head>', 1)

# ------------------------------------------------------------------ Elevator Pitch
# Von den Storyboard-Aussagen zum kurzen, gesprochenen Pitch (30 und 10 Sekunden).
PITCH = [  # (Nr, Baustein, Frage des Gegenübers, Quelle im Storyboard, Satz im Pitch, warum so)
    ("1", "Aufhänger", "Kennt der meine Lage?", "F2 · Punkt 3 · Punkt 4",
     "Sie müssen alles im Blick haben. Und am Ende zählt nur das Ergebnis.",
     "Startet bei ihm, nicht bei uns. Er nickt, bevor wir über uns reden."),
    ("2", "Der Schmerz", "Warum klappt es bisher nicht?", "F3 · Punkte 5–6",
     "Ob Sie ein Thema Ihrem Team geben oder Externe holen: Es kommt selten so zurück, wie Sie es brauchen.",
     "Ein konkretes Erlebnis aus seinem Alltag statt einer Behauptung über den Markt."),
    ("3", "Unsere Antwort", "Was macht ihr anders?", "F4 · Punkt 7 · Aussagen 8, 9",
     "Da setzen wir an. Sie geben uns die Verantwortung für ein Thema, etwa die Vorlage für den Aufsichtsrat. Wir strukturieren es, arbeiten es mit Ihrem Team aus und liefern das Ergebnis.",
     "Versprechen plus ein Beispiel, das er sofort einordnen kann. Weitere Beispiele, wenn er nachfragt."),
    ("4", "Sein Aufwand", "Was kostet mich das?", "F6 · Punkt 9",
     "Von Ihnen brauchen wir dafür meist nur ein kurzes Telefonat zwischendurch.",
     "Räumt den häufigsten Einwand aus: keine Zeit für noch ein Projekt."),
    ("5", "Sein Gewinn", "Was habe ich davon?", "F7 · Punkt 11",
     "So haben Sie Ihre Themen im Griff.",
     "Das Gefühl, um das es eigentlich geht, in einem Satz."),
    ("6", "Nächster Schritt", "Was soll ich jetzt tun?", "F8 · Punkt 12",
     "Liegt gerade so ein Thema auf Ihrem Tisch? Dann lassen Sie uns kurz sprechen.",
     "Niedrige Schwelle, konkreter Anlass. Im Nachgespräch: Das erste Gespräch kostet nichts."),
]
PITCH_10 = ("Wir übernehmen für Führungskräfte in der Versicherungsbranche komplexe Themen, von der Vorlage für den Aufsichtsrat "
            "bis zur Überführung der Strategie in den Alltag, und liefern das Ergebnis. Sie brauchen dafür nur kurze Abstimmungen.")
WEG = [  # nach dem Pitch: worauf wir im Gespräch bewusst hinsteuern
    ("Sein Thema", "Wir fragen, was bei ihm gerade ansteht. Passt eines unserer Einsatzgebiete, nennen wir es mit einem Beispiel. Den Überblick gibt das PDF."),
    ("Der Beleg aus eigener Erfahrung", "Fragt er, ob das funktioniert, erzählen wir, wie wir eine Führungskraft genau so begleitet haben."),
    ("Unser Netzwerk", "Fragt er „Und wenn ihr etwas nicht könnt?“, erzählen wir, welche Spezialisten wir dazuholen."),
    ("Die Formate", "Wird es konkret, zeigen wir die Bandbreite: Telefonat, Videokonferenz, Workshop, wo er sinnvoll ist."),
    ("Wer wir sind", "Name und Rolle in der Vorstellung. Werdegang und Fakten stehen auf Über uns und im PDF."),
    ("Der nächste Schritt", "Ein Gespräch zu seinem Thema vereinbaren. Das erste Gespräch kostet nichts: Wir sagen offen, ob und wie wir es umsetzen können."),
]
LENKUNG = [  # Lenkungsfragen: herausfinden, was für das Gegenüber wichtig ist
    ("„Was liegt bei Ihnen gerade auf dem Tisch, das nicht so vorankommt, wie Sie es brauchen?“", "Zeigt das konkrete Thema."),
    ("„Wo greifen Sie im Moment selbst ein, obwohl Sie es eigentlich abgegeben haben?“", "Zeigt, wo es hakt und was ihn Zeit kostet."),
    ("„Was steht als Nächstes im Vorstand oder im Aufsichtsrat an?“", "Zeigt Anlass und Termin."),
    ("„Wer aus Ihrem Team arbeitet daran, und was fehlt dort?“", "Zeigt, wie wir mit seinem Team arbeiten würden."),
    ("„Woran würden Sie in drei Monaten merken, dass das Thema im Griff ist?“", "Zeigt sein Zielbild."),
]
REGELN = [
    ("Bei ihm anfangen", "Die ersten zwei Sätze handeln nur von seiner Lage. Über uns sprechen wir erst ab Satz drei."),
    ("Ein Gedanke je Satz", "Kurze Sätze, die man gesprochen versteht. Keine Aufzählungen mit mehr als zwei Beispielen."),
    ("Sein Wortschatz", "Aufsichtsrat, Bereiche, Team, Telefonat: Dinge aus seinem Kalender, keine Beraterbegriffe."),
    ("Mit einer Einladung enden", "Ein konkreter, kleiner nächster Schritt. Er muss nichts entscheiden außer einem Gespräch."),
]


def elevator_pitch():
    quellen = ""
    for _, _, fragen in STORY:
        for fnr, frage, punkte in fragen:
            if fnr in ("1", "5"):
                continue
            quellen += (f'<div class="ep-quelle"><span class="sb-f">F{fnr}</span><b>{frage}</b>'
                        f'<p>{VERDICHTUNG[fnr]}</p></div>')
    zeilen = "".join(
        f'''<div class="ep-zeile">
      <div class="ep-quelle-k"><small>{q}</small></div>
      <div class="ep-baustein"><span>{n}</span><b>{t}</b><em>„{frage}“</em></div>
      <div class="ep-satz"><p>{satz}</p><small>{warum}</small></div>
    </div>''' for n, t, frage, q, satz, warum in PITCH)
    pitch_text = " ".join(satz for *_, satz, _ in [(p[0], p[1], p[2], p[3], p[4], p[5]) for p in PITCH])
    woerter = len(pitch_text.split())
    weg = "".join(f"<li><b>{t}</b>{x}</li>" for t, x in WEG)
    lenkung = "".join(f"<li><b>{t}</b>{x}</li>" for t, x in LENKUNG)
    regeln_kurz = "".join(f"<li>{t}</li>" for t, _ in REGELN)
    themen_chips = "".join(f'<li{" class=passt" if i == 2 else ""}>{t}</li>' for i, (_, t, *_) in enumerate(THEMEN))
    regeln = "".join(f'<div class="sb-karte"><h3>{t}</h3><p>{x}</p></div>' for t, x in REGELN)
    absaetze = "".join(f"<p>{p[4]}</p>" for p in PITCH)
    main = f"""
<section class="held held--klein"><div class="wrap ep-held">
  <div>
    <p class="kicker">Elevator Pitch</p>
    <h1>Unsere Story<br>in 30/10 Sekunden.</h1>
    <p class="lead">Die Landingpage ist die lange Fassung unserer Story. Hier verdichten wir sie auf das, was Sie einem Vorstand in einer Kaffeepause sagen: ohne Bild, mit einfachen Worten, aus seiner Sicht. Jeder Satz beantwortet seine stille Frage: Was bringt mir das?</p>
  </div>
  <a class="ep-dl" href="/entwicklung/downloads/elevator-pitch.pdf" target="_blank" rel="noopener">
    <div class="ep-dl__bild" aria-hidden="true"><img class="ep-dl__seite ep-dl__seite--hinten" src="/entwicklung/downloads/elevator-pitch-2.png" alt=""><img class="ep-dl__seite ep-dl__seite--vorn" src="/entwicklung/downloads/elevator-pitch-1.png" alt=""></div>
    <p class="kicker">Download · intern</p>
    <b>Der Pitch und wie er entstanden ist.</b>
    <span class="ep-dl__meta">PDF · 2 Seiten · 0,2 MB</span>
    <span class="knopf knopf--hell">PDF herunterladen <svg class="ico" aria-hidden="true"><use href="#i-weiter"/></svg></span>
  </a>
</div></section>

<section class="sek sek--navy ep-viz"><div class="wrap">
  <p class="kicker">So hängt es zusammen</p>
  <div class="ep-weg3">
    <div class="ep-stufe ep-stufe--pitch">
      <h3>Pitch</h3>
      <div class="ep-dauer"><span>30 Sekunden</span><span>10 Sekunden</span></div>
      <ul class="ep-regeln-kurz">{regeln_kurz}</ul>
    </div>
    <span class="ep-pfeil" aria-hidden="true"></span>
    <div class="ep-stufe">
      <h3>Fragen</h3>
      <p class="ep-zitat">„Wie ist bei Ihnen gerade die Situation?“</p>
    </div>
    <span class="ep-pfeil" aria-hidden="true"></span>
    <div class="ep-stufe">
      <h3>Sein Thema</h3>
      <ul class="ep-themen">{themen_chips}</ul>
    </div>
  </div>
</div></section>

<section class="sek sek--sand ep-pitch-kompakt"><div class="wrap">
  <p class="kicker">Der Pitch</p>
  <div class="ep-zwei">
    <div>
      <h3>30 Sekunden</h3>
      <div class="ep-text-k">{absaetze}</div>
      <p class="ep-mass-k">{woerter} Wörter · gesprochen etwa {round(woerter / 2.5 / 5) * 5} Sekunden</p>
    </div>
    <div>
      <h3>10 Sekunden</h3>
      <div class="ep-text-k"><p>{PITCH_10}</p><p>Kurz gesagt: Wir sind die rechte Hand, die Sie sich für Ihre wichtigsten Themen immer gewünscht haben.</p></div>
      <p class="ep-mass-k">Für die Vorstellungsrunde oder die Frage „Und was machen Sie?“</p>
    </div>
  </div>
</div></section>

<section class="sek"><div class="wrap">
  <p class="kicker">Nach dem Pitch</p>
  <h2 class="h2">Nächste Schritte und Gesprächsführung.</h2>
  <p class="lead">Der Pitch öffnet das Gespräch. Danach fragen wir, was für das Gegenüber wichtig ist, und steuern bewusst auf sein Thema zu.</p>
  <div class="ep-weg ep-gespraech">
    <div><h3>Lenkungsfragen</h3><p>Damit finden wir heraus, welches Thema ihn gerade beschäftigt.</p></div>
    <ul>{lenkung}</ul>
  </div>
  <div class="ep-weg ep-gespraech">
    <div><h3>Worauf wir hinsteuern</h3><p>Was wir im Gespräch einbringen, sobald er danach fragt.</p></div>
    <ul>{weg}</ul>
  </div>
</div></section>

<section class="sek sek--navy ep-streifen"><div class="wrap">
  <p class="ep-streifen__satz">Jetzt kennen Sie den Pitch und seine Anwendung. Wie ist er entstanden?</p>
</div></section>

<section class="sek sek--sand"><div class="wrap">
  <p class="kicker">Ausgangsmaterial</p>
  <h2 class="h2">Diese Aussagen haben wir im Storyboard entwickelt.</h2>
  <p class="lead">Die Verdichtungen je Leserfrage. F1 (für wen) ist im Gespräch durch die Situation geklärt, F5 (Beleg) heben wir für das Nachgespräch auf.</p>
  <div class="ep-quellen">{quellen}</div>
</div></section>

<section class="sek"><div class="wrap">
  <p class="kicker">Zuordnung</p>
  <h2 class="h2">Sechs Bausteine, sechs Sätze.</h2>
  <p class="lead">Links die Herkunft im Storyboard, in der Mitte der Baustein mit der Frage, die sich das Gegenüber stellt, rechts der Satz, wie er gesprochen wird.</p>
  <div class="ep-kopf"><span>Herkunft</span><span>Baustein · seine Frage</span><span>Satz im Pitch · warum so</span></div>
  <div class="ep-zeilen">{zeilen}</div>
</div></section>

<section class="sek sek--sand"><div class="wrap">
  <p class="kicker">Aufbau eines guten kurzen Pitches</p>
  <h2 class="h2">Vier Regeln.</h2>
  <div class="sb-karten ep-regeln">{regeln}</div>
</div></section>"""
    html = seite("Müller &amp; Ströbel – Elevator Pitch (Business Story 2.0)", "Elevator Pitch: von den Storyboard-Aussagen zum kurzen Pitch", "bs2-pitch", "", main)
    return html.replace("</head>", f'<link rel="stylesheet" href="/entwicklung/storyboard.css?v={VERSION}">\n</head>', 1)


if __name__ == "__main__":
    (ZIEL / "business-story-2.html").write_text(startseite(), encoding="utf-8")
    (ZIEL / "business-story-2-ueber-uns.html").write_text(ueber_uns(), encoding="utf-8")
    (ZIEL / "storyboard.html").write_text(storyboard(), encoding="utf-8")
    (ZIEL / "elevator-pitch.html").write_text(elevator_pitch(), encoding="utf-8")
    print("gebaut: business-story-2.html, business-story-2-ueber-uns.html, storyboard.html")
