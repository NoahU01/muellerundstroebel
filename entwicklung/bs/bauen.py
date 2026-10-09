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


def team_reihe(mit_netz=False):
    leute = "".join(f'<a class="bs-mensch" href="/entwicklung/bs-steckbrief-{k}.html"><div class="bs-mensch__bild"><img src="{PORTRAIT[k]}" alt="{p["name"]}"></div>'
                    f'<b>{p["name"]}</b><span>{p["rolle"]}</span><em>Steckbrief {PF}</em></a>' for k, p in PERSONEN.items())
    netz = ""
    if mit_netz:
        netz = (f'<div class="bs-mensch bs-mensch--netz"><div class="bs-mensch__bild">{orbit(klein=True)}</div><b>Unser Netzwerk</b>'
                f'<span>Gezielt eingebunden, von uns koordiniert</span></div>')
    return f'<div class="bs-menschen{" bs-menschen--drei" if mit_netz else ""}">{leute}{netz}</div>'


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
    return f'''<section class="bs-sek bs-navy bs-schluss"><div class="bs-wrap">
  {AMP}
  <p class="bs-kicker bs-kicker--hell">Ihr Thema</p>
  <h2 class="bs-h1 bs-h1--hell">Welches Thema liegt auf Ihrem Tisch<span class="bs-dot">?</span></h2>
  <div class="bs-knoepfe"><a class="bs-knopf bs-knopf--weiss" href="{MAIL_BEIDE}">Thema besprechen {PF}</a></div>
</div></section>'''


# ---------------------------------------------------------------- Startseite
def startseite():
    themen_wolke = ["Aufsichtsratsvorlage", "Strategie 2030", "Kennzahlen", "Reorganisation", "Vertriebsziele", "KI-Einsatz",
                    "Budget", "Projekt-Review", "Gremienvorlage", "Kooperation", "Personal", "Solvency"]
    m = [f'''<section class="bs-held bs-navy"><div class="bs-wrap">
  {AMP}
  <p class="bs-kicker bs-kicker--hell">Für Vorstände und Führungskräfte in Versicherungsunternehmen</p>
  <h1 class="bs-h1 bs-h1--held">Sie geben uns ein Thema.<br><em>Wir machen daraus ein Ergebnis.</em></h1>
  <p class="bs-dreiwort"><span>Mitdenken</span><span>Organisieren</span><span>Selber machen</span></p>
  <div class="bs-knoepfe"><a class="bs-knopf bs-knopf--weiss" href="{MAIL_BEIDE}">Thema besprechen {PF}</a><a class="bs-knopf bs-knopf--hell" href="#modell">Wie wir arbeiten</a></div>
</div></section>''',
         f'''<section class="bs-sek"><div class="bs-wrap bs-zwei">
  <div>{kopf("Die Ausgangslage", 'Zu viele Themen.<br>Zu wenig Hände<span class="bs-dot">.</span>', "Ob Vorstand, Hauptabteilungs- oder Bereichsleitung: Auf dem Tisch liegt mehr, als sich selbst bearbeiten lässt.")}</div>
  <div class="bs-wolke" aria-hidden="true">{"".join(f'<span style="--i:{i}">{t}</span>' for i, t in enumerate(themen_wolke))}</div>
</div></section>''',
         f'''<section class="bs-sek bs-sand"><div class="bs-wrap">
  {kopf("Die Lücke", 'Berater, Projektmanager, Spezialisten.<br>Und wer hält alles zusammen<span class="bs-dot">?</span>', mitte=True)}
  <div class="bs-gegen">
    <figure><figcaption>Üblich</figcaption>
      <svg viewBox="0 0 360 300" class="bs-diag" role="img" aria-label="Drei Dienstleister, die Koordination bleibt bei Ihnen">
        <path d="M60 70 C60 150 180 140 180 220M180 70V220M300 70C300 150 180 140 180 220" class="d-l"/>
        <g class="d-n"><circle cx="60" cy="54" r="34"/><circle cx="180" cy="54" r="34"/><circle cx="300" cy="54" r="34"/></g>
        <g class="d-t"><text x="60" y="58">Berater</text><text x="180" y="58">Projekt</text><text x="300" y="58">Spezialist</text></g>
        <circle cx="180" cy="236" r="42" class="d-sie"/><text x="180" y="242" class="d-t2">Sie</text>
      </svg>
      <p>Die Koordination bleibt bei Ihnen.</p></figure>
    <figure class="bs-gegen--wir"><figcaption>Mit Müller &amp; Ströbel</figcaption>
      <svg viewBox="0 0 360 300" class="bs-diag" role="img" aria-label="Ein Partner, ein Ergebnis">
        <path d="M180 120V196" class="d-l d-l--wir"/>
        <circle cx="180" cy="66" r="56" class="d-wir"/><text x="180" y="86" class="d-amp">&amp;</text>
        <circle cx="180" cy="236" r="42" class="d-erg"/><text x="180" y="242" class="d-t2 d-t2--hell">Ergebnis</text>
      </svg>
      <p>Ein Partner. Ein Ergebnis.</p></figure>
  </div>
</div></section>''',
         f'''<section class="bs-sek" id="modell"><div class="bs-wrap">
  {kopf("Unser Modell", 'Drei Leistungen. Eine Verantwortung<span class="bs-dot">.</span>')}
  <div class="bs-trio">
    <div><span>01 · Fachliches Sparring</span><b>Mitdenken<i>.</i></b><p>Wir denken auf Ihrer Ebene mit und bereiten Entscheidungen vor.</p></div>
    <div><span>02 · Projektmanagement</span><b>Organisieren<i>.</i></b><p>Wir steuern die Bearbeitung – mit allen Beteiligten.</p></div>
    <div><span>03 · Operative Umsetzung</span><b>Selber machen<i>.</i></b><p>Wo wir die Fachkompetenz haben, arbeiten wir selbst mit.</p></div>
  </div>
  <div class="bs-klammer"><span>Aus einer Hand – Sie müssen nichts koordinieren.</span></div>
</div></section>''',
         f'''<section class="bs-sek bs-navy bs-ursprung"><div class="bs-wrap bs-ursprung__raster">
  <div>
    <p class="bs-kicker bs-kicker--hell">Entstanden aus der Praxis</p>
    <blockquote class="bs-gross-zitat">„Du hast das Projektmanagement übernommen, mit den Leuten gesprochen und dafür gesorgt, dass die Dinge weiterlaufen. Und dort, wo du die fachliche Kompetenz hattest, hast du selbst mit angepackt.“</blockquote>
    <p class="bs-quelle"><b>Tobias Müller</b>damals Geschäftsführer des HÖV, über die Zusammenarbeit mit Daniel Ströbel</p>
  </div>
  <div class="bs-ursprung__bild"><img src="{PORTRAIT["tobias"]}" alt="Tobias Müller"></div>
</div></section>''',
         f'''<section class="bs-sek bs-sand"><div class="bs-wrap bs-zwei bs-zwei--mitte">
  <div>{kopf("Was bei Ihnen nicht mehr hängen bleibt", 'Sie geben ab. Wir bringen es zu Ende<span class="bs-dot">.</span>')}</div>
  <ul class="bs-weg"><li>Berater briefen und Ergebnisse nachhalten</li><li>Projekte und Beteiligte koordinieren</li><li>Spezialisten suchen und steuern</li></ul>
</div></section>''',
         f'''<section class="bs-sek"><div class="bs-wrap">
  {kopf("Von der ersten Klärung bis zum Ergebnis", 'So übernehmen wir ein Thema<span class="bs-dot">.</span>')}
  <ol class="bs-pfad"><li><b>Klären</b><span>Auch wenn noch offen ist, worum es geht.</span></li><li><b>Mitdenken</b><span>Zielbild, Optionen, Vorgehen.</span></li><li><b>Organisieren</b><span>Die richtigen Menschen, ein Plan.</span></li><li><b>Ergebnis</b><span>Mit dem Sie weiterarbeiten.</span></li></ol>
</div></section>''',
         f'''<section class="bs-sek bs-sand"><div class="bs-wrap bs-zwei bs-zwei--mitte">
  <div>{kopf("Unser Netzwerk", 'Und wenn es mehr braucht, bringen wir die richtigen Leute mit<span class="bs-dot">.</span>', "Erfahrene Persönlichkeiten – gezielt eingebunden, von uns koordiniert, ein Ansprechpartner für Sie.")}</div>
  <div>{orbit()}</div>
</div></section>''',
         f'''<section class="bs-sek bs-sek--team"><div class="bs-wrap">
  {kopf("Wer dahintersteht", 'Erfahrene Führungskräfte.<br>Auf Ihrer Seite des Tisches<span class="bs-dot">.</span>')}
  {team_reihe()}
  <p class="bs-mehr"><a href="/entwicklung/bs-ueber-uns.html">Über uns und unsere Themenfelder {PF}</a></p>
</div></section>''',
         abschluss()]
    return rahmen("Müller & Ströbel – Business Story (Entwurf)", "Entwurf der Startseite auf Basis der Business Story", "\n".join(m), "business-story.html")


# ---------------------------------------------------------------- Über uns
def ueber_uns():
    staerken = [("Auf Augenhöhe", "Wir diskutieren mit Vorstand, Aufsichtsrat und Fachbereich."),
                ("Den Überblick behalten", "Viele Themen und Projekte gleichzeitig im Blick."),
                ("Menschen zusammenbringen", "Wir organisieren die richtigen Leute und Kompetenzen."),
                ("Verantwortung übernehmen", "Wir arbeiten selbst mit – bis das Ergebnis steht.")]
    m = [f'''<section class="bs-held bs-held--ueber"><div class="bs-wrap bs-ueber__raster">
  <div><p class="bs-kicker">Über uns</p>
    <h1 class="bs-h1">Erfahrung einer Führungskraft. Ohne eine Stelle zu besetzen<span class="bs-dot">.</span></h1>
    <p class="bs-sub">Wir ersetzen niemanden. Wir nehmen Führungskräften ein ganzes Aufgabenpaket ab.</p></div>
  <div class="bs-ueber__bild"><img src="{PORTRAIT["tobias"]}" alt="Tobias Müller"><img src="{PORTRAIT["daniel"]}" alt="Daniel Ströbel"></div>
</div></section>''',
         f'''<section class="bs-sek"><div class="bs-wrap">
  {kopf("Was Sie bekommen", 'Die Erfahrung langjähriger Führungskräfte<span class="bs-dot">.</span>')}
  <div class="bs-vier">{"".join(f'<div><span>0{i+1}</span><b>{t}</b><p>{x}</p></div>' for i, (t, x) in enumerate(staerken))}</div>
</div></section>''',
         f'''<section class="bs-sek bs-sand bs-sek--team" id="team"><div class="bs-wrap">
  {kopf("Das Team", 'Partner, die selbst mitarbeiten<span class="bs-dot">.</span>')}
  {team_reihe(mit_netz=True)}
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
    m = [f'''<section class="bs-held bs-navy bs-profil"><div class="bs-wrap bs-profil__raster">
  <div>
    <p class="bs-kicker bs-kicker--hell">Partner · Müller &amp; Ströbel</p>
    <h1 class="bs-h1 bs-h1--held">{p["name"]}</h1>
    <p class="bs-profil__rolle">{p["rolle"]}</p>
    <p class="bs-profil__kurz">{p["kurz"]}</p>
    <div class="bs-aktionen">
      <a href="tel:{p["tel_roh"]}">Anrufen</a><a href="mailto:{p["mail"]}">E-Mail</a><a href="{p["linkedin"]}" target="_blank" rel="noopener">LinkedIn</a><a href="{vcf}" download class="bs-aktionen__haupt">Kontakt speichern</a>
    </div>
  </div>
  <div class="bs-profil__bild"><img src="{PORTRAIT[key]}" alt="{p["name"]}"></div>
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
