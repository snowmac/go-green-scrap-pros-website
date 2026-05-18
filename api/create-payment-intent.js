'use strict';

const { calculate } = require('../lib/pricing');
const { validateBookingPayload } = require('../lib/validation');
const { createPaymentIntent } = require('../lib/stripe');
const { insertBookingDraft } = require('../lib/supabase');
const { readJsonBody, setCors, json } = require('./_helpers');

module.exports = async function handler(req, res) {
  setCors(res);
  if (req.method === 'OPTIONS') { res.statusCode = 204; return res.end(); }
  if (req.method !== 'POST') return json(res, 405, { error: true, message: 'method not allowed', code: 'method_not_allowed' });

  let payload;
  try { payload = await readJsonBody(req); }
  catch (e) { return json(res, 400, { error: true, message: 'invalid request body', code: 'bad_body' }); }

  const v = validateBookingPayload(payload);
  if (!v.ok) return json(res, 400, { error: true, message: 'validation failed', code: 'validation_failed', details: v.errors });

  const totals = calculate(payload);
  if (!totals.totalCents || totals.totalCents <= 0) {
    return json(res, 400, { error: true, message: 'order total must be greater than zero', code: 'zero_total' });
  }

  let bookingDraftId = null;
  try {
    const draft = await insertBookingDraft({
      customer: payload.customer,
      pickup_date: payload.pickupDate,
      junk: payload.junk || {},
      scrap: payload.scrap || {},
      ewaste: payload.ewaste || {},
      totals,
      created_at: new Date().toISOString()
    });
    bookingDraftId = draft && draft.id ? draft.id : null;
  } catch (e) {
    // Supabase optional in dev — log and continue with a synthetic id.
    console.error('insertBookingDraft failed', e && e.message);
    bookingDraftId = `draft_${Date.now()}`;
  }

  let intent;
  try {
    intent = await createPaymentIntent({
      amountCents: totals.totalCents,
      metadata: {
        bookingDraftId: String(bookingDraftId),
        pickupDate: payload.pickupDate,
        city: payload.customer.city,
        zip: payload.customer.zip
      }
    });
  } catch (e) {
    console.error('Stripe create error', e && e.message);
    return json(res, 502, { error: true, message: 'payment provider error', code: 'stripe_error' });
  }

  return json(res, 200, {
    clientSecret: intent.client_secret,
    paymentIntentId: intent.id,
    totalAmount: totals.total,
    totalCents: totals.totalCents,
    bookingDraftId
  });
};
