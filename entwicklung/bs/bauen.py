#!/usr/bin/env python3
"""Baut die Entwicklungs-Variante „Business Story“ (nur Branch daniel – Ordner entwicklung/ geht nie auf main).

Seiten: entwicklung/business-story.html (Startseite), bs-ueber-uns.html, bs-steckbrief-tobias.html, bs-steckbrief-daniel.html.
Grundlage: Daniels Ausarbeitung „Die zentrale Story unseres Geschäftsmodells“ (09.10.2026).
Rahmen (Kopf, Menü, Fuß, Skripte) kommt unverändert aus ueber-uns.html; Gestaltung in entwicklung/business-story.css.

    python3 entwicklung/bs/bauen.py
"""
import re
from pathlib import Path

WURZEL = Path(__file__).resolve().parents[2]
ZIEL = WURZEL / "entwicklung"
CSS = '<link rel="stylesheet" href="/entwicklung/business-story.css">'
AKTIV = ' aria-current="page"'
PF = '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>'
MAIL_BEIDE = "mailto:daniel@muellerundstroebel.de,tobias@muellerundstroebel.de?subject=Thema%20besprechen"

PERSONEN = {
    "tobias": dict(
        name="Tobias Müller", rolle="Governance, Gremien &amp; Risiko", bild="/assets/tobias-kreis.webp",
        mail="tobias@muellerundstroebel.de", tel="+49 176 2152 9798", tel_roh="+4917621529798",
        linkedin="https://www.linkedin.com/in/tobias-m%C3%BCller-b5606b24/",
        kurz="Aus der Rückversicherung, heute Aufsichtsrat in zwei Versicherungsvereinen.",
        fakt=("2", "Aufsichtsratsmandate in Versicherungsunternehmen"),
        fakt2=("12+", "Jahre eigene Beratung für Versicherer und Rückversicherer"),
        warum=[
            ("Er kennt die Gremienlogik von innen.", "Als Aufsichtsrat und ehemaliger Geschäftsführer weiß er, wie Entscheidungen vorbereitet werden müssen, damit Vorstand und Aufsichtsrat entscheiden können."),
            ("Er führt Themen zum Ergebnis.", "Als Geschäftsführer des HÖV hat er selbst erlebt, wie viele Themen gleichzeitig auf dem Tisch einer Führungskraft liegen – und was es braucht, damit sie vorankommen."),
            ("Er denkt in Risiko und Rechnungslegung.", "Aus Underwriting und Rückversicherung bringt er den Blick für Risiken, Kennzahlen und tragfähige Strukturen mit."),
        ],
        schwerpunkte=["Governance &amp; Gremienlogik", "Aufsichtsrats- &amp; Vorstandssicht", "Risiko &amp; Rechnungslegung"],
        werdegang="Tobias Müller kommt aus der Rückversicherung: Nach Stationen bei SCOR und als Underwriter bei Hannover Re führte er über zwölf Jahre die Müller Unternehmensberatung für Versicherer und Rückversicherer. Heute ist er Mitglied der Aufsichtsräte von Gartenbau-Versicherung und Grundeigentümer-Versicherung.",
    ),
    "daniel": dict(
        name="Daniel Ströbel", rolle="Strategie, Führung &amp; Vertrieb", bild="/assets/daniel-kreis.webp",
        mail="daniel@muellerundstroebel.de", tel="+49 176 3134 7217", tel_roh="+4917631347217",
        linkedin="https://www.linkedin.com/in/daniel-stroebel/",
        kurz="Konzernstrategie bei einem Versicherer, seit 2012 über 300 Projekte für die Branche.",
        fakt=("300+", "Projekte für die Versicherungsbranche"),
        fakt2=("40", "Mitarbeitende in seiner früheren Abteilung"),
        warum=[
            ("Er denkt auf Vorstandsebene mit.", "Aus Konzernstrategie, Konzernsteuerung und Risikomanagement kennt er die Fragen, die Führungskräfte in Versicherungsunternehmen wirklich beschäftigen."),
            ("Er organisiert die Bearbeitung.", "Er strukturiert komplexe Themen, spricht mit den Beteiligten, behält Projekte im Blick und sorgt dafür, dass aus einer Entscheidung ein Ergebnis wird."),
            ("Er packt selbst mit an.", "Wo er die fachliche Tiefe hat – Strategie, Geschäftsmodell, Vertrieb, Kommunikation –, erarbeitet er Konzepte und Ergebnisse selbst."),
        ],
        schwerpunkte=["Strategie &amp; Geschäftsmodell", "Struktur &amp; Führung", "Vertrieb &amp; Stakeholderfokus"],
        werdegang="Daniel Ströbel verantwortete bei der SV SparkassenVersicherung Konzernstrategie und Risikomanagement, baute das Inhouse-Consulting Leben auf und leitete eine Abteilung mit rund 40 Mitarbeitenden. Seit 2012 führt er die empiria GmbH – mit über 300 Projekten für die Versicherungsbranche.",
    ),
}

THEMEN = [
    ("Strategie &amp; Geschäftsmodell", "Wenn die Richtung klar sein muss – und im Alltag ankommen soll."),
    ("Kennzahlen &amp; Steuerung", "Wenn Zahlen da sind, aber nicht steuern."),
    ("Entscheidungen &amp; Gremien", "Wenn Themen seit Monaten „in Bearbeitung“ sind."),
    ("Vertrieb &amp; Wachstum", "Wenn Potenziale im Markt liegen bleiben."),
    ("KI-Transformation", "Wenn KI das Geschäftsmodell verändern soll, nicht nur Prozesse."),
    ("Resilienz", "Wenn Unsicherheit zur dauerhaften Managementaufgabe wird."),
]
NETZWERK = ["IT-Spezialisten", "Prozess-Spezialisten", "Ehemalige Vorstände", "Aufsichtsratsmitglieder", "Marketingexperten", "Programmierer", "Grafiker"]


def cv(name):
    t = (WURZEL / "ueber-uns.html").read_text(encoding="utf-8")
    return re.search(rf'<template id="m-cv-{name}">.*?(<ol class="v-cv">.*?</ol>)</template>', t, re.S).group(1)


def rahmen(titel, beschreibung, main, aktiv):
    t = (WURZEL / "ueber-uns.html").read_text(encoding="utf-8")
    kopf = t[:t.index("<main>")]
    fuss = t[t.index("</main>") + 7:]
    kopf = re.sub(r"<title>.*?</title>", f"<title>{titel}</title>", kopf, 1, flags=re.S)
    kopf = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{beschreibung}">', kopf, 1)
    kopf = kopf.replace('<meta name="robots" content="index', '<meta name="robots" content="noindex')
    kopf = kopf.replace("</head>", CSS + "\n</head>", 1)
    nav = [("business-story.html", "Startseite"), ("bs-ueber-uns.html", "Über uns &amp; Themen"),
           ("bs-steckbrief-tobias.html", "Steckbrief Tobias"), ("bs-steckbrief-daniel.html", "Steckbrief Daniel")]
    leiste = ('<div class="bs-dev"><div class="bs-wrap"><span>Entwurf Business Story</span><nav>' +
              "".join(f'<a href="/entwicklung/{h}"{AKTIV if h == aktiv else ""}>{n}</a>' for h, n in nav) + "</nav></div></div>")
    return kopf + "<main class=\"bs\">\n" + leiste + main + "\n</main>" + fuss


def kopf(k, h, sub=None, hell=False, mitte=False):
    return (f'<div class="bs-kopf{" bs-kopf--mitte" if mitte else ""}"><p class="bs-kicker{" bs-kicker--hell" if hell else ""}">{k}</p><h2 class="bs-h2">{h}</h2>' +
            (f'<p class="bs-sub">{sub}</p>' if sub else "") + "</div>")


AMP = '<img class="bs-amp" src="/pdf/bausteine/ampersand-konstruktion.svg" alt="" aria-hidden="true">'
PORTRAIT = {"tobias": "/assets/tobias-portrait.webp", "daniel": "/assets/daniel-portrait.webp"}


def portraitkarte(key, klein=False):
    """Person als Karte: farbige Fläche, freigestelltes Porträt steht auf der Unterkante, Name als Etikett."""
    p = PERSONEN[key]
    return (f'<figure class="bs-pk bs-pk--{key}{" bs-pk--klein" if klein else ""}"><img src="{PORTRAIT[key]}" alt="{p["name"]}">'
            f'<figcaption><b>{p["name"]}</b><span>{p["rolle"]}</span></figcaption></figure>')


def duo():
    return f'<div class="bs-duo">{portraitkarte("tobias")}{portraitkarte("daniel")}</div>'


def team_reihe(mit_netz=False):
    return f'<div class="bs-duo bs-duo--reihe">{portraitkarte("tobias")}{portraitkarte("daniel")}</div>'


def orbit(klein=False):
    n = len(NETZWERK); import math
    r = 150; cx = cy = 210
    punkte = ""
    for i, name in enumerate(NETZWERK):
        w = -math.pi / 2 + 2 * math.pi * i / n
        x, y = cx + r * math.cos(w), cy + r * math.sin(w)
        anker = "middle" if abs(math.cos(w)) < .3 else ("start" if math.cos(w) > 0 else "end")
        dx = 0 if anker == "middle" else (14 if anker == "start" else -14)
        dy = -16 if math.sin(w) < -.5 else (26 if math.sin(w) > .5 else 5)
        punkte += f'<line x1="{cx}" y1="{cy}" x2="{x:.0f}" y2="{y:.0f}" class="o-l"/><circle cx="{x:.0f}" cy="{y:.0f}" r="7" class="o-p"/>'
        if not klein:
            punkte += f'<text x="{x+dx:.0f}" y="{y+dy:.0f}" text-anchor="{anker}" class="o-t">{name}</text>'
    return (f'<svg class="bs-orbit{" bs-orbit--klein" if klein else ""}" viewBox="{"-60 0 540 420" if not klein else "40 40 340 340"}" role="img" aria-label="Netzwerk">'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" class="o-k"/>{punkte}<circle cx="{cx}" cy="{cy}" r="52" class="o-m"/>'
            f'<text x="{cx}" y="{cy+15}" text-anchor="middle" class="o-amp">&amp;</text></svg>')


def abschluss():
    kontakte = "".join(f'<div class="bs-ruf"><img src="{PERSONEN[k]["bild"]}" alt=""><div><b>{PERSONEN[k]["name"]}</b>'
                       f'<a href="tel:{PERSONEN[k]["tel_roh"]}">{PERSONEN[k]["tel"]}</a><a href="mailto:{PERSONEN[k]["mail"]}">{PERSONEN[k]["mail"]}</a></div></div>' for k in PERSONEN)
    return f'''<section class="bs-sek bs-schluss"><div class="bs-wrap bs-zwei bs-zwei--mitte">
  <div>{kopf("Ihr Thema", 'Welches Thema liegt gerade auf Ihrem Tisch<span class="bs-dot">?</span>', "Rufen Sie an oder schreiben Sie uns. Wir sagen Ihnen offen, ob und wie wir es übernehmen.")}
    <div class="bs-knoepfe"><a class="bs-knopf" href="{MAIL_BEIDE}">Thema besprechen {PF}</a></div></div>
  <div class="bs-rufe">{kontakte}</div>
</div></section>'''


# ---------------------------------------------------------------- Startseite
def startseite():
    m = [f'''<section class="bs-held"><div class="bs-wrap bs-held__raster">
  <div>
    <p class="bs-kicker">Für Führungskräfte in Versicherungsunternehmen</p>
    <h1 class="bs-h1">Sie geben uns ein Thema. Wir sorgen dafür, dass daraus ein Ergebnis wird<span class="bs-dot">.</span></h1>
    <p class="bs-lead">Wir denken auf Augenhöhe mit, organisieren die Bearbeitung und packen selbst mit an. Sie müssen nichts koordinieren.</p>
    <div class="bs-knoepfe"><a class="bs-knopf" href="{MAIL_BEIDE}">Thema besprechen {PF}</a><a class="bs-knopf bs-knopf--rand" href="#loesung">So arbeiten wir</a></div>
  </div>
  {duo()}
</div></section>''',
         '''<section class="bs-sek bs-sand"><div class="bs-wrap bs-zwei">
  <div><p class="bs-kicker">Kennen Sie das?</p>
    <h2 class="bs-h2">Viele wichtige Themen. Und alle liegen bei Ihnen<span class="bs-dot">.</span></h2>
    <p class="bs-text">Sie wissen meist genau, was wichtig ist. Aber Strategie, Entscheidungen, Projekte und Tagesgeschäft laufen gleichzeitig. Für vieles fehlt schlicht die Zeit, die Kapazität oder die passende Kompetenz.</p>
    <p class="bs-fazit">Unterschiedliche Ebene, gleiches Problem.</p></div>
  <div class="bs-stimmen">
    <blockquote><span>Vorstand</span>„Ich muss den Aufsichtsrat vorbereiten, Entscheidungen treffen und meine Bereiche koordinieren.“</blockquote>
    <blockquote><span>Hauptabteilungsleitung</span>„Ich soll Vorgaben umsetzen, Abteilungen abstimmen und Ergebnisse liefern.“</blockquote>
    <blockquote><span>Bereichsleitung</span>„Ich stimme mich mit dem Vorstand ab, führe meine Teams und treibe zig Themen voran.“</blockquote>
  </div>
</div></section>''',
         '''<section class="bs-sek"><div class="bs-wrap bs-zwei bs-zwei--mitte">
  <div><p class="bs-kicker">Warum Beratung allein nicht reicht</p>
    <h2 class="bs-h2">Ein Berater gibt Ihnen Empfehlungen. Die Arbeit bleibt bei Ihnen<span class="bs-dot">.</span></h2>
    <p class="bs-text">Sie können einen Strategieberater holen, einen Projektmanager und Spezialisten. Dann müssen Sie trotzdem alles zusammenbringen, die Beteiligten koordinieren und dranbleiben, bis ein Ergebnis da ist.</p>
    <p class="bs-fazit">Genau diese Last nehmen wir Ihnen ab.</p></div>
  <div class="bs-gegen">
    <figure><figcaption>Üblich</figcaption>
      <svg viewBox="0 0 360 300" class="bs-diag" role="img" aria-label="Drei Dienstleister, die Koordination bleibt bei Ihnen">
        <path d="M60 70 C60 150 180 140 180 220M180 70V220M300 70C300 150 180 140 180 220" class="d-l"/>
        <g class="d-n"><circle cx="60" cy="54" r="34"/><circle cx="180" cy="54" r="34"/><circle cx="300" cy="54" r="34"/></g>
        <g class="d-t"><text x="60" y="58">Berater</text><text x="180" y="58">Projekt</text><text x="300" y="58">Spezialist</text></g>
        <circle cx="180" cy="236" r="42" class="d-sie"/><text x="180" y="242" class="d-t2">Sie</text>
      </svg></figure>
    <figure class="bs-gegen--wir"><figcaption>Mit Müller &amp; Ströbel</figcaption>
      <svg viewBox="0 0 360 300" class="bs-diag" role="img" aria-label="Ein Partner, ein Ergebnis">
        <path d="M180 120V196" class="d-l d-l--wir"/>
        <circle cx="180" cy="66" r="56" class="d-wir"/><text x="180" y="86" class="d-amp">&amp;</text>
        <circle cx="180" cy="236" r="42" class="d-erg"/><text x="180" y="242" class="d-t2 d-t2--hell">Ergebnis</text>
      </svg></figure>
  </div>
</div></section>''',
         '''<section class="bs-sek bs-sand" id="loesung"><div class="bs-wrap">
  <div class="bs-kopf"><p class="bs-kicker">So lösen wir es</p><h2 class="bs-h2">Mitdenken. Organisieren. Selber machen<span class="bs-dot">.</span></h2></div>
  <div class="bs-trio">
    <div><span>01</span><b>Mitdenken</b><p>Wir verstehen, wie Versicherungsunternehmen funktionieren, und denken auf Ihrer Ebene mit. Wir ordnen Ihr Thema ein, entwickeln Optionen und bereiten Entscheidungen vor. Und wir sagen offen, wo wir selbst nicht tief genug drin sind.</p></div>
    <div><span>02</span><b>Organisieren</b><p>Nach dem Gespräch lassen wir Sie nicht mit einer Liste allein. Wir sprechen mit den Beteiligten, setzen Prioritäten, halten Projekte am Laufen und legen Ihnen vor, was Sie entscheiden müssen.</p></div>
    <div><span>03</span><b>Selber machen</b><p>Wo wir die Fachkompetenz haben, arbeiten wir selbst mit: Konzepte, Analysen, Lösungen. Wo es mehr braucht, holen wir passende Spezialisten aus unserem Netzwerk dazu.</p></div>
  </div>
  <p class="bs-satz">Das Besondere ist nicht eine dieser Leistungen, sondern dass Sie alle drei aus einer Hand bekommen.</p>
</div></section>''',
         '''<section class="bs-sek"><div class="bs-wrap">
  <div class="bs-kopf"><p class="bs-kicker">So gehen wir vor</p><h2 class="bs-h2">Vom ersten Gespräch bis zum Ergebnis<span class="bs-dot">.</span></h2></div>
  <ol class="bs-pfad"><li><b>Zuhören</b><span>Wir klären mit Ihnen, worum es wirklich geht, auch wenn das am Anfang noch offen ist.</span></li><li><b>Vorgehen</b><span>Wir entwickeln gemeinsam, wie wir das Thema angehen.</span></li><li><b>Bearbeiten</b><span>Wir übernehmen die Bearbeitung und halten Sie auf dem Laufenden.</span></li><li><b>Ergebnis</b><span>Sie bekommen ein Ergebnis, mit dem Sie weiterarbeiten können.</span></li></ol>
</div></section>''',
         f'''<section class="bs-sek bs-navy"><div class="bs-wrap bs-zwei">
  <div><p class="bs-kicker bs-kicker--hell">So fühlt sich das an</p>
    <h2 class="bs-h2">Ein Ansprechpartner für jedes Thema<span class="bs-dot">.</span></h2>
    <p class="bs-text bs-text--hell">Sie haben jemanden, mit dem Sie über jedes Thema sprechen können. Sie geben ein Thema ab. Es kommt zu Ihnen zurück, wenn etwas zu entscheiden ist oder wenn es fertig ist. Dazwischen müssen Sie sich um nichts kümmern.</p></div>
  <figure class="bs-beleg">
    <p class="bs-beleg__label">So war es beim HÖV</p>
    <blockquote>„Ich konnte mit dir über jedes Thema sprechen. Du hast verstanden, worum es geht. Wenn du dich fachlich auskanntest, konntest du direkt mitdenken. Wenn du dich nicht auskanntest, hast du das offen gesagt und wusstest trotzdem, wie man das Thema angehen kann.“</blockquote>
    <blockquote>„Du hast das Projektmanagement übernommen. Du hast mit den Leuten gesprochen, die Projekte im Blick behalten und dafür gesorgt, dass die Dinge weiterlaufen. Und dort, wo du die fachliche Kompetenz hattest, hast du selbst mit angepackt.“</blockquote>
    <figcaption><img src="{PERSONEN["tobias"]["bild"]}" alt=""><span><b>Tobias Müller</b>damals Geschäftsführer des HÖV, über die Zusammenarbeit mit Daniel Ströbel</span></figcaption>
  </figure>
</div></section>''',
         f'''<section class="bs-sek"><div class="bs-wrap bs-zwei bs-zwei--mitte">
  <div><p class="bs-kicker">Unser Netzwerk</p>
    <h2 class="bs-h2">Wenn ein Thema mehr braucht<span class="bs-dot">.</span></h2>
    <p class="bs-text">Dann holen wir gezielt die richtigen Leute dazu. Wir steuern sie, und Sie haben weiter einen Ansprechpartner.</p></div>
  <ul class="bs-netz">{"".join(f"<li>{n}</li>" for n in ["IT- und Prozess-Spezialisten", "Ehemalige Vorstände", "Aufsichtsratsmitglieder", "Marketingexperten", "Programmierer", "Grafiker"])}</ul>
</div></section>''',
         f'''<section class="bs-sek bs-sand" id="wir"><div class="bs-wrap">
  <div class="bs-kopf"><p class="bs-kicker">Wer wir sind</p><h2 class="bs-h2">Zwei Partner, die selbst mitarbeiten<span class="bs-dot">.</span></h2></div>
  <div class="bs-wir">{"".join(f'<article>{portraitkarte(k, klein=True)}<div><p class="bs-text">{PERSONEN[k]["werdegang"]}</p><a class="bs-link" href="/entwicklung/bs-steckbrief-{k}.html">Steckbrief von {PERSONEN[k]["name"]} {PF}</a></div></article>' for k in PERSONEN)}</div>
</div></section>''',
         abschluss()]
    return rahmen("Müller & Ströbel – Business Story (Entwurf)", "Entwurf der Startseite auf Basis der Business Story", "\n".join(m), "business-story.html")


# ---------------------------------------------------------------- Über uns
def ueber_uns():
    staerken = [("Auf Augenhöhe", "Wir diskutieren mit Vorstand, Aufsichtsrat und Fachbereich."),
                ("Den Überblick behalten", "Viele Themen und Projekte gleichzeitig im Blick."),
                ("Menschen zusammenbringen", "Wir organisieren die richtigen Leute und Kompetenzen."),
                ("Verantwortung übernehmen", "Wir arbeiten selbst mit – bis das Ergebnis steht.")]
    m = [f'''<section class="bs-held"><div class="bs-wrap bs-held__raster">
  <div><p class="bs-kicker">Über uns</p>
    <h1 class="bs-h1">Erfahrung einer Führungskraft. Ohne eine Stelle zu besetzen<span class="bs-dot">.</span></h1>
    <p class="bs-lead">Wir ersetzen keine Führungskraft. Wir nehmen ihr ein vollständiges Aufgabenpaket ab – ob Vorstand, Hauptabteilungs- oder Bereichsleitung. Entscheidend ist nicht die Stellenbezeichnung, sondern dass ein Thema zum Ergebnis kommt.</p></div>
  {duo()}
</div></section>''',
         f'''<section class="bs-sek"><div class="bs-wrap">
  {kopf("Was Sie bekommen", 'Die Erfahrung langjähriger Führungskräfte<span class="bs-dot">.</span>')}
  <div class="bs-vier">{"".join(f'<div><span>0{i+1}</span><b>{t}</b><p>{x}</p></div>' for i, (t, x) in enumerate(staerken))}</div>
</div></section>''',
         f'''<section class="bs-sek bs-sand bs-sek--team" id="team"><div class="bs-wrap">
  {kopf("Das Team", 'Partner, die selbst mitarbeiten<span class="bs-dot">.</span>')}
  <div class="bs-wir">{"".join(f'<article>{portraitkarte(k, klein=True)}<div><p class="bs-text">{PERSONEN[k]["werdegang"]}</p><a class="bs-link" href="/entwicklung/bs-steckbrief-{k}.html">Steckbrief von {PERSONEN[k]["name"]} {PF}</a></div></article>' for k in PERSONEN)}</div>
  <p class="bs-text" style="margin-top:3rem;max-width:44rem">Dazu kommt unser Netzwerk: IT- und Prozess-Spezialisten, ehemalige Vorstände und Aufsichtsratsmitglieder, Marketingexperten, Programmierer und Grafiker. Wir binden sie gezielt ein und steuern sie für Sie.</p>
</div></section>''',
         f'''<section class="bs-sek" id="themen"><div class="bs-wrap bs-zwei">
  <div>{kopf("Unsere Themenfelder", 'Hier setzen wir an<span class="bs-dot">.</span>', "Wenn Zusammenhänge unklar sind und ein Thema nicht vorankommt.")}</div>
  <ol class="bs-index">{"".join(f'<li><b>{t}</b><span>{w}</span></li>' for t, w in THEMEN)}</ol>
</div></section>''',
         '''<section class="bs-sek bs-sand"><div class="bs-wrap">
  <p class="bs-kicker">Unsere Haltung</p>
  <div class="bs-haltung"><div><b>Umsetzen<i>.</i></b><span>Wir bleiben, bis das Ergebnis steht.</span></div><div><b>Sofort<i>.</i></b><span>Wir müssen nicht abgeholt werden.</span></div><div><b>Überzeugt<i>.</i></b><span>Wir machen nur, woran wir glauben.</span></div></div>
</div></section>''',
         abschluss()]
    return rahmen("Müller & Ströbel – Über uns (Entwurf Business Story)", "Über uns, Team und Themenfelder", "\n".join(m), "bs-ueber-uns.html")


# ---------------------------------------------------------------- Steckbrief
def steckbrief(key):
    p = PERSONEN[key]
    vcf = f"/entwicklung/bs/{key}.vcf"
    vn = p["name"].split()[0]
    m = [f'''<section class="bs-held bs-profil"><div class="bs-wrap bs-profil__raster">
  <div>
    <p class="bs-kicker">Partner · Müller &amp; Ströbel</p>
    <h1 class="bs-h1">{p["name"]}</h1>
    <p class="bs-profil__rolle">{p["rolle"]}</p>
    <p class="bs-profil__kurz">{p["kurz"]}</p>
    <div class="bs-aktionen">
      <a href="tel:{p["tel_roh"]}">Anrufen</a><a href="mailto:{p["mail"]}">E-Mail</a><a href="{p["linkedin"]}" target="_blank" rel="noopener">LinkedIn</a><a href="{vcf}" download class="bs-aktionen__haupt">Kontakt speichern</a>
    </div>
  </div>
  {portraitkarte(key)}
</div></section>''',
         f'''<section class="bs-sek"><div class="bs-wrap">
  {kopf("Warum in Ihrem Projekt", f'Was {vn} einbringt<span class="bs-dot">.</span>')}
  <div class="bs-vier bs-vier--drei">{"".join(f'<div><span>0{i+1}</span><b>{t}</b><p>{x}</p></div>' for i, (t, x) in enumerate(p["warum"]))}</div>
  <div class="bs-zahlen"><div><b>{p["fakt"][0]}</b><span>{p["fakt"][1]}</span></div><div><b>{p["fakt2"][0]}</b><span>{p["fakt2"][1]}</span></div></div>
</div></section>''',
         f'''<section class="bs-sek bs-sand"><div class="bs-wrap bs-zwei">
  <div>{kopf("Schwerpunkte", 'Kompetenzen<span class="bs-dot">.</span>')}
    <ul class="bs-kompetenzen">{"".join(f"<li>{x}</li>" for x in p["schwerpunkte"])}</ul>
    <p class="bs-kicker" style="margin-top:3rem">Im Projekt</p>
    <p class="bs-rollen"><span>Mitdenken</span><span>Organisieren</span><span>Selber machen</span></p></div>
  <div>{kopf("Werdegang", 'Stationen<span class="bs-dot">.</span>')}<div class="bs-cv">{cv(key)}</div></div>
</div></section>''',
         abschluss()]
    return rahmen(f"{p['name']} – Steckbrief · Müller & Ströbel (Entwurf)", f"Beraterprofil {p['name']}", "\n".join(m), f"bs-steckbrief-{key}.html")


def vcard(key):
    p = PERSONEN[key]
    vn, nn = p["name"].split(" ", 1)
    return ("BEGIN:VCARD\r\nVERSION:3.0\r\n" f"N:{nn};{vn};;;\r\nFN:{p['name']}\r\nORG:Müller & Ströbel\r\nTITLE:Partner – {p['rolle'].replace('&amp;', '&')}\r\n"
            f"TEL;TYPE=CELL:{p['tel_roh']}\r\nEMAIL;TYPE=WORK:{p['mail']}\r\nURL:https://www.muellerundstroebel.de\r\nEND:VCARD\r\n")


def main():
    (ZIEL / "business-story.html").write_text(startseite(), encoding="utf-8")
    (ZIEL / "bs-ueber-uns.html").write_text(ueber_uns(), encoding="utf-8")
    for k in PERSONEN:
        (ZIEL / f"bs-steckbrief-{k}.html").write_text(steckbrief(k), encoding="utf-8")
        (ZIEL / "bs" / f"{k}.vcf").write_text(vcard(k), encoding="utf-8")
    print("gebaut: business-story, bs-ueber-uns, bs-steckbrief-tobias, bs-steckbrief-daniel")


if __name__ == "__main__":
    main()
