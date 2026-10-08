/* B2 – Kopf 1–5 zum Vergleichen (nur Entwicklung). Auswahl bleibt pro Browser gespeichert, ?kopf=2 öffnet direkt. */
(function () {
  var w = (location.search.match(/kopf=([1-5])/) || [])[1];
  try { w = w || localStorage.getItem("b2-kopf-12"); } catch (e) {}
  function setze(n) {
    document.body.setAttribute("data-kopf", n);
    document.querySelectorAll("[data-hv]").forEach(function (b) { b.setAttribute("aria-checked", String(b.getAttribute("data-hv") === String(n))); });
    try { localStorage.setItem("b2-kopf-12", n); } catch (e) {}
  }
  document.querySelectorAll("[data-hv]").forEach(function (b) { b.addEventListener("click", function () { setze(b.getAttribute("data-hv")); }); });
  setze(/^[1-5]$/.test(w || "") ? w : "1");
})();
