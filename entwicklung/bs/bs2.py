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
VERSION = 14

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
    return f'''<header class="kopf"><div class="wrap">
  <a class="marke" href="{start}" aria-label="Müller &amp; Ströbel – Startseite"><img src="/assets/logo.svg" alt="Müller &amp; Ströbel"></a>
  <nav class="nav" aria-label="Hauptmenü">{nav}
{DEV}
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
</body>
</html>
'''


# ------------------------------------------------------------------ Startseite
def platz(punkt, titel, hinweis, status="offen", klein=False):
    """Sichtbar markierter Platzhalter für einen noch offenen Punkt aus dem Storyboard."""
    return (f'<div class="platz platz--{status}{" platz--klein" if klein else ""}"><span class="platz__tag">{punkt} · {STATUS[status]}</span>'
            f'<b>{titel}</b><p>{hinweis}</p></div>')


def startseite():
    T, D = PERSONEN["tobias"], PERSONEN["daniel"]
    sprite = """<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="l-tel" viewBox="0 0 24 24"><circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/></symbol>
  <symbol id="l-pfeil" viewBox="0 0 24 24"><path d="M4 12h16M14 6l6 6-6 6"/></symbol>
</svg>"""
    duo = "".join(f'<figure><div class="kreis"><img src="/assets/{k}-portrait.webp" alt="{p["name"]}"></div><figcaption><b>{p["name"]}</b>{p["kurz"]}</figcaption></figure>'
                  for k, p in PERSONEN.items())
    gespraeche = [("Sie schildern das Thema.", "Ideen"), ("Sie legen die Richtung fest.", "Optionen"),
                  ("Sie entscheiden.", "Entwürfe"), ("Sie geben frei.", "Ergebnis")]
    treppe = "".join(f'''<li class="lp-stufe"><span class="lp-stufe__ico"><svg class="ico"><use href="#l-tel"/></svg></span>
        <small>Gespräch {i}</small><h3>{s}</h3><p><b>Dazwischen liefern wir</b>{x}</p></li>''' for i, (s, x) in enumerate(gespraeche, 1))
    wege = "".join(f'''<div class="lp-weg"><span class="lp-weg__nr">Weg {i}</span>
        {platz("Punkt 5", "Was die Führungskraft vorher probiert hat", "z. B. Berater, Workshop, eigene Leute – Ihre Antwort", klein=True)}
        {platz("Punkt 6", "Warum das nicht gereicht hat", "ein Satz, aus Sicht der Führungskraft", klein=True)}</div>''' for i in (1, 2, 3))
    kontakte = "".join(f'''<article class="person"><div class="kreis"><img src="/assets/{k}-portrait.webp" alt="{p['name']}"></div><div>
      <h3>{p['name']}</h3><p class="person__kurz">{p['kurz']}</p>
      <div class="wege"><a href="tel:{p['tel_roh']}">{p['tel']}</a><a href="mailto:{p['mail']}">{p['mail']}</a><a href="{p['linkedin']}" target="_blank" rel="noopener">LinkedIn</a></div>
    </div></article>''' for k, p in PERSONEN.items())
    main = f"""{sprite}
<div class="entwurf-hinweis"><div class="wrap">Entwurf nach dem <a href="/entwicklung/storyboard.html">Storyboard</a>: gestrichelte Felder sind offene Punkte und werden durch Ihre freigegebenen Sätze ersetzt.</div></div>

<!-- Abschnitt 1 · Kopf (F1 + F4) -->
<section class="held lp-held"><div class="wrap held__raster">
  <div>
    <p class="kicker">Für Führungskräfte in der Versicherungsbranche</p>
    <h1>Sie geben uns ein Thema und die Verantwortung dafür. Wir liefern das Ergebnis.</h1>
    {platz("Punkte 1–2", "Ein Satz darunter: für wen und in welcher Lage", "Rollen und Unternehmen aus Punkt 1 und 2, in einem Satz")}
    <div class="knoepfe"><a class="knopf" href="#kontakt">Direkt anrufen <svg class="ico" aria-hidden="true"><use href="#i-weiter"/></svg></a><a class="knopf knopf--rand" href="#lage">Kennen Sie das?</a></div>
  </div>
  <div class="duo">{duo}</div>
</div></section>

<!-- Abschnitt 2 · Ihre Lage (F2 + F3) -->
<section class="sek sek--sand" id="lage"><div class="wrap">
  <p class="kicker">Ihre Lage</p>
  <h2 class="h2 lp-gross">„Es ging schon wieder nichts voran.“</h2>
  <div class="lp-szene">{platz("Punkt 3", "Szene aus dem Alltag", "Der Moment, in dem eine Führungskraft zum Telefon greift und Sie anruft – konkret, mit Ort, Anlass, Frist")}</div>
  <div class="lp-bahn">
    <div class="lp-bahn__kopf"><span>Warum es bisher nicht geklappt hat</span><h3>Die üblichen Wege</h3></div>
    {wege}
  </div>
</div></section>

<!-- Abschnitt 3 · So arbeiten wir (F5 + F6) -->
<section class="sek" id="arbeitsweise"><div class="wrap">
  <p class="kicker">So arbeiten wir</p>
  <h2 class="h2">Wir bleiben im regelmäßigen, kurzen Austausch.</h2>
  <p class="lead">Oft reicht ein Telefonat, manchmal eine längere Videokonferenz, und wenn es sinnvoll ist, ein Workshop. So bleibt Ihr Thema präsent, und Sie haben es im Griff. Dazwischen arbeiten wir. <span class="platz-marke">Punkte 9–10 Entwurf</span></p>
  <ol class="lp-treppe">{treppe}</ol>
  <div class="lp-beleg">{platz("Punkt 8", "Der Beleg: ein erzählter Fall", "Die Zusammenarbeit beim HÖV – erzählt in drei, vier Sätzen, ohne Namen", status="teil")}</div>
</div></section>

<!-- Abschnitt 4 · Ergebnis + Kontakt (F7 + F8) -->
<section class="sek sek--navy lp-ende" id="kontakt"><div class="wrap">
  <p class="kicker">Ihr Ergebnis <span class="platz-marke platz-marke--hell">Punkt 11 teilweise</span></p>
  <h2 class="h2 lp-gross">Sie entscheiden und steuern, statt den Mangel zu verwalten.</h2>
  <div class="lp-anruf">{platz("Punkt 12", "Das erste Gespräch schafft Klarheit.", "Sie erzählen uns, was ansteht. Wir stellen Fragen, sagen offen, ob und wie wir es gemeinsam mit Ihnen umsetzen können, und geben direkt unsere Meinung. Kein Pitch, keine Rechnung.", status="teil", klein=True)}</div>
  <div class="personen">{kontakte}</div>
</div></section>"""
    return seite("Müller &amp; Ströbel – Business Story 2.0 (Entwurf)", "Entwurf der Startseite: Business Story 2.0", "bs2", "", main)


# ------------------------------------------------------------------ Über uns
def ueber_uns():
    bloecke = ""
    for i, (k, p) in enumerate(PERSONEN.items()):
        punkte = "".join(f"<span>{s}</span>" for s in p["schwerpunkte"])
        bloecke += f'''<article class="profil{" profil--rechts" if i else ""}">
    <div class="profil__bild"><div class="kreis"><img src="/assets/{k}-portrait.webp" alt="{p['name']}"></div></div>
    <div class="profil__text">
      <p class="kicker">Partner</p><h2 class="h2">{p['name']}</h2><p class="profil__rolle">{p['rolle']}</p>
      <p class="lead">{p['werdegang']}</p>
      <div class="profil__punkte">{punkte}</div>
      <details class="mehr"><summary><i aria-hidden="true">+</i>Stationen im Lebenslauf</summary><div class="stationen">{stationen(k)}</div></details>
    </div>
  </article>'''
    main = f'''
<section class="held held--klein"><div class="wrap">
  <p class="kicker">Über uns</p>
  <h1>Tobias Müller <i>&amp;</i> Daniel Ströbel</h1>
  <p class="lead">Wir kennen das Geschäftsmodell Versicherung von innen und haben schon viele Projekte gemeinsam umgesetzt. Jeder von uns bringt klare Schwerpunkte mit. Im Projekt arbeiten wir beide selbst mit.</p>
</div></section>

<section class="sek sek--sand profile"><div class="wrap">{bloecke}</div></section>

<section class="sek sek--navy"><div class="wrap ergebnis">
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
</div></section>

<section class="sek"><div class="wrap netzwerk">
  <div><p class="kicker">Unser Netzwerk</p><h2 class="h2">Wenn ein Thema mehr braucht, holen wir die passenden Leute dazu.</h2></div>
  <div class="netzwerk__liste">{"".join(f"<span>{n}</span>" for n in NETZWERK)}</div>
</div></section>

{kontakt("Welches Thema geben Sie uns?", "Rufen Sie einen von uns direkt an. Nach dem ersten Gespräch wissen Sie, wie es weitergeht.")}'''
    return seite("Müller &amp; Ströbel – Über uns (Entwurf Business Story 2.0)", "Entwurf: Über uns zur Business Story 2.0", "bs2-ueber", "Über uns", main)


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
            ("11", "Was am Ende anders ist, konkret", "teil", "Entscheiden und steuern statt Mangel verwalten")]),
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
    "11": ["„Du verwaltest keinen Mangel mehr.“", "„Du bekommst Themen so aufbereitet, dass du damit arbeiten kannst, du entscheidest und steuerst, und die Ergebnisse kommen.“",
           "Management macht wieder Spaß: permanent Themen zugeliefert, über die man entscheiden kann.", "„Einmal mit Profis arbeiten.“"],
}
# Verdichtung: der Satz für den Leser je Frage (Entwurf, gestrichelt bis zur Freigabe)
VERDICHTUNG = {
    "1": "Für Führungskräfte in der Versicherungsbranche.",
    "2": "Sie müssen alles im Blick haben. Und am Ende zählt nur das Ergebnis.",
    "3": "Ob eigenes Team oder Externe: Das Ergebnis kommt nicht so zurück, wie Sie es brauchen. Sie greifen doch wieder selbst ein. Und nach dem großen Workshop tut sich wochenlang nichts.",
    "4": "Wir verstehen Sie, strukturieren das Thema, sorgen für die Abarbeitung und liefern das Ergebnis. Und belasten Sie dabei nur minimal.",
    "5": "Aus eigener Erfahrung: Wir haben eine Führungskraft genau so begleitet. Mitgedacht, die Bearbeitung übernommen und dort selbst angepackt, wo wir die Fachkompetenz hatten.",
    "6": "Wir bleiben regelmäßig und kurz im Austausch, oft reicht ein Telefonat. So bleibt Ihr Thema präsent, und Sie haben es im Griff. Dazwischen arbeiten wir und kommen mit Optionen und Entwürfen zurück, über die Sie entscheiden.",
    "7": "Sie verwalten keinen Mangel mehr. Sie entscheiden und steuern, und die Ergebnisse kommen.",
    "8": "Rufen Sie an. Schon das erste Gespräch schafft Klarheit. Kein Pitch, keine Rechnung.",
}
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
    ]),
    ("weiss", [
        ("A", [("H2", "Wir arbeiten. Sie entscheiden.", "Punkte 9, 10"),
               ("Text", "Wir bleiben im regelmäßigen, kurzen Austausch, oft reicht ein Telefonat. Danach liegen Optionen, Entwürfe und Entscheidungsvorlagen auf Ihrem Tisch, professionell aufbereitet.", "Punkt 9 · Punkt 10 · Entscheidungsvorlagen: Einsatzgebiet Gremien"),
               ("Element", "Formate je nach Bedarf: kurzes Telefonat · längere Videokonferenz · Workshop, wenn sinnvoll", "Punkt 9"),
               ("Element", "Treppe aus vier Gesprächen: Ideen → Optionen → Entwürfe → Ergebnis", "Punkt 10"),
               ("Element", "Netzwerk: ehemalige Vorstände, Aufsichtsräte, IT- und Prozess-Spezialisten, Entwickler, Grafiker", "Netzwerk-Hinweis")]),
        ("B", [("H2", "Zwischen zwei Telefonaten entstehen Konzept, Analyse und Entscheidungsvorlage.", "Punkt 10 · Ausarbeitung 3.3"),
               ("Text", "Wir sprechen mit Ihren Leuten, arbeiten selbst mit und holen Spezialisten aus unserem Netzwerk dazu. Mit Ihnen bleiben wir im regelmäßigen, kurzen Austausch: So bleibt das Thema präsent, und Sie haben es im Griff.", "Ausarbeitung 3.2, 3.3 · Punkt 9"),
               ("Element", "Treppe aus vier Gesprächen · Formate: Telefonat, Videokonferenz, Workshop, wenn sinnvoll", "Punkte 9, 10"),
               ("Kasten", "Aus eigener Erfahrung: Ein Geschäftsführer konnte mit uns über jedes Thema sprechen. Wir haben die Projekte übernommen, mit den Leuten gesprochen und selbst angepackt.", "Punkt 8, Fall HÖV, ohne Namen")]),
    ]),
    ("navy", [
        ("A", [("H2", "Sie verwalten keinen Mangel mehr. Sie entscheiden über fertige Vorlagen.", "Punkt 11"),
               ("Text", "Themen kommen so aufbereitet auf Ihren Tisch, dass Sie damit arbeiten können.", "Punkt 11"),
               ("Kasten", "Das erste Gespräch: Sie erzählen, was ansteht. Wir sagen offen, ob und wie wir es umsetzen, und geben direkt unsere Meinung. Kein Pitch, keine Rechnung.", "Punkt 12"),
               ("Element", "Tobias und Daniel mit Telefon, Mail, LinkedIn", "Punkt 12")]),
        ("B", [("H2", "„Einmal mit Profis arbeiten.“", "Punkt 11, Aussage 27"),
               ("Text", "Sie entscheiden über Vorlagen, Zielbild und Fahrplan und sehen, wie es vorangeht.", "Punkt 11 · Zielbild: Grundstory"),
               ("Kasten", "Das erste Gespräch schafft Klarheit. Kein Pitch, keine Rechnung.", "Punkt 12"),
               ("Element", "Tobias und Daniel mit Telefon, Mail, LinkedIn", "Punkt 12")]),
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
        art, varianten = SKIZZE[i - 1]
        skizze = ""
        for v, teile in varianten:
            zeilen_sk = "".join(f'<div class="sk-teil sk-teil--{t.lower()}"><em>{t}</em><p>{x}</p><span>{q}</span></div>' for t, x, q in teile)
            skizze += f'<div class="sk-var"><b class="sk-var__kopf">Fassung {v}</b>{zeilen_sk}</div>'
        baum += (f'<div class="sb-t-gruppe"><div class="sb-t-zeilen">{zeilen}</div>'
                 f'<div class="sb-t-abschnitt"><span>0{i}</span><b>{abschnitt}</b><p>{wirkung}</p></div>'
                 f'<div class="sk sk--{art}"><div class="sk__kopf">Abschnitt {i} · {abschnitt}</div><div class="sk__vars">{skizze}</div></div></div>\n')

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
    <div class="sb-mock__a sb-mock__a--3"><span class="sb-tag sb-tag--h">F6 · Ablauf</span><b class="sb-bar sb-bar--h2"></b><div class="sb-treppe"><i></i><i></i><i></i><i></i></div><span class="sb-tag sb-tag--h">F5 · Beleg</span></div>
    <div class="sb-mock__a sb-mock__a--4"><span class="sb-tag">F7 · Ergebnis</span><b class="sb-bar sb-bar--h2"></b><em class="sb-kreise sb-kreise--klein"><i></i><i></i></em><span class="sb-knopf">F8 · Anrufen</span></div>
  </div>
</div></section>"""
    html = seite("Müller &amp; Ströbel – Storyboard Business Story 2.0", "Storyboard: von den Antworten zur Landingpage", "bs2-story", "", main)
    return html.replace("</head>", f'<link rel="stylesheet" href="/entwicklung/storyboard.css?v={VERSION}">\n</head>', 1)

if __name__ == "__main__":
    (ZIEL / "business-story-2.html").write_text(startseite(), encoding="utf-8")
    (ZIEL / "business-story-2-ueber-uns.html").write_text(ueber_uns(), encoding="utf-8")
    (ZIEL / "storyboard.html").write_text(storyboard(), encoding="utf-8")
    print("gebaut: business-story-2.html, business-story-2-ueber-uns.html, storyboard.html")
