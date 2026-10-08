/* B2 – Kopf-Konzepte A–C zum Vergleichen (nur Entwicklung). Auswahl bleibt pro Browser gespeichert, ?kopf=B öffnet direkt. */
(function () {
  var kopf = document.getElementById("hero"); if (!kopf) return;
  var w = (location.search.match(/kopf=([A-C])/) || [])[1];
  try { w = w || localStorage.getItem("b2-kopf-abc"); } catch (e) {}
  function setze(n) {
    kopf.setAttribute("data-kopf", n);
    kopf.querySelectorAll("[data-hv]").forEach(function (b) { b.setAttribute("aria-checked", String(b.getAttribute("data-hv") === String(n))); });
    try { localStorage.setItem("b2-kopf-abc", n); } catch (e) {}
  }
  kopf.querySelectorAll("[data-hv]").forEach(function (b) { b.addEventListener("click", function () { setze(b.getAttribute("data-hv")); }); });
  setze(/^[A-C]$/.test(w || "") ? w : "A");
})();
