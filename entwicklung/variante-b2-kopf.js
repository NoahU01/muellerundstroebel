/* B2 – Kopf 1–3 zum Vergleichen (nur Entwicklung). Sichtbare Nummer → interner Kopf: 1→6 (ohne Und, Start), 2→3 (mit Und), 3→4 (Schlagzeile).
   Auswahl bleibt pro Browser gespeichert, ?kopf=3 öffnet die sichtbare Nummer 3 direkt. */
(function () {
  var NR = { 1: "6", 2: "3", 3: "4" };
  var w = NR[(location.search.match(/kopf=([1-3])/) || [])[1]];
  try { w = w || localStorage.getItem("b2-kopf-v3"); } catch (e) {}
  function setze(n) {
    document.body.setAttribute("data-kopf", n);
    document.querySelectorAll("[data-hv]").forEach(function (b) { b.setAttribute("aria-checked", String(b.getAttribute("data-hv") === String(n))); });
    try { localStorage.setItem("b2-kopf-v3", n); } catch (e) {}
  }
  document.querySelectorAll("[data-hv]").forEach(function (b) { b.addEventListener("click", function () { setze(b.getAttribute("data-hv")); }); });
  setze(/^[346]$/.test(w || "") ? w : "6");
})();
