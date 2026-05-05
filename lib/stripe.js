'use strict';

let _stripe = null;

function getStripe() {
  if (_stripe) return _stripe;
  const key = process.env.STRIPE_SECRET_KEY;
  if (!key) throw new Error('STRIPE_SECRET_KEY not configured');
  // eslint-disable-next-line global-require
  const Stripe = require('stripe');
  _stripe = Stripe(key, { apiVersion: '2024-06-20' });
  return _stripe;
}

async function createPaymentIntent({ amountCents, metadata }) {
  const stripe = getStripe();
  return stripe.paymentIntents.create({
    amount: amountCents,
    currency: 'usd',
    automatic_payment_methods: { enabled: true },
    metadata: metadata || {},
    description: 'Go Green Scrap Pros pickup'
  });
}

async function retrievePaymentIntent(id) {
  const stripe = getStripe();
  return stripe.paymentIntents.retrieve(id);
}

module.exports = { getStripe, createPaymentIntent, retrievePaymentIntent };
