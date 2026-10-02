/* Variante E – Umschalter fuer E2 (Auswahl) und E3 (Diagnose).
   Beide tauschen denselben Panel-Typ aus: ein Knopf mit data-fall zeigt das
   Element mit passendem data-panel und blendet die uebrigen aus. */
(function () {
  var knoepfe = document.querySelectorAll('[data-fall]');
  if (!knoepfe.length) return;
  var panels = document.querySelectorAll('[data-panel]');

  function zeige(id, scrollen) {
    knoepfe.forEach(function (k) {
      var an = k.getAttribute('data-fall') === id;
      k.classList.toggle('is-on', an);
      k.setAttribute('aria-pressed', String(an));
    });
    panels.forEach(function (p) {
      var an = p.getAttribute('data-panel') === id;
      p.hidden = !an;
      if (an) {
        p.classList.remove('e-fade');
        void p.offsetWidth;            /* Animation neu anstossen */
        p.classList.add('e-fade');
      }
    });
    if (scrollen) {
      var ziel = document.querySelector('[data-panel="' + id + '"]');
      if (!ziel) return;
      var oben = ziel.getBoundingClientRect().top + window.pageYOffset - 110;
      if (ziel.getBoundingClientRect().top < 0 ||
          ziel.getBoundingClientRect().bottom > window.innerHeight) {
        window.scrollTo({ top: oben, behavior: 'smooth' });
      }
    }
  }

  knoepfe.forEach(function (k) {
    k.setAttribute('aria-pressed', String(k.classList.contains('is-on')));
    k.addEventListener('click', function () {
      zeige(k.getAttribute('data-fall'), true);
    });
  });
})();
