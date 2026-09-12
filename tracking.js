/* ---------------------------------------------------------------------------
   Tracking für muellerundstroebel.de

   Sendet über window.gtag mit dataLayer-Fallback, damit ein späterer Umzug
   auf den Google Tag Manager ohne Umbau funktioniert.

   Die Seite hat kein Formular. Echte Conversions sind deshalb die
   Kontaktklicks (E-Mail, Telefon, LinkedIn). Alles andere sind
   Interessens-Signale für die Absprung-Analyse.

   Cookies setzt diese Datei nicht. Ob GA4 speichern darf, entscheidet
   ausschließlich der Consent Mode, der von Cookiebot gesteuert wird.
   --------------------------------------------------------------------------- */
(function () {
  'use strict';

  function track(name, params) {
    var payload = params || {};
    if (typeof window.gtag === 'function') {
      window.gtag('event', name, payload);
    } else {
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push(Object.assign({ event: name }, payload));
    }
  }
  window.msTrack = track;

  function textOf(el) {
    return (el && el.textContent || '').replace(/\s+/g, ' ').trim();
  }

  /* ---------------- 1. Kontaktklicks: die eigentlichen Conversions --------- */
  document.querySelectorAll('.contact-bullet').forEach(function (a) {
    var href = a.getAttribute('href') || '';
    var name = href.indexOf('mailto:') === 0 ? 'kontakt_email'
             : href.indexOf('tel:') === 0    ? 'kontakt_telefon'
             : href.indexOf('linkedin') > -1 ? 'kontakt_linkedin'
             : null;
    if (!name) return;

    var card = a.closest('.contact-card');
    var person = card ? textOf(card.querySelector('h3')) : '';

    // Kein "ziel"-Parameter mit der Adresse: GA4 erkennt E-Mail-Adressen als
    // personenbezogen und ersetzt sie durch "(redacted)". Wer kontaktiert wurde,
    // steht in "person", wie kontaktiert wurde im Event-Namen.
    a.addEventListener('click', function () {
      track(name, { person: person });
    });
  });

  /* ---------------- 2. CTA-Klicks: Interesse, keine Conversion ------------- */
  document.querySelectorAll('.primary-button').forEach(function (a) {
    var label = textOf(a.querySelector('.button-text'));
    var bereich = a.closest('.nav-bar')        ? 'navigation'
                : a.closest('.section-hero')   ? 'hero'
                : a.closest('.section-ergebnis') ? 'ergebnis'
                : 'sonstige';
    a.addEventListener('click', function () {
      track('cta_klick', { cta_label: label, cta_bereich: bereich });
    });
  });

  /* ---------------- 3. Einsatzgebiete: welches Thema zieht? ---------------- */
  document.querySelectorAll('.show-more-button').forEach(function (btn) {
    var card = btn.closest('.card-1');
    var thema = card ? textOf(card.querySelector('h3')) : '';
    btn.addEventListener('click', function () {
      track('einsatzgebiet_geoeffnet', { thema: thema });
    });
  });

  /* ---------------- 4. Modul-Tracking: Reichweite und Verweildauer --------
     Port der SectionTracker-Komponente von admemory.de, gleiche Event-Namen
     und Parameter, damit der Report dort ohne Umbau auch hier läuft.

     section_view_<id>  einmal pro Seitenaufruf, sobald die Sektion sichtbar
                        war. Reichweite: bis wohin wird gescrollt.
     section_time_<id>  im Viewport verbrachte Sekunden als `value`. GA4
                        summiert das in eventValue; Durchschnitt = eventValue
                        geteilt durch die Anzahl der section_view-Events.

     Sichtbar heißt: 15 % der Sektion im Viewport ODER die Sektion füllt mehr
     als 30 % des Viewports. Sehr hohe Sektionen erreichen hohe Ratios nie.
     Die Uhr läuft nur, solange der Tab im Vordergrund ist. Gesendet wird beim
     Tab-Wechsel und beim Verlassen der Seite, per Beacon, damit der Request
     das Entladen überlebt.                                                 */
  if ('IntersectionObserver' in window) {
    var VISIBLE_RATIO = 0.15;
    var VIEWPORT_FILL = 0.3;
    var MAX_SECONDS = 600;   // Deckel gegen Tabs, die stundenlang offen liegen
    var MIN_SECONDS = 1;     // darunter ist es Durchscrollen, keine Aufmerksamkeit

    var page = window.location.pathname;
    var pageLocation = window.location.href;
    var seen = {};      // id -> true, section_view schon gesendet
    var visible = {};   // id -> true, gerade im Viewport
    var since = {};     // id -> performance.now() beim Sichtbarwerden
    var totals = {};    // id -> aufgelaufene Millisekunden

    function now() { return performance.now(); }

    // Laufende Uhren stoppen und aufaddieren (Tab-Wechsel, Seitenwechsel).
    function pauseAll() {
      for (var id in since) totals[id] = (totals[id] || 0) + (now() - since[id]);
      since = {};
    }
    // Uhren für alles wieder starten, was gerade sichtbar ist. Nur wenn der Tab
    // vorn ist: send() ruft das auch beim Wechsel in den Hintergrund auf, und
    // ohne diese Prüfung liefe die Uhr dort weiter und zählte beim nächsten
    // Vordergrund die gesamte Hintergrundzeit mit.
    function resumeAll() {
      if (document.visibilityState !== 'visible') return;
      for (var id in visible) if (!(id in since)) since[id] = now();
    }

    function send() {
      pauseAll();
      for (var id in totals) {
        // Erst gegen die Rohzeit prüfen: Math.round machte aus 0,6 s eine 1 s
        // und ließ Durchscrollen als Verweildauer durchgehen.
        if (totals[id] < MIN_SECONDS * 1000) continue;
        var seconds = Math.round(totals[id] / 1000);
        track('section_time_' + id, {
          value: Math.min(seconds, MAX_SECONDS),
          page: page,
          page_location: pageLocation,
          transport_type: 'beacon'
        });
      }
      totals = {};
      resumeAll(); // Sichtbares läuft weiter, falls der Nutzer zurückkommt
    }

    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        var id = e.target.id;
        if (!id) return;
        var isVisible = e.isIntersecting &&
          (e.intersectionRatio >= VISIBLE_RATIO ||
           e.intersectionRect.height > window.innerHeight * VIEWPORT_FILL);

        if (isVisible) {
          if (!seen[id]) {
            seen[id] = true;
            track('section_view_' + id, { page: page, page_location: pageLocation });
          }
          visible[id] = true;
          if (document.visibilityState === 'visible' && !(id in since)) since[id] = now();
        } else {
          delete visible[id];
          if (id in since) {
            totals[id] = (totals[id] || 0) + (now() - since[id]);
            delete since[id];
          }
        }
      });
    }, { threshold: [0, VISIBLE_RATIO, 0.5] });

    // Sofort anhängen, dann nochmal für spät gerenderte Sektionen.
    // observe() auf ein bereits beobachtetes Element ist folgenlos.
    function attach() {
      document.querySelectorAll('section[id]').forEach(function (s) { obs.observe(s); });
    }
    attach();
    setTimeout(attach, 400);
    setTimeout(attach, 1200);

    document.addEventListener('visibilitychange', function () {
      if (document.visibilityState === 'hidden') send(); else resumeAll();
    });
    window.addEventListener('pagehide', send);
  }
})();

/* ---------------------------------------------------------------------------
   Cookie-Einstellungen im Footer: Widerruf muss so einfach sein wie die
   Einwilligung. Öffnet das Cookiebot-Banner erneut.
   --------------------------------------------------------------------------- */
(function () {
  var btn = document.getElementById('cookie-settings');
  if (!btn) return;
  btn.addEventListener('click', function () {
    if (window.Cookiebot && typeof window.Cookiebot.renew === 'function') {
      window.Cookiebot.renew();
    }
  });
})();
