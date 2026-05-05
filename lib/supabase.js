'use strict';

let _client = null;

function getSupabase() {
  if (_client) return _client;
  const url = process.env.SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!url || !key) throw new Error('Supabase env vars missing (SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)');
  // eslint-disable-next-line global-require
  const { createClient } = require('@supabase/supabase-js');
  _client = createClient(url, key, {
    auth: { autoRefreshToken: false, persistSession: false }
  });
  return _client;
}

async function insertBookingDraft(draft) {
  const supabase = getSupabase();
  const { data, error } = await supabase
    .from('booking_drafts')
    .insert(draft)
    .select('id')
    .single();
  if (error) throw error;
  return data;
}

async function insertBooking(booking) {
  const supabase = getSupabase();
  const { data, error } = await supabase
    .from('bookings')
    .insert(booking)
    .select('id')
    .single();
  if (error) throw error;
  return data;
}

async function findBookingByPaymentIntent(paymentIntentId) {
  const supabase = getSupabase();
  const { data, error } = await supabase
    .from('bookings')
    .select('id, confirmation_number')
    .eq('payment_intent_id', paymentIntentId)
    .maybeSingle();
  if (error) throw error;
  return data;
}

module.exports = { getSupabase, insertBookingDraft, insertBooking, findBookingByPaymentIntent };
