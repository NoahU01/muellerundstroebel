(function () {
  'use strict';
  var body = document.body;
  var current = body.getAttribute('data-variante');

  /* Umschalter unten rechts */
  var sw = document.createElement('div');
  sw.className = 'v-switch';
  sw.innerHTML =
    '<a href="variante-a.html" data-v="a">A</a><a href="variante-b.html" data-v="b">B</a><a href="variante-c.html" data-v="c">C</a><a href="variante-d.html" data-v="d">D</a><a href="ueber-uns.html" data-v="ueber">Über uns</a>' +
    '<span></span><button type="button" id="v-labels">Labels</button><span></span><a href="../index.html">Neue Startseite</a><a href="../archiv/startseite-live-2026-09.html">Archiv</a>';
  body.appendChild(sw);
  sw.querySelectorAll('a[data-v]').forEach(function (a) { if (a.getAttribute('data-v') === current) a.classList.add('is-current'); });
  document.getElementById('v-labels').addEventListener('click', function () { body.classList.toggle('hide-labels'); });

  /* Scroll-Reveal */
  var els = document.querySelectorAll('.v-rv');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    els.forEach(function (el) { io.observe(el); });
  } else { els.forEach(function (el) { el.classList.add('is-in'); }); }

  /* Akkordeon */
  document.querySelectorAll('.v-acc-item').forEach(function (item) {
    var btn = item.querySelector('.v-acc-btn'), bodyEl = item.querySelector('.v-acc-body');
    btn.addEventListener('click', function () {
      var open = !item.classList.contains('is-open');
      item.parentNode.querySelectorAll('.v-acc-item').forEach(function (o) { o.classList.remove('is-open'); o.querySelector('.v-acc-body').style.maxHeight = null; });
      if (open) { item.classList.add('is-open'); bodyEl.style.maxHeight = bodyEl.scrollHeight + 'px'; }
    });
  });

  /* Modals: [data-modal="id"] öffnet <template id="m-id"> */
  var modal = document.createElement('div');
  modal.className = 'v-modal';
  modal.innerHTML = '<div class="v-modal-box" role="dialog" aria-modal="true"><button class="v-modal-close" type="button" aria-label="Schließen">&times;</button><div class="v-modal-content"></div></div>';
  body.appendChild(modal);
  var content = modal.querySelector('.v-modal-content');
  function close() { modal.classList.remove('is-open'); }
  document.querySelectorAll('[data-modal]').forEach(function (t) {
    t.addEventListener('keydown', function (e) { if (e.key === 'Enter') t.click(); });
    t.addEventListener('click', function (e) {
      e.preventDefault();
      var tpl = document.getElementById('m-' + t.getAttribute('data-modal'));
      if (!tpl) return;
      content.innerHTML = tpl.innerHTML;
      modal.classList.add('is-open');
    });
  });
  modal.addEventListener('click', function (e) { if (e.target === modal) close(); });
  modal.querySelector('.v-modal-close').addEventListener('click', close);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
})();

/* Über uns – Umschalter Ü2c */
(function () {
  document.querySelectorAll('.u2c-tab').forEach(function (tab) {
    tab.addEventListener('click', function () {
      var key = tab.getAttribute('data-u2c');
      document.querySelectorAll('.u2c-tab').forEach(function (t) { t.classList.toggle('is-active', t === tab); });
      document.querySelectorAll('.u2c-panel').forEach(function (p) { p.classList.toggle('is-active', p.getAttribute('data-u2c-panel') === key); });
    });
  });
})();
