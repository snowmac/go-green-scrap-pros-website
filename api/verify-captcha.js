'use strict';

const { verifyHCaptcha } = require('../lib/captcha');
const { readJsonBody, setCors, json, clientIp } = require('./_helpers');

module.exports = async function handler(req, res) {
  setCors(res);
  if (req.method === 'OPTIONS') { res.statusCode = 204; return res.end(); }
  if (req.method !== 'POST') return json(res, 405, { error: true, message: 'method not allowed', code: 'method_not_allowed' });
  let payload;
  try { payload = await readJsonBody(req); }
  catch (e) { return json(res, 400, { error: true, message: 'invalid request body', code: 'bad_body' }); }

  const r = await verifyHCaptcha(payload.token, clientIp(req));
  return json(res, r.success ? 200 : 400, { success: !!r.success });
};
