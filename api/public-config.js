'use strict';

const { setCors, json } = require('./_helpers');

// Exposes only client-safe values. Lets the static booking page learn the
// hCaptcha site key and Stripe publishable key without baking them in.
module.exports = function handler(req, res) {
  setCors(res);
  if (req.method === 'OPTIONS') { res.statusCode = 204; return res.end(); }
  if (req.method !== 'GET') return json(res, 405, { error: true, message: 'method not allowed', code: 'method_not_allowed' });

  return json(res, 200, {
    hcaptchaSiteKey: process.env.HCAPTCHA_SITE_KEY || process.env.NEXT_PUBLIC_HCAPTCHA_SITE_KEY || '',
    stripePublishableKey: process.env.STRIPE_PUBLISHABLE_KEY || '',
    taxRate: parseFloat(process.env.TAX_RATE_DEFAULT || '0.085')
  });
};
