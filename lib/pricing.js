'use strict';

const JUNK_PER_QTY = 75;
const SCRAP_FLAT = 50;
const EWASTE_FLAT = 50;
const TAX_RATE = parseFloat(process.env.TAX_RATE_DEFAULT || '0.085');
const MAX_QTY = 20;

const JUNK_ITEMS = [
  'mattress_twin', 'mattress_full', 'mattress_queen', 'mattress_king',
  'box_spring', 'sofa', 'loveseat', 'sectional_section', 'recliner',
  'chair', 'ottoman', 'coffee_table', 'end_table', 'dining_table',
  'dining_chair', 'desk', 'office_chair', 'dresser', 'nightstand',
  'bookshelf', 'wardrobe', 'bed_frame', 'headboard', 'tv_stand',
  'refrigerator', 'freezer', 'washer', 'dryer', 'dishwasher',
  'stove_oven', 'microwave', 'water_heater', 'ac_unit', 'treadmill',
  'exercise_bike', 'elliptical', 'weight_bench', 'grill', 'lawn_mower',
  'snow_blower', 'patio_set_section', 'cardboard_box', 'trash_bag',
  'piano_upright', 'hot_tub_section', 'carpet_roll', 'pool_table_section',
  'misc_item'
];

const SCRAP_ITEMS = [
  'copper', 'brass', 'aluminum', 'steel', 'iron', 'stainless_steel',
  'lead', 'zinc', 'wire_cable', 'auto_battery', 'rims', 'radiator',
  'catalytic_converter', 'sheet_metal', 'rebar', 'pipe', 'misc_metal'
];

const EWASTE_ITEMS = [
  'tv_crt', 'tv_flat', 'computer_tower', 'laptop', 'monitor',
  'printer', 'scanner', 'fax_machine', 'keyboard_mouse', 'router_modem',
  'cable_box', 'gaming_console', 'stereo', 'speakers', 'cell_phone',
  'tablet', 'small_electronic', 'cables_cords'
];

function clampQty(n) {
  const v = parseInt(n, 10);
  if (!Number.isFinite(v) || v < 1) return 1;
  if (v > MAX_QTY) return MAX_QTY;
  return v;
}

function calculate(payload) {
  const junk = (payload && payload.junk) || {};
  const scrap = (payload && payload.scrap) || {};
  const ewaste = (payload && payload.ewaste) || {};

  let junkTotal = 0;
  const junkLines = [];
  for (const key of Object.keys(junk)) {
    if (!JUNK_ITEMS.includes(key)) continue;
    const q = clampQty(junk[key]);
    if (q < 1) continue;
    const line = q * JUNK_PER_QTY;
    junkTotal += line;
    junkLines.push({ key, qty: q, lineTotal: line });
  }

  const scrapKeys = Object.keys(scrap).filter(k => SCRAP_ITEMS.includes(k) && scrap[k]);
  const ewasteKeys = Object.keys(ewaste).filter(k => EWASTE_ITEMS.includes(k) && ewaste[k]);

  const scrapTotal = scrapKeys.length > 0 ? SCRAP_FLAT : 0;
  const ewasteTotal = ewasteKeys.length > 0 ? EWASTE_FLAT : 0;

  const subtotal = junkTotal + scrapTotal + ewasteTotal;
  const tax = Math.round(subtotal * TAX_RATE * 100) / 100;
  const total = Math.round((subtotal + tax) * 100) / 100;

  return {
    junkTotal,
    scrapTotal,
    ewasteTotal,
    subtotal,
    taxRate: TAX_RATE,
    tax,
    total,
    totalCents: Math.round(total * 100),
    junkLines,
    scrapKeys,
    ewasteKeys
  };
}

module.exports = {
  calculate,
  clampQty,
  JUNK_ITEMS,
  SCRAP_ITEMS,
  EWASTE_ITEMS,
  JUNK_PER_QTY,
  SCRAP_FLAT,
  EWASTE_FLAT,
  TAX_RATE,
  MAX_QTY
};
