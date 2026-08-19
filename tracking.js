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

  /* ---------------- 4. Modul-Tracking: wo wird abgesprungen? --------------
     Sektion steckt im Event-NAMEN, nicht im Parameter. Erspart in GA4 die
     Anlage einer Custom Dimension.
     Ausgelöst bei 15 % Sichtbarkeit ODER wenn die Sektion mehr als 30 % des
     Viewports füllt: sehr hohe Sektionen erreichen hohe Ratios nie.          */
  if ('IntersectionObserver' in window) {
    var gesehen = {};
    var obs = new IntersectionObserver(function (eintraege) {
      eintraege.forEach(function (e) {
        var id = e.target.id;
        if (gesehen[id]) return;
        var fuelltViewport = e.intersectionRect.height / window.innerHeight > 0.3;
        if (e.intersectionRatio >= 0.15 || (e.isIntersecting && fuelltViewport)) {
          gesehen[id] = true;
          track('section_view_' + id);
        }
      });
    }, { threshold: [0, 0.15, 0.3, 0.5] });

    document.querySelectorAll('section[id]').forEach(function (s) { obs.observe(s); });
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
