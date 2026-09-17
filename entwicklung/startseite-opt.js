/* Startseite optimieren – Tabs (Variante A) */
(function () {
  document.querySelectorAll('[data-tabs]').forEach(function (box) {
    var tabs = box.querySelectorAll('.ms-tab'), panels = box.querySelectorAll('.ms-tabpanel');
    tabs.forEach(function (t) {
      function go() {
        var k = t.getAttribute('data-tab');
        tabs.forEach(function (x) { var on = x === t; x.classList.toggle('is-active', on); x.setAttribute('aria-selected', String(on)); });
        panels.forEach(function (p) { p.classList.toggle('is-active', p.getAttribute('data-panel') === k); });
      }
      t.addEventListener('click', go);
      t.addEventListener('mouseenter', function () { if (window.innerWidth > 991) go(); });
    });
  });
})();
