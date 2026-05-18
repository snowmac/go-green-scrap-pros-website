'use strict';

async function sendSms({ to, body }) {
  const sid = process.env.TWILIO_ACCOUNT_SID;
  const token = process.env.TWILIO_AUTH_TOKEN;
  const from = process.env.TWILIO_FROM_NUMBER;
  if (!sid || !token || !from || !to) {
    return { skipped: true, reason: 'twilio not configured' };
  }

  const auth = Buffer.from(`${sid}:${token}`).toString('base64');
  const params = new URLSearchParams({ To: to, From: from, Body: body });
  const res = await fetch(`https://api.twilio.com/2010-04-01/Accounts/${sid}/Messages.json`, {
    method: 'POST',
    headers: {
      'Authorization': `Basic ${auth}`,
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: params.toString()
  });
  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(`Twilio send failed: ${res.status} ${text}`);
  }
  return res.json();
}

function renderCustomerSms(b) {
  return `Go Green Scrap Pros: pickup ${b.confirmationNumber} confirmed for ${b.pickupDateHuman}. Total $${b.totals.total.toFixed(2)}. Curbside by 8 AM. 720-675-7693`;
}

function renderOwnerSms(b) {
  return `New GGS booking ${b.confirmationNumber}: ${b.customer.firstName} ${b.customer.lastName} ${b.customer.city} ${b.pickupDateHuman} $${b.totals.total.toFixed(2)}`;
}

module.exports = { sendSms, renderCustomerSms, renderOwnerSms };
