/* Müller & Ströbel – Startseite: Scroll-Reveal, Akkordeon, Pop-ups */
(function () {
  'use strict';
  var els = document.querySelectorAll('.v-rv');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    els.forEach(function (el) { io.observe(el); });
  } else { els.forEach(function (el) { el.classList.add('is-in'); }); }

  document.querySelectorAll('.v-acc-item').forEach(function (item) {
    var btn = item.querySelector('.v-acc-btn'), body = item.querySelector('.v-acc-body');
    btn.addEventListener('click', function () {
      var open = !item.classList.contains('is-open');
      item.parentNode.querySelectorAll('.v-acc-item').forEach(function (o) { o.classList.remove('is-open'); o.querySelector('.v-acc-body').style.maxHeight = null; });
      if (open) { item.classList.add('is-open'); body.style.maxHeight = body.scrollHeight + 'px'; }
    });
  });

  var modal = document.createElement('div');
  modal.className = 'v-modal';
  modal.innerHTML = '<div class="v-modal-box" role="dialog" aria-modal="true"><button class="v-modal-close" type="button" aria-label="Schließen">&times;</button><div class="v-modal-content"></div></div>';
  document.body.appendChild(modal);
  var content = modal.querySelector('.v-modal-content'), last = null;
  function close() { modal.classList.remove('is-open'); document.documentElement.style.overflow = ''; if (last) last.focus({ preventScroll: true }); }
  document.querySelectorAll('[data-modal]').forEach(function (t) {
    t.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); t.click(); } });
    t.addEventListener('click', function (e) {
      e.preventDefault();
      var tpl = document.getElementById('m-' + t.getAttribute('data-modal'));
      if (!tpl) return;
      last = t; content.innerHTML = tpl.innerHTML;
      modal.classList.add('is-open'); document.documentElement.style.overflow = 'hidden';
      modal.querySelector('.v-modal-box').scrollTop = 0;
    });
  });
  modal.addEventListener('click', function (e) { if (e.target === modal) close(); });
  modal.querySelector('.v-modal-close').addEventListener('click', close);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && modal.classList.contains('is-open')) close(); });
})();

/* Navigation: Dropdown „Lösungen“ */
(function () {
  var d = document.querySelector('.ms-dd'); if (!d) return;
  var b = d.querySelector('.ms-dd-toggle'), t;
  function set(o) { d.classList.toggle('is-open', o); b.setAttribute('aria-expanded', String(o)); }
  b.addEventListener('click', function (e) { e.stopPropagation(); if (window.innerWidth > 991 && d.matches(':hover')) { set(true); } else { set(!d.classList.contains('is-open')); } });
  d.addEventListener('mouseenter', function () { if (window.innerWidth > 991) { clearTimeout(t); set(true); } });
  d.addEventListener('mouseleave', function () { if (window.innerWidth > 991) { t = setTimeout(function () { set(false); }, 180); } });
  document.addEventListener('click', function (e) { if (!d.contains(e.target)) set(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') set(false); });
})();
