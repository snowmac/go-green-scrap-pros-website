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

(function appliancesAreScrapFlat(){
  // Refrigerator/washer/etc moved from junk ($75/ea) to scrap (flat $50).
  const t = calculate({ scrap: { refrigerator: true, washer: true, dryer: true } });
  assert.strictEqual(t.junkTotal, 0);
  assert.strictEqual(t.scrapTotal, 50);
  assert.strictEqual(t.subtotal, 50);
})();

(function appliancesUnderJunkKeyAreIgnored(){
  // If a stale client posts an appliance under junk, pricing must not charge $75.
  const t = calculate({ junk: { refrigerator: 3 } });
  assert.strictEqual(t.junkTotal, 0);
  assert.strictEqual(t.subtotal, 0);
})();

(function removedItemsAreIgnored(){
  const removed = ['patio_set_section','cardboard_box','trash_bag','piano_upright','hot_tub_section','carpet_roll','pool_table_section'];
  const junk = {};
  removed.forEach(k => { junk[k] = 2; });
  const t = calculate({ junk });
  assert.strictEqual(t.junkTotal, 0);
  assert.strictEqual(t.subtotal, 0);
})();

console.log('pricing.test.js ok');
