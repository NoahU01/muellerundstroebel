(function () {
  'use strict';

  /* ---------------------------------------------------------------
     1. Navigations-Linie: blendet über die ersten 5 % Scroll-Fortschritt ein
     --------------------------------------------------------------- */
  var line = document.getElementById('navigation-line');

  function updateLine() {
    var max = document.documentElement.scrollHeight - window.innerHeight;
    var progress = max > 0 ? window.scrollY / max : 0;
    line.style.opacity = String(Math.min(progress / 0.05, 1));
  }

  if (line) {
    updateLine();
    window.addEventListener('scroll', updateLine, { passive: true });
    window.addEventListener('resize', updateLine);
  }

  /* ---------------------------------------------------------------
     2. Mobile-Menü
     --------------------------------------------------------------- */
  var menuButton = document.getElementById('menu-button');
  var navBackdrop = document.getElementById('navigation-background');
  var navOpen = false;

  function setMenu(open) {
    navOpen = open;
    document.documentElement.classList.toggle('nav-open', open);
    menuButton.setAttribute('aria-expanded', String(open));

    // Der Abdunkler existiert nur auf der Startseite.
    if (!navBackdrop) return;
    if (open) {
      navBackdrop.classList.add('is-visible');
      requestAnimationFrame(function () { navBackdrop.classList.add('is-shown'); });
    } else {
      navBackdrop.classList.remove('is-shown');
      setTimeout(function () {
        if (!navOpen) navBackdrop.classList.remove('is-visible');
      }, 250);
    }
  }

  if (menuButton) {
    menuButton.addEventListener('click', function () { setMenu(!navOpen); });
  }

  document.querySelectorAll('.navigation-wrapper a').forEach(function (a) {
    a.addEventListener('click', function () { if (navOpen) setMenu(false); });
  });

  window.addEventListener('resize', function () {
    if (navOpen && window.innerWidth > 991) setMenu(false);
  });

  /* ---------------------------------------------------------------
     3. Modals ("Mehr anzeigen")
     --------------------------------------------------------------- */
  var wrapper = document.getElementById('modal-wrapper');
  var modals = document.querySelectorAll('.modal');
  var lastTrigger = null;

  if (!wrapper) return; // Rechtsseiten haben keine Modals

  function closeModal() {
    wrapper.classList.remove('is-open');
    modals.forEach(function (m) { m.classList.remove('is-open'); });
    if (lastTrigger && document.activeElement !== document.body) { lastTrigger.focus(); }
    lastTrigger = null;
  }

  // Fokus wird nur bei Tastaturbedienung in das Modal gezogen, damit ein
  // Mausklick keinen sichtbaren Fokusring auf dem Schließen-Button erzeugt.
  function openModal(id, trigger, moveFocus) {
    modals.forEach(function (m) {
      m.classList.toggle('is-open', m.getAttribute('data-modal') === id);
    });
    wrapper.classList.add('is-open');
    lastTrigger = trigger || null;
    var open = wrapper.querySelector('.modal.is-open');
    if (open) { open.scrollTop = 0; }
    if (moveFocus && open) {
      var close = open.querySelector('.close-modal');
      if (close) close.focus();
    }
  }

  document.querySelectorAll('.show-more-button').forEach(function (btn) {
    btn.addEventListener('click', function () { openModal(btn.getAttribute('data-open'), btn, false); });
    btn.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        openModal(btn.getAttribute('data-open'), btn, true);
      }
    });
  });

  document.querySelectorAll('.close-modal').forEach(function (btn) {
    btn.addEventListener('click', closeModal);
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && wrapper.classList.contains('is-open')) closeModal();
  });
})();
