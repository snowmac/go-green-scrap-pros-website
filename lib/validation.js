'use strict';

const SERVICE_CITIES = [
  'Thornton', 'Arvada', 'Westminster', 'Golden',
  'Wheat Ridge', 'Broomfield', 'Northglenn'
];

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const PHONE_RE = /^\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$/;
const ZIP_RE = /^\d{5}$/;

function normalizePhone(p) {
  if (!p) return '';
  return String(p).replace(/\D+/g, '').slice(-10);
}

function isAllowedCity(city) {
  if (!city) return false;
  return SERVICE_CITIES.includes(String(city).trim());
}

// Pickup must be Mon/Wed/Fri, >=48h from now, <=14 days, in Mountain Time.
function isValidPickupDate(dateStr) {
  if (!dateStr || !/^\d{4}-\d{2}-\d{2}$/.test(dateStr)) return false;

  // Parse as Mountain Time noon to avoid TZ edge issues.
  const [y, m, d] = dateStr.split('-').map(Number);
  const pickupUtcNoon = new Date(Date.UTC(y, m - 1, d, 18, 0, 0)); // 12 MT ≈ 18 UTC (MDT)
  if (Number.isNaN(pickupUtcNoon.getTime())) return false;

  const now = Date.now();
  const minMs = now + 48 * 3600 * 1000;
  const maxMs = now + 14 * 24 * 3600 * 1000;
  if (pickupUtcNoon.getTime() < minMs) return false;
  if (pickupUtcNoon.getTime() > maxMs) return false;

  // Day-of-week in Mountain Time
  const mtFmt = new Intl.DateTimeFormat('en-US', { timeZone: 'America/Denver', weekday: 'short' });
  const wd = mtFmt.format(pickupUtcNoon);
  return ['Mon', 'Wed', 'Fri'].includes(wd);
}

function validateBookingPayload(payload) {
  const errors = [];
  const c = (payload && payload.customer) || {};

  if (!c.firstName || !String(c.firstName).trim()) errors.push('firstName required');
  if (!c.lastName || !String(c.lastName).trim()) errors.push('lastName required');
  if (!c.email || !EMAIL_RE.test(String(c.email).trim())) errors.push('valid email required');
  if (!c.phone || !PHONE_RE.test(String(c.phone).trim())) errors.push('valid US phone required');
  if (!c.address || !String(c.address).trim()) errors.push('street address required');
  if (!c.city || !isAllowedCity(c.city)) errors.push('service city not supported');
  if (c.state && String(c.state).toUpperCase() !== 'CO') errors.push('state must be CO');
  if (!c.zip || !ZIP_RE.test(String(c.zip).trim())) errors.push('5-digit ZIP required');

  if (!payload.pickupDate || !isValidPickupDate(payload.pickupDate)) {
    errors.push('pickup date must be a Mon/Wed/Fri at least 48 hours out and within 14 days');
  }

  const junk = (payload && payload.junk) || {};
  const scrap = (payload && payload.scrap) || {};
  const ewaste = (payload && payload.ewaste) || {};
  const hasJunk = Object.values(junk).some(v => parseInt(v, 10) > 0);
  const hasScrap = Object.values(scrap).some(Boolean);
  const hasEwaste = Object.values(ewaste).some(Boolean);
  if (!hasJunk && !hasScrap && !hasEwaste) errors.push('select at least one item');

  return { ok: errors.length === 0, errors };
}

function generateConfirmationNumber(date) {
  const d = date || new Date();
  const yyyy = d.getUTCFullYear();
  const mm = String(d.getUTCMonth() + 1).padStart(2, '0');
  const dd = String(d.getUTCDate()).padStart(2, '0');
  const rand = Math.random().toString(36).toUpperCase().replace(/[^A-Z0-9]/g, '').slice(0, 4) || 'XXXX';
  return `GGS-${yyyy}${mm}${dd}-${rand}`;
}

module.exports = {
  SERVICE_CITIES,
  validateBookingPayload,
  isValidPickupDate,
  isAllowedCity,
  normalizePhone,
  generateConfirmationNumber
};
