#!/usr/bin/env python3
"""
Generate 56 city+service HTML pages for Go Green Scrap Pros.
8 services x 7 cities = 56 unique pages.

Note: Most services intentionally don't render an exact price - pages drive
visitors toward calling/texting for a quote. Where a service does publish a
number (scrap metal, TV recycling), it's pulled from pricing.json, the single
source of truth also used to render the templated static pages in templates/
(see render_pricing_templates() below). Edit pricing.json, not prices inline.
"""
import os
import json
import datetime
import glob

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(_BASE_DIR, "pricing.json")) as _f:
    PRICING = json.load(_f)

# ─── City Data ───────────────────────────────────────────────────────────────
CITIES = {
    "thornton": {
        "name": "Thornton",
        "slug": "thornton",
        "zips": ["80229", "80233", "80241"],
        "lat": 39.8680,
        "lng": -104.9719,
        "neighborhoods": [
            "Eastlake", "Todd Creek", "Hunters Glen", "Thorncreek",
            "North End", "Trail Creek", "Woodglen", "Cherrywood Park"
        ],
        "flavor": "one of the fastest-growing cities along the I-25 corridor north of Denver",
        "housing": "a mix of established 1970s–90s subdivisions and brand-new master-planned communities in the north end",
        "nearby": ["northglenn", "westminster", "broomfield"],
        "scrap_zone": 1,
    },
    "arvada": {
        "name": "Arvada",
        "slug": "arvada",
        "zips": ["80002", "80003", "80004", "80005"],
        "lat": 39.8028,
        "lng": -105.0875,
        "neighborhoods": [
            "Olde Town Arvada", "Ralston Valley", "West Woods", "Leyden Rock",
            "Candelas", "Arvada Ridge", "Quaker Acres", "Scenic Heights"
        ],
        "flavor": "a charming city blending historic Olde Town character with modern growth stretching west toward the foothills",
        "housing": "established neighborhoods near Olde Town alongside newer developments like Candelas and Leyden Rock",
        "nearby": ["wheat-ridge", "westminster", "golden"],
        "scrap_zone": 1,
    },
    "westminster": {
        "name": "Westminster",
        "slug": "westminster",
        "zips": ["80030", "80031", "80234", "80235"],
        "lat": 39.8367,
        "lng": -105.0372,
        "neighborhoods": [
            "Downtown Westminster", "Bradburn Village", "The Orchard",
            "Hyland Hills", "Shaw Heights", "Countryside", "Sheridan Green", "Kings Mill"
        ],
        "flavor": "a thriving suburb straddling the Adams-Jefferson county line with easy access to both Denver and Boulder",
        "housing": "a diverse housing stock ranging from mid-century ranches near the southern border to contemporary builds around the revitalized downtown",
        "nearby": ["arvada", "thornton", "broomfield"],
        "scrap_zone": 1,
    },
    "golden": {
        "name": "Golden",
        "slug": "golden",
        "zips": ["80401", "80403"],
        "lat": 39.7555,
        "lng": -105.2211,
        "neighborhoods": [
            "Downtown Golden", "North Table Mountain", "Fossil Trace",
            "Mesa Meadows", "Pleasant View", "Coal Creek Canyon", "Applewood", "Fairmount"
        ],
        "flavor": "a mountain-town-meets-suburb nestled right at the foothills with the Colorado School of Mines at its heart",
        "housing": "a unique blend of historic downtown bungalows, hillside homes with views, and newer planned communities like Fossil Trace",
        "nearby": ["wheat-ridge", "arvada", "westminster"],
        "scrap_zone": 1,
    },
    "wheat-ridge": {
        "name": "Wheat Ridge",
        "slug": "wheat-ridge",
        "zips": ["80033"],
        "lat": 39.7664,
        "lng": -105.0772,
        "neighborhoods": [
            "Kullerstrand", "Panorama Park", "Wilmore-Davis",
            "Paramount Heights", "Anderson Park", "Leppla Park", "Fruitdale", "Youngfield"
        ],
        "flavor": "a small-town-feel city tucked between Arvada, Lakewood, and Denver with surprisingly deep roots as a farming community",
        "housing": "predominantly mid-century ranch homes and split-levels built in the 1950s–70s, many now seeing renovation and updates",
        "nearby": ["arvada", "golden", "westminster"],
        "scrap_zone": 1,
    },
    "broomfield": {
        "name": "Broomfield",
        "slug": "broomfield",
        "zips": ["80021", "80023", "80038"],
        "lat": 39.9206,
        "lng": -105.0867,
        "neighborhoods": [
            "Interlocken", "Broadlands", "Anthem Highlands",
            "McKay Landing", "Wildgrass", "Baseline", "Highland Park", "Eagle Trace"
        ],
        "flavor": "a unique city-county hybrid along the US-36 tech corridor with rapid residential growth and a master-planned, suburban feel",
        "housing": "newer construction dominated by 2000s-era planned communities like Broadlands and Anthem alongside the Interlocken business park area",
        "nearby": ["westminster", "thornton", "arvada"],
        "scrap_zone": 1,
    },
    "northglenn": {
        "name": "Northglenn",
        "slug": "northglenn",
        "zips": ["80233", "80234"],
        "lat": 39.8853,
        "lng": -104.9872,
        "neighborhoods": [
            "Northglenn Marketplace", "Malley Park", "Croke Reservoir",
            "Jaycee Park", "Fox Run", "Huron Heights", "Community Center area", "Wagon Road"
        ],
        "flavor": "a compact, friendly suburb directly north of Denver along I-25 with a strong sense of community pride",
        "housing": "mostly 1960s–80s single-family homes and townhomes built during the original suburban boom, with some infill development near the civic center",
        "nearby": ["thornton", "westminster", "broomfield"],
        "scrap_zone": 1,
    },
    "welby": {
        "name": "Welby",
        "slug": "welby",
        "zips": ["80229"],
        "lat": 39.8483,
        "lng": -104.9614,
        "neighborhoods": ["Rotella Park", "Perl Mack Manor"],
        "flavor": "an unincorporated Adams County community just north of Denver proper, a working-class mix of ranch homes, mobile-home communities, and light industrial areas along the I-25/I-270 corridor",
        "housing": "long-established ranch homes and mobile-home communities near Rotella Park",
        "nearby": ["thornton", "federal-heights", "northglenn"],
        "scrap_zone": 1,
    },
    "federal-heights": {
        "name": "Federal Heights",
        "slug": "federal-heights",
        "zips": ["80260", "80221", "80234"],
        "lat": 39.8583,
        "lng": -105.0128,
        "neighborhoods": ["Holiday Hills", "Northborough Heights"],
        "flavor": "a small home-rule city in western Adams County - Denver's northern doorstep - known locally for the Water World park and a mostly mid-century housing stock",
        "housing": "1960s-70s split-level and bi-level ranch homes, with the Holiday Hills 55+ community and Northborough Heights among the established named areas",
        "nearby": ["westminster", "northglenn", "welby"],
        "scrap_zone": 1,
    },
    "sherrelwood": {
        "name": "Sherrelwood",
        "slug": "sherrelwood",
        "zips": ["80221"],
        "lat": 39.8228,
        "lng": -105.0089,
        "neighborhoods": ["Sherrelwood Estates", "Perl Mack"],
        "flavor": "a dense, established unincorporated neighborhood in Adams County bordering Westminster, with mostly 1950s-70s single-family housing",
        "housing": "1950s-70s single-family homes in the Sherrelwood Estates area and the historic Perl Mack subdivision",
        "nearby": ["westminster", "welby", "federal-heights"],
        "scrap_zone": 1,
    },
    "brighton": {
        "name": "Brighton",
        "slug": "brighton",
        "zips": ["80601", "80602", "80603", "80640"],
        "lat": 39.9853,
        "lng": -104.8206,
        "neighborhoods": ["Prairie Center", "Eagle Shadow North", "Eagle Shadow South", "Historic Downtown Brighton"],
        "flavor": "an agricultural-heritage city turned fast-growing Denver-metro suburb along the South Platte River and I-76 corridor",
        "housing": "new master-planned growth around Prairie Center and Eagle Shadow alongside the walkable historic downtown core",
        "nearby": ["thornton", "dacono", "frederick"],
        "scrap_zone": 3,
    },
    "dacono": {
        "name": "Dacono",
        "slug": "dacono",
        "zips": ["80514"],
        "lat": 40.0631,
        "lng": -104.9358,
        "neighborhoods": ["Sweetgrass", "Autumn Valley", "Village at Palisade Park", "Carriage Square"],
        "flavor": "a small, fast-growing Weld County city in the Carbon Valley, historically a coal-mining and farming town now filling in with new-construction subdivisions",
        "housing": "newer master-planned communities like Sweetgrass alongside the older town core",
        "nearby": ["frederick", "firestone", "brighton"],
        "scrap_zone": 2,
    },
    "frederick": {
        "name": "Frederick",
        "slug": "frederick",
        "zips": ["80530", "80504", "80516"],
        "lat": 40.0983,
        "lng": -104.9497,
        "neighborhoods": ["Wyndham Hill", "Hidden Creek"],
        "flavor": "a fast-growing Weld County town in the Carbon Valley, spanning a patchwork of zip codes as new subdivisions fill in the land between I-25 and Highway 52",
        "housing": "newer subdivisions like Wyndham Hill and Hidden Creek filling in around the historic town core",
        "nearby": ["firestone", "dacono", "longmont"],
        "scrap_zone": 2,
    },
    "firestone": {
        "name": "Firestone",
        "slug": "firestone",
        "zips": ["80520", "80504"],
        "lat": 40.1097,
        "lng": -104.9425,
        "neighborhoods": ["Barefoot Lakes", "Saddleback"],
        "flavor": "a small, rapidly-expanding Weld County town off I-25 in the Carbon Valley, filling with new master-planned subdivisions",
        "housing": "new-construction communities like Barefoot Lakes alongside the established Saddleback area",
        "nearby": ["frederick", "dacono", "longmont"],
        "scrap_zone": 2,
    },
    "gunbarrel": {
        "name": "Gunbarrel",
        "slug": "gunbarrel",
        "zips": ["80301", "80503"],
        "lat": 40.0625,
        "lng": -105.2130,
        "neighborhoods": ["Twin Lakes", "Gunbarrel Commons"],
        "flavor": "an unincorporated Boulder County community northeast of Boulder proper, built up around the IBM campus in the 1960s and now home to Celestial Seasonings and Avery Brewing",
        "housing": "1960s-70s development alongside newer infill near Twin Lakes",
        "nearby": ["boulder", "longmont", "niwot"],
        "scrap_zone": 3,
    },
    "boulder": {
        "name": "Boulder",
        "slug": "boulder",
        "zips": ["80301", "80302", "80303", "80304", "80305"],
        "lat": 40.0150,
        "lng": -105.2705,
        "neighborhoods": ["Chautauqua", "North Boulder", "Table Mesa", "Downtown Boulder"],
        "flavor": "Colorado's iconic university-and-outdoors city at the base of the Flatirons, home to CU Boulder and a lifestyle built around trails and tech",
        "housing": "a mix of historic Chautauqua-area homes, mid-century North Boulder neighborhoods, and foothills properties near Table Mesa",
        "nearby": ["gunbarrel", "longmont", "niwot"],
        "scrap_zone": 3,
    },
    "longmont": {
        "name": "Longmont",
        "slug": "longmont",
        "zips": ["80501", "80503", "80504"],
        "lat": 40.1672,
        "lng": -105.1019,
        "neighborhoods": ["Prospect New Town", "Southmoor Park", "Renaissance", "Historic Downtown Longmont"],
        "flavor": "a mid-size St. Vrain Valley city between Boulder and Weld County, blending agricultural heritage with newer master-planned growth like Prospect New Town",
        "housing": "established neighborhoods like Southmoor Park alongside newer developments like Prospect New Town",
        "nearby": ["firestone", "frederick", "niwot"],
        "scrap_zone": 3,
    },
    "niwot": {
        "name": "Niwot",
        "slug": "niwot",
        "zips": ["80503"],
        "lat": 40.0994,
        "lng": -105.1714,
        "neighborhoods": ["Old Town Niwot", "Cottonwood Square", "Somerset Estates"],
        "flavor": "a small unincorporated Boulder County town along the Left Hand Creek corridor, named for Arapaho Chief Niwot, known for its historic Second Avenue storefronts and high-end acreage estates",
        "housing": "historic Old Town storefront-era homes alongside high-end estate properties in Somerset Estates",
        "nearby": ["longmont", "boulder", "gunbarrel"],
        "scrap_zone": 3,
    },
    "lyons": {
        "name": "Lyons",
        "slug": "lyons",
        "zips": ["80540"],
        "lat": 40.2247,
        "lng": -105.2719,
        "neighborhoods": ["Bohn Park", "Meadow Park", "The Confluence"],
        "flavor": "a small, artsy foothills town at the confluence of the North and South St. Vrain Creeks, known for red sandstone and a tight-knit community that rebuilt after the 2013 flood",
        "housing": "a mix of historic in-town homes and mountain-foothills properties",
        "nearby": ["niwot", "longmont", "boulder"],
        "scrap_zone": 3,
    },
}

# ─── Service Data ────────────────────────────────────────────────────────────
# Each service has:
#   - price_free: True only when curbside pickup is genuinely free with no
#     conditions attached (no service currently qualifies - see pricing.json's
#     scrap_metal block for the qualifying-load exception model instead).
#   - Most services intentionally publish no dollar amount in their copy and
#     drive toward a call/text quote instead. Where a service does publish a
#     price (scrap metal, TV recycling), the number comes from the PRICING
#     dict (loaded from pricing.json above) via the _PRICE_* shortcuts below -
#     never hardcode a dollar amount directly in a SERVICES string.
_PRICE_TV = PRICING["tv_recycling"]["per_unit"]
_PRICE_SCRAP_Z1 = PRICING["scrap_metal"]["zone1_fee"]
_PRICE_SCRAP_Z2 = PRICING["scrap_metal"]["zone2_fee"]
_PRICE_SCRAP_Z3 = PRICING["scrap_metal"]["zone3_fee"]
_PRICE_SCRAP_Z1_MI = PRICING["scrap_metal"]["zone1_max_miles"]
_PRICE_SCRAP_Z2_MI = PRICING["scrap_metal"]["zone2_max_miles"]
_PRICE_INSIDE_FEE = PRICING["scrap_metal"]["inside_pickup_fee"]

SERVICES = {
    "tv-recycling": {
        "name": "TV Recycling",
        "slug": "tv-recycling",
        "item": "TV",
        "price_free": False,
        "short": "TV recycling",
        "action": f"Curbside TV pickup and responsible e-waste recycling — ${_PRICE_TV} per unit",
        "what_we_take": "CRT TVs, flat screens, LED, LCD, plasma, and projection TVs",
        "schema_name": "TV Recycling & E-Waste Pickup",
        "intro_templates": [
            (
                "Old TVs are one of the most common — and most hazardous — items "
                "sitting in garages and basements across {city_name}. Whether it's a bulky CRT set that's been "
                "gathering dust for a decade or a flat screen that finally gave out, you can't just toss it in "
                "the trash. {city_name} residents know that e-waste contains lead, mercury, and cadmium "
                "that don't belong in any landfill. That's where Go Green Scrap Pros comes in."
            ),
            (
                "We'll pick up your old TV curbside anywhere in {city_name} — "
                "zip codes {zips_text}. No hauling it to a drop-off. No loading it in your car. "
                "Just set it at the curb and we'll handle the rest. We properly disassemble and recycle "
                "every TV we collect, recovering metals, plastics, and circuit boards for responsible processing."
            ),
            (
                "Serving {neighborhoods_short} and every neighborhood in between, "
                "we make TV recycling in {city_name} as easy as a phone call. "
                f"Text or call Adam at 720-675-7693 — ${_PRICE_TV} per unit, usually same-day or next-day pickup."
            ),
        ],
        "how_it_works": [
            ("Schedule Your Pickup", "Call or text Adam at 720-675-7693. Let us know what type and size of TV you have. We'll confirm a pickup window — most jobs are same-day or next-day."),
            ("Set It at the Curb", "Place your TV at the curb or driveway. No need to box it or wrap it. CRTs, flat screens, any size — just get it outside and we take it from there."),
            ("We Recycle It Right", "Your TV gets properly disassembled and recycled. Metals, glass, plastics, and circuit boards are separated and sent to certified processing facilities — not the landfill."),
        ],
        "why_choose": [
            f"${_PRICE_TV} flat per unit — no hidden fees, no surprises",
            "CRTs, flat screens, plasma, LED, LCD — we take them all",
            "Proper e-waste recycling with certified processors",
            "Curbside pickup — you don't have to haul it anywhere",
            "Same-day and next-day pickup available in {city_name}",
            "Locally owned and operated — you deal with Adam directly",
        ],
        "faqs": [
            ("How much does TV recycling cost in {city_name}?",
             f"${_PRICE_TV} per unit, flat — CRT, flat screen, any size. Call or text Adam at 720-675-7693 with your address and we'll confirm a pickup window."),
            ("Do you pick up CRT TVs in {city_name}?",
             (
                 "Yes, we pick up all TV types in {city_name} including CRT, LED, LCD, plasma, and projection TVs, all at the same "
                 f"${_PRICE_TV} flat rate. CRTs are some of the most important to recycle properly because of the lead in the glass."
             )),
            ("Why can't I just throw my old TV in the trash?",
             "TVs contain hazardous materials including lead, mercury, and cadmium that contaminate soil and groundwater in landfills. Colorado law requires proper e-waste disposal. We make sure your TV is recycled responsibly."),
            ("What zip codes do you serve in {city_name}?",
             "We serve all of {city_name} including zip codes {zips_text}. From {neighborhoods_two} and everywhere in between — we'll come to you."),
            ("How quickly can you pick up my old TV in {city_name}?",
             "Most TV pickups in {city_name} are same-day or next-day. Call or text Adam at 720-675-7693 and we'll lock in a time that works for you."),
        ],
        "items_section": [
            "Flat screen TVs (LED, LCD, plasma)",
            "CRT (tube) TVs of any size",
            "Projection TVs and rear-projection units",
            "Computer monitors and bundled e-waste",
        ],
    },
    "mattress-removal": {
        "name": "Mattress Removal",
        "slug": "mattress-removal",
        "item": "mattress",
        "price_free": False,
        "short": "mattress removal",
        "action": "Curbside mattress pickup and eco-friendly disposal",
        "what_we_take": "Twin, full, queen, king mattresses, box springs, futons, and mattress toppers",
        "schema_name": "Mattress Removal & Recycling",
        "intro_templates": [
            (
                "Getting rid of an old mattress in {city_name} is harder than it should be. "
                "The city won't take it with regular trash. Most mattress stores won't haul your old one away "
                "unless you buy from them — and even then, they charge extra. Meanwhile, that worn-out mattress "
                "is taking up space in your garage, leaning against a wall, or blocking a room you actually need. "
                "Go Green Scrap Pros makes it simple: call for a flat-rate quote and we handle the rest."
            ),
            (
                "We'll pick up your mattress curbside anywhere in {city_name} — all zip codes including "
                "{zips_text}. Twin, full, queen, king — doesn't matter. Box springs too. "
                "We separate the steel springs, foam, and fabric for recycling whenever possible, "
                "keeping as much out of the landfill as we can."
            ),
            (
                "If you're in {neighborhoods_short} or anywhere else in {city_name}, "
                "just text Adam at 720-675-7693 for a free quote. Most pickups are same-day or next-day. "
                "Stop stepping over that mattress — let us take it."
            ),
        ],
        "how_it_works": [
            ("Text or Call Adam", "Reach out at 720-675-7693 for a free quote. Let us know the mattress size and where you are in {city_name}. We'll confirm a pickup window right away."),
            ("Place It Curbside", "Drag it to the curb or driveway — that's all you need to do. If it's still in a bedroom and you need help, ask about our in-home removal option."),
            ("We Haul & Recycle", "We take it away and separate what we can — steel springs go to metal recycling, foam and fabric get processed. No illegal dumping, no shortcuts."),
        ],
        "why_choose": [
            "Flat-rate quote for any mattress size — twin to king",
            "Box springs covered too — same flat-rate pickup",
            "We recycle springs, foam, and fabric when possible",
            "Curbside pickup — no need to haul it to a dump yourself",
            "Same-day and next-day pickup available in {city_name}",
            "Locally owned — Adam handles every job personally",
        ],
        "faqs": [
            ("How do I get a quote for mattress removal in {city_name}?",
             "Call or text Adam at 720-675-7693. Mattress removal in {city_name} is flat-rate — any size, curbside pickup, no hidden fees or upcharges. We'll confirm pricing before we ever roll up."),
            ("Do you take box springs too?",
             "Yes. Box springs are picked up at the same flat rate as mattresses. If you're replacing a full set, we'll take both in the same trip — call us for a combined quote."),
            ("Can you pick up a mattress inside my house?",
             "Our flat rate is for curbside pickup. If you need the mattress removed from inside your home, give us a call and we can work something out — especially for stairs or tight spaces."),
            ("What zip codes in {city_name} do you cover?",
             "We cover all of {city_name} — zip codes {zips_text}. From {neighborhoods_two} and everywhere in between."),
            ("What happens to my old mattress after pickup?",
             "We separate recyclable materials — steel springs, foam, and fabric — and send them to appropriate recycling facilities. We keep as much out of the landfill as possible."),
        ],
        "items_section": [
            "Twin, full, queen, and king mattresses",
            "Box springs (any size)",
            "Futons and mattress toppers",
            "Pillow-top, memory foam, and hybrid mattresses",
        ],
    },
    "large-appliance-removal": {
        "name": "Large Appliance Removal",
        "slug": "large-appliance-removal",
        "item": "appliance",
        "price_free": False,
        "short": "large appliance removal",
        "action": "Curbside pickup for washers, dryers, stoves, and dishwashers",
        "what_we_take": "Washers, dryers, stoves, ovens, ranges, dishwashers, and other large household appliances (not including refrigerators or ACs)",
        "schema_name": "Large Appliance Removal & Recycling",
        "intro_templates": [
            (
                "When a washer dies, a dryer quits heating, or an old stove finally gives up, "
                "most {city_name} homeowners face the same problem: how do you actually get rid of it? "
                "These things are heavy, awkward, and a pain to move. Go Green Scrap Pros takes the hassle away "
                "with flat-rate curbside appliance removal for {city_name} and the surrounding area."
            ),
            (
                "We'll pick up your old washer, dryer, stove, oven, dishwasher, "
                "or any other large household appliance from curbside. We serve all of {city_name} — "
                "zip codes {zips_text}. Every appliance we pick up gets stripped for metal, which goes straight "
                "to recycling. That's the Go Green way."
            ),
            (
                "Whether you're upgrading your kitchen in {neighborhoods_sample} or "
                "finally replacing that 20-year-old washer, we've got you covered. "
                "Call or text Adam at 720-675-7693 for a free quote — same-day or next-day pickup in {city_name}."
            ),
        ],
        "how_it_works": [
            ("Call or Text Us", "Reach Adam at 720-675-7693 for a free quote. Tell us what appliance you need removed and your address in {city_name}. We'll set up a pickup window."),
            ("Move It to the Curb", "Get the appliance to curbside or your driveway. If it's too heavy or awkward, let us know and we can discuss options."),
            ("We Pick Up & Recycle", "We load it up, haul it away, and recycle every bit of metal from the unit. Steel, copper, aluminum — it all gets a second life."),
        ],
        "why_choose": [
            "Flat-rate quote per appliance — no surprise fees",
            "Washers, dryers, stoves, dishwashers — all covered",
            "Metal from every appliance gets recycled",
            "Curbside pickup means zero hassle for you",
            "Same-day and next-day availability in {city_name}",
            "Owner-operated — Adam handles your job personally",
        ],
        "faqs": [
            ("How do I get an appliance removal quote in {city_name}?",
             "Call or text Adam at 720-675-7693 with the appliance type and your {city_name} address. We quote flat-rate per appliance — curbside pickup and recycling for washers, dryers, stoves, dishwashers, and more."),
            ("Do you take refrigerators too?",
             "Refrigerators require special handling for freon recovery, so they have a separate service. Check our refrigerator removal page for {city_name} for details on that."),
            ("What happens to the old appliance?",
             "We strip every appliance for recyclable metals — steel, copper, aluminum. The metal goes to certified recyclers. We recover as much material as possible and keep it out of the landfill."),
            ("What {city_name} zip codes do you serve?",
             "We serve all of {city_name} including zip codes {zips_text}. {neighborhoods_two} — we cover every neighborhood."),
            ("Can you pick up multiple appliances at once?",
             "Absolutely. If you're doing a kitchen or laundry room overhaul in {city_name}, we'll take all the old appliances in one trip. Call for a multi-unit quote."),
        ],
        "items_section": [
            "Washers and dryers (gas or electric)",
            "Stoves, ovens, ranges, and cooktops",
            "Dishwashers and trash compactors",
            "Microwaves, range hoods, and similar large kitchen appliances",
        ],
    },
    "refrigerator-removal": {
        "name": "Refrigerator Removal",
        "slug": "refrigerator-removal",
        "item": "refrigerator",
        "price_free": False,
        "short": "refrigerator removal",
        "action": "Safe curbside fridge pickup with proper freon recovery",
        "what_we_take": "Refrigerators, freezers, mini-fridges, wine coolers, and other refrigerant-containing units",
        "schema_name": "Refrigerator Removal & Disposal",
        "intro_templates": [
            (
                "You can't just put an old refrigerator on the curb and hope someone takes it. "
                "Fridges contain refrigerants like freon that require proper handling under EPA regulations. "
                "In {city_name}, illegal dumping of refrigerant-containing appliances can mean fines — and it harms the environment. "
                "Go Green Scrap Pros handles all of that for you, legally and responsibly."
            ),
            (
                "We pick up your old fridge, stand-up freezer, mini-fridge, or wine cooler "
                "from curbside anywhere in {city_name} — zip codes {zips_text}. "
                "We ensure proper refrigerant recovery before the unit is dismantled, and the metal "
                "gets recycled. It's the right way to get rid of an old fridge."
            ),
            (
                "From {neighborhoods_short} to every corner of {city_name}, "
                "we make fridge disposal easy and compliant. "
                "Call or text Adam at 720-675-7693 for a free quote — most pickups happen same-day or next-day."
            ),
        ],
        "how_it_works": [
            ("Schedule the Pickup", "Call or text Adam at 720-675-7693 for a free quote. Let us know what type of unit you have — fridge, freezer, mini-fridge — and your {city_name} address."),
            ("Set It Curbside", "Move the fridge to the curb or driveway. Defrost it if you can, but don't worry about cleaning it out — we've seen it all."),
            ("We Handle Freon & Recycling", "We ensure proper refrigerant recovery per EPA guidelines, then dismantle and recycle the metal. No shortcuts, no illegal dumping."),
        ],
        "why_choose": [
            "Flat-rate pickup — fridge, freezer, mini-fridge, wine cooler",
            "Proper freon recovery per EPA regulations",
            "All metal gets recycled after refrigerant removal",
            "No fines, no risk — we handle compliance for you",
            "Same-day and next-day pickup in {city_name}",
            "Honest, owner-operated service — call or text Adam",
        ],
        "faqs": [
            ("How do I get a refrigerator removal quote in {city_name}?",
             "Call or text Adam at 720-675-7693. Refrigerator removal in {city_name} is flat-rate and includes curbside pickup, proper refrigerant recovery, and metal recycling."),
            ("Why does fridge removal cost more than other appliances?",
             "Fridges require certified refrigerant (freon) recovery before they can be recycled or disposed of. This extra step is required by the EPA and adds to the process — but it keeps harmful chemicals out of the atmosphere."),
            ("Do you take freezers and mini-fridges too?",
             "Yes. Stand-up freezers, chest freezers, mini-fridges, wine coolers — any unit that contains refrigerant. Same flat-rate pickup."),
            ("What {city_name} areas do you serve?",
             "We serve all of {city_name} — zip codes {zips_text} — including {neighborhoods_two} and surrounding areas."),
            ("Is it illegal to dump a refrigerator in {city_name}?",
             "Yes. Dumping appliances containing refrigerants is illegal under federal EPA regulations. Fines can be significant. We handle compliant disposal so you don't have to worry about it."),
        ],
        "items_section": [
            "Full-size refrigerators (top, bottom, and side-by-side)",
            "Stand-up and chest freezers",
            "Mini-fridges and dorm-size units",
            "Wine coolers and beverage refrigerators",
        ],
    },
    "air-conditioner-removal": {
        "name": "Air Conditioner Removal",
        "slug": "air-conditioner-removal",
        "item": "air conditioner",
        "price_free": False,
        "short": "AC removal",
        "action": "Curbside pickup for window units and portable ACs",
        "what_we_take": "Window AC units, portable air conditioners, and small cooling units",
        "schema_name": "Air Conditioner Removal & Recycling",
        "intro_templates": [
            (
                "That old window AC unit sitting in your garage or still wedged in a window you don't use anymore? "
                "It's not doing you any good — and like refrigerators, air conditioners contain refrigerants that "
                "need proper handling. {city_name} residents can count on Go Green Scrap Pros to remove old AC units "
                "safely and recycle the materials responsibly."
            ),
            (
                "We'll pick up your window AC or portable air conditioner curbside anywhere in "
                "{city_name}. We serve zip codes {zips_text} and handle proper refrigerant recovery before "
                "recycling the metal housing, copper coils, and other materials. "
                "Affordable, easy, and the right thing to do."
            ),
            (
                "Whether you're in {neighborhoods_short} or anywhere else in {city_name}, "
                "AC removal doesn't have to be a headache. "
                "Text or call Adam at 720-675-7693 for a free estimate and we'll schedule a quick pickup."
            ),
        ],
        "how_it_works": [
            ("Contact Adam", "Call or text 720-675-7693 for a free estimate. Let us know how many AC units you have and your location in {city_name}. We'll schedule your pickup."),
            ("Put It at the Curb", "Window units and portable ACs are small enough to carry outside. Just set it at the curb or driveway and we'll grab it."),
            ("Proper Disposal & Recycling", "We recover any refrigerant safely, then recycle the metal — copper coils, aluminum fins, steel housing. Done the right way."),
        ],
        "why_choose": [
            "Flat-rate per unit — affordable AC disposal",
            "Window units and portable ACs both accepted",
            "Proper refrigerant handling — no shortcuts",
            "Metals recycled: copper, aluminum, steel",
            "Quick curbside pickup in {city_name}",
            "Owner-operated — Adam picks up the phone and does the work",
        ],
        "faqs": [
            ("How do I get an AC removal quote in {city_name}?",
             "Call or text Adam at 720-675-7693 for a free estimate. Air conditioner removal in {city_name} is flat-rate per unit — covers curbside pickup, refrigerant handling, and metal recycling."),
            ("Do you remove central AC units?",
             "We focus on window units and portable AC units. Central AC systems require HVAC professionals for removal. If you have a window unit or portable AC, we're your guys."),
            ("Why can't I throw an AC unit in the trash?",
             "AC units contain refrigerants that are harmful to the ozone layer and must be recovered by certified professionals. Tossing them in the trash or leaving them at the curb for garbage pickup is not allowed."),
            ("What areas of {city_name} do you cover?",
             "All of {city_name} — zip codes {zips_text}. {neighborhoods_two} and every neighborhood in between."),
            ("Can you pick up multiple AC units at once?",
             "Absolutely. If you're cleaning out a rental property or doing a seasonal purge, we'll take all your old AC units in one trip. Call us for a multi-unit estimate."),
        ],
        "items_section": [
            "Window AC units of any BTU rating",
            "Portable / floor-standing AC units",
            "Through-the-wall AC sleeves",
            "Dehumidifiers and small cooling units",
        ],
    },
    "treadmill-removal": {
        "name": "Treadmill Removal",
        "slug": "treadmill-removal",
        "item": "treadmill",
        "price_free": False,
        "short": "treadmill removal",
        "action": "Curbside pickup for treadmills and heavy exercise equipment",
        "what_we_take": "Treadmills, ellipticals, exercise bikes, home gym equipment, and weight machines",
        "schema_name": "Treadmill & Exercise Equipment Removal",
        "intro_templates": [
            (
                "Let's be honest — that treadmill in the basement isn't getting used anymore. "
                "It's become an expensive clothes rack, and now you need the space. "
                "The problem? Treadmills are incredibly heavy, awkward to move, and a nightmare to get through "
                "doorways. {city_name} homeowners call Go Green Scrap Pros when they're done wrestling with it."
            ),
            (
                "We'll pick up your treadmill curbside anywhere in {city_name} — "
                "zip codes {zips_text}. The metal frame, motor housing, and steel components all get recycled. "
                "You get your space back, and another hunk of metal stays out of the landfill."
            ),
            (
                "From {neighborhoods_short} to every corner of {city_name}, "
                "we've hauled treadmills out of basements, spare bedrooms, and garages. "
                "Call or text Adam at 720-675-7693 for a free quote and let's get that thing gone."
            ),
        ],
        "how_it_works": [
            ("Call or Text Adam", "Reach out at 720-675-7693 for a free quote. Describe the equipment — treadmill, elliptical, weight machine — and your location in {city_name}."),
            ("Get It to the Curb", "If you can get it to the curb or driveway, perfect — that's our flat curbside rate. Can't move it? Ask about our in-home removal option."),
            ("We Haul & Recycle", "We load it up and recycle the metal frame, motor, and steel components. The heavy lifting is on us."),
        ],
        "why_choose": [
            "Flat-rate curbside pickup for treadmill removal — no surprises",
            "Ellipticals, weight machines, exercise bikes also accepted",
            "Metal frames and motors get recycled",
            "We handle the heavy lifting — these things are beasts",
            "Same-day and next-day pickup in {city_name}",
            "Locally owned — Adam gives you straight answers",
        ],
        "faqs": [
            ("How do I get a treadmill removal quote in {city_name}?",
             "Call or text Adam at 720-675-7693 for a free quote. Treadmill removal in {city_name} is flat-rate for curbside pickup. If you need help getting it out of a basement or upstairs room, mention it on the call and we'll work something out."),
            ("Do you take other exercise equipment besides treadmills?",
             "Yes. Ellipticals, stationary bikes, weight machines, home gym systems — we take it all. Pricing depends on the item, so give us a call for a quote."),
            ("Why are treadmills more expensive to remove than smaller items?",
             "Treadmills are exceptionally heavy — most weigh 200-350 pounds. The motor assembly, steel frame, and belt mechanism make them one of the heaviest single household items. The flat rate reflects the effort involved."),
            ("What {city_name} areas do you serve for treadmill removal?",
             "All of {city_name} — zip codes {zips_text}. From {neighborhoods_two} and everywhere in between. If you're in {city_name}, we'll come to you."),
            ("Can you pick up a treadmill from my basement?",
             "Our flat curbside rate covers pickup at the curb or driveway. Basement or upstairs removal is possible but may add to the quote depending on the stairs and access. Call Adam at 720-675-7693 and we'll work something out."),
        ],
        "items_section": [
            "Treadmills (folding and non-folding)",
            "Ellipticals and stair-climbers",
            "Stationary and recumbent exercise bikes",
            "Weight benches, racks, and home gym systems",
        ],
    },
    "couch-removal": {
        "name": "Couch Removal",
        "slug": "couch-removal",
        "item": "couch",
        "price_free": False,
        "short": "couch removal",
        "action": "Curbside pickup for couches, sofas, and sectionals",
        "what_we_take": "Couches, sofas, loveseats, sectionals, recliners, sofa beds, and futons",
        "schema_name": "Couch & Sofa Removal",
        "intro_templates": [
            (
                "That old couch has served its time. Maybe the springs are shot, the fabric is torn, "
                "or you're just upgrading and need the old one gone before the new one arrives. "
                "Either way, getting a full-size couch out of a {city_name} home and disposed of properly "
                "is way harder than it sounds. That's why Go Green Scrap Pros offers flat-rate curbside couch removal."
            ),
            (
                "We pick up your old couch, sofa, loveseat, or sectional from curbside "
                "anywhere in {city_name}. We serve all zip codes: {zips_text}. "
                "When the couch is in decent shape, we'll try to donate it. When it's not, "
                "we separate recyclable materials — wood frames, metal springs, foam — and handle disposal responsibly."
            ),
            (
                "From {neighborhoods_short} to the rest of {city_name}, "
                "we've hauled more couches than we can count. "
                "Call or text Adam at 720-675-7693 for a free quote and we'll get that couch out of your way."
            ),
        ],
        "how_it_works": [
            ("Schedule the Pickup", "Text or call Adam at 720-675-7693 for a free quote. Let us know what you've got — couch, loveseat, sectional — and your {city_name} address."),
            ("Get It to the Curb", "Drag it to the curb or driveway. Can't fit it through the door? We've been there — ask about our in-home removal option."),
            ("We Haul, Donate, or Recycle", "We pick it up and donate when possible. If it's past its useful life, we separate wood, metal, and foam for recycling."),
        ],
        "why_choose": [
            "Flat-rate quote — couches, sofas, loveseats",
            "Sectionals and sofa beds accepted too",
            "Donation when the couch is still in good shape",
            "Materials recycled when donation isn't an option",
            "Same-day and next-day availability in {city_name}",
            "Honest pricing from a local, owner-operated business",
        ],
        "faqs": [
            ("How do I get a couch removal quote in {city_name}?",
             "Call or text Adam at 720-675-7693 for a free quote. Couch removal in {city_name} is flat-rate for curbside pickup of a standard couch or sofa. Sectionals are quoted by size."),
            ("Do you take sectionals and sofa beds?",
             "Yes. Sectionals, sofa beds, futons, recliners, loveseats — we take it all. Oversized sectionals may run a little higher, but we'll quote the whole job upfront before we ever roll up."),
            ("Will you donate my old couch?",
             "If the couch is in usable condition, we absolutely try to donate it to local charities. We'd rather see it get a second life than end up in a landfill."),
            ("What {city_name} zip codes do you serve?",
             "We serve all of {city_name} — zip codes {zips_text}. {neighborhoods_two} and every neighborhood in between."),
            ("Can you remove a couch from inside my house?",
             "Our flat rate is for curbside pickup. If you need help getting a couch out of a room, through a tight hallway, or down stairs, call Adam and we'll discuss options."),
        ],
        "items_section": [
            "Standard couches and sofas",
            "Loveseats and accent chairs",
            "Sectionals (any configuration)",
            "Sofa beds, futons, and recliners",
        ],
    },
    "estate-cleanout": {
        "name": "Estate Cleanout",
        "slug": "estate-cleanout",
        "item": "estate",
        "price_free": False,
        "short": "estate cleanout",
        "action": "Full estate cleanouts, inherited property reclamation, and hoarder cleanouts",
        "what_we_take": "Furniture, appliances, household goods, yard debris, scrap metal, and general junk from every room, closet, garage, basement, attic, shed, and outbuilding",
        "schema_name": "Estate Cleanout & Inherited Property Reclamation",
        "intro_templates": [
            (
                "Clearing out an estate in {city_name} is rarely just about the stuff. It's grief, paperwork, a tight timeline, "
                "and a property that doesn't feel like yours yet \u2014 all at once. Whether you've inherited a home that hasn't "
                "been cleared in years, you're working through probate, or you're a realtor prepping a {city_name} listing, "
                "Go Green Scrap Pros handles the cleanout so you can handle everything else."
            ),
            (
                "We serve all of {city_name} \u2014 zip codes {zips_text} \u2014 and the broader Denver Metro area. "
                "We work respectfully, on your schedule, and we tell you honestly what's recoverable, what's donatable, and what "
                "has to go to the transfer station. We recycle first and landfill last. "
                "On our recent Northglenn estate cleanout we moved 50,000 lbs of steel and 160 cubic yards of debris \u2014 "
                "<a href=\"/case-studies/northglenn-estate-cleanout/\">see the full case study</a>."
            ),
            (
                "Serving {neighborhoods_short} and every neighborhood in between. For families on tight estate budgets with "
                "substantial recoverable scrap on the property, we offer flexible labor + expenses + scrap pricing structures "
                "that can make jobs affordable when hourly pricing would have priced them out of reach. Text or call Adam "
                "at 720-675-7693 with a few photos of the property and we'll come back with a straight quote."
            ),
        ],
        "how_it_works": [
            ("Walk the Property With Us", "Call or text Adam at 720-675-7693. Send a few photos or schedule an on-site walk-through in {city_name}. We'll identify what's recoverable, flag any hazmat, and quote the job honestly \u2014 no high-pressure sales."),
            ("We Build a Plan Around Your Constraints", "Tight budget, tight timeline, working around showings or court dates \u2014 we plan the job around your reality. For larger properties we coordinate dumpsters; for smaller ones we run trucks and trailers."),
            ("We Clear, Sort, and Recycle", "Furniture, appliances, scrap metal, yard debris, household goods \u2014 every zone of the property. Metals get sorted and recycled. Reusable items get diverted. Only what can't be diverted goes to landfill."),
        ],
        "why_choose": [
            "Flexible pricing for tight estate budgets \u2014 labor + expenses + scrap structures available",
            "Compassionate, respectful crew \u2014 we've worked these jobs and we get it",
            "Recycling-first disposal \u2014 majority of material weight stays out of the landfill",
            "Hazmat-aware \u2014 we identify it, give you 3 disposal options, and adjust the plan",
            "Coordination with realtors, executors, and estate attorneys",
            "Locally owned, owner-operated in {city_name} and across Denver Metro",
            "Real case studies with real numbers \u2014 not stock photos",
        ],
        "faqs": [
            ("How much does an estate cleanout cost in {city_name}?",
             "Most estate cleanouts in {city_name} run between $500 and $3,500+ depending on size, volume, access, and whether hoarding or hazmat is involved. For families on tight budgets with substantial recoverable scrap on the property, we offer a flexible labor + expenses + scrap pricing model. Text us a few photos at 720-675-7693 for a straight quote."),
            ("How long does an estate cleanout take in {city_name}?",
             "A standard furnished single-family home in {city_name} typically takes one to two days. Larger properties, hoarding, or properties with outbuildings and workshops can take a full week or more. Our recent Northglenn estate cleanout was a 7-day, 3-crew job that moved 50,000 lbs of steel and 160 cubic yards of trash."),
            ("What's included in an estate cleanout?",
             "Furniture, appliances, household goods, yard debris, scrap metal, and general junk from every room, closet, garage, basement, attic, shed, and outbuilding in {city_name}. We sort donatable items from recyclables and from landfill-bound trash, coordinate dumpsters when warranted, and provide photo documentation for estate records on request."),
            ("Do you handle hoarder cleanouts in {city_name}?",
             "Yes. We've worked properties that hadn't been cleared in years, with tight access, unstable piles, pests, and mixed debris throughout. We work respectfully, at a safe pace, and we don't gut working systems \u2014 we sort and preserve what's worth keeping."),
            ("Do you handle hazardous materials?",
             "No \u2014 we're not licensed to transport hazmat. But if we find oils, paints, solvents, or other flammables on your {city_name} property, we'll identify them, give you three vetted disposal options in writing, and adjust the plan around them. We don't pretend, and we don't leave you to figure it out alone."),
            ("Do you work with realtors and estate attorneys in {city_name}?",
             "Yes. We coordinate with realtors prepping {city_name} listings, executors handling probate, and families managing inherited properties. We work around showings, court timelines, and family schedules."),
            ("What {city_name} zip codes do you serve?",
             "We serve all of {city_name} including zip codes {zips_text}. From {neighborhoods_two} and everywhere in between."),
        ],
        "items_section": [
            "Furniture (couches, beds, dressers, tables, chairs)",
            "Appliances (washers, dryers, stoves, dishwashers, refrigerators)",
            "Household goods, clothing, books, and personal items",
            "Yard debris, fencing, and outdoor accumulation",
            "Scrap metal \u2014 sorted and recycled",
            "Garage, basement, attic, shed, and workshop contents",
            "Estate-record photo documentation on request",
        ],
    },
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
                "for free pickup. Everything else gets a flat, distance-based dispatch fee — {scrap_fee} in {city_name}."
            ),
            (
                "Steel, aluminum, copper, brass, iron — old grills, metal shelving, car parts, fencing, "
                "pipes, wiring, appliance shells. We serve all of {city_name} including zip codes {zips_text}. "
                "High-value loads (HVAC units, server racks, clean copper/brass) may be picked up free; "
                "standard loads in {city_name} run {scrap_fee}, based on distance from our Thornton hub."
            ),
            (
                "Whether you're in {neighborhoods_short} or anywhere else in {city_name}, scrap metal "
                "pickup starts with a photo. Text or call Adam at 720-675-7693 — we'll confirm your "
                "dispatch fee, or confirm it's free, before we're on the way. Usually same-day or next-day."
            ),
        ],
        "how_it_works": [
            ("Text a Photo & Address", "Send a photo of your scrap metal and your address to 720-675-7693. We need to see it before we can quote it."),
            ("Get Your Dispatch Quote", f"We'll confirm your rate — free if it's a qualifying high-value load (commercial HVAC, server racks, clean copper/brass), or a flat dispatch fee (${_PRICE_SCRAP_Z1}-${_PRICE_SCRAP_Z3}) based on distance if not."),
            ("We Haul It Away", "We show up, load it up, and take it to the recycler. No surprises beyond the rate we quoted."),
        ],
        "why_choose": [
            "Free pickup for qualifying high-value loads — commercial HVAC units, server racks, clean copper/brass batches",
            (
                f"Flat, distance-based dispatch fee otherwise — ${_PRICE_SCRAP_Z1} (0-{_PRICE_SCRAP_Z1_MI}mi), "
                f"${_PRICE_SCRAP_Z2} ({_PRICE_SCRAP_Z1_MI + 1}-{_PRICE_SCRAP_Z2_MI}mi), "
                f"${_PRICE_SCRAP_Z3} ({_PRICE_SCRAP_Z2_MI + 1}mi+) from our Thornton hub"
            ),
            "Steel, aluminum, copper, brass, iron — all accepted",
            "Your rate is confirmed by photo before we schedule — no guessing, no surprise charges",
            "Same-day and next-day pickup in {city_name}",
            "Locally owned — Adam is the one who shows up",
        ],
        "faqs": [
            ("Is scrap metal pickup free in {city_name}?",
             (
                 "It can be. Commercial HVAC units, server racks, and clean copper or brass batches often qualify for free "
                 "pickup — text a photo to 720-675-7693 and we'll confirm. Everything else gets a flat dispatch fee based on "
                 "distance — {scrap_fee} for {city_name}."
             )),
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
}

# ─── Helper functions ────────────────────────────────────────────────────────

def format_zips(zips):
    """Format zip list as human-readable text."""
    if len(zips) == 1:
        return zips[0]
    return ", ".join(zips[:-1]) + ", and " + zips[-1]


def neighborhoods_short(city):
    """Return 2-3 neighborhood names for a short mention. Degrades gracefully
    for cities with fewer verified named neighborhoods (real small towns don't
    all have 3+ distinct named areas - padding with invented names is worse
    than a shorter, honest list)."""
    nh = city["neighborhoods"]
    if len(nh) >= 3:
        return f"{nh[0]}, {nh[1]}, and {nh[2]}"
    if len(nh) == 2:
        return f"{nh[0]} and {nh[1]}"
    return nh[0]


def neighborhoods_two(city):
    """Return two neighborhoods for FAQ-style mention."""
    nh = city["neighborhoods"]
    if len(nh) >= 2:
        return f"{nh[0]} to {nh[-1]}"
    return nh[0]


def neighborhoods_sample(city):
    """Return a neighborhood sample for general mention."""
    nh = city["neighborhoods"]
    if len(nh) >= 2:
        return f"{nh[0]} or {nh[1]}"
    return nh[0]


def scrap_fee_for(city):
    """Dollar amount for this city's scrap-metal dispatch zone (defaults to
    zone 1 for any city that doesn't set scrap_zone explicitly)."""
    zone = city.get("scrap_zone", 1)
    return PRICING["scrap_metal"][f"zone{zone}_fee"]


def fill_template(text, city, service):
    """Replace all placeholders in a text template."""
    return (
        text
        .replace("{city_name}", city["name"])
        .replace("{city}", city["slug"])
        .replace("{zips_text}", format_zips(city["zips"]))
        .replace("{neighborhoods_short}", neighborhoods_short(city))
        .replace("{neighborhoods_two}", neighborhoods_two(city))
        .replace("{neighborhoods_sample}", neighborhoods_sample(city))
        .replace("{service_name}", service["name"])
        .replace("{scrap_fee}", f"${scrap_fee_for(city)}")
    )


def clip_meta(text, limit=160):
    """Trim a meta description to <= limit chars on a word boundary.

    Avoids mid-word truncation and leaves no trailing punctuation/space.
    Returns the text unchanged if it already fits.
    """
    text = " ".join(text.split())  # normalize whitespace
    if len(text) <= limit:
        return text
    clipped = text[:limit]
    # back up to the last space so we don't cut a word in half
    if " " in clipped:
        clipped = clipped[:clipped.rfind(" ")]
    return clipped.rstrip(" ,.;:-\u2014")


def clip_title(text, limit=60):
    """Trim a <title> to <= limit chars on a word boundary.

    Drops a trailing '| ...' suffix segment first if removing it brings the
    title under the limit, otherwise trims words. Returns unchanged if it fits.
    """
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    # Try dropping the last "| ..." segment to preserve whole words
    if " | " in text:
        head = text.rsplit(" | ", 1)[0]
        if len(head) <= limit:
            return head
    clipped = text[:limit]
    if " " in clipped:
        clipped = clipped[:clipped.rfind(" ")]
    return clipped.rstrip(" |,.;:-\u2014")


def generate_page(city_key, service_key):
    """Generate complete HTML page for a city+service combination."""
    city = CITIES[city_key]
    service = SERVICES[service_key]
    slug = f"{service['slug']}-{city['slug']}"
    city_name = city["name"]
    service_name = service["name"]
    is_free = service["price_free"]

    canonical = f"https://gogreenscrappros.com/{slug}/"
    zips_text = format_zips(city["zips"])

    # --- Title (kept <=60 chars so it isn't truncated in search results) ---
    if is_free:
        title = f"{service_name} {city_name} CO | Free Pickup"
    else:
        title = f"{service_name} {city_name} CO | Same-Day Pickup"
    title = clip_title(title, 60)

    # --- Meta description ---
    if is_free:
        meta_desc = (
            f"Free {service['short']} in {city_name}, CO. Steel, aluminum, copper, brass — "
            f"curbside pickup at no charge. Call Adam: 720-675-7693."
        )
    else:
        # Lead with location + CTA (kept intact), then append the items list,
        # which clip_meta trims to fit the 160-char limit if needed. This keeps
        # the phone number from ever being cut off.
        meta_lead = f"{service_name} in {city_name}, CO. Call Adam for a free quote: 720-675-7693."
        meta_desc = f"{meta_lead} We take {service['what_we_take'][0].lower()}{service['what_we_take'][1:]}."

    # Keep meta description within the ~160 char limit search engines display.
    meta_desc = clip_meta(meta_desc, 160)

    # --- OG tags ---
    if is_free:
        og_title = f"Free {service_name} in {city_name} CO | Go Green Scrap Pros"
        og_desc = f"Free curbside {service['short']} in {city_name}. We recycle all metals. Call 720-675-7693."
    else:
        og_title = f"{service_name} {city_name} CO | Free Quote"
        og_desc = f"{service_name} in {city_name} — {service['action']}. Call 720-675-7693 for a free quote."

    # --- JSON-LD: LocalBusiness (no price values exposed in offers) ---
    local_business = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": "Go Green Scrap Pros",
        "@id": "https://gogreenscrappros.com",
        "url": canonical,
        "telephone": "+1-720-675-7693",
        "priceRange": "$" if is_free else "$$",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Thornton",
            "addressRegion": "CO",
            "postalCode": "80229",
            "addressCountry": "US"
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": city["lat"],
            "longitude": city["lng"]
        },
        "openingHours": "Mo-Su 08:00-18:00",
        "description": f"{service_name} in {city_name}, CO. {service['action']}. Call 720-675-7693 for a free quote.",
        "areaServed": city_name,
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": f"{service_name} in {city_name}",
            "itemListElement": [
                {
                    "@type": "Offer",
                    "itemOffered": {"@type": "Service", "name": service["schema_name"]}
                }
            ]
        }
    }

    # --- JSON-LD: FAQPage ---
    faq_entities = []
    for q_template, a_template in service["faqs"]:
        q = fill_template(q_template, city, service)
        a = fill_template(a_template, city, service)
        faq_entities.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": a
            }
        })
    faq_page = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": faq_entities
    }

    # --- JSON-LD: BreadcrumbList ---
    breadcrumb_name = f"{service_name} in {city_name}, CO"
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://gogreenscrappros.com"},
            {"@type": "ListItem", "position": 2, "name": breadcrumb_name, "item": canonical}
        ]
    }

    # --- Intro paragraphs ---
    intros = []
    for tmpl in service["intro_templates"]:
        intros.append(fill_template(tmpl, city, service))

    # --- How it works ---
    how_steps = []
    for step_title, step_desc in service["how_it_works"]:
        how_steps.append((step_title, fill_template(step_desc, city, service)))

    # --- Why choose ---
    why_items = []
    for item in service["why_choose"]:
        why_items.append(fill_template(item, city, service))

    # --- FAQs (HTML) ---
    faq_html_items = []
    for q_template, a_template in service["faqs"]:
        q = fill_template(q_template, city, service)
        a = fill_template(a_template, city, service)
        faq_html_items.append((q, a))

    # --- Nearby cities ---
    nearby_links = []
    for nc in city["nearby"]:
        nc_data = CITIES[nc]
        nearby_links.append(
            f'<a href="/{service["slug"]}-{nc}/">{nc_data["name"]}</a>'
        )
    nearby_html = ",\n          ".join(nearby_links)

    # --- City nav links (for same service across all cities) ---
    # Current city plus its nearby cities shown inline; every other city in
    # CITIES goes in a CSS-only dropdown. Scales automatically as cities are
    # added/removed instead of a fixed hardcoded list.
    main_cities = [city_key] + [nc for nc in city["nearby"] if nc in CITIES][:4]
    more_cities = [ck for ck in CITIES if ck not in main_cities]
    city_nav_links = []
    for ck in main_cities:
        cd = CITIES[ck]
        href = f"/{service['slug']}-{ck}/"
        active = ' class="active"' if ck == city_key else ""
        city_nav_links.append(f'      <a href="{href}"{active}>{cd["name"]}</a>')
    more_items = []
    for ck in more_cities:
        cd = CITIES[ck]
        href = f"/{service['slug']}-{ck}/"
        active = ' class="active"' if ck == city_key else ""
        more_items.append(f'          <a href="{href}"{active}>{cd["name"]}</a>')
    city_nav_links.append(
        '      <div class="city-more">\n'
        '        <span class="city-more-toggle" tabindex="0">More Cities ▾</span>\n'
        '        <div class="city-more-menu">\n'
        + "\n".join(more_items) + "\n"
        '        </div>\n'
        '      </div>'
    )
    city_nav_html = "\n".join(city_nav_links)

    # --- "What we take" rows (no prices, just items) ---
    items_rows = []
    for item_text in service["items_section"]:
        items_rows.append(f"          <li>{item_text}</li>")
    items_html = "\n".join(items_rows)

    # --- How it works HTML ---
    how_html = []
    for i, (step_title, step_desc) in enumerate(how_steps, 1):
        how_html.append(
            f'          <li><strong>Step {i}: {step_title}</strong> — {step_desc}</li>'
        )
    how_html_str = "\n".join(how_html)

    # --- Why choose HTML ---
    why_html = []
    for item in why_items:
        why_html.append(f"          <li>{item}</li>")
    why_html_str = "\n".join(why_html)

    # --- FAQ details HTML ---
    faq_details = []
    for q, a in faq_html_items:
        faq_details.append(
            f'''          <details style="margin-bottom:1.2rem;background:#fff;padding:1.2rem 1.5rem;border-radius:10px;box-shadow:0 3px 10px rgba(0,0,0,0.07);">
            <summary style="font-weight:600;color:#1e5a4a;cursor:pointer;font-size:1.05rem;">{q}</summary>
            <p style="margin-top:0.75rem;color:#555;">{a}</p>
          </details>'''
        )
    faq_details_html = "\n\n".join(faq_details)

    # --- Neighborhoods section ---
    nh_items = []
    for nh in city["neighborhoods"]:
        nh_items.append(f"          <li>{nh}</li>")
    nh_items.append(f'          <li>All zip codes: {zips_text}</li>')
    nh_html = "\n".join(nh_items)

    # --- CTA / hero text (no dollar amounts) ---
    if is_free:
        hero_subtitle = f"Free curbside {service['short']} — steel, aluminum, copper, brass. Serving all of {city_name}."
        cta_text = f"Schedule Free {service_name} in {city_name}"
        final_cta_heading = f"Schedule Your Free Pickup in {city_name}"
        items_heading = f"What We Pick Up &mdash; Free in {city_name}"
        items_intro = "We take any metal item. No minimums. No charge for curbside pickup."
    else:
        hero_subtitle = f"{service_name} in {city_name} — flat-rate curbside pickup. Call or text for a free quote."
        cta_text = f"Request a Free Quote — {service_name} in {city_name}"
        final_cta_heading = f"Get a Free Quote in {city_name}"
        items_heading = f"What We Take &mdash; {service_name} in {city_name}"
        items_intro = "Flat-rate curbside pickup. Call or text us for a free quote — no surprises when we arrive."

    # --- Footer city links (keep pointing to junk-removal-* pages like existing site) ---
    footer_city_links = []
    for ck in ["thornton", "arvada", "westminster", "golden", "wheat-ridge", "broomfield", "northglenn"]:
        cd = CITIES[ck]
        footer_city_links.append(f'        <a href="/junk-removal-{ck}/">{cd["name"]}</a>')
    footer_cities_html = "\n".join(footer_city_links)

    # --- Footer service links (cross-link to other services in this city) ---
    footer_service_links = []
    for sk in ["junk-removal", "mattress-removal", "couch-removal", "large-appliance-removal",
               "refrigerator-removal", "tv-recycling", "scrap-metal-pickup", "treadmill-removal",
               "air-conditioner-removal"]:
        if sk == "junk-removal":
            label = f"Junk Removal {city_name}"
            href = f"/junk-removal-{city_key}/"
        else:
            svc = SERVICES.get(sk)
            if svc is None:
                continue
            label = f"{svc['name']} {city_name}"
            href = f"/{sk}-{city_key}/"
        footer_service_links.append(f'        <a href="{href}">{label}</a>')
    footer_services_html = "\n".join(footer_service_links)

    # === Build the full HTML ===
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{meta_desc}">
  <meta property="og:title" content="{og_title}">
  <meta property="og:description" content="{og_desc}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:type" content="website">
  <meta property="og:image" content="https://gogreenscrappros.com/assets/images/logo.png">
  <link rel="canonical" href="{canonical}">

  <script type="application/ld+json">
  {json.dumps(local_business, indent=4)}
  </script>

  <script type="application/ld+json">
  {json.dumps(faq_page, indent=4)}
  </script>

  <script type="application/ld+json">
  {json.dumps(breadcrumb, indent=4)}
  </script>
  <meta name="robots" content="index, follow">
  <title>{title}</title>
  <link rel="stylesheet" href="../assets/style.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" as="style" onload="this.onload=null;this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap"></noscript>
</head>
<body>

  <nav class="site-nav">
    <div class="container">
      <a href="/" class="brand">Go Green Scrap Pros</a>
      <div class="nav-links">
        <a href="/mattress-removal/">Mattress Removal</a>
        <a href="/scrap-metal-pickup/">Scrap Metal</a>
        <a href="/sitemap/">Service Areas</a>
        <a href="/about/">About</a>
        <a href="/contact/">Contact</a>
      </div>
      <div class="nav-actions">
        <a href="tel:7206757693" class="nav-cta">Call 720-675-7693</a>
        <a href="sms:7206757693" class="nav-sms">Text Us</a>
      </div>
    </div>
  </nav>

  <nav class="city-nav" aria-label="Service areas">
    <div class="container">
{city_nav_html}
    </div>
  </nav>

  <nav class="breadcrumb" aria-label="Breadcrumb">
    <div class="container">
      <ol>
        <li><a href="/">Home</a></li>
        <li>{breadcrumb_name}</li>
      </ol>
    </div>
  </nav>

  <div class="location-hero">
    <div class="container">
      <h1>{service_name} in {city_name}, Colorado</h1>
      <p>{hero_subtitle}</p>
      <a href="tel:7206757693" class="cta-button">{cta_text}</a>
    </div>
  </div>

  <main>
    <section>
      <div class="container">
        <h2>{service_name} in {city_name} &mdash; Done Right</h2>
        <p class="intro-text">
          {intros[0]}
        </p>
        <p class="intro-text">
          {intros[1]}
        </p>
        <p class="intro-text">
          {intros[2]}
        </p>
      </div>
    </section>

    <section class="services">
      <div class="container">
        <h2>{items_heading}</h2>
        <p class="intro-text">{items_intro}</p>
        <ul class="services-list">
{items_html}
        </ul>
        <div style="text-align:center;margin-top:2rem;">
          <a href="tel:7206757693" class="cta-button">{cta_text}</a>
        </div>
      </div>
    </section>

    <section>
      <div class="container">
        <h2>How It Works &mdash; {service_name} in {city_name}</h2>
        <ol class="why-list" style="max-width:700px;margin:2rem auto 0;text-align:left;">
{how_html_str}
        </ol>
      </div>
    </section>

    <section class="why-us">
      <div class="container">
        <h2>{city_name} Neighborhoods We Serve</h2>
        <p class="intro-text">We cover all of {city_name} — {city["flavor"]}.</p>
        <ul class="why-list">
{nh_html}
        </ul>
      </div>
    </section>

    <section>
      <div class="container">
        <h2>Why {city_name} Residents Choose Go Green Scrap Pros</h2>
        <ul class="why-list" style="max-width:700px;margin:2rem auto 0;text-align:left;">
{why_html_str}
        </ul>
      </div>
    </section>

    <section class="testimonials">
      <div class="container">
        <h2>What Our Customers Say</h2>
        <div class="testimonial-grid">
          <div class="testimonial-card">
            <blockquote>"We thank Adam for his prompt service, flexibility, care in moving, and willingness to locally donate our old sofa and rocker-recliner in a tight timeline. Thank you so much!"</blockquote>
            <div class="author">&mdash; Kathryn S., Westminster, CO</div>
          </div>
          <div class="testimonial-card">
            <blockquote>"Adam did a great job understanding my junk removal, he asked questions and listened to what was needed. Communicative, timely and reasonable price."</blockquote>
            <div class="author">&mdash; Eric Miles, Denver, CO</div>
          </div>
        </div>
      </div>
    </section>

    <section class="why-us">
      <div class="container">
        <h2>Frequently Asked Questions &mdash; {service_name} in {city_name}</h2>
        <div style="max-width:750px;margin:2rem auto 0;text-align:left;">

{faq_details_html}

        </div>
      </div>
    </section>

    <section>
      <div class="container">
        <h2>{final_cta_heading}</h2>
        <p class="intro-text">Call or text 720-675-7693 for a free quote. We'll get back to you fast — usually within the hour.</p>
        <a href="tel:7206757693" class="cta-button">{cta_text}</a>
        <p class="nearby-cities" style="margin-top:2rem;">
          Also serving nearby:
          {nearby_html}
        </p>
        <p style="margin-top:1.5rem;">
          See all our service areas on the <a href="/sitemap/">site map</a>.
        </p>
      </div>
    </section>
  </main>

  <footer>
    <div class="container">
      <div class="footer-nav">
        <a href="/">Home</a>
        <a href="/sitemap/">Site Map</a>
        <a href="tel:7206757693">Get a Free Quote</a>
      </div>
      <div class="footer-cities">
{footer_cities_html}
      </div>
      <div class="footer-cities" aria-label="{city_name} services">
{footer_services_html}
      </div>
      <p>Go Green Scrap Pros &mdash; Thornton, CO 80229 &mdash; 720-675-7693</p>
      <p style="margin-top:1.5rem;font-size:0.9rem;">&copy; 2026 Go Green Scrap Pros. All Rights Reserved.</p>
    </div>
  </footer>
</body>
</html>
'''
    return slug, html


# ─── Sitemap generation ──────────────────────────────────────────────────────
BASE_URL = "https://gogreenscrappros.com"

# Pages that must never appear in the sitemap (internal / utility / disallowed).
SITEMAP_EXCLUDE = {
    "routes-trash",   # disallowed in robots.txt
    "sitemap",        # the HTML sitemap page itself
    "cardinal",       # legacy / unrelated page
    "404",
}


def _sitemap_attrs(path):
    """Return (changefreq, priority) for a given site-relative path.

    Mirrors the conventions used in the hand-maintained sitemap so the
    generated file stays consistent.
    """
    p = path.strip("/")
    service_keys = list(SERVICES.keys())
    city_keys = list(CITIES.keys())

    # Homepage
    if p == "":
        return "weekly", "1.0"
    # Blog index and posts
    if p == "blog":
        return "weekly", "0.8"
    if p.startswith("blog/"):
        return "monthly", "0.7"
    # Static info / conversion pages
    if p == "booking.html":
        return "monthly", "0.7"
    if p == "about":
        return "yearly", "0.6"
    if p == "contact":
        return "yearly", "0.7"
    if p == "case-studies":
        return "monthly", "0.8"
    if p.startswith("case-studies/"):
        return "yearly", "0.8"

    # Service hub pages (e.g. /mattress-removal/)
    if p in service_keys:
        return "monthly", "0.9"

    # City hub pages (e.g. /junk-removal-arvada/) -> 0.8
    if p.startswith("junk-removal-"):
        return "monthly", "0.8"

    # Service+city combo pages (e.g. /mattress-removal-arvada/)
    for s in service_keys:
        for c in city_keys:
            if p == f"{s}-{c}":
                # estate-cleanout and scrap-metal-pickup combos rank 0.8, rest 0.7
                if s in ("estate-cleanout", "scrap-metal-pickup"):
                    return "monthly", "0.8"
                return "monthly", "0.7"

    # Sensible default for anything else discovered on disk
    return "monthly", "0.7"


def discover_all_paths(base_dir):
    """Discover every real page on disk as a set of site-relative paths (e.g.
    "mattress-removal-arvada", "" for the homepage, "booking.html"). This is
    the single source of truth both sitemap.xml and the human-readable
    /sitemap/ page are built from, so they can never drift out of sync with
    each other or with what's actually on disk."""
    paths = set()

    # Directory-based pages: any folder containing an index.html -> "/folder/"
    for idx in glob.glob(os.path.join(base_dir, "**", "index.html"), recursive=True):
        rel = os.path.relpath(os.path.dirname(idx), base_dir)
        rel = "" if rel == "." else rel.replace(os.sep, "/")
        top = rel.split("/")[0] if rel else ""
        if top in SITEMAP_EXCLUDE:
            continue
        paths.add(rel)

    # Standalone top-level .html conversion pages (booking, quote)
    for html in glob.glob(os.path.join(base_dir, "*.html")):
        name = os.path.basename(html)
        if name in ("404.html",):
            continue
        if name == "index.html":
            continue
        paths.add(name)

    return paths


def _sitemap_sort_key(p):
    # Homepage first, then service hubs, then everything else alphabetically
    if p == "":
        return (0, "")
    if p in SERVICES:
        return (1, p)
    if p.startswith("junk-removal-"):
        return (2, p)
    if p.endswith(".html"):
        return (3, p)
    return (4, p)


def generate_sitemap(base_dir, paths):
    """Write sitemap.xml from the discovered path set.

    lastmod is set to today for every URL, so the sitemap always reflects the
    current build. Deleted pages drop out automatically; new pages are picked up.
    """
    today = datetime.date.today().isoformat()

    entries = []
    for p in sorted(paths, key=_sitemap_sort_key):
        if p == "":
            loc = f"{BASE_URL}/"
        elif p.endswith(".html"):
            loc = f"{BASE_URL}/{p}"
        else:
            loc = f"{BASE_URL}/{p}/"
        cf, pr = _sitemap_attrs(p)
        entries.append(
            "  <url>\n"
            f"    <loc>{loc}</loc>\n"
            f"    <lastmod>{today}</lastmod>\n"
            f"    <changefreq>{cf}</changefreq>\n"
            f"    <priority>{pr}</priority>\n"
            "  </url>"
        )

    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n\n'
        + "\n".join(entries)
        + "\n\n</urlset>\n"
    )
    with open(os.path.join(base_dir, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(xml)
    print(f"  Wrote sitemap.xml with {len(entries)} URLs (lastmod={today}).")
    return len(entries)


SERVICE_EMOJI = {
    "estate-cleanout": "🏠",
    "mattress-removal": "🛏️",
    "couch-removal": "🛋️",
    "large-appliance-removal": "🔌",
    "refrigerator-removal": "🧊",
    "air-conditioner-removal": "❄️",
    "treadmill-removal": "🏃",
    "tv-recycling": "📺",
    "scrap-metal-pickup": "🔩",
}


def _city_display_name(city_slug):
    """Name for a city slug, using CITIES if we have it, otherwise a
    title-cased fallback (covers junk-removal-only cities like Loveland
    that predate the CITIES dict and don't have a full entry)."""
    if city_slug in CITIES:
        return CITIES[city_slug]["name"]
    return city_slug.replace("-", " ").title()


def generate_html_sitemap(base_dir, paths):
    """Build the human-readable /sitemap/ page from the same discovered path
    set as sitemap.xml, instead of a hand-maintained list that drifts out of
    sync every time a city or service is added."""
    junk_removal_cities = sorted(
        p[len("junk-removal-"):] for p in paths if p.startswith("junk-removal-")
    )

    service_city_lists = {}
    for service_key in SERVICES:
        prefix = f"{service_key}-"
        cities = sorted(
            p[len(prefix):] for p in paths
            if p.startswith(prefix) and p != service_key
        )
        service_city_lists[service_key] = cities

    case_study_paths = sorted(
        p for p in paths if p.startswith("case-studies/")
    )

    def city_col(cities_slice, title_prefix=""):
        items = "\n".join(
            f'                <li><a href="/junk-removal-{slug}/">{title_prefix}{_city_display_name(slug)}</a></li>'
            for slug in cities_slice
        )
        return items

    # Split the junk-removal city list into two roughly even alphabetical
    # columns for layout - there's no verified "region" data to group by.
    mid = (len(junk_removal_cities) + 1) // 2
    jr_col_a = city_col(junk_removal_cities[:mid], "Junk Removal ")
    jr_col_b = city_col(junk_removal_cities[mid:], "Junk Removal ")

    core_services_items = "\n".join(
        f'                <li><a href="/{key}/">{SERVICES[key]["name"]}</a></li>'
        for key in SERVICES
    )

    case_study_items = ['                <li><a href="/case-studies/">All Case Studies</a></li>']
    for p in case_study_paths:
        slug = p[len("case-studies/"):]
        label = slug.replace("-", " ").title()
        case_study_items.append(f'                <li><a href="/{p}/">{label}</a></li>')

    service_sections = []
    for service_key, cities in service_city_lists.items():
        if not cities:
            continue
        emoji = SERVICE_EMOJI.get(service_key, "")
        name = SERVICES[service_key]["name"]
        items = "\n".join(
            f'                <li><a href="/{service_key}-{slug}/">{name} {_city_display_name(slug)}</a></li>'
            for slug in cities
        )
        service_sections.append(f'''          <div class="sitemap-section">
            <div class="sitemap-col">
              <h3>{emoji} {name}</h3>
              <ul>
{items}
              </ul>
            </div>
          </div>''')
    # Case studies sits alongside the per-service cards in the same grid.
    service_sections.insert(1, f'''          <div class="sitemap-section">
            <div class="sitemap-col">
              <h3>📸 Case Studies</h3>
              <ul>
{chr(10).join(case_study_items)}
              </ul>
            </div>
          </div>''')
    specialty_grid = "\n\n".join(service_sections)

    total_pages = len(paths)

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Browse every page on Go Green Scrap Pros — services and service areas across the Denver Metro, Boulder County, and Northern Colorado.">
  <meta property="og:title" content="Site Map | Go Green Scrap Pros">
  <meta property="og:description" content="Every page on gogreenscrappros.com — services, city pages, and tools.">
  <meta property="og:url" content="https://gogreenscrappros.com/sitemap/">
  <meta property="og:image" content="https://gogreenscrappros.com/assets/images/logo.png">
  <link rel="canonical" href="https://gogreenscrappros.com/sitemap/">

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://gogreenscrappros.com" }},
      {{ "@type": "ListItem", "position": 2, "name": "Site Map", "item": "https://gogreenscrappros.com/sitemap/" }}
    ]
  }}
  </script>

  <meta name="robots" content="index, follow">
  <title>Site Map | Go Green Scrap Pros</title>
  <link rel="stylesheet" href="../assets/style.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" as="style" onload="this.onload=null;this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap"></noscript>
  <style>
    .sitemap-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; max-width: 1100px; margin: 0 auto; }}
    .sitemap-col h3 {{ color: #1e5a4a; margin-bottom: 0.75rem; font-size: 1.1rem; border-bottom: 2px solid #e5efe9; padding-bottom: 0.4rem; }}
    .sitemap-col ul {{ list-style: none; padding: 0; margin: 0 0 1.5rem 0; }}
    .sitemap-col li {{ margin-bottom: 0.4rem; }}
    .sitemap-col a {{ color: #2a6f5e; text-decoration: none; }}
    .sitemap-col a:hover {{ text-decoration: underline; }}
    .sitemap-section {{ background: #fff; border-radius: 10px; padding: 1.5rem; box-shadow: 0 3px 10px rgba(0,0,0,0.05); }}
  </style>
</head>
<body>

  <nav class="site-nav">
    <div class="container">
      <a href="/" class="brand">Go Green Scrap Pros</a>
      <div class="nav-links">
        <a href="/estate-cleanout/">Estate Cleanout</a>
        <a href="/scrap-metal-pickup/">Scrap Metal</a>
        <a href="/case-studies/">Case Studies</a>
        <a href="/blog/">Blog</a>
        <a href="/sitemap/" class="active">Service Areas</a>
        <a href="/about/">About</a>
        <a href="/contact/">Contact</a>
      </div>
      <div class="nav-actions">
        <a href="tel:7206757693" class="nav-cta">Call 720-675-7693</a>
        <a href="sms:7206757693" class="nav-sms">Text Us</a>
      </div>
    </div>
  </nav>

  <nav class="breadcrumb" aria-label="Breadcrumb">
    <div class="container">
      <ol>
        <li><a href="/">Home</a></li>
        <li>Site Map</li>
      </ol>
    </div>
  </nav>

  <div class="location-hero">
    <div class="container">
      <h1>Site Map &amp; Service Areas</h1>
      <p>Every page on the site ({total_pages} total), organized by section. Find the city or service you need.</p>
      <a href="tel:7206757693" class="cta-button">Call or Text for a Free Quote</a>
    </div>
  </div>

  <main>
    <section>
      <div class="container">
        <h2>Main Pages</h2>
        <div class="sitemap-grid">
          <div class="sitemap-section">
            <div class="sitemap-col">
              <h3>Site</h3>
              <ul>
                <li><a href="/">Home</a></li>
                <li><a href="/about/">About Adam &amp; Go Green</a></li>
                <li><a href="/contact/">Contact</a></li>
                <li><a href="/blog/">Blog</a></li>
                <li><a href="/booking.html">Book a Pickup</a></li>
                <li><a href="/sitemap.xml">XML Sitemap (for search engines)</a></li>
              </ul>
            </div>
          </div>
          <div class="sitemap-section">
            <div class="sitemap-col">
              <h3>Core Services</h3>
              <ul>
{core_services_items}
              </ul>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="why-us">
      <div class="container">
        <h2>Junk Removal by City</h2>
        <p class="intro-text">Local junk hauling pages for each city we serve.</p>
        <div class="sitemap-grid">
          <div class="sitemap-section">
            <div class="sitemap-col">
              <h3>Cities A&ndash;{junk_removal_cities[mid-1][0].upper() if mid else ""}</h3>
              <ul>
{jr_col_a}
              </ul>
            </div>
          </div>
          <div class="sitemap-section">
            <div class="sitemap-col">
              <h3>Cities {junk_removal_cities[mid][0].upper() if mid < len(junk_removal_cities) else ""}&ndash;Z</h3>
              <ul>
{jr_col_b}
              </ul>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section>
      <div class="container">
        <h2>Specialty Removal &amp; Recycling — by City</h2>
        <p class="intro-text">Single-item pickup and recycling pages, organized by service. Each link below is a dedicated, local page with FAQs and details for that city.</p>

        <div class="sitemap-grid">
{specialty_grid}
        </div>
      </div>
    </section>

    <section>
      <div class="container">
        <h2>Don't See Your City?</h2>
        <p class="intro-text">
          We serve the entire Denver Metro, Boulder County, and Northern Colorado. If your city isn't
          listed, give us a call — we may already be working in your area.
        </p>
        <a href="tel:7206757693" class="cta-button">Call or Text 720-675-7693</a>
      </div>
    </section>
  </main>

  <footer>
    <div class="container">
      <div class="footer-nav">
        <a href="/">Home</a>
        <a href="/sitemap/">Site Map</a>
        <a href="/about/">About</a>
        <a href="/contact/">Contact</a>
        <a href="tel:7206757693">Get a Free Quote</a>
      </div>
      <p>Go Green Scrap Pros — Thornton, CO 80229 — 720-675-7693</p>
      <p style="margin-top: 1.5rem; font-size: 0.9rem;">© 2026 Go Green Scrap Pros. All Rights Reserved.</p>
    </div>
  </footer>
</body>
</html>
'''

    out_dir = os.path.join(base_dir, "sitemap")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  Wrote sitemap/index.html covering {total_pages} pages.")


# ─── Main: Generate all 56 pages ────────────────────────────────────────────
# ─── Templated static pages ──────────────────────────────────────────────────
# Hand-authored pages (homepage, service hub pages, contact, llms.txt) that
# reference a price live in templates/ with {{PRICE_*}} placeholders instead
# of literal dollar amounts. render_pricing_templates() substitutes each
# placeholder from pricing.json and writes the real file. To change a price:
# edit pricing.json, then rerun this script - never hand-edit a dollar amount
# directly in the rendered output, it will be overwritten on the next build.
PRICE_TOKENS = {
    "{{PRICE_MATTRESS}}": f"${PRICING['mattress']['first_item']}",
    "{{PRICE_MATTRESS_ADDITIONAL}}": f"${PRICING['mattress']['additional_item']}",
    "{{PRICE_MATTRESS_SET}}": f"${PRICING['mattress']['set']}",
    "{{PRICE_COUCH_STARTING}}": f"${PRICING['couch']['starting']}",
    "{{PRICE_APPLIANCE_STARTING}}": f"${PRICING['large_appliance']['starting']}",
    "{{PRICE_GARAGE_LOW}}": f"${PRICING['garage_cleanout']['low']:,}",
    "{{PRICE_GARAGE_HIGH}}": f"${PRICING['garage_cleanout']['high']:,}",
    "{{PRICE_AC}}": f"${PRICING['air_conditioner']['flat']}",
    "{{PRICE_TV}}": f"${PRICING['tv_recycling']['per_unit']}",
    "{{PRICE_ESTATE_LOW}}": f"${PRICING['estate_cleanout']['low']:,}",
    "{{PRICE_ESTATE_HIGH}}": f"${PRICING['estate_cleanout']['high']:,}",
    "{{PRICE_SCRAP_Z1}}": f"${PRICING['scrap_metal']['zone1_fee']}",
    "{{PRICE_SCRAP_Z2}}": f"${PRICING['scrap_metal']['zone2_fee']}",
    "{{PRICE_SCRAP_Z3}}": f"${PRICING['scrap_metal']['zone3_fee']}",
    "{{PRICE_INSIDE_FEE}}": f"${PRICING['scrap_metal']['inside_pickup_fee']}",
}

TEMPLATE_MAP = {
    "index.html": "index.html",
    "contact__index.html": "contact/index.html",
    "scrap-metal-pickup__index.html": "scrap-metal-pickup/index.html",
    "tv-recycling__index.html": "tv-recycling/index.html",
    "mattress-removal__index.html": "mattress-removal/index.html",
    "couch-removal__index.html": "couch-removal/index.html",
    "large-appliance-removal__index.html": "large-appliance-removal/index.html",
    "air-conditioner-removal__index.html": "air-conditioner-removal/index.html",
    "estate-cleanout__index.html": "estate-cleanout/index.html",
    "llms.txt": "llms.txt",
}


def render_pricing_templates(base_dir):
    """Render templates/*.html + templates/llms.txt into their real output
    paths, substituting {{PRICE_*}} placeholders with values from pricing.json."""
    count = 0
    for template_name, output_rel_path in TEMPLATE_MAP.items():
        template_path = os.path.join(base_dir, "templates", template_name)
        with open(template_path, encoding="utf-8") as f:
            content = f.read()
        for token, value in PRICE_TOKENS.items():
            content = content.replace(token, value)
        output_path = os.path.join(base_dir, output_rel_path)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        count += 1
        print(f"  Rendered: {output_rel_path}")
    print(f"\nRendered {count} pricing-templated pages.")


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    count = 0

    for service_key in SERVICES:
        for city_key in CITIES:
            slug, html = generate_page(city_key, service_key)
            page_dir = os.path.join(base_dir, slug)
            os.makedirs(page_dir, exist_ok=True)
            filepath = os.path.join(page_dir, "index.html")
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(html)
            count += 1
            print(f"  Created: {slug}/index.html")

    print(f"\nGenerated {count} city+service pages.")

    render_pricing_templates(base_dir)

    # Always refresh both sitemaps so they reflect the current build - any
    # added/removed page is picked up automatically in both, from the same
    # discovered path set, so they can't drift out of sync with each other.
    all_paths = discover_all_paths(base_dir)
    generate_sitemap(base_dir, all_paths)
    generate_html_sitemap(base_dir, all_paths)
    print("\nDone!")


if __name__ == "__main__":
    main()
