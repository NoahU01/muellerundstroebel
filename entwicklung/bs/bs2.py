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
VERSION = 7

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
    links = [(f"{start}#themen", "Themen"), (f"{start}#vorteile", "Was Sie bekommen"),
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
def startseite():
    duo = "".join(f'<figure><div class="kreis"><img src="/assets/{k}-portrait.webp" alt="{p["name"]}"></div><figcaption><b>{p["name"]}</b>{p["kurz"]}</figcaption></figure>'
                  for k, p in PERSONEN.items())
    themen = "".join(f'<button class="thema" type="button" data-thema="{k}"><span class="thema__ico">{icon(k)}</span><b>{n}</b><span class="thema__wenn">{w}</span><span class="thema__mehr">Was wir konkret tun <svg class="ico" aria-hidden="true"><use href="#i-weiter"/></svg></span></button>'
                     for k, n, w in THEMEN)
    vorlagen = "".join(f'<template id="t-{k}">{thema_detail(k)}</template>' for k, _, _ in THEMEN)
    netz = "".join(f"<span>{n}</span>" for n in ["Ihre Fachbereiche"] + NETZWERK)
    main = f'''
<!-- 1 Kopf: der Leser und sein Problem -->
<section class="held"><div class="wrap held__raster">
  <div>
    <p class="kicker">Für Führungskräfte in Versicherungsunternehmen</p>
    <div class="wahl" data-gruppe="kopf"><span>Überschrift</span><button type="button" aria-pressed="true">1</button><button type="button" aria-pressed="false">2</button><button type="button" aria-pressed="false">3</button></div>
    <h1 data-gruppe="kopf" data-variante="1">Zu viele wichtige Themen. Zu wenig Zeit, sie voranzubringen.</h1>
    <h1 data-gruppe="kopf" data-variante="2" hidden>Geben Sie uns Ihr Thema. Und die Verantwortung dafür.</h1>
    <h1 data-gruppe="kopf" data-variante="3" hidden>Sie entscheiden. Wir bringen Ihre Themen ins Ziel.</h1>
    <p class="lead">Wir übernehmen Ihr Thema samt Verantwortung, bringen es auf den Punkt und treiben es voran, bis das Ergebnis steht. Sie entscheiden.</p>
    <div class="knoepfe"><a class="knopf" href="#kontakt">Thema besprechen <svg class="ico" aria-hidden="true"><use href="#i-weiter"/></svg></a><a class="knopf knopf--rand" href="#themen">Für welche Themen?</a></div>
  </div>
  <div class="duo">{duo}</div>
</div></section>

<!-- 2 Wiedererkennen: Schmerz + typische Themen -->
<section class="sek sek--sand" id="themen"><div class="wrap">
  <div class="kopfteil">
    <p class="kicker">Kennen Sie das?</p>
    <h2 class="h2">„Es ging schon wieder nichts voran.“</h2>
    <p class="lead">Ein Thema ist komplex, viele sind beteiligt, der Kern ist unklar. Wochen vergehen, und am Ende landet es wieder bei Ihnen. Mit diesen Themen holen Führungskräfte uns dazu:</p>
  </div>
  <div class="themen">{themen}</div>
</div></section>

<!-- 3 Was Sie bekommen: drei Vorteile, je mit Bild -->
<section class="sek" id="vorteile"><div class="wrap">
  <div class="kopfteil">
    <p class="kicker">Was Sie bekommen</p>
    <h2 class="h2">Sobald wir übernehmen, ändert sich für Sie dreierlei.</h2>
  </div>

  <div class="vorteil">
    <div class="vorteil__text"><span class="vorteil__nr">1</span><h3>Sie haben sofort Klarheit.</h3>
      <p>Sie müssen nichts vorbereiten. Wir fragen gezielt nach und bringen Ihr Thema auf eine Seite: Zielbild, Stand, nächste Entscheidung. Die Verantwortung für diese Klarheit liegt bei uns.</p></div>
    <div class="board" aria-label="Beispiel: ein Thema auf einer Seite">
      <div class="board__kopf"><span>Ihr Thema auf einer Seite</span><em>Beispiel</em></div>
      <div class="board__ziel"><small>Zielbild</small><b>Neue Vertriebssteuerung, beschlussreif zum Führungskreis im November</b></div>
      <p class="board__label">Wo wir stehen</p>
      <ol class="fahrplan"><li>Thema geklärt</li><li>Zielbild steht</li><li class="jetzt">Optionen bewertet</li><li class="offen">Beschluss</li><li class="offen">Umsetzung</li></ol>
      <div class="board__entscheid"><p><b>Ihre nächste Entscheidung:</b> Variante B oder C</p><span>Vorlage liegt bei</span></div>
    </div>
  </div>

  <div class="vorteil vorteil--rechts">
    <div class="vorteil__text"><span class="vorteil__nr">2</span><h3>Sie investieren 30 Minuten statt zwei Workshop-Tage.</h3>
      <p>Ein Telefonat, wenn es in Ihren Kalender passt, gern auch aus dem Auto. Dazwischen arbeiten wir. Jedes Gespräch setzt eine Stufe höher an, und Sie entscheiden direkt.</p></div>
    <ol class="takt" aria-label="Ablauf in kurzen Gesprächen">
      <li><span><svg class="ico" aria-hidden="true"><use href="#i-uhr"/></svg>30 Min.</span><b>Sie schildern das Thema.</b></li>
      <li><span><svg class="ico" aria-hidden="true"><use href="#i-uhr"/></svg>30 Min.</span><b>Sie legen die Richtung fest.</b></li>
      <li><span><svg class="ico" aria-hidden="true"><use href="#i-uhr"/></svg>30 Min.</span><b>Sie entscheiden.</b></li>
      <li><span><svg class="ico" aria-hidden="true"><use href="#i-uhr"/></svg>30 Min.</span><b>Sie geben frei.</b></li>
    </ol>
  </div>

  <div class="vorteil">
    <div class="vorteil__text"><span class="vorteil__nr">3</span><h3>Sie koordinieren niemanden mehr.</h3>
      <p>Wir steuern das Projekt, sprechen mit Ihren Leuten und schreiben Konzepte und Vorlagen selbst. Wo Spezialwissen fehlt, holen wir es aus unserem Netzwerk. Sie haben einen Ansprechpartner.</p></div>
    <div class="buendel" aria-label="Sie haben einen Ansprechpartner, wir koordinieren alle Beteiligten">
      <span class="buendel__sie">Sie</span>
      <span class="buendel__wir"><span>Müller <i>&amp;</i> Ströbel</span><small>Ihr einziger Ansprechpartner</small></span>
      <div class="buendel__netz">{netz}</div>
    </div>
  </div>
</div></section>

<!-- 4 Ergebnis -->
<section class="sek sek--navy"><div class="wrap ergebnis">
  <div>
    <p class="kicker">Ihr Ergebnis</p>
    <h2 class="h2">Sie verwalten keinen Mangel mehr. Sie entscheiden und steuern.</h2>
  </div>
  <ul class="ergebnis__liste">
    <li><svg aria-hidden="true"><use href="#i-haken"/></svg>Themen kommen entscheidungsreif auf Ihren Tisch.</li>
    <li><svg aria-hidden="true"><use href="#i-haken"/></svg>Ihre Vorhaben laufen weiter, während Sie im Tagesgeschäft sind.</li>
    <li><svg aria-hidden="true"><use href="#i-haken"/></svg>Sie sehen Ergebnisse. Und Führung macht wieder Spaß.</li>
  </ul>
</div></section>

{kontakt("Sie geben uns ein Thema und die Verantwortung dafür. Wir liefern das Ergebnis.", "Rufen Sie einen von uns direkt an. Nach dem ersten Gespräch wissen Sie, wie es weitergeht.")}

<dialog class="fenster" id="fenster" aria-labelledby="fenster-titel"><div class="fenster__inhalt"></div><button class="fenster__zu" type="button" aria-label="Schließen"><svg class="ico" aria-hidden="true"><use href="#i-zu"/></svg></button></dialog>
{vorlagen}'''
    skript = '''<script>
/* Variantenwahl (nur Entwurf) */
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
/* Zweite Ebene: Einsatzgebiet im Fenster */
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
</script>'''
    return seite("Müller &amp; Ströbel – Business Story 2.0 (Entwurf)", "Entwurf der Startseite: Business Story 2.0", "bs2", "", main, skript)


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
            ("1", "Welche Rollen genau", "offen", ""),
            ("2", "Welche Unternehmen genau", "offen", "")]),
        ("4", "Was ist eure Antwort?", [
            ("7", "Das Versprechen im Wortlaut", "da", "Sie geben uns ein Thema und die Verantwortung dafür. Wir liefern das Ergebnis.")]),
    ]),
    ("Ihre Lage", "Der Leser nickt: Genau so ist es bei mir, und darum hat es bisher nicht geklappt.", [
        ("2", "Verstehen die mein Problem?", [
            ("3", "Der Moment, in dem man euch anruft", "offen", ""),
            ("4", "Das Problem in einem Satz", "teil", "Es ging schon wieder nichts voran.")]),
        ("3", "Warum hat das bisher keiner gelöst?", [
            ("5", "Was die Person vorher probiert hat", "offen", ""),
            ("6", "Warum das nicht gereicht hat", "offen", "")]),
    ]),
    ("So arbeiten wir", "Der Leser glaubt es und sieht, wie wenig Aufwand es ihn kostet.", [
        ("5", "Warum soll ich euch das glauben?", [
            ("8", "Der eine Beleg, der euch glaubwürdig macht", "teil", "Die Zusammenarbeit beim HÖV")]),
        ("6", "Wie läuft das ab, und was kostet es mich?", [
            ("9", "Der Zeitaufwand für den Kunden, konkret", "da", "30 Minuten am Telefon, gern aus dem Auto"),
            ("10", "Was ihr zwischen den Gesprächen liefert", "teil", "Ideen, Optionen, Entwürfe")]),
    ]),
    ("Ergebnis + Kontakt", "Der Leser weiß, was er davon hat, und greift zum Telefon.", [
        ("7", "Was habe ich am Ende davon?", [
            ("11", "Was am Ende anders ist, konkret", "teil", "Entscheiden und steuern statt Mangel verwalten")]),
        ("8", "Was ist der nächste Schritt?", [
            ("12", "Was im ersten Anruf passiert", "offen", "")]),
    ]),
]
STATUS = {"da": "vorhanden", "teil": "teilweise", "offen": "offen"}
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
        return f'<li class="sb-p sb-p--{st}"><i aria-label="{STATUS[st]}"></i><div><small>Punkt {nr}</small><b>{txt}</b>{q}</div></li>'

    baum = ""
    for i, (abschnitt, wirkung, fragen) in enumerate(STORY, 1):
        zeilen = ""
        for fnr, frage, punkte in fragen:
            pk = "".join(punkt(*p) for p in punkte)
            zeilen += (f'<div class="sb-t-zeile"><ul class="sb-t-punkte">{pk}</ul>'
                       f'<div class="sb-t-frage"><span class="sb-f">F{fnr}</span><b>{frage}</b></div></div>')
        baum += (f'<div class="sb-t-gruppe"><div class="sb-t-zeilen">{zeilen}</div>'
                 f'<div class="sb-t-abschnitt"><span>0{i}</span><b>{abschnitt}</b><p>{wirkung}</p></div></div>\n')

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
  <p class="lead">Sie beantworten enge Punkte. Daraus werden die Antworten auf die Fragen, die sich der Leser stellt. Und daraus die Seite.</p>
  <ol class="sb-weg">
    <li><span class="sb-weg__ico"><svg class="ico"><use href="#s-antwort"/></svg></span><b>12 Punkte</b><h2>Ihre Antworten</h2><p>Enge Fragen, je eine klare Antwort.</p></li>
    <li class="sb-weg__pfeil" aria-hidden="true"><svg class="ico"><use href="#s-pfeil"/></svg></li>
    <li><span class="sb-weg__ico"><svg class="ico"><use href="#s-leser"/></svg></span><b>8 Fragen</b><h2>Die Gedanken des Lesers</h2><p>In der Reihenfolge, in der er sie sich stellt.</p></li>
    <li class="sb-weg__pfeil" aria-hidden="true"><svg class="ico"><use href="#s-pfeil"/></svg></li>
    <li class="sb-weg--ziel"><span class="sb-weg__ico"><svg class="ico"><use href="#s-seite"/></svg></span><b>4 Abschnitte</b><h2>Die Landingpage</h2><p>Je zwei Fragen ergeben einen Abschnitt.</p></li>
  </ol>
</div></section>

<section class="sek sek--sand"><div class="wrap">
  <div class="sb-titel"><div><p class="kicker">Zuordnung</p><h2 class="h2">Jeder Punkt hat genau einen Platz.</h2></div>
    <ul class="sb-legende"><li class="sb-p--da"><i></i>vorhanden</li><li class="sb-p--teil"><i></i>teilweise</li><li class="sb-p--offen"><i></i>offen</li></ul></div>
  <div class="sb-t-kopf"><span><i>1</i>Ihre Antworten<small>12 Punkte</small></span><span><i>2</i>Fragen des Lesers<small>8 Fragen</small></span><span><i>3</i>Landingpage<small>4 Abschnitte</small></span></div>
  <div class="sb-t">{baum}</div>
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
