-- Go Green Scrap Pros — booking schema
-- Run in the Supabase SQL editor.

create extension if not exists "pgcrypto";

create table if not exists public.booking_drafts (
  id uuid primary key default gen_random_uuid(),
  customer jsonb not null,
  pickup_date date not null,
  junk jsonb not null default '{}'::jsonb,
  scrap jsonb not null default '{}'::jsonb,
  ewaste jsonb not null default '{}'::jsonb,
  totals jsonb not null,
  created_at timestamptz not null default now()
);

create table if not exists public.bookings (
  id uuid primary key default gen_random_uuid(),
  confirmation_number text not null unique,
  payment_intent_id text not null unique,
  amount_cents integer not null check (amount_cents > 0),
  customer jsonb not null,
  pickup_date date not null,
  junk jsonb not null default '{}'::jsonb,
  scrap jsonb not null default '{}'::jsonb,
  ewaste jsonb not null default '{}'::jsonb,
  totals jsonb not null,
  created_at timestamptz not null default now()
);

create index if not exists bookings_pickup_date_idx on public.bookings (pickup_date);
create index if not exists bookings_created_at_idx  on public.bookings (created_at);

-- Enable RLS. The service role key bypasses RLS, so the API can still
-- read/write. We intentionally add NO public policies — anon/auth users
-- get nothing.
alter table public.booking_drafts enable row level security;
alter table public.bookings       enable row level security;
