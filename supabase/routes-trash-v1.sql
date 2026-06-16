-- =========================================================================
-- SCRAP-MAP / routes-trash V1 — scouting_pins schema + storage bucket
-- =========================================================================
-- Paste this whole file into the Supabase SQL editor and run once.
-- Project: ipxhrlbnimarslpeuuaz
-- Frontend: /routes-trash/index.html (publishable key only, no secrets)
--
-- This file is idempotent enough to paste twice without exploding, but the
-- create-policy statements use DROP-then-CREATE so you can re-run safely.
--
-- !!! V1 SECURITY MODEL — READ BEFORE PRODUCTION !!!
-- The /routes-trash page is a hidden (noindex) internal operations dashboard
-- shared by a small ops crew. V1 uses the publishable anon key from the
-- browser and *anonymous* RLS policies. Anyone who learns the URL + the
-- publishable key can read/write scouting pins.
--
-- Acceptable risk for V1 because:
--   * the page is noindex/private
--   * no PII or customer data lives in scouting_pins
--   * pin data is operational, low-stakes, and easy to clean up
--
-- DO NOT leave these anon policies on once real customer data, payouts,
-- crew identities, or anything sensitive flows through here. Replace the
-- anon policies with `auth.uid()`-based policies, move to Supabase Auth
-- (magic link or password), and tighten the storage bucket to authed
-- uploads + signed-URL reads. There is a "TIGHTEN LATER" section near
-- the bottom with the rough shape of what V2 should look like.
-- =========================================================================


-- -------------------------------------------------------------------------
-- 0. Extensions
-- -------------------------------------------------------------------------
-- gen_random_uuid() needs pgcrypto. Supabase usually pre-enables it but
-- this CREATE EXTENSION is a no-op if it's already there.
create extension if not exists pgcrypto;

-- PostGIS is optional for V1. If you want to query "pins within X meters of
-- this lat/lng" cheaply later, uncomment the next line and the geog column
-- block further down. V1 uses plain lat/lng columns and a btree index, which
-- is enough for "give me pins for district 3 this week".
-- create extension if not exists postgis;


-- -------------------------------------------------------------------------
-- 1. scouting_pins table
-- -------------------------------------------------------------------------
create table if not exists public.scouting_pins (
  id               uuid primary key default gen_random_uuid(),

  -- Geography (V1: plain numerics; see optional PostGIS block below)
  lat              double precision not null,
  lng              double precision not null,

  -- Denver LIP routing context — populated by the frontend from the
  -- currently-active district/week/day so the pin is searchable by shift.
  district         integer,
  trash_day        text,    -- 'MO' | 'TU' | 'WE' | 'TH' | 'FR' | combo codes
  route            text,    -- raw NEW_TRASH_ROUTE value
  setout_code      text,    -- raw NEW_TRASH_SETOUT value (A, C, ES, NS, ...)
  service_week     date,    -- the Monday of the operational week

  -- Operational state
  status           text not null default 'new'
                     check (status in ('new', 'checked', 'picked', 'skip')),
  material_type    text,    -- free text for V1: 'steel', 'appliance', 'mixed', ...
  estimated_value  numeric(10, 2),
  notes            text,

  -- Photo (optional, Supabase Storage bucket "scouting-photos")
  photo_path       text,    -- e.g. "2026/05/18/<uuid>.jpg" inside the bucket
  photo_url        text,    -- cached public URL (only meaningful if bucket is public)

  -- Audit
  created_at       timestamptz not null default now(),
  updated_at       timestamptz not null default now()
);

comment on table public.scouting_pins is
  'SCRAP-MAP V1 scouting pins for /routes-trash. Operator-entered, low-stakes, anon-writable. Do not store PII here.';

-- updated_at trigger so any UPDATE refreshes it without the client needing
-- to remember.
create or replace function public.scouting_pins_touch_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at := now();
  return new;
end;
$$;

drop trigger if exists trg_scouting_pins_touch on public.scouting_pins;
create trigger trg_scouting_pins_touch
  before update on public.scouting_pins
  for each row execute function public.scouting_pins_touch_updated_at();


-- -------------------------------------------------------------------------
-- 2. Indexes
-- -------------------------------------------------------------------------
-- Most common query: "active district + active week, optionally a day".
create index if not exists scouting_pins_district_week_day_idx
  on public.scouting_pins (district, service_week, trash_day);

-- Status filter (e.g. "show me everything still 'new'").
create index if not exists scouting_pins_status_idx
  on public.scouting_pins (status);

-- created_at for default ordering / recent activity.
create index if not exists scouting_pins_created_at_idx
  on public.scouting_pins (created_at desc);

-- Cheap geographic-ish lookup: btree on (lat, lng) lets us bound boxes.
-- Not a real spatial index — fine for a few thousand pins. Upgrade to
-- PostGIS GIST when this gets big.
create index if not exists scouting_pins_lat_lng_idx
  on public.scouting_pins (lat, lng);


-- -------------------------------------------------------------------------
-- 2b. (Optional) PostGIS geography column
-- -------------------------------------------------------------------------
-- Uncomment this block AFTER enabling the postgis extension above if you
-- want true spatial queries (ST_DWithin, ST_Distance, etc).
--
-- alter table public.scouting_pins
--   add column if not exists geog geography(point, 4326)
--     generated always as (st_setsrid(st_makepoint(lng, lat), 4326)::geography) stored;
--
-- create index if not exists scouting_pins_geog_idx
--   on public.scouting_pins using gist (geog);


-- -------------------------------------------------------------------------
-- 3. Row Level Security
-- -------------------------------------------------------------------------
alter table public.scouting_pins enable row level security;

-- !!! V1 ANON POLICIES — REPLACE BEFORE STORING ANYTHING SENSITIVE !!!
-- These let the publishable key in the browser do CRUD against
-- scouting_pins. That is the entire point of V1 (no auth, no friction)
-- but it also means anyone who finds the URL + key can scribble on
-- this table. See the TIGHTEN LATER section at the bottom.

drop policy if exists scouting_pins_anon_select on public.scouting_pins;
create policy scouting_pins_anon_select
  on public.scouting_pins
  for select
  to anon, authenticated
  using (true);

drop policy if exists scouting_pins_anon_insert on public.scouting_pins;
create policy scouting_pins_anon_insert
  on public.scouting_pins
  for insert
  to anon, authenticated
  with check (true);

drop policy if exists scouting_pins_anon_update on public.scouting_pins;
create policy scouting_pins_anon_update
  on public.scouting_pins
  for update
  to anon, authenticated
  using (true)
  with check (true);

drop policy if exists scouting_pins_anon_delete on public.scouting_pins;
create policy scouting_pins_anon_delete
  on public.scouting_pins
  for delete
  to anon, authenticated
  using (true);


-- -------------------------------------------------------------------------
-- 4. Storage bucket: scouting-photos
-- -------------------------------------------------------------------------
-- Public bucket so popups can show a plain <img src> without signing
-- every URL. Files are scouting photos of curbs/alleys — no PII expected.
-- Tighten to private + signed URLs in V2.

insert into storage.buckets (id, name, public)
  values ('scouting-photos', 'scouting-photos', true)
on conflict (id) do update set public = excluded.public;

-- !!! V1 ANON STORAGE POLICIES — REPLACE BEFORE PRODUCTION !!!
drop policy if exists scouting_photos_anon_select on storage.objects;
create policy scouting_photos_anon_select
  on storage.objects
  for select
  to anon, authenticated
  using (bucket_id = 'scouting-photos');

drop policy if exists scouting_photos_anon_insert on storage.objects;
create policy scouting_photos_anon_insert
  on storage.objects
  for insert
  to anon, authenticated
  with check (bucket_id = 'scouting-photos');

-- Allowing anon delete is convenient for "I uploaded the wrong photo"
-- flows but is also the most abusable policy here. Keep it for V1, drop
-- in V2.
drop policy if exists scouting_photos_anon_delete on storage.objects;
create policy scouting_photos_anon_delete
  on storage.objects
  for delete
  to anon, authenticated
  using (bucket_id = 'scouting-photos');


-- =========================================================================
-- TIGHTEN LATER (V2 sketch — DO NOT RUN AS-IS, this is a checklist)
-- =========================================================================
-- 1. Turn on Supabase Auth (magic-link is enough for an ops crew).
-- 2. Add an `owner uuid references auth.users(id)` column to scouting_pins
--    and default it to auth.uid() on insert.
-- 3. Drop every "anon" policy above and replace with:
--      using (auth.role() = 'authenticated')
--    or, for write paths:
--      using (owner = auth.uid()) with check (owner = auth.uid())
-- 4. Flip the storage bucket back to private (public=false), drop the anon
--    storage policies, and switch the frontend to createSignedUrl() for
--    reads.
-- 5. Consider a separate `scouting_pin_events` table for status changes if
--    you ever need an audit trail of "who marked this skipped and when".
-- =========================================================================
