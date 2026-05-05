'use strict';

// Google Calendar via service account JWT. Service account JSON is provided
// base64-encoded in GOOGLE_SERVICE_ACCOUNT_JSON; calendar in GOOGLE_CALENDAR_ID.

const crypto = require('crypto');

function loadServiceAccount() {
  const b64 = process.env.GOOGLE_SERVICE_ACCOUNT_JSON;
  if (!b64) return null;
  try {
    const json = Buffer.from(b64, 'base64').toString('utf8');
    return JSON.parse(json);
  } catch (e) {
    return null;
  }
}

function base64url(input) {
  return Buffer.from(input).toString('base64')
    .replace(/=+$/, '')
    .replace(/\+/g, '-')
    .replace(/\//g, '_');
}

async function getAccessToken(sa) {
  const now = Math.floor(Date.now() / 1000);
  const header = base64url(JSON.stringify({ alg: 'RS256', typ: 'JWT' }));
  const claim = base64url(JSON.stringify({
    iss: sa.client_email,
    scope: 'https://www.googleapis.com/auth/calendar',
    aud: 'https://oauth2.googleapis.com/token',
    iat: now,
    exp: now + 3600
  }));
  const signingInput = `${header}.${claim}`;
  const signer = crypto.createSign('RSA-SHA256');
  signer.update(signingInput);
  const sig = signer.sign(sa.private_key);
  const jwt = `${signingInput}.${base64url(sig)}`;

  const params = new URLSearchParams({
    grant_type: 'urn:ietf:params:oauth:grant-type:jwt-bearer',
    assertion: jwt
  });
  const res = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: params.toString()
  });
  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(`Google token error: ${res.status} ${text}`);
  }
  const j = await res.json();
  return j.access_token;
}

async function createCalendarEvent({ summary, description, dateStr, location }) {
  const calendarId = process.env.GOOGLE_CALENDAR_ID;
  const sa = loadServiceAccount();
  if (!sa || !calendarId) {
    return { skipped: true, reason: 'calendar not configured' };
  }
  const token = await getAccessToken(sa);

  // Pickup window: 8 AM – 12 PM Mountain Time on the pickup date.
  const event = {
    summary,
    description,
    location,
    start: { dateTime: `${dateStr}T08:00:00`, timeZone: 'America/Denver' },
    end:   { dateTime: `${dateStr}T12:00:00`, timeZone: 'America/Denver' }
  };

  const url = `https://www.googleapis.com/calendar/v3/calendars/${encodeURIComponent(calendarId)}/events`;
  const res = await fetch(url, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(event)
  });
  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(`Calendar insert failed: ${res.status} ${text}`);
  }
  return res.json();
}

module.exports = { createCalendarEvent };
