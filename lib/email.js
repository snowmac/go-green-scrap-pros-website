'use strict';

// Resend-based email. Falls back to no-op if RESEND_API_KEY not set,
// so partial config does not break the booking flow.

async function sendEmail({ to, subject, html, text, from }) {
  const apiKey = process.env.RESEND_API_KEY;
  const sender = from || process.env.EMAIL_FROM;
  if (!apiKey || !sender) {
    return { skipped: true, reason: 'email not configured' };
  }
  const res = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      from: sender,
      to: Array.isArray(to) ? to : [to],
      subject,
      html,
      text
    })
  });
  if (!res.ok) {
    const body = await res.text().catch(() => '');
    throw new Error(`Resend send failed: ${res.status} ${body}`);
  }
  return res.json();
}

function renderCustomerEmail(b) {
  const safe = (s) => String(s == null ? '' : s).replace(/[<>]/g, '');
  const lines = [];
  lines.push(`<h2>Pickup confirmed — ${safe(b.confirmationNumber)}</h2>`);
  lines.push(`<p>Hi ${safe(b.customer.firstName)}, thanks for booking with Go Green Scrap Pros.</p>`);
  lines.push(`<p><strong>Pickup date:</strong> ${safe(b.pickupDateHuman)}</p>`);
  lines.push(`<p><strong>Address:</strong> ${safe(b.customer.address)}, ${safe(b.customer.city)}, CO ${safe(b.customer.zip)}</p>`);
  lines.push(`<p><strong>Total charged:</strong> $${b.totals.total.toFixed(2)}</p>`);
  lines.push(`<p><strong>Curbside Service Only:</strong> All items must be at the curb or end of the driveway by 8:00 AM on your scheduled pickup day. We are unable to enter homes, garages, or backyards.</p>`);
  lines.push(`<p>Questions? Call or text 720-675-7693.</p>`);
  return lines.join('\n');
}

function renderOwnerEmail(b) {
  const safe = (s) => String(s == null ? '' : s).replace(/[<>]/g, '');
  const itemsLine = [];
  if (b.totals.junkLines && b.totals.junkLines.length) {
    itemsLine.push(`Junk: ${b.totals.junkLines.map(l => `${l.key} x${l.qty}`).join(', ')}`);
  }
  if (b.totals.scrapKeys && b.totals.scrapKeys.length) itemsLine.push(`Scrap: ${b.totals.scrapKeys.join(', ')}`);
  if (b.totals.ewasteKeys && b.totals.ewasteKeys.length) itemsLine.push(`E-waste: ${b.totals.ewasteKeys.join(', ')}`);
  return `
    <h2>New booking ${safe(b.confirmationNumber)}</h2>
    <p>${safe(b.customer.firstName)} ${safe(b.customer.lastName)} — ${safe(b.customer.phone)} — ${safe(b.customer.email)}</p>
    <p>${safe(b.customer.address)}, ${safe(b.customer.city)}, CO ${safe(b.customer.zip)}</p>
    <p>Pickup: ${safe(b.pickupDateHuman)}</p>
    <p>Total: $${b.totals.total.toFixed(2)} (junk $${b.totals.junkTotal} / scrap $${b.totals.scrapTotal} / e-waste $${b.totals.ewasteTotal} / tax $${b.totals.tax.toFixed(2)})</p>
    <p>${safe(itemsLine.join(' | '))}</p>
    <p>PaymentIntent: ${safe(b.paymentIntentId)}</p>
  `;
}

module.exports = { sendEmail, renderCustomerEmail, renderOwnerEmail };
