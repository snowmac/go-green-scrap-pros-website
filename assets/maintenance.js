// ── Site status toggle ────────────────────────────────────────────────────
// true  = site is in "temporarily closed" mode: every page except the
//         homepage redirects to "/", and the closure notice on the homepage
//         is shown.
// false = normal operation. Flip this one flag back to false to reopen the
//         site — no other files need to change.
window.MAINTENANCE_MODE = true;
// ─────────────────────────────────────────────────────────────────────────

(function () {
  if (!window.MAINTENANCE_MODE) return;

  var path = window.location.pathname;
  var isHome = path === "/" || path === "/index.html";

  if (!isHome) {
    window.location.replace("/");
  }
})();
