/* Kopf-Varianten zum Vergleichen (nur Entwicklung). Sichtbare Nummer → interner Kopf: 1→6 (ohne Und), 2→3 (mit Und), 3→4 (Schlagzeile).
   Beim Aufruf startet die Seite immer mit Kopf 1 – die Auswahl wird bewusst nicht gespeichert. ?kopf=2 öffnet eine Nummer direkt. */
(function () {
  var NR = { 1: "6", 2: "3", 3: "4" };
  var w = NR[(location.search.match(/kopf=([1-3])/) || [])[1]] || "6";
  try { localStorage.removeItem("b2-kopf-v3"); localStorage.removeItem("b2-kopf-intern"); } catch (e) {}
  function setze(n) {
    document.body.setAttribute("data-kopf", n);
    document.querySelectorAll("[data-hv]").forEach(function (b) { b.setAttribute("aria-checked", String(b.getAttribute("data-hv") === String(n))); });
  }
  document.querySelectorAll("[data-hv]").forEach(function (b) { b.addEventListener("click", function () { setze(b.getAttribute("data-hv")); }); });
  setze(w);
})();
