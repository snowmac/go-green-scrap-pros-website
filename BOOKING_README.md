# Booking + Prepayment

Customer-facing booking and prepayment page lives at `/booking.html`. The form
talks to Vercel serverless functions in `/api/*`. Shared logic is in `/lib/*`.

## Endpoints

- `POST /api/create-payment-intent` — validates payload, recalculates total
  server-side at the Thornton tax rate (8.5%), creates a Stripe PaymentIntent,
  inserts a `booking_drafts` row, returns `{ clientSecret, paymentIntentId,
  totalAmount, totalCents, bookingDraftId }`.
- `POST /api/submit-booking` — verifies hCaptcha, retrieves the PaymentIntent,
  confirms `status === 'succeeded'` and amount matches a fresh recalculation,
  writes the `bookings` row, sends customer + owner email and SMS, creates a
  Google Calendar event. Notification/calendar failures do not fail the
  booking. Returns `{ success, bookingId, confirmationNumber }`.
- `POST /api/verify-captcha` — optional standalone hCaptcha check.
- `GET  /api/public-config` — returns client-safe values (Stripe publishable
  key, hCaptcha site key, tax rate). The static page calls this on load so
  keys stay out of the HTML.

All errors are `{ error: true, message, code }` with no internals.

## Pricing

- Junk / furniture: $75 per quantity, max 20 per item.
- Scrap metal & appliances: flat $50 if any selected (includes
  refrigerators, freezers, washers, dryers, dishwashers, stoves,
  microwaves, water heaters, AC units alongside ferrous/non-ferrous metals).
- E-waste: flat $50 if any selected.
- Sales tax: 8.5% (Thornton — the licensing city, not the pickup city).
  Override via `TAX_RATE_DEFAULT`.
- Confirmation numbers look like `GGS-YYYYMMDD-XXXX`.

## Pickup dates

Mon/Wed/Fri only, ≥48 h from now, ≤14 d out. Day-of-week test runs in
America/Denver. Calendar event is 8 AM – 12 PM MT on that date.

## Local dev

```bash
npm install
npm run syntax       # require()s every module to catch parse errors
npm test             # runs lib/pricing + lib/validation tests
```

To run end-to-end locally use the Vercel CLI: `vercel dev`. Without it the
static site still serves via the existing `serve.sh`, but `/api/*` won't run.

## Required environment variables

See `.env.example`. Server-only keys: `STRIPE_SECRET_KEY`,
`SUPABASE_SERVICE_ROLE_KEY`, `RESEND_API_KEY`, Twilio creds,
`GOOGLE_SERVICE_ACCOUNT_JSON`, `HCAPTCHA_SECRET_KEY`. Client-safe keys:
`STRIPE_PUBLISHABLE_KEY`, `HCAPTCHA_SITE_KEY` (served via
`/api/public-config`).

## Database

Run `supabase/bookings.sql` in the Supabase SQL editor. RLS is on; there are
no public policies, so only the service-role key (used server-side) can read
or write.

## Notes / tradeoffs

- The static booking page reads its public config from `/api/public-config` at
  load time. This avoids baking keys into the HTML and avoids a build step.
- Resend is the default email provider per the brief. Adding SendGrid would
  require a small adapter; not done.
- The PaymentIntent is recreated whenever the cart total changes (debounced).
  This keeps the Stripe-side amount in sync with the cart.
- A soft "ZIP looks like a different city" warning fires for known ZIPs but
  never blocks submission — only the explicit "Other / Not Listed" choice
  blocks.
- All notification calls use `Promise.allSettled` so a Twilio outage does not
  fail an otherwise-confirmed booking.
