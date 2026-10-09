#!/usr/bin/env python3
"""Business Story – Neustart (Daniel, 10.10.2026): frisches Layout, nur Schriften (Lora, Poppins) und Farben aus dem CD.
Baut entwicklung/business-story.html. Gestaltung: entwicklung/business-story-neu.css (eigenständig, keine alten Bausteine)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import bauen as b

PF = '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>'
JA = '<svg viewBox="0 0 20 20" aria-label="ja"><circle cx="10" cy="10" r="9"/><path d="M6 10.4l2.6 2.6L14 7.6"/></svg>'
NEIN = '<svg viewBox="0 0 20 20" aria-label="nein"><circle cx="10" cy="10" r="9"/><path d="M7 7l6 6M13 7l-6 6"/></svg>'
T, D = b.PERSONEN["tobias"], b.PERSONEN["daniel"]


def main_html():
    tisch = ["Aufsichtsratssitzung vorbereiten", "Strategie in die Bereiche bringen", "Projekt-Review mit dem Vorstand", "Kennzahlen für das Reporting",
             "Kooperation prüfen", "Vertriebsziele umsetzen", "Reorganisation abstimmen", "KI-Vorhaben priorisieren"]
    zeilen = [("Denkt auf Ihrer Ebene mit", [1, 0, 0, 1]), ("Organisiert die Bearbeitung", [0, 1, 0, 1]),
              ("Arbeitet selbst mit", [0, 0, 1, 1]), ("Hält alles zusammen", [0, 0, 0, 1])]
    s = [f'''<section class="nb-held"><div class="nb-wrap nb-held__raster">
  <div class="nb-held__text">
    <p class="nb-kicker">Für Führungskräfte in Versicherungsunternehmen</p>
    <h1>Sie geben uns ein Thema. Wir sorgen dafür, dass daraus ein Ergebnis wird.</h1>
    <p class="nb-lead">Wir denken auf Augenhöhe mit, organisieren die Bearbeitung und packen selbst mit an. Sie müssen nichts koordinieren.</p>
    <div class="nb-knoepfe"><a class="nb-knopf" href="{b.MAIL_BEIDE}">Thema besprechen {PF}</a><a class="nb-knopf nb-knopf--leise" href="#so">So arbeiten wir</a></div>
  </div>
  <div class="nb-paar" aria-label="Tobias Müller und Daniel Ströbel">
    <figure><img src="/assets/tobias-portrait.webp" alt="Tobias Müller"><figcaption><b>Tobias Müller</b>Governance, Gremien &amp; Risiko</figcaption></figure>
    <span class="nb-paar__und" aria-hidden="true">&amp;</span>
    <figure><img src="/assets/daniel-portrait.webp" alt="Daniel Ströbel"><figcaption><b>Daniel Ströbel</b>Strategie, Führung &amp; Vertrieb</figcaption></figure>
  </div>
</div></section>''',
         f'''<section class="nb-sek nb-sand"><div class="nb-wrap nb-zwei">
  <div>
    <p class="nb-kicker">Kennen Sie das?</p>
    <h2>Viele wichtige Themen. Und alle liegen bei Ihnen.</h2>
    <p class="nb-text">Sie wissen meist genau, was wichtig ist. Aber Strategie, Entscheidungen, Projekte und Tagesgeschäft laufen gleichzeitig. Für vieles fehlt schlicht die Zeit, die Kapazität oder die passende Kompetenz.</p>
  </div>
  <div class="nb-tisch" aria-label="Typische Themen auf dem Tisch einer Führungskraft">
    <p class="nb-tisch__kopf"><span>Auf Ihrem Tisch</span><b>{len(tisch)} offen</b></p>
    <ul>{"".join(f"<li><i></i>{t}</li>" for t in tisch)}</ul>
  </div>
</div>
<div class="nb-wrap"><div class="nb-ebenen">
  <blockquote><p>„Ich muss den Aufsichtsrat vorbereiten, Entscheidungen treffen und meine Bereiche koordinieren.“</p><cite>Vorstand</cite></blockquote>
  <blockquote><p>„Ich soll Vorgaben umsetzen, Abteilungen abstimmen und Ergebnisse liefern.“</p><cite>Hauptabteilungsleitung</cite></blockquote>
  <blockquote><p>„Ich stimme mich mit dem Vorstand ab, führe meine Teams und treibe zig Themen voran.“</p><cite>Bereichsleitung</cite></blockquote>
</div><p class="nb-schluss">Unterschiedliche Ebene, gleiches Problem.</p></div></section>''',
         f'''<section class="nb-sek"><div class="nb-wrap">
  <div class="nb-kopf"><p class="nb-kicker">Warum Beratung allein nicht reicht</p>
    <h2>Ein Berater gibt Ihnen Empfehlungen. Die Arbeit bleibt bei Ihnen.</h2>
    <p class="nb-text">Sie können einen Strategieberater holen, einen Projektmanager und Spezialisten. Dann müssen Sie trotzdem alles zusammenbringen, die Beteiligten koordinieren und dranbleiben, bis ein Ergebnis da ist. Genau diese Last nehmen wir Ihnen ab.</p></div>
  <div class="nb-vergleich" role="table">
    <div class="nb-vergleich__kopf" role="row"><span role="columnheader"></span><span role="columnheader">Strategie&shy;berater</span><span role="columnheader">Projekt&shy;manager</span><span role="columnheader">Spezialist</span><span role="columnheader" class="nb-wir">Müller <i>&amp;</i> Ströbel</span></div>
    {"".join(f'<div class="nb-vergleich__zeile" role="row"><span role="rowheader">{z}</span>' + "".join(f'<span role="cell" class="{"nb-wir" if i == 3 else ""}">{JA if v else NEIN}</span>' for i, v in enumerate(w)) + "</div>" for z, w in zeilen)}
  </div>
</div></section>''',
         '''<section class="nb-sek nb-navy" id="so"><div class="nb-wrap">
  <div class="nb-kopf"><p class="nb-kicker nb-kicker--hell">So lösen wir es</p><h2>Mitdenken. Organisieren. Selber machen.</h2>
    <p class="nb-text nb-text--hell">Das Besondere ist nicht eine dieser Leistungen, sondern dass Sie alle drei aus einer Hand bekommen.</p></div>
  <ol class="nb-drei">
    <li><span>01</span><h3>Mitdenken</h3><p>Wir verstehen, wie Versicherungsunternehmen funktionieren, und denken auf Ihrer Ebene mit. Wir ordnen Ihr Thema ein, entwickeln Optionen und bereiten Entscheidungen vor. Und wir sagen offen, wo wir selbst nicht tief genug drin sind.</p></li>
    <li><span>02</span><h3>Organisieren</h3><p>Nach dem Gespräch lassen wir Sie nicht mit einer Liste allein. Wir sprechen mit den Beteiligten, setzen Prioritäten, halten Projekte am Laufen und legen Ihnen vor, was Sie entscheiden müssen.</p></li>
    <li><span>03</span><h3>Selber machen</h3><p>Wo wir die Fachkompetenz haben, arbeiten wir selbst mit: Konzepte, Analysen, Lösungen. Wo es mehr braucht, holen wir passende Spezialisten aus unserem Netzwerk dazu.</p></li>
  </ol>
</div></section>''',
         '''<section class="nb-sek"><div class="nb-wrap">
  <div class="nb-kopf"><p class="nb-kicker">So gehen wir vor</p><h2>Vom ersten Gespräch bis zum Ergebnis.</h2></div>
  <ol class="nb-weg">
    <li><b>Zuhören</b><p>Wir klären mit Ihnen, worum es wirklich geht – auch wenn das am Anfang noch offen ist.</p></li>
    <li><b>Vorgehen</b><p>Wir entwickeln gemeinsam, wie wir das Thema angehen.</p></li>
    <li><b>Bearbeiten</b><p>Wir übernehmen die Bearbeitung und halten Sie auf dem Laufenden.</p></li>
    <li><b>Ergebnis</b><p>Sie bekommen ein Ergebnis, mit dem Sie weiterarbeiten können.</p></li>
  </ol>
  <div class="nb-alltag"><p class="nb-kicker">So fühlt sich das an</p><p>Sie haben jemanden, mit dem Sie über jedes Thema sprechen können. Sie geben ein Thema ab. Es kommt zu Ihnen zurück, wenn etwas zu entscheiden ist oder wenn es fertig ist. <b>Dazwischen müssen Sie sich um nichts kümmern.</b></p></div>
</div></section>''',
         f'''<section class="nb-sek nb-sand"><div class="nb-wrap nb-zitat">
  <p class="nb-kicker">So war es beim HÖV</p>
  <blockquote><p>„Ich konnte mit dir über jedes Thema sprechen. Du hast verstanden, worum es geht. Wenn du dich fachlich auskanntest, konntest du direkt mitdenken. Wenn du dich nicht auskanntest, hast du das offen gesagt und wusstest trotzdem, wie man das Thema angehen kann.“</p>
  <p>„Du hast das Projektmanagement übernommen. Du hast mit den Leuten gesprochen, die Projekte im Blick behalten und dafür gesorgt, dass die Dinge weiterlaufen. Und dort, wo du die fachliche Kompetenz hattest, hast du selbst mit angepackt.“</p></blockquote>
  <p class="nb-zitat__wer"><img src="{T["bild"]}" alt=""><span><b>Tobias Müller</b>damals Geschäftsführer des HÖV, über die Zusammenarbeit mit Daniel Ströbel</span></p>
</div></section>''',
         '''<section class="nb-sek"><div class="nb-wrap nb-zwei">
  <div><p class="nb-kicker">Unser Netzwerk</p><h2>Wenn ein Thema mehr braucht.</h2>
    <p class="nb-text">Dann holen wir gezielt die richtigen Leute dazu. Wir steuern sie – und Sie haben weiter einen Ansprechpartner.</p></div>
  <ul class="nb-netz"><li>IT- und Prozess-Spezialisten</li><li>Ehemalige Vorstände</li><li>Aufsichtsratsmitglieder</li><li>Marketingexperten</li><li>Programmierer</li><li>Grafiker</li></ul>
</div></section>''',
         f'''<section class="nb-sek nb-sand"><div class="nb-wrap">
  <div class="nb-kopf"><p class="nb-kicker">Wer wir sind</p><h2>Zwei Partner, die selbst mitarbeiten.</h2></div>
  <div class="nb-partner">{"".join(f"""<article><div class="nb-partner__bild"><img src="/assets/{k}-portrait.webp" alt="{p['name']}"></div><div><h3>{p['name']}</h3><p class="nb-rolle">{p['rolle']}</p><p class="nb-text">{p['werdegang']}</p><a class="nb-link" href="/entwicklung/bs-steckbrief-{k}.html">Zum Steckbrief {PF}</a></div></article>""" for k, p in b.PERSONEN.items())}</div>
</div></section>''',
         f'''<section class="nb-sek nb-ende"><div class="nb-wrap nb-zwei">
  <div><p class="nb-kicker">Ihr Thema</p><h2>Welches Thema liegt gerade auf Ihrem Tisch?</h2>
    <p class="nb-text">Rufen Sie an oder schreiben Sie uns. Wir sagen Ihnen offen, ob und wie wir es übernehmen.</p></div>
  <div class="nb-ruf">{"".join(f"""<div><b>{p['name']}</b><a href="tel:{p['tel_roh']}">{p['tel']}</a><a href="mailto:{p['mail']}">{p['mail']}</a></div>""" for p in (T, D))}</div>
</div></section>''']
    return "\n".join(s)


def bauen():
    html = b.rahmen("Müller & Ströbel – Business Story (Entwurf)", "Entwurf der Startseite auf Basis der Business Story", main_html(), "business-story.html")
    html = html.replace(b.CSS, '<link rel="stylesheet" href="/entwicklung/business-story-neu.css">').replace('<main class="bs">', '<main class="nb">')
    html = html.replace('<div class="bs-dev"><div class="bs-wrap">', '<div class="nb-dev"><div>')
    (b.ZIEL / "business-story.html").write_text(html, encoding="utf-8")
    print("gebaut: business-story.html (Neustart)")


if __name__ == "__main__":
    bauen()
