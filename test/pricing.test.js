'use strict';
const assert = require('assert');
process.env.TAX_RATE_DEFAULT = '0.085';
const { calculate } = require('../lib/pricing');

(function empty(){
  const t = calculate({});
  assert.strictEqual(t.total, 0);
  assert.strictEqual(t.totalCents, 0);
})();

(function junkOnly(){
  const t = calculate({ junk: { sofa: 2, mattress_queen: 1 } });
  assert.strictEqual(t.junkTotal, 225);
  assert.strictEqual(t.scrapTotal, 0);
  assert.strictEqual(t.subtotal, 225);
  assert.ok(Math.abs(t.tax - 19.13) < 0.01);
  assert.strictEqual(t.totalCents, Math.round(t.total * 100));
})();

(function flatScrapAndEwaste(){
  const t = calculate({ scrap: { copper: true }, ewaste: { laptop: true, monitor: true } });
  assert.strictEqual(t.scrapTotal, 50);
  assert.strictEqual(t.ewasteTotal, 50);
  assert.strictEqual(t.subtotal, 100);
})();

(function clamping(){
  const t = calculate({ junk: { sofa: 999 } });
  assert.strictEqual(t.junkTotal, 20 * 75);
})();

(function ignoresUnknownKeys(){
  const t = calculate({ junk: { not_a_real_item: 5 }, scrap: { fake: true } });
  assert.strictEqual(t.subtotal, 0);
})();

console.log('pricing.test.js ok');
