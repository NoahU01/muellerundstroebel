# Handoff: muellerundstroebel.de

Stand 12.09.2026. Die Seite ist live, das Tracking läuft, die Rechtstexte sind
aktualisiert. Dieses Dokument beschreibt den Stand, die offenen Punkte und die
Fallen, die schon Zeit gekostet haben.

## Wo liegt was

| | |
|---|---|
| Live | https://www.muellerundstroebel.de (kanonisch mit `www`, Apex leitet per 308) |
| Repo | https://github.com/NoahU01/muellerundstroebel (public, seit 12.09.), Branch `main` |
| Hosting | Vercel, Team `empiria-gmb-h` (Hobby), Deployment automatisch bei jedem Push auf `main` |
| DNS | IONOS. Apex A auf Vercel, `www` CNAME auf Vercel |
| GA4 | `G-KSWHNGZS3P` |
| Cookiebot | `8870d24b-eae6-4dd4-8406-28c7c01e48b1` |

## Was fertig ist

**Die Seite** ist ein Nachbau der alten Webflow-Site als statisches HTML, ohne
Framework und ohne Build-Schritt. Gegen das Original abgeglichen: 0 abweichende
Pixel auf 17 Breiten von 320 bis 1920, in allen Zuständen. Bewusste Abweichungen
stehen in der `README.md`.

**Tracking** läuft mit Consent Mode v2. Vor der Einwilligung 0 Cookies, danach
`_ga`, `_ga_KSWHNGZS3P` und `CookieConsent`. Events: `kontakt_email`,
`kontakt_telefon`, `kontakt_linkedin`, `cta_klick`, `einsatzgebiet_geoeffnet`,
`section_view_<id>` für den Scroll-Funnel und seit 12.09. `section_time_<id>`
für die Verweildauer je Sektion (Sekunden als `value`, identisch mit admemory.de,
damit dessen Report hier läuft). Alle live im `/g/collect`-Payload nachgewiesen.

**SEO** steht: robots.txt mit ausdrücklicher Freigabe für GPTBot, OAI-SearchBot,
ChatGPT-User, ClaudeBot, PerplexityBot und Google-Extended. Sitemap, canonical,
OpenGraph, Twitter-Card, JSON-LD `ProfessionalService`, `llms.txt`.
Search Console und Bing Webmaster sind eingerichtet, GA4 ist mit Google Ads
verknüpft, die Datenaufbewahrung steht auf 14 Monate.

**Performance** ist unkritisch. Gemessen mobil mit gedrosseltem 4G und
vierfach gebremster CPU: FCP 412 ms, LCP 628 ms, CLS 0,013. Die Schwellen liegen
bei 2500 ms und 0,1.

## Offene Punkte

### Klein, jederzeit machbar

1. **Fonts als WOFF2.** Aktuell liegen sie als TTF, zusammen 665 KB. Als WOFF2
   wären es rund 250 KB. Das ist der größte verbliebene Brocken: von den 795 KB
   eigener Dateien sind 665 KB Schriften. Die `@font-face`-Regeln für Poppins
   300 und 700 sind Karteileichen, die Gewichte werden nirgends benutzt.
2. **Cookiebot-Banner-Text.** Der Standardtext spricht von „Funktionen für
   soziale Medien" und „Partner für Werbung und Analysen". Beides trifft nicht
   zu, die Seite hat nur Analytics. Anpassbar in der Domain Group.
3. **Bing-Sitemap gegenprüfen.** Beim Import aus der Search Console zeigt Bing
   oft „0 Sitemaps" und man muss sie dort einmal von Hand nachtragen.
4. **Datenschutz von einem Anwalt prüfen lassen.** Der Text ist inhaltlich an
   den tatsächlichen Stand angepasst (Vercel statt Webflow, GA4 mit 14 Monaten,
   Cookiebot), aber wir sind keine Juristen.

### Größer, sinnvoll in zwei bis vier Wochen

5. **Reporting-Pipeline** (Phase 11 im Tracking-Skill). Skript, das GA4 und
   Search Console abfragt und monatlich einen Markdown-Report schreibt. Vorher
   fehlt die Datenlage. Achtung laut Skill: Google blockt Dienstkonto-Schlüssel
   per Policy, es braucht einen OAuth-Desktop-Client, und die OAuth-App muss auf
   „In Produktion" stehen, sonst stirbt der Refresh-Token nach 7 Tagen.
6. **Monitoring** (`website-monitoring`-Skill). Täglicher HTTP-Check, ob alle
   Sitemap-URLs 200 liefern und das Tracking noch im HTML steht.

## Wie man etwas prüft

```bash
# lokal, verhält sich wie Vercel (cleanUrls)
npx serve .

# ist ein Deployment durch?
curl -s https://www.muellerundstroebel.de/ | grep -o 'id="Cookiebot"'

# liefern alle Seiten aus?
for p in / /impressum /datenschutz /robots.txt /sitemap.xml /llms.txt; do
  printf "%-16s " $p
  curl -s -o /dev/null -w "%{http_code}\n" "https://www.muellerundstroebel.de$p"
done
```

**Vercel blockiert Pushes von Fremden im Hobby-Plan.** Das Projekt liegt im
Team des Kunden. Solange das Repo privat war, wies Vercel jeden Commit von
`NoahU01` mit „Deployment was blocked" ab, weil im Hobby-Plan nur der
Kontoinhaber deployen darf. Seit das Repo public ist, geht es durch. Wird es
wieder privat, kommt das Problem zurück; dann hilft nur Pro oder der
Redeploy-Knopf im Dashboard.

**Security Checkpoint auf der Custom Domain.** Seit 11.09. beantwortet
`www.muellerundstroebel.de` Requests ohne JavaScript mit 403
(`x-vercel-mitigated: challenge`). Am 12.09. blockte es auch Googlebot-UA und
sichtbaren Chrome von der Test-IP. Für andere Besucher unklar. Prüfen unter
Projekt → Firewall → Attack Challenge Mode und ausschalten, wenn niemand ihn
bewusst gesetzt hat. Bis dahin für Tests die Vercel-Domain nehmen:
`muellerundstroebel-git-main-empiria-gmb-h.vercel.app`.

## Fallen, die schon Zeit gekostet haben

**Cookiebot blockiert den Google-Tag.** `data-blockingmode="auto"` blockiert
auch `gtag.js` selbst. Dann läuft der Consent Mode nie an und GA4 sieht auch
nach der Einwilligung nichts. Deshalb tragen der Google-Tag, der
Consent-Default-Block und die eigenen Skripte `data-cookieconsent="ignore"`.
Nicht entfernen.

**GA4 verwirft E-Mail-Adressen in Parametern** und ersetzt sie durch
`(redacted)`. Deshalb steht in den Kontakt-Events nur der Name des
Ansprechpartners, nicht die Adresse.

**GA4 bündelt Events im POST-Body**, nicht in der Request-URL. Wer beim Testen
nur die URL liest, hält funktionierende Events für fehlend.

**Puppeteers `click()` läuft in einen Timeout**, seit `scroll-behavior: smooth`
aktiv ist, weil es auf das Ende der Bewegung wartet. Im Test stattdessen
`element.click()` innerhalb von `page.evaluate()` benutzen.

**Cookiebot zeigt lokal kein Banner**, weil `127.0.0.1` nicht in der Domain
Group steht. Die `configuration.js` gibt dann 404. Das ist harmlos, aber die
Consent-Verifikation muss gegen die Live-Domain laufen.

**Bei einem DNS-Umzug lügt die Fehlermeldung.** Nach dem Wechsel von Webflow
kam erst eine 404, dann `ERR_SSL_VERSION_OR_CIPHER_MISMATCH`. Beides kam vom
alten, noch gecachten DNS-Eintrag, nicht von Vercel. Im Zweifel am Cache vorbei
prüfen:

```bash
curl -I --resolve www.muellerundstroebel.de:443:216.198.79.1 \
  https://www.muellerundstroebel.de/
```
