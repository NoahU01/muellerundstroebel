/* Variante E – Umschalter fuer E2 (Auswahl) und E3 (Diagnose).
   Ein Knopf mit data-fall schaltet das Element mit passendem data-panel an.

   Bewusst ueber eine Klasse und nicht ueber das hidden-Attribut: in E2 liegen
   alle Faelle per Grid in derselben Zelle uebereinander. Wuerden die inaktiven
   aus dem Layout genommen, bestimmte der gerade sichtbare Fall die Hoehe und
   die Spalte wuerde bei jedem Wechsel springen. So bleibt sie stehen. */
(function () {
  var knoepfe = document.querySelectorAll('[data-fall]');
  if (!knoepfe.length) return;
  var panels = document.querySelectorAll('[data-panel]');

  function zeige(id) {
    knoepfe.forEach(function (k) {
      var an = k.getAttribute('data-fall') === id;
      k.classList.toggle('is-on', an);
      k.setAttribute('aria-pressed', String(an));
    });
    panels.forEach(function (p) {
      var an = p.getAttribute('data-panel') === id;
      p.classList.toggle('is-on', an);
      /* visibility:hidden nimmt die inaktiven Faelle aus Tabfolge und
         Vorlesereihenfolge, ohne ihren Platz freizugeben. */
      p.setAttribute('aria-hidden', String(!an));
    });
  }

  knoepfe.forEach(function (k) {
    k.setAttribute('aria-pressed', String(k.classList.contains('is-on')));
    k.addEventListener('click', function () { zeige(k.getAttribute('data-fall')); });
  });
  /* Absicherung: faellt die Startmarkierung im Markup weg, waere sonst gar
     kein Fall sichtbar. Dann den zum aktiven Knopf passenden einschalten. */
  var offen = false;
  panels.forEach(function (p) {
    if (p.classList.contains('is-on')) offen = true;
    p.setAttribute('aria-hidden', String(!p.classList.contains('is-on')));
  });
  if (!offen) {
    var aktiv = document.querySelector('[data-fall].is-on') || knoepfe[0];
    zeige(aktiv.getAttribute('data-fall'));
  }
})();
