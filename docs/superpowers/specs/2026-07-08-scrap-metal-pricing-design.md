# Scrap Metal Pricing Design

## Business rule

Scrap metal pickup is no longer unconditionally free. It's free only when the load is a
qualifying high-value category — **commercial HVAC units, server racks, or pure copper/brass
batches** — confirmed by a photo texted to 720-675-7693 (the existing photo-first contact
pattern already used across the site, no new upload mechanism needed).

Everything else gets a distance-based dispatch fee from the Thornton hub:

| Zone | Distance | Fee |
|---|---|---|
| 1 | 0–15 mi | $35 |
| 2 | 16–30 mi | $65 |
| 3 | 31+ mi | $95 |

## Scope

**In scope:**
- `generate_pages.py`: rewrite the `scrap-metal-pickup` service entry (flip `price_free` →
  `False`, rewrite all prose fields), regenerate the 7 existing city pages
  (scrap-metal-pickup, +arvada/broomfield/golden/northglenn/thornton/westminster/wheat-ridge)
- `index.html`: update the Scrap Metal Pickup card, fold the separate Copper Pipe & Wire card
  into it, and fix two other "free scrap metal" mentions on the homepage (lines 181, 303)

**Out of scope (explicitly deferred):**
- TV/CRT surcharge, inside-pickup fee, public JS dispatch calculator — not part of this change
- Removing Loveland or Lyons — staying as-is, untouched
- Adding scrap-metal-pickup (or any other service) pages for the 13-15 cities that don't have
  one yet (Welby, Federal Heights, Sherrelwood, Derby, Brighton, Dacono, Frederick, Firestone,
  Gunbarrel, Boulder, Longmont, Niwot, Hygiene, plus Lyons/Loveland) — this is a separate,
  much larger follow-on project (full 9-service coverage was requested, ~104+ new pages) that
  needs real zip code and neighborhood data sourced and verified before it ships. Not
  attempted here.

## Zone reference table (all cities, for phone/text quoting)

All 7 cities with an existing scrap-metal-pickup page happen to fall in Zone 1, so this pass
only puts a $35 price on any live page. The full table below is recorded so Adam can quote
callers from anywhere in the service area accurately, and so the future city-expansion project
has zone assignments ready to go. Distances are driving miles from Thornton; zone assignments
are Adam's judgment call (factoring in real drive time/roads, not just mileage — e.g. Lyons is
37 mi but effectively farther by canyon road than raw distance suggests).

| Zone 1 — $35 | Zone 2 — $65 | Zone 3 — $95 | No service |
|---|---|---|---|
| Thornton * | Dacono | Brighton | Loveland |
| Northglenn * | Frederick | Gunbarrel | |
| Welby | Firestone | Boulder | |
| Federal Heights | | Longmont | |
| Sherrelwood | | Niwot | |
| Westminster * | | Hygiene | |
| Derby | | Lyons | |
| Broomfield * | | | |
| Arvada * | | | |
| Wheat Ridge * | | | |
| Golden * | | | |

\* = has an existing scrap-metal-pickup page today; gets the $35 fee in this pass.

## Content changes

### `generate_pages.py` — `SERVICES["scrap-metal-pickup"]`

Replace the entry (currently `generate_pages.py:615-674`) with:

```python
"scrap-metal-pickup": {
    "name": "Scrap Metal Pickup",
    "slug": "scrap-metal-pickup",
    "item": "scrap metal",
    "price_free": False,
    "short": "scrap metal pickup",
    "action": "Curbside scrap metal pickup — free for qualifying high-value loads, dispatch fee otherwise",
    "what_we_take": "Steel, aluminum, copper, brass, iron, old metal furniture, metal fencing, auto parts, and any other metal items",
    "schema_name": "Scrap Metal Pickup",
    "intro_templates": [
        (
            "Got scrap metal piling up in the garage, backyard, or on a job site in {city_name}? "
            "Text a photo to 720-675-7693 and we'll tell you the rate before we schedule anything. "
            "Commercial HVAC units, server racks, and clean copper or brass batches often qualify "
            "for free pickup. Everything else gets a flat, distance-based dispatch fee — starting at $35."
        ),
        (
            "Steel, aluminum, copper, brass, iron — old grills, metal shelving, car parts, fencing, "
            "pipes, wiring, appliance shells. We serve all of {city_name} including zip codes {zips_text}. "
            "High-value loads (HVAC units, server racks, clean copper/brass) may be picked up free; "
            "standard loads run $35-$95 based on distance from our Thornton hub."
        ),
        (
            "Whether you're in {neighborhoods_short} or anywhere else in {city_name}, scrap metal "
            "pickup starts with a photo. Text or call Adam at 720-675-7693 — we'll confirm your "
            "dispatch fee, or confirm it's free, before we're on the way. Usually same-day or next-day."
        ),
    ],
    "how_it_works": [
        ("Text a Photo & Address", "Send a photo of your scrap metal and your address to 720-675-7693. We need to see it before we can quote it."),
        ("Get Your Dispatch Quote", "We'll confirm your rate — free if it's a qualifying high-value load (commercial HVAC, server racks, clean copper/brass), or a flat dispatch fee ($35-$95) based on distance if not."),
        ("We Haul It Away", "We show up, load it up, and take it to the recycler. No surprises beyond the rate we quoted."),
    ],
    "why_choose": [
        "Free pickup for qualifying high-value loads — commercial HVAC units, server racks, clean copper/brass batches",
        "Flat, distance-based dispatch fee otherwise — $35 (0-15mi), $65 (16-30mi), $95 (31mi+) from our Thornton hub",
        "Steel, aluminum, copper, brass, iron — all accepted",
        "Your rate is confirmed by photo before we schedule — no guessing, no surprise charges",
        "Same-day and next-day pickup in {city_name}",
        "Locally owned — Adam is the one who shows up",
    ],
    "faqs": [
        ("Is scrap metal pickup free in {city_name}?",
         "It can be. Commercial HVAC units, server racks, and clean copper or brass batches often qualify for free pickup — text a photo to 720-675-7693 and we'll confirm. Everything else gets a flat dispatch fee based on distance, typically $35-$95."),
        ("What types of metal do you pick up?",
         "Steel, aluminum, copper, brass, iron, tin — basically all metals. Old grills, metal furniture, car parts, fencing, pipes, wiring, appliance shells, bed frames, filing cabinets — if it's metal, we want it."),
        ("Is there a minimum amount of scrap metal?",
         "No set minimum, but smaller general loads are more likely to carry the standard dispatch fee rather than qualify as free. Clean copper/brass in volume, commercial HVAC units, and server racks are what typically offsets the fee."),
        ("What {city_name} zip codes do you serve?",
         "All of {city_name} — zip codes {zips_text}. From {neighborhoods_two} and everywhere in between."),
        ("How quickly can you pick up scrap metal in {city_name}?",
         "Most pickups are same-day or next-day once we've confirmed your rate by photo. Call or text Adam at 720-675-7693 to get started."),
    ],
    "items_section": [
        "Steel, iron, and tin (any condition)",
        "Aluminum: cans, siding, gutters, frames",
        "Copper pipe, copper wire, brass fittings",
        "Mixed metal piles, old appliances, bed frames, fencing",
        "Commercial HVAC units, server racks, and clean copper/brass batches — may qualify for free pickup",
    ],
},
```

Flipping `price_free` to `False` also automatically fixes the page `<title>`, meta description,
OG tags, and JSON-LD `priceRange` (`$` → `$$`) via the existing `is_free` branches in
`generate_page()` — no changes needed there.

### `index.html`

1. **Line 181** — change:
   `We also offer free scrap metal pickup curbside because recycling metal is what we love.`
   to:
   `We also offer scrap metal pickup — free for qualifying high-value loads — because recycling metal is what we love.`

2. **Lines 247-257** — replace the two cards:
   ```html
   <div class="service-card-new">
     <div class="service-title">🔩 Scrap Metal Pickup</div>
     <div class="service-price">FREE Curbside</div>
     <div class="service-note">Steel, aluminum, brass, copper — no charge at the curb</div>
   </div>

   <div class="service-card-new">
     <div class="service-title">🔧 Copper Pipe &amp; Wire</div>
     <div class="service-price">FREE</div>
     <div class="service-note">Pre-separated or piled at curb</div>
   </div>
   ```
   with a single merged card:
   ```html
   <div class="service-card-new">
     <div class="service-title">🔩 Scrap Metal Pickup</div>
     <div class="service-price">$35–$95 Dispatch Fee</div>
     <div class="service-note">Free for qualifying loads — HVAC, server racks, clean copper &amp; brass</div>
   </div>
   ```

3. **Line 303** — change:
   `appliance haul-away, and free scrap metal pickup, with a dedicated page for each city.`
   to:
   `appliance haul-away, and scrap metal pickup, with a dedicated page for each city.`

## Build & deploy

After the `generate_pages.py` edit, run the generator to regenerate the 7 affected city pages,
diff the output to confirm only the scrap-metal-pickup pages changed, then commit, push, and
let the existing deploy pipeline pick it up.

## Explicitly not done in this pass

- `drafts/is-scrap-metal-pickup-free.md` (unpublished, scheduled 2027-09-07) describes the old
  unconditional-free model and will read as contradictory once published. Flagged, not edited.
- No zip/neighborhood data was fabricated for the 13-15 cities without a scrap page — that data
  will be sourced (publicly, then user-verified) as part of the separate expansion project.
