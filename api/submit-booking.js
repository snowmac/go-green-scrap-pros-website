'use strict';

const { calculate } = require('../lib/pricing');
const { validateBookingPayload, generateConfirmationNumber } = require('../lib/validation');
const { retrievePaymentIntent } = require('../lib/stripe');
const { insertBooking, findBookingByPaymentIntent } = require('../lib/supabase');
const { verifyHCaptcha } = require('../lib/captcha');
const { sendEmail, renderCustomerEmail, renderOwnerEmail } = require('../lib/email');
const { sendSms, renderCustomerSms, renderOwnerSms } = require('../lib/sms');
const { createCalendarEvent } = require('../lib/calendar');
const { readJsonBody, setCors, json, clientIp, humanDate } = require('./_helpers');

module.exports = async function handler(req, res) {
  setCors(res);
  if (req.method === 'OPTIONS') { res.statusCode = 204; return res.end(); }
  if (req.method !== 'POST') return json(res, 405, { error: true, message: 'method not allowed', code: 'method_not_allowed' });

  let payload;
  try { payload = await readJsonBody(req); }
  catch (e) { return json(res, 400, { error: true, message: 'invalid request body', code: 'bad_body' }); }

  const captcha = await verifyHCaptcha(payload.captchaToken, clientIp(req));
  if (!captcha.success) {
    return json(res, 400, { error: true, message: 'captcha verification failed', code: 'captcha_failed' });
  }

  const v = validateBookingPayload(payload);
  if (!v.ok) return json(res, 400, { error: true, message: 'validation failed', code: 'validation_failed', details: v.errors });

  const totals = calculate(payload);
  if (!totals.totalCents || totals.totalCents <= 0) {
    return json(res, 400, { error: true, message: 'order total must be greater than zero', code: 'zero_total' });
  }

  if (!payload.paymentIntentId) {
    return json(res, 400, { error: true, message: 'paymentIntentId required', code: 'missing_pi' });
  }

  let intent;
  try {
    intent = await retrievePaymentIntent(payload.paymentIntentId);
  } catch (e) {
    console.error('retrievePaymentIntent failed', e && e.message);
    return json(res, 400, { error: true, message: 'payment intent not found', code: 'pi_not_found' });
  }

  if (!intent || intent.status !== 'succeeded') {
    return json(res, 400, { error: true, message: 'payment not completed', code: 'pi_not_succeeded' });
  }
  if (intent.amount !== totals.totalCents) {
    return json(res, 400, { error: true, message: 'payment amount mismatch', code: 'amount_mismatch' });
  }

  // Idempotency: if a booking with this PI already exists, return it.
  try {
    const existing = await findBookingByPaymentIntent(intent.id);
    if (existing && existing.id) {
      return json(res, 200, { success: true, bookingId: existing.id, confirmationNumber: existing.confirmation_number });
    }
  } catch (e) { /* non-fatal */ }

  const confirmationNumber = generateConfirmationNumber();
  let bookingId = null;
  try {
    const inserted = await insertBooking({
      confirmation_number: confirmationNumber,
      payment_intent_id: intent.id,
      amount_cents: intent.amount,
      customer: payload.customer,
      pickup_date: payload.pickupDate,
      junk: payload.junk || {},
      scrap: payload.scrap || {},
      ewaste: payload.ewaste || {},
      totals,
      created_at: new Date().toISOString()
    });
    bookingId = inserted && inserted.id ? inserted.id : null;
  } catch (e) {
    console.error('insertBooking failed', e && e.message);
    return json(res, 500, { error: true, message: 'could not save booking', code: 'db_error' });
  }

  const enriched = {
    confirmationNumber,
    paymentIntentId: intent.id,
    customer: payload.customer,
    pickupDate: payload.pickupDate,
    pickupDateHuman: humanDate(payload.pickupDate),
    totals
  };

  // Best-effort notifications. Failures here MUST NOT fail the booking.
  const notifications = await Promise.allSettled([
    sendEmail({
      to: payload.customer.email,
      subject: `Pickup confirmed — ${confirmationNumber}`,
      html: renderCustomerEmail(enriched)
    }),
    process.env.OWNER_EMAIL ? sendEmail({
      to: process.env.OWNER_EMAIL,
      subject: `New booking ${confirmationNumber}`,
      html: renderOwnerEmail(enriched)
    }) : Promise.resolve({ skipped: true }),
    sendSms({ to: `+1${String(payload.customer.phone).replace(/\D/g, '')}`, body: renderCustomerSms(enriched) }),
    process.env.OWNER_BUSINESS_PHONE ? sendSms({ to: process.env.OWNER_BUSINESS_PHONE, body: renderOwnerSms(enriched) }) : Promise.resolve({ skipped: true }),
    createCalendarEvent({
      summary: `Pickup ${confirmationNumber} — ${payload.customer.firstName} ${payload.customer.lastName}`,
      description: `Total $${totals.total.toFixed(2)}\n${payload.customer.phone} ${payload.customer.email}\n${JSON.stringify({ junk: payload.junk, scrap: payload.scrap, ewaste: payload.ewaste })}`,
      dateStr: payload.pickupDate,
      location: `${payload.customer.address}, ${payload.customer.city}, CO ${payload.customer.zip}`
    })
  ]);
  notifications.forEach((r, i) => {
    if (r.status === 'rejected') console.error(`notification ${i} failed`, r.reason && r.reason.message);
  });

  return json(res, 200, { success: true, bookingId, confirmationNumber });
};
