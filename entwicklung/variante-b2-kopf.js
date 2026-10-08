/* B2 – Kopf 1–4 zum Vergleichen (nur Entwicklung). Sichtbare Nummer → interner Kopf: 1→1, 2→3, 3→6, 4→4.
   Auswahl bleibt pro Browser gespeichert, ?kopf=3 öffnet die sichtbare Nummer 3 direkt. */
(function () {
  var NR = { 1: "1", 2: "3", 3: "6", 4: "4" };
  var w = NR[(location.search.match(/kopf=([1-4])/) || [])[1]];
  try { w = w || localStorage.getItem("b2-kopf-intern"); } catch (e) {}
  function setze(n) {
    document.body.setAttribute("data-kopf", n);
    document.querySelectorAll("[data-hv]").forEach(function (b) { b.setAttribute("aria-checked", String(b.getAttribute("data-hv") === String(n))); });
    try { localStorage.setItem("b2-kopf-intern", n); } catch (e) {}
  }
  document.querySelectorAll("[data-hv]").forEach(function (b) { b.addEventListener("click", function () { setze(b.getAttribute("data-hv")); }); });
  setze(/^[1346]$/.test(w || "") ? w : "1");
})();
