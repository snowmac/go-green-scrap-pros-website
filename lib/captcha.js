'use strict';

async function verifyHCaptcha(token, remoteip) {
  const secret = process.env.HCAPTCHA_SECRET_KEY;
  if (!secret) {
    // Fail-closed if a token was supplied but no secret is configured —
    // we don't want to silently bypass CAPTCHA in production.
    return { success: false, error: 'hcaptcha not configured' };
  }
  if (!token) return { success: false, error: 'missing token' };

  const params = new URLSearchParams({ secret, response: token });
  if (remoteip) params.set('remoteip', remoteip);

  const res = await fetch('https://hcaptcha.com/siteverify', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: params.toString()
  });
  if (!res.ok) return { success: false, error: `hcaptcha http ${res.status}` };
  const j = await res.json();
  return { success: !!j.success, raw: j };
}

module.exports = { verifyHCaptcha };
