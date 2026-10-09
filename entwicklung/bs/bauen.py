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


def kopfzeile(k, h, lead=None, mitte=False, hell=False):
    return (f'<div class="bs-kopf{" bs-kopf--mitte" if mitte else ""}"><p class="bs-kicker{" bs-kicker--hell" if hell else ""}">{k}</p><h2 class="bs-h2">{h}</h2>' +
            (f'<p class="bs-lead">{lead}</p>' if lead else "") + "</div>")


def personenkarte(key):
    p = PERSONEN[key]
    return (f'<a class="bs-person" href="/entwicklung/bs-steckbrief-{key}.html"><img src="{p["bild"]}" alt="{p["name"]}" width="96" height="96">'
            f'<div><b>{p["name"]}</b><span>{p["rolle"]}</span><p>{p["kurz"]}</p><em>Zum Steckbrief {PF}</em></div></a>')


# ---------------------------------------------------------------- Startseite
def startseite():
    m = []
    m.append(f'''<section class="bs-held"><div class="bs-wrap bs-held__raster">
  <div>
    <p class="bs-kicker">Für Führungskräfte in Versicherungsunternehmen</p>
    <h1 class="bs-h1">Sie geben uns ein Thema. Wir machen daraus ein Ergebnis<span class="bs-dot">.</span></h1>
    <p class="bs-lead">Wir denken auf Ihrer Ebene mit, organisieren die Bearbeitung und packen selbst mit an – von der ersten Klärung bis zum fertigen Ergebnis. Ohne dass Sie die einzelnen Schritte selbst orchestrieren müssen.</p>
    <div class="bs-knoepfe"><a class="bs-knopf" href="{MAIL_BEIDE}">Thema besprechen {PF}</a><a class="bs-knopf bs-knopf--rand" href="#modell">So arbeiten wir</a></div>
  </div>
  <div class="bs-dreiklang" aria-label="Mitdenken. Organisieren. Selber machen.">
    <div><span>01</span><b>Mitdenken<i>.</i></b><small>Fachliches Sparring auf Führungsebene</small></div>
    <div><span>02</span><b>Organisieren<i>.</i></b><small>Projektmanagement und Koordination</small></div>
    <div><span>03</span><b>Selber machen<i>.</i></b><small>Operative Umsetzung im Projektteam</small></div>
  </div>
</div></section>''')
    m.append(f'''<section class="bs-sek bs-sand" id="ausgangslage"><div class="bs-wrap">
  {kopfzeile("Die Ausgangslage", 'Zu viele wichtige Themen. Und niemand, der sie Ihnen wirklich abnimmt<span class="bs-dot">.</span>')}
  <blockquote class="bs-zitat">„Ich habe zu viele wichtige Themen auf dem Tisch. Ich brauche jemanden, der meine Situation versteht, mitdenkt – und mir nicht noch zusätzliche Koordinationsarbeit verursacht.“</blockquote>
  <div class="bs-ebenen">
    <div><span>Vorstand</span><p>Themen mit dem Aufsichtsrat klären, Entscheidungen vorbereiten, die Bereichsleitungen koordinieren.</p></div>
    <div><span>Hauptabteilungsleitung</span><p>Strategische Vorgaben in konkrete Aktivitäten übersetzen, Abteilungen koordinieren, Ergebnisse sicherstellen.</p></div>
    <div><span>Bereichsleitung</span><p>Mit dem Vorstand abstimmen, Teamleitungen führen, zahlreiche fachliche und organisatorische Themen voranbringen.</p></div>
  </div>
  <p class="bs-fazit">Die Hierarchie unterscheidet sich. Das Problem ist dasselbe: mehr Themen, als sich selbst im notwendigen Umfang bearbeiten und koordinieren lassen.</p>
</div></section>''')
    m.append(f'''<section class="bs-sek" id="luecke"><div class="bs-wrap">
  {kopfzeile("Die Lücke", 'Berater, Projektmanager, Spezialisten – und wer hält alles zusammen<span class="bs-dot">?</span>', "Ein Unternehmen kann einen Strategieberater beauftragen, einen Projektmanager engagieren und Spezialisten hinzuziehen. Dann bleibt eine wesentliche Aufgabe bei der Führungskraft selbst: die Leistungen verbinden, die Beteiligten koordinieren und dafür sorgen, dass am Ende ein Ergebnis entsteht.")}
  <div class="bs-vergleich">
    <div class="bs-vergleich__seite">
      <p class="bs-vergleich__label">Üblich</p>
      <div class="bs-bausteine"><span>Strategieberater</span><span>Projektmanager</span><span>Spezialisten</span></div>
      <div class="bs-pfeile" aria-hidden="true"><i></i><i></i><i></i></div>
      <div class="bs-last"><b>Sie</b><small>koordinieren, verbinden, treiben an</small></div>
    </div>
    <div class="bs-vergleich__seite bs-vergleich__seite--wir">
      <p class="bs-vergleich__label">Mit Müller &amp; Ströbel</p>
      <div class="bs-eins"><b>Müller &amp; Ströbel</b><small>Sparring · Projektmanagement · Umsetzung</small></div>
      <div class="bs-pfeile bs-pfeile--eins" aria-hidden="true"><i></i></div>
      <div class="bs-ergebnis"><b>Ihr Ergebnis</b><small>Sie entscheiden, wir kümmern uns um den Rest</small></div>
    </div>
  </div>
</div></section>''')
    leist = [
        ("01", "Fachliches Sparring", "Wir denken auf Führungsebene mit.",
         ["Themen aufnehmen, einordnen und strukturieren", "Komplexität reduzieren, Handlungsoptionen entwickeln", "Entscheidungen und Zielbilder vorbereiten", "Offen sagen, wo zusätzliche Spezialisten nötig sind"],
         "Einen erfahrenen Gesprächspartner auf Augenhöhe, der Ihre Themen versteht."),
        ("02", "Projektmanagement", "Wir übernehmen die Verantwortung für die Bearbeitung.",
         ["Organisation und Koordination der weiteren Bearbeitung", "Gespräche mit Führungskräften, Teams und Spezialisten", "Prioritäten setzen, Fortschritt im Blick behalten", "Regelmäßig berichten und Entscheidungen vorlegen"],
         "Sie müssen sich nicht selbst darum kümmern, dass aus einer guten Idee ein Ergebnis wird."),
        ("03", "Operative Umsetzung", "Wir packen selbst mit an.",
         ["Konzepte erstellen, Sachverhalte analysieren", "Lösungen entwickeln und Ergebnisse erarbeiten", "Teil des operativen Projektteams sein", "Spezialisten aus unserem Netzwerk einbinden"],
         "Nicht nur Empfehlungen und Steuerung, sondern die notwendige operative Unterstützung."),
    ]
    m.append(f'''<section class="bs-sek bs-sand" id="modell"><div class="bs-wrap">
  {kopfzeile("Unser Modell", 'Mitdenken. Organisieren. Selber machen<span class="bs-dot">.</span>', "Drei Leistungen, die zusammengehören. Nicht die einzelne Leistung macht den Unterschied, sondern ihre Kombination – aus einer Hand.")}
  <div class="bs-drei">{"".join(f'<article class="bs-leistung"><span class="bs-nr">{n}</span><h3>{t}</h3><p class="bs-leistung__satz">{s}</p><ul>{"".join(f"<li>{x}</li>" for x in l)}</ul><p class="bs-leistung__nutzen"><b>Sie bekommen</b>{u}</p></article>' for n, t, s, l, u in leist)}</div>
</div></section>''')
    m.append(f'''<section class="bs-sek bs-navy" id="praxis"><div class="bs-wrap bs-praxis">
  <div>{kopfzeile("Aus der Praxis", 'Entstanden aus einer echten Zusammenarbeit<span class="bs-dot">.</span>', None, hell=True)}
    <p class="bs-lead bs-lead--hell">Als Tobias Müller Geschäftsführer des Haftpflichtverbands öffentlicher Verkehrsbetriebe (HÖV) war, lagen viele Themen gleichzeitig auf seinem Tisch – fachlich unterschiedlich, teils komplex, über Personen, Projekte und Einheiten hinweg. Daniel Ströbel hat ihn dabei begleitet. Aus dieser Zusammenarbeit ist Müller &amp; Ströbel entstanden.</p></div>
  <figure class="bs-stimme">
    <blockquote>„Ich konnte mit dir über jedes Thema sprechen. Du hast verstanden, worum es geht. Wenn du dich nicht auskanntest, hast du das offen gesagt – und wusstest trotzdem, wie man das Thema angehen kann.“</blockquote>
    <blockquote>„Du hast das Projektmanagement übernommen, mit den Leuten gesprochen und dafür gesorgt, dass die Dinge weiterlaufen. Und dort, wo du die fachliche Kompetenz hattest, hast du selbst mit angepackt.“</blockquote>
    <figcaption><img src="/assets/tobias-kreis.webp" alt="" width="44" height="44"><span><b>Tobias Müller</b>über die gemeinsame Zeit beim HÖV</span></figcaption>
  </figure>
</div></section>''')
    versprechen = ["Wir verstehen das Thema und die dahinterliegende Herausforderung.", "Wir bringen die Erfahrung mit, um auf Führungsebene mitzudenken.",
                   "Wir machen aus komplexen Aufgaben eine strukturierte Bearbeitung.", "Wir organisieren die notwendigen Menschen und Kompetenzen.",
                   "Wir koordinieren die gesamte Bearbeitung.", "Wir arbeiten selbst mit, wo wir die Fachkompetenz besitzen.",
                   "Wir binden bei Bedarf weitere Spezialisten ein.", "Wir liefern ein Ergebnis, mit dem Sie weiterarbeiten können."]
    m.append(f'''<section class="bs-sek" id="versprechen"><div class="bs-wrap bs-versprechen">
  <div>{kopfzeile("Unser Versprechen", 'Eine Gesamtlösung statt einzelner Leistungen<span class="bs-dot">.</span>', "Sie müssen die einzelnen Leistungen nicht selbst organisieren. Sie können uns ein vollständiges Thema übertragen.")}</div>
  <ol class="bs-liste">{"".join(f"<li>{v}</li>" for v in versprechen)}</ol>
</div></section>''')
    schritte = [("Klären", "Auch wenn noch offen ist, worum es genau geht: Wir ordnen das Thema gemeinsam ein."),
                ("Mitdenken", "Wir entwickeln mit Ihnen Zielbild, Optionen und die richtige Vorgehensweise."),
                ("Organisieren", "Wir stellen die passenden Menschen und Kompetenzen zusammen und steuern die Bearbeitung."),
                ("Ergebnis liefern", "Wir arbeiten selbst mit und legen Ihnen ein Ergebnis vor, mit dem Sie weiterarbeiten.")]
    m.append(f'''<section class="bs-sek bs-sand" id="ablauf"><div class="bs-wrap">
  {kopfzeile("Von der ersten Klärung bis zum Ergebnis", 'So übernehmen wir ein Thema<span class="bs-dot">.</span>')}
  <div class="bs-schritte">{"".join(f'<div><span>0{i+1}</span><h3>{t}</h3><p>{p}</p></div>' for i, (t, p) in enumerate(schritte))}</div>
</div></section>''')
    m.append(f'''<section class="bs-sek" id="netzwerk"><div class="bs-wrap bs-netzwerk">
  <div>{kopfzeile("Unser Netzwerk", 'Wenn es mehr braucht, bringen wir die richtigen Leute mit<span class="bs-dot">.</span>', "Erfahrene Persönlichkeiten, die wir gezielt einsetzen – koordiniert von uns, mit einem Ansprechpartner für Sie.")}</div>
  <div class="bs-chips">{"".join(f"<span>{n}</span>" for n in NETZWERK)}</div>
</div></section>''')
    m.append(f'''<section class="bs-sek bs-sand" id="wir"><div class="bs-wrap">
  {kopfzeile("Wer dahintersteht", 'Erfahrene Führungskräfte auf Ihrer Seite des Tisches<span class="bs-dot">.</span>')}
  <div class="bs-personen">{personenkarte("tobias")}{personenkarte("daniel")}</div>
  <p class="bs-mehr"><a href="/entwicklung/bs-ueber-uns.html">Über uns und unsere Themenfelder {PF}</a></p>
</div></section>''')
    m.append(abschluss())
    return rahmen("Müller & Ströbel – Business Story (Entwurf)", "Entwurf der Startseite auf Basis der Business Story", "\n".join(m), "business-story.html")


def abschluss():
    return f'''<section class="bs-sek bs-navy bs-schluss"><div class="bs-wrap bs-kopf--mitte">
  <p class="bs-kicker bs-kicker--hell">Ihr Thema</p>
  <h2 class="bs-h2">Welches Thema liegt auf Ihrem Tisch<span class="bs-dot">?</span></h2>
  <p class="bs-lead bs-lead--hell">Erzählen Sie uns davon. Wir sagen Ihnen offen, ob und wie wir es übernehmen.</p>
  <div class="bs-knoepfe"><a class="bs-knopf bs-knopf--weiss" href="{MAIL_BEIDE}">Thema besprechen {PF}</a></div>
</div></section>'''


# ---------------------------------------------------------------- Über uns
def ueber_uns():
    eigenschaften = ["Auf Augenhöhe mit anderen Führungskräften diskutieren", "Strategische und operative Zusammenhänge verstehen",
                     "Unterschiedliche Themen und Projekte gleichzeitig im Blick behalten", "Menschen und Fachkompetenzen zusammenbringen",
                     "Aufgaben organisieren und koordinieren", "Entscheidungen vorbereiten", "Selbst operativ mitarbeiten",
                     "Verantwortung für die vereinbarte Bearbeitung übernehmen"]
    m = [f'''<section class="bs-held bs-held--schmal"><div class="bs-wrap">
  <p class="bs-kicker">Über uns</p>
  <h1 class="bs-h1">Erfahrung einer Führungskraft. Ohne eine Stelle zu besetzen<span class="bs-dot">.</span></h1>
  <p class="bs-lead">Wir ersetzen keine Führungskraft. Wir entlasten sie um ein vollständiges Aufgabenpaket – egal ob Vorstand, Hauptabteilungs- oder Bereichsleitung. Entscheidend ist nicht die Stellenbezeichnung, sondern dass ein Thema zum Ergebnis kommt.</p>
</div></section>''',
         f'''<section class="bs-sek bs-sand"><div class="bs-wrap bs-versprechen">
  <div>{kopfzeile("Was uns ausmacht", 'Was Sie von uns erwarten können<span class="bs-dot">.</span>', "Wir bringen die Erfahrung langjähriger Führungskräfte mit – verbunden mit Branchenkenntnis, Methodenkompetenz, Projektmanagement und operativer Umsetzungsfähigkeit.")}</div>
  <ol class="bs-liste">{"".join(f"<li>{v}</li>" for v in eigenschaften)}</ol>
</div></section>''',
         f'''<section class="bs-sek" id="team"><div class="bs-wrap">
  {kopfzeile("Das Team", 'Partner, die selbst mitarbeiten<span class="bs-dot">.</span>', "Im Projekt arbeiten wir selbst mit. Jede Person hat einen eigenen Steckbrief – mit Schwerpunkten, Erfahrung und dem, wofür Sie sie einsetzen.")}
  <div class="bs-team">{personenkarte("tobias")}{personenkarte("daniel")}
    <div class="bs-person bs-person--netz"><div class="bs-netz-sym" aria-hidden="true"><i></i><i></i><i></i><i></i></div><div><b>Unser Netzwerk</b><span>Gezielt eingebunden</span><p>{", ".join(NETZWERK[:-1])} und {NETZWERK[-1]}.</p></div></div>
  </div>
</div></section>''',
         f'''<section class="bs-sek bs-sand" id="themen"><div class="bs-wrap">
  {kopfzeile("Unsere Themenfelder", 'Hier setzen wir an<span class="bs-dot">.</span>', "Wir werden eingebunden, wenn Zusammenhänge unklar sind, die Komplexität zu groß ist und ein Thema nicht vorankommt.")}
  <div class="bs-themen">{"".join(f'<div><span>0{i+1}</span><h3>{t}</h3><p>{w}</p></div>' for i, (t, w) in enumerate(THEMEN))}</div>
</div></section>''',
         f'''<section class="bs-sek" id="haltung"><div class="bs-wrap">
  {kopfzeile("Unsere Haltung", 'Umsetzen. Sofort. Überzeugt<span class="bs-dot">.</span>')}
  <div class="bs-drei bs-drei--haltung">
    <div class="bs-haltung"><h3>Umsetzen</h3><p>Wir bleiben, bis das Ergebnis steht.</p></div>
    <div class="bs-haltung"><h3>Sofort</h3><p>Wir müssen nicht abgeholt werden.</p></div>
    <div class="bs-haltung bs-haltung--stark"><h3>Überzeugt</h3><p>Wir machen nur, woran wir glauben.</p></div>
  </div>
</div></section>''',
         abschluss()]
    return rahmen("Müller & Ströbel – Über uns (Entwurf Business Story)", "Über uns, Team und Themenfelder", "\n".join(m), "bs-ueber-uns.html")


# ---------------------------------------------------------------- Steckbrief
def steckbrief(key):
    p = PERSONEN[key]
    vcf = f"/entwicklung/bs/{key}.vcf"
    m = [f'''<section class="bs-karte"><div class="bs-wrap bs-karte__raster">
  <div class="bs-karte__person">
    <img src="{p["bild"]}" alt="{p["name"]}" width="200" height="200">
    <div><p class="bs-kicker">Partner · Müller &amp; Ströbel</p><h1 class="bs-h1 bs-h1--name">{p["name"]}</h1><p class="bs-karte__rolle">{p["rolle"]}</p></div>
  </div>
  <div class="bs-aktionen">
    <a href="tel:{p["tel_roh"]}"><i>☎</i><span><b>Anrufen</b>{p["tel"]}</span></a>
    <a href="mailto:{p["mail"]}"><i>@</i><span><b>E-Mail</b>{p["mail"]}</span></a>
    <a href="{p["linkedin"]}" target="_blank" rel="noopener"><i>in</i><span><b>LinkedIn</b>Profil ansehen</span></a>
    <a href="{vcf}" download><i>+</i><span><b>Kontakt speichern</b>Visitenkarte fürs Adressbuch</span></a>
  </div>
</div></section>''',
         f'''<section class="bs-sek bs-sand"><div class="bs-wrap">
  {kopfzeile("Warum in Ihrem Projekt", f'Was {p["name"].split()[0]} einbringt<span class="bs-dot">.</span>')}
  <div class="bs-drei">{"".join(f'<article class="bs-leistung"><span class="bs-nr">0{i+1}</span><h3>{t}</h3><p>{x}</p></article>' for i, (t, x) in enumerate(p["warum"]))}</div>
  <div class="bs-fakten"><div><b>{p["fakt"][0]}</b><span>{p["fakt"][1]}</span></div><div><b>{p["fakt2"][0]}</b><span>{p["fakt2"][1]}</span></div></div>
</div></section>''',
         f'''<section class="bs-sek"><div class="bs-wrap bs-zwei">
  <div>{kopfzeile("Schwerpunkte", 'Kompetenzen<span class="bs-dot">.</span>')}
    <div class="bs-chips bs-chips--dunkel">{"".join(f"<span>{s}</span>" for s in p["schwerpunkte"])}</div>
    <p class="bs-text">{p["werdegang"]}</p>
    <h3 class="bs-h3">Im Projekt</h3>
    <ul class="bs-rollen"><li><b>Sparring</b>denkt auf Führungsebene mit</li><li><b>Projektmanagement</b>organisiert und steuert die Bearbeitung</li><li><b>Umsetzung</b>arbeitet selbst im Projektteam mit</li></ul></div>
  <div>{kopfzeile("Werdegang", 'Stationen<span class="bs-dot">.</span>')}<div class="bs-cv">{cv(key)}</div></div>
</div></section>''',
         abschluss()]
    return rahmen(f"{p['name'].replace('&amp;', '&')} – Steckbrief · Müller & Ströbel (Entwurf)", f"Beraterprofil {p['name']}", "\n".join(m), f"bs-steckbrief-{key}.html")


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
