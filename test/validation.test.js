'use strict';
const assert = require('assert');
const {
  validateBookingPayload, isValidPickupDate, isAllowedCity,
  generateConfirmationNumber
} = require('../lib/validation');

(function citiesOk(){
  assert.strictEqual(isAllowedCity('Thornton'), true);
  assert.strictEqual(isAllowedCity('__OTHER__'), false);
  assert.strictEqual(isAllowedCity(''), false);
})();

(function pickupDateRules(){
  assert.strictEqual(isValidPickupDate(''), false);
  assert.strictEqual(isValidPickupDate('notadate'), false);
  // 30 days in the future is past max
  const far = new Date(Date.now() + 30*24*3600*1000);
  const farStr = far.toISOString().slice(0,10);
  assert.strictEqual(isValidPickupDate(farStr), false);
})();

(function fullValidation(){
  const r = validateBookingPayload({
    customer: {
      firstName:'A', lastName:'B', email:'a@b.co', phone:'(720) 555-1234',
      address:'1 Main', city:'Thornton', state:'CO', zip:'80229'
    },
    pickupDate: '2020-01-01',
    junk: { sofa: 1 }
  });
  assert.strictEqual(r.ok, false);
  assert.ok(r.errors.find(e => e.toLowerCase().includes('pickup')));
})();

(function confNumberShape(){
  const c = generateConfirmationNumber(new Date(Date.UTC(2026,4,5)));
  assert.ok(/^GGS-2026[0-9]{4}-[A-Z0-9]{1,4}$/.test(c), 'shape: ' + c);
})();

console.log('validation.test.js ok');
