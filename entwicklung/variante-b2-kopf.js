/* B2 – vier Kopf-Varianten zum Vergleichen (nur Entwicklung). Auswahl bleibt pro Browser gespeichert, ?kopf=3 öffnet direkt. */
(function () {
  var kopf = document.getElementById("hero"); if (!kopf) return;
  var w = (location.search.match(/kopf=(\d)/) || [])[1];
  try { w = w || localStorage.getItem("b2-kopf"); } catch (e) {}
  function setze(n) {
    kopf.setAttribute("data-kopf", n);
    kopf.querySelectorAll("[data-hv]").forEach(function (b) { b.setAttribute("aria-checked", String(b.getAttribute("data-hv") === String(n))); });
    try { localStorage.setItem("b2-kopf", n); } catch (e) {}
  }
  kopf.querySelectorAll("[data-hv]").forEach(function (b) { b.addEventListener("click", function () { setze(b.getAttribute("data-hv")); }); });
  setze(/^[1-4]$/.test(w || "") ? w : "1");
})();
