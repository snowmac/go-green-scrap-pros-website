#!/usr/bin/env python3
"""
Generate 56 city+service HTML pages for Go Green Scrap Pros.
8 services x 7 cities = 56 unique pages.
"""
import os
import json

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
    },
}

# ─── Service Data ────────────────────────────────────────────────────────────
SERVICES = {
    "tv-recycling": {
        "name": "TV Recycling",
        "slug": "tv-recycling",
        "item": "TV",
        "price": "$50",
        "price_num": "50",
        "price_free": False,
        "short": "TV recycling",
        "action": "Curbside TV pickup and responsible e-waste recycling",
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
                "For a flat $50, we'll pick up your old TV curbside anywhere in {city_name} — "
                "zip codes {zips_text}. No hauling it to a drop-off. No loading it in your car. "
                "Just set it at the curb and we'll handle the rest. We properly disassemble and recycle "
                "every TV we collect, recovering metals, plastics, and circuit boards for responsible processing."
            ),
            (
                "Serving {neighborhoods_short} and every neighborhood in between, "
                "we make TV recycling in {city_name} as easy as a phone call. "
                "Text or call Adam at 720-675-7693 and we'll get your old TV picked up — usually same-day or next-day."
            ),
        ],
        "how_it_works": [
            ("Schedule Your Pickup", "Call or text Adam at 720-675-7693. Let us know what type and size of TV you have. We'll confirm a pickup window — most jobs are same-day or next-day."),
            ("Set It at the Curb", "Place your TV at the curb or driveway. No need to box it or wrap it. CRTs, flat screens, any size — just get it outside and we take it from there."),
            ("We Recycle It Right", "Your TV gets properly disassembled and recycled. Metals, glass, plastics, and circuit boards are separated and sent to certified processing facilities — not the landfill."),
        ],
        "why_choose": [
            "Flat $50 rate — no hidden fees, no surprises",
            "CRTs, flat screens, plasma, LED, LCD — we take them all",
            "Proper e-waste recycling with certified processors",
            "Curbside pickup — you don't have to haul it anywhere",
            "Same-day and next-day pickup available in {city_name}",
            "Locally owned and operated — you deal with Adam directly",
        ],
        "faqs": [
            ("How much does TV recycling cost in {city_name}?",
             "TV recycling in {city_name} is a flat $50 per TV with Go Green Scrap Pros. That covers curbside pickup and responsible e-waste recycling — no extra fees regardless of TV type or size."),
            ("Do you pick up CRT TVs in {city_name}?",
             "Yes, we pick up all TV types in {city_name} including CRT, LED, LCD, plasma, and projection TVs. CRTs are some of the most important to recycle properly because of the lead in the glass."),
            ("Why can't I just throw my old TV in the trash?",
             "TVs contain hazardous materials including lead, mercury, and cadmium that contaminate soil and groundwater in landfills. Colorado law requires proper e-waste disposal. We make sure your TV is recycled responsibly."),
            ("What zip codes do you serve in {city_name}?",
             "We serve all of {city_name} including zip codes {zips_text}. From {neighborhoods_two} and everywhere in between — we'll come to you."),
            ("How quickly can you pick up my old TV in {city_name}?",
             "Most TV pickups in {city_name} are same-day or next-day. Call or text Adam at 720-675-7693 and we'll lock in a time that works for you."),
        ],
        "pricing_section": [
            ("Single TV (any type, any size)", "$50"),
            ("Multiple TVs", "$50 each"),
            ("TV + other e-waste (monitors, printers)", "Call for bundle price"),
        ],
    },
    "mattress-removal": {
        "name": "Mattress Removal",
        "slug": "mattress-removal",
        "item": "mattress",
        "price": "$80",
        "price_num": "80",
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
                "Go Green Scrap Pros solves this for $80 flat."
            ),
            (
                "We'll pick up your mattress curbside anywhere in {city_name} — all zip codes including "
                "{zips_text}. Twin, full, queen, king — doesn't matter. Box springs too, at the same $80 rate. "
                "We separate the steel springs, foam, and fabric for recycling whenever possible, "
                "keeping as much out of the landfill as we can."
            ),
            (
                "If you're in {neighborhoods_short} or anywhere else in {city_name}, "
                "just text Adam at 720-675-7693. Most pickups are same-day or next-day. "
                "Stop stepping over that mattress — let us take it."
            ),
        ],
        "how_it_works": [
            ("Text or Call Adam", "Reach out at 720-675-7693. Let us know the mattress size and where you are in {city_name}. We'll confirm a pickup window right away."),
            ("Place It Curbside", "Drag it to the curb or driveway — that's all you need to do. If it's still in a bedroom and you need help, ask about our in-home removal option."),
            ("We Haul & Recycle", "We take it away and separate what we can — steel springs go to metal recycling, foam and fabric get processed. No illegal dumping, no shortcuts."),
        ],
        "why_choose": [
            "Flat $80 rate for any mattress size — twin to king",
            "Box springs also $80 — same flat price",
            "We recycle springs, foam, and fabric when possible",
            "Curbside pickup — no need to haul it to a dump yourself",
            "Same-day and next-day pickup available in {city_name}",
            "Locally owned — Adam handles every job personally",
        ],
        "faqs": [
            ("How much does mattress removal cost in {city_name}?",
             "Mattress removal in {city_name} is $80 flat with Go Green Scrap Pros — any size, curbside pickup. Box springs are also $80. No hidden fees or upcharges."),
            ("Do you take box springs too?",
             "Yes. Box springs are $80, same as mattresses. If you're replacing a full set, we'll take both in the same trip."),
            ("Can you pick up a mattress inside my house?",
             "Our standard $80 rate is for curbside pickup. If you need the mattress removed from inside your home, give us a call and we can work something out — especially for stairs or tight spaces."),
            ("What zip codes in {city_name} do you cover?",
             "We cover all of {city_name} — zip codes {zips_text}. From {neighborhoods_two} and everywhere in between."),
            ("What happens to my old mattress after pickup?",
             "We separate recyclable materials — steel springs, foam, and fabric — and send them to appropriate recycling facilities. We keep as much out of the landfill as possible."),
        ],
        "pricing_section": [
            ("Mattress Removal (any size)", "$80"),
            ("Box Spring Removal", "$80"),
            ("Mattress + Box Spring combo", "$160 ($80 each)"),
        ],
    },
    "large-appliance-removal": {
        "name": "Large Appliance Removal",
        "slug": "large-appliance-removal",
        "item": "appliance",
        "price": "$100",
        "price_num": "100",
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
                "For $100 flat, we'll pick up your old washer, dryer, stove, oven, dishwasher, "
                "or any other large household appliance from curbside. We serve all of {city_name} — "
                "zip codes {zips_text}. Every appliance we pick up gets stripped for metal, which goes straight "
                "to recycling. That's the Go Green way."
            ),
            (
                "Whether you're upgrading your kitchen in {neighborhoods_sample} or "
                "finally replacing that 20-year-old washer, we've got you covered. "
                "Call or text Adam at 720-675-7693 for same-day or next-day pickup in {city_name}."
            ),
        ],
        "how_it_works": [
            ("Call or Text Us", "Reach Adam at 720-675-7693. Tell us what appliance you need removed and your address in {city_name}. We'll set up a pickup window."),
            ("Move It to the Curb", "Get the appliance to curbside or your driveway. If it's too heavy or awkward, let us know and we can discuss options."),
            ("We Pick Up & Recycle", "We load it up, haul it away, and recycle every bit of metal from the unit. Steel, copper, aluminum — it all gets a second life."),
        ],
        "why_choose": [
            "Flat $100 rate per appliance — no surprise fees",
            "Washers, dryers, stoves, dishwashers — all covered",
            "Metal from every appliance gets recycled",
            "Curbside pickup means zero hassle for you",
            "Same-day and next-day availability in {city_name}",
            "Owner-operated — Adam handles your job personally",
        ],
        "faqs": [
            ("How much does appliance removal cost in {city_name}?",
             "Large appliance removal in {city_name} is $100 flat per appliance with Go Green Scrap Pros. That covers curbside pickup and recycling for washers, dryers, stoves, dishwashers, and more."),
            ("Do you take refrigerators too?",
             "Refrigerators require special handling for freon recovery, so they have a separate service. Check our refrigerator removal page for {city_name} for details on that."),
            ("What happens to the old appliance?",
             "We strip every appliance for recyclable metals — steel, copper, aluminum. The metal goes to certified recyclers. We recover as much material as possible and keep it out of the landfill."),
            ("What {city_name} zip codes do you serve?",
             "We serve all of {city_name} including zip codes {zips_text}. {neighborhoods_two} — we cover every neighborhood."),
            ("Can you pick up multiple appliances at once?",
             "Absolutely. If you're doing a kitchen or laundry room overhaul in {city_name}, we'll take all the old appliances in one trip. Each unit is $100."),
        ],
        "pricing_section": [
            ("Washer or Dryer Removal", "$100"),
            ("Stove / Oven / Range Removal", "$100"),
            ("Dishwasher Removal", "$100"),
            ("Multiple appliances", "$100 each"),
        ],
    },
    "refrigerator-removal": {
        "name": "Refrigerator Removal",
        "slug": "refrigerator-removal",
        "item": "refrigerator",
        "price": "$100",
        "price_num": "100",
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
                "For $100 flat, we'll pick up your old fridge, stand-up freezer, mini-fridge, or wine cooler "
                "from curbside anywhere in {city_name} — zip codes {zips_text}. "
                "We ensure proper refrigerant recovery before the unit is dismantled, and the metal "
                "gets recycled. It's the right way to get rid of an old fridge."
            ),
            (
                "From {neighborhoods_short} to every corner of {city_name}, "
                "we make fridge disposal easy and compliant. "
                "Call or text Adam at 720-675-7693 — most pickups happen same-day or next-day."
            ),
        ],
        "how_it_works": [
            ("Schedule the Pickup", "Call or text Adam at 720-675-7693. Let us know what type of unit you have — fridge, freezer, mini-fridge — and your {city_name} address."),
            ("Set It Curbside", "Move the fridge to the curb or driveway. Defrost it if you can, but don't worry about cleaning it out — we've seen it all."),
            ("We Handle Freon & Recycling", "We ensure proper refrigerant recovery per EPA guidelines, then dismantle and recycle the metal. No shortcuts, no illegal dumping."),
        ],
        "why_choose": [
            "Flat $100 rate — fridge, freezer, mini-fridge, wine cooler",
            "Proper freon recovery per EPA regulations",
            "All metal gets recycled after refrigerant removal",
            "No fines, no risk — we handle compliance for you",
            "Same-day and next-day pickup in {city_name}",
            "Honest, owner-operated service — call or text Adam",
        ],
        "faqs": [
            ("How much does refrigerator removal cost in {city_name}?",
             "Refrigerator removal in {city_name} is $100 flat with Go Green Scrap Pros. That covers curbside pickup, proper refrigerant recovery, and metal recycling."),
            ("Why does fridge removal cost $100?",
             "Fridges require certified refrigerant (freon) recovery before they can be recycled or disposed of. This extra step is required by the EPA and adds to the process — but it keeps harmful chemicals out of the atmosphere."),
            ("Do you take freezers and mini-fridges too?",
             "Yes. Stand-up freezers, chest freezers, mini-fridges, wine coolers — any unit that contains refrigerant. Same $100 flat rate."),
            ("What {city_name} areas do you serve?",
             "We serve all of {city_name} — zip codes {zips_text} — including {neighborhoods_two} and surrounding areas."),
            ("Is it illegal to dump a refrigerator in {city_name}?",
             "Yes. Dumping appliances containing refrigerants is illegal under federal EPA regulations. Fines can be significant. We handle compliant disposal so you don't have to worry about it."),
        ],
        "pricing_section": [
            ("Refrigerator Removal", "$100"),
            ("Stand-up Freezer Removal", "$100"),
            ("Mini-Fridge or Wine Cooler", "$100"),
        ],
    },
    "air-conditioner-removal": {
        "name": "Air Conditioner Removal",
        "slug": "air-conditioner-removal",
        "item": "air conditioner",
        "price": "$50",
        "price_num": "50",
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
                "For just $50, we'll pick up your window AC or portable air conditioner curbside anywhere in "
                "{city_name}. We serve zip codes {zips_text} and handle proper refrigerant recovery before "
                "recycling the metal housing, copper coils, and other materials. "
                "It's cheap, easy, and the right thing to do."
            ),
            (
                "Whether you're in {neighborhoods_short} or anywhere else in {city_name}, "
                "AC removal doesn't have to be a headache. "
                "Text or call Adam at 720-675-7693 and we'll schedule a quick pickup."
            ),
        ],
        "how_it_works": [
            ("Contact Adam", "Call or text 720-675-7693. Let us know how many AC units you have and your location in {city_name}. We'll schedule your pickup."),
            ("Put It at the Curb", "Window units and portable ACs are small enough to carry outside. Just set it at the curb or driveway and we'll grab it."),
            ("Proper Disposal & Recycling", "We recover any refrigerant safely, then recycle the metal — copper coils, aluminum fins, steel housing. Done the right way."),
        ],
        "why_choose": [
            "Only $50 per unit — affordable AC disposal",
            "Window units and portable ACs both accepted",
            "Proper refrigerant handling — no shortcuts",
            "Metals recycled: copper, aluminum, steel",
            "Quick curbside pickup in {city_name}",
            "Owner-operated — Adam picks up the phone and does the work",
        ],
        "faqs": [
            ("How much does AC removal cost in {city_name}?",
             "Air conditioner removal in {city_name} is $50 flat per unit with Go Green Scrap Pros. That covers curbside pickup, refrigerant handling, and metal recycling."),
            ("Do you remove central AC units?",
             "We focus on window units and portable AC units. Central AC systems require HVAC professionals for removal. If you have a window unit or portable AC, we're your guys."),
            ("Why can't I throw an AC unit in the trash?",
             "AC units contain refrigerants that are harmful to the ozone layer and must be recovered by certified professionals. Tossing them in the trash or leaving them at the curb for garbage pickup is not allowed."),
            ("What areas of {city_name} do you cover?",
             "All of {city_name} — zip codes {zips_text}. {neighborhoods_two} and every neighborhood in between."),
            ("Can you pick up multiple AC units at once?",
             "Absolutely. If you're cleaning out a rental property or doing a seasonal purge, we'll take all your old AC units in one trip. $50 each."),
        ],
        "pricing_section": [
            ("Window AC Unit Removal", "$50"),
            ("Portable AC Removal", "$50"),
            ("Multiple units", "$50 each"),
        ],
    },
    "treadmill-removal": {
        "name": "Treadmill Removal",
        "slug": "treadmill-removal",
        "item": "treadmill",
        "price": "$150",
        "price_num": "150",
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
                "For $150 flat, we'll pick up your treadmill curbside anywhere in {city_name} — "
                "zip codes {zips_text}. The metal frame, motor housing, and steel components all get recycled. "
                "You get your space back, and another hunk of metal stays out of the landfill."
            ),
            (
                "From {neighborhoods_short} to every corner of {city_name}, "
                "we've hauled treadmills out of basements, spare bedrooms, and garages. "
                "Call or text Adam at 720-675-7693 and let's get that thing gone."
            ),
        ],
        "how_it_works": [
            ("Call or Text Adam", "Reach out at 720-675-7693. Describe the equipment — treadmill, elliptical, weight machine — and your location in {city_name}."),
            ("Get It to the Curb", "If you can get it to the curb or driveway, perfect — that's our $150 flat rate. Can't move it? Ask about our in-home removal option."),
            ("We Haul & Recycle", "We load it up and recycle the metal frame, motor, and steel components. The heavy lifting is on us."),
        ],
        "why_choose": [
            "$150 flat rate for treadmill removal — no surprises",
            "Ellipticals, weight machines, exercise bikes also accepted",
            "Metal frames and motors get recycled",
            "We handle the heavy lifting — these things are beasts",
            "Same-day and next-day pickup in {city_name}",
            "Locally owned — Adam gives you straight answers",
        ],
        "faqs": [
            ("How much does treadmill removal cost in {city_name}?",
             "Treadmill removal in {city_name} is $150 flat with Go Green Scrap Pros. That's for curbside pickup. If you need help getting it out of a basement or upstairs room, give us a call to discuss options."),
            ("Do you take other exercise equipment besides treadmills?",
             "Yes. Ellipticals, stationary bikes, weight machines, home gym systems — we take it all. Pricing depends on the item, but $150 is the treadmill rate."),
            ("Why are treadmills so expensive to remove?",
             "Treadmills are exceptionally heavy — most weigh 200-350 pounds. The motor assembly, steel frame, and belt mechanism make them one of the heaviest single household items. The $150 rate reflects the effort involved."),
            ("What {city_name} areas do you serve for treadmill removal?",
             "All of {city_name} — zip codes {zips_text}. From {neighborhoods_two} and everywhere in between. If you're in {city_name}, we'll come to you."),
            ("Can you pick up a treadmill from my basement?",
             "Our $150 flat rate covers curbside pickup. Basement or upstairs removal is possible but may cost extra depending on the stairs and access. Call Adam at 720-675-7693 and we'll work something out."),
        ],
        "pricing_section": [
            ("Treadmill Removal (curbside)", "$150"),
            ("Elliptical Removal", "Call for pricing"),
            ("Exercise Bike / Weight Machine", "Call for pricing"),
        ],
    },
    "couch-removal": {
        "name": "Couch Removal",
        "slug": "couch-removal",
        "item": "couch",
        "price": "$90",
        "price_num": "90",
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
                "For $90 flat, we pick up your old couch, sofa, loveseat, or sectional from curbside "
                "anywhere in {city_name}. We serve all zip codes: {zips_text}. "
                "When the couch is in decent shape, we'll try to donate it. When it's not, "
                "we separate recyclable materials — wood frames, metal springs, foam — and handle disposal responsibly."
            ),
            (
                "From {neighborhoods_short} to the rest of {city_name}, "
                "we've hauled more couches than we can count. "
                "Call or text Adam at 720-675-7693 and we'll get that couch out of your way."
            ),
        ],
        "how_it_works": [
            ("Schedule the Pickup", "Text or call Adam at 720-675-7693. Let us know what you've got — couch, loveseat, sectional — and your {city_name} address."),
            ("Get It to the Curb", "Drag it to the curb or driveway. Can't fit it through the door? We've been there — ask about our in-home removal option."),
            ("We Haul, Donate, or Recycle", "We pick it up and donate when possible. If it's past its useful life, we separate wood, metal, and foam for recycling."),
        ],
        "why_choose": [
            "$90 flat rate — couches, sofas, loveseats",
            "Sectionals and sofa beds accepted too",
            "Donation when the couch is still in good shape",
            "Materials recycled when donation isn't an option",
            "Same-day and next-day availability in {city_name}",
            "Honest pricing from a local, owner-operated business",
        ],
        "faqs": [
            ("How much does couch removal cost in {city_name}?",
             "Couch removal in {city_name} is $90 flat with Go Green Scrap Pros. That covers curbside pickup for a standard couch or sofa. Sectionals may be slightly more depending on size."),
            ("Do you take sectionals and sofa beds?",
             "Yes. Sectionals, sofa beds, futons, recliners, loveseats — we take it all. Oversized sectionals may have a small upcharge, but we'll tell you upfront."),
            ("Will you donate my old couch?",
             "If the couch is in usable condition, we absolutely try to donate it to local charities. We'd rather see it get a second life than end up in a landfill."),
            ("What {city_name} zip codes do you serve?",
             "We serve all of {city_name} — zip codes {zips_text}. {neighborhoods_two} and every neighborhood in between."),
            ("Can you remove a couch from inside my house?",
             "Our $90 rate is for curbside pickup. If you need help getting a couch out of a room, through a tight hallway, or down stairs, call Adam and we'll discuss options."),
        ],
        "pricing_section": [
            ("Couch / Sofa Removal", "$90"),
            ("Loveseat Removal", "$90"),
            ("Sectional Removal", "From $90 (depends on size)"),
            ("Recliner Removal", "$90"),
        ],
    },
    "scrap-metal-pickup": {
        "name": "Scrap Metal Pickup",
        "slug": "scrap-metal-pickup",
        "item": "scrap metal",
        "price": "FREE",
        "price_num": "0",
        "price_free": True,
        "short": "scrap metal pickup",
        "action": "Free curbside scrap metal pickup and recycling",
        "what_we_take": "Steel, aluminum, copper, brass, iron, old metal furniture, metal fencing, auto parts, and any other metal items",
        "schema_name": "Free Scrap Metal Pickup",
        "intro_templates": [
            (
                "Got scrap metal piling up in the garage, backyard, or on a job site in {city_name}? "
                "Don't pay someone to take it — we'll pick it up for free. Go Green Scrap Pros offers "
                "free curbside scrap metal pickup across all of {city_name} because we make our money "
                "by recycling the metal. You win, we win, the landfill loses. That's the deal."
            ),
            (
                "Steel, aluminum, copper, brass, iron — old grills, metal shelving, car parts, fencing, "
                "pipes, wiring, appliance shells — if it's metal and you can get it to the curb, "
                "we'll take it at no charge. We serve all of {city_name} including zip codes {zips_text}. "
                "No catch, no minimum quantity."
            ),
            (
                "Whether you're in {neighborhoods_short} or anywhere else in {city_name}, "
                "free scrap metal pickup is just a phone call away. "
                "Text or call Adam at 720-675-7693 and we'll swing by — usually same-day or next-day."
            ),
        ],
        "how_it_works": [
            ("Contact Adam", "Call or text 720-675-7693. Tell us what kind of metal you have and roughly how much. We'll schedule a pickup."),
            ("Set It at the Curb", "Pile your scrap metal at the curb or driveway. Steel beams, old appliances, copper pipe, aluminum cans — whatever you've got."),
            ("We Pick It Up Free", "We come by, load it up, and take it to the recycler. You pay nothing. We make money on the scrap value, and the metal gets a second life."),
        ],
        "why_choose": [
            "Always FREE — no charge for curbside scrap metal pickup",
            "Steel, aluminum, copper, brass, iron — all accepted",
            "No minimum quantity — even a few pieces are fine",
            "We recycle everything we collect",
            "Same-day and next-day pickup in {city_name}",
            "Locally owned — Adam is the one who shows up",
        ],
        "faqs": [
            ("Is scrap metal pickup really free in {city_name}?",
             "Yes, 100% free. We make our money by selling the scrap metal to recyclers. As long as it's at the curb and it's metal, there's no charge. {city_name} zip codes {zips_text} — all covered."),
            ("What types of metal do you pick up?",
             "Steel, aluminum, copper, brass, iron, tin — basically all metals. Old grills, metal furniture, car parts, fencing, pipes, wiring, appliance shells, bed frames, filing cabinets — if it's metal, we want it."),
            ("Do I need a minimum amount of scrap metal?",
             "No minimum. Whether it's a single old metal shelf or a whole pile of scrap from a renovation project in {city_name}, we'll come get it."),
            ("What {city_name} zip codes do you serve?",
             "All of {city_name} — zip codes {zips_text}. From {neighborhoods_two} and everywhere in between."),
            ("How quickly can you pick up scrap metal in {city_name}?",
             "Most pickups are same-day or next-day. Call or text Adam at 720-675-7693 and we'll get on the schedule fast."),
        ],
        "pricing_section": [
            ("Scrap Metal Pickup (curbside)", "FREE"),
            ("Steel, Iron, Aluminum", "FREE"),
            ("Copper, Brass", "FREE"),
            ("Mixed metals / clean-out piles", "FREE"),
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
    """Return 2-3 neighborhood names for a short mention."""
    nh = city["neighborhoods"]
    return f"{nh[0]}, {nh[1]}, and {nh[2]}"


def neighborhoods_two(city):
    """Return two neighborhoods for FAQ-style mention."""
    nh = city["neighborhoods"]
    return f"{nh[0]} to {nh[3]}"


def neighborhoods_sample(city):
    """Return a neighborhood sample for general mention."""
    nh = city["neighborhoods"]
    return f"{nh[0]} or {nh[4]}"


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
        .replace("{price}", service["price"])
        .replace("{service_name}", service["name"])
    )


def generate_page(city_key, service_key):
    """Generate complete HTML page for a city+service combination."""
    city = CITIES[city_key]
    service = SERVICES[service_key]
    slug = f"{service['slug']}-{city['slug']}"
    city_name = city["name"]
    service_name = service["name"]
    price = service["price"]
    price_num = service["price_num"]
    is_free = service["price_free"]

    canonical = f"https://gogreenscrappros.com/{slug}/"
    zips_text = format_zips(city["zips"])

    # --- Title ---
    if is_free:
        title = f"{service_name} {city_name} CO | Free Curbside Pickup"
    else:
        title = f"{service_name} {city_name} CO | {price} Curbside Pickup"

    # --- Meta description ---
    if is_free:
        meta_desc = (
            f"Free {service['short']} in {city_name}, CO. Steel, aluminum, copper, brass — "
            f"curbside pickup at no charge. Call Adam: 720-675-7693."
        )
    else:
        meta_desc = (
            f"{service_name} in {city_name}, CO — {price} flat rate curbside pickup. "
            f"{service['what_we_take']}. Call Adam: 720-675-7693."
        )

    # --- OG tags ---
    if is_free:
        og_title = f"Free {service_name} in {city_name} CO | Go Green Scrap Pros"
        og_desc = f"Free curbside {service['short']} in {city_name}. We recycle all metals. Call 720-675-7693."
    else:
        og_title = f"{service_name} {city_name} CO | {price} Flat Rate"
        og_desc = f"{service_name} in {city_name} — {price} flat. {service['action']}. Call 720-675-7693."

    # --- JSON-LD: LocalBusiness ---
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
        "description": f"{service_name} in {city_name}, CO. {service['action']}. Call 720-675-7693.",
        "areaServed": city_name,
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": f"{service_name} in {city_name}",
            "itemListElement": [
                {
                    "@type": "Offer",
                    "itemOffered": {"@type": "Service", "name": service["schema_name"]},
                    "price": price_num,
                    "priceCurrency": "USD"
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
    city_nav_links = []
    for ck in ["thornton", "arvada", "westminster", "golden", "wheat-ridge", "broomfield", "northglenn"]:
        cd = CITIES[ck]
        href = f"/{service['slug']}-{ck}/"
        active = ' class="active"' if ck == city_key else ""
        city_nav_links.append(f'      <a href="{href}"{active}>{cd["name"]}</a>')
    city_nav_html = "\n".join(city_nav_links)

    # --- Pricing rows ---
    pricing_rows = []
    for item_name, item_price in service["pricing_section"]:
        pricing_rows.append(
            f'          <li>{item_name} <span class="price">{item_price}</span></li>'
        )
    pricing_html = "\n".join(pricing_rows)

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

    # --- CTA text ---
    if is_free:
        hero_subtitle = f"Free curbside {service['short']} — steel, aluminum, copper, brass. Serving all of {city_name}."
        cta_text = f"Book Now &mdash; Free {service_name} in {city_name}"
        final_cta_heading = f"Schedule Your Free Pickup in {city_name}"
    else:
        hero_subtitle = f"{service_name} {price} flat rate — curbside pickup serving all of {city_name}."
        cta_text = f"Book Now &mdash; {service_name} in {city_name}"
        final_cta_heading = f"Get a Quote in {city_name}"

    # --- Footer city links (keep pointing to junk-removal-* pages like existing site) ---
    footer_city_links = []
    for ck in ["thornton", "arvada", "westminster", "golden", "wheat-ridge", "broomfield", "northglenn"]:
        cd = CITIES[ck]
        footer_city_links.append(f'        <a href="/junk-removal-{ck}/">{cd["name"]}</a>')
    footer_cities_html = "\n".join(footer_city_links)

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
      <a href="/booking.html?ref={slug}" class="cta-button">{cta_text}</a>
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
        <h2>{service_name} &mdash; Pricing in {city_name}</h2>
        <p class="intro-text">Straight prices. No surprise charges when we arrive.</p>
        <ul class="services-list">
{pricing_html}
        </ul>
        <div style="text-align:center;margin-top:2rem;">
          <a href="/booking.html?ref={slug}" class="cta-button">{cta_text}</a>
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
        <p class="intro-text">Call or text 720-675-7693. We'll get back to you fast — usually within the hour.</p>
        <a href="/booking.html?ref={slug}" class="cta-button">{cta_text}</a>
        <p class="nearby-cities" style="margin-top:2rem;">
          Also serving nearby:
          {nearby_html}
        </p>
      </div>
    </section>
  </main>

  <footer>
    <div class="container">
      <div class="footer-nav">
        <a href="/">Home</a>
        <a href="tel:7206757693">Get a Quote</a>
      </div>
      <div class="footer-cities">
{footer_cities_html}
      </div>
      <p>Go Green Scrap Pros &mdash; Thornton, CO 80229 &mdash; 720-675-7693</p>
      <p style="margin-top:1.5rem;font-size:0.9rem;">&copy; 2026 Go Green Scrap Pros. All Rights Reserved.</p>
    </div>
  </footer>
</body>
</html>
'''
    return slug, html


# ─── Main: Generate all 56 pages ────────────────────────────────────────────
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

    print(f"\nDone! Generated {count} pages.")


if __name__ == "__main__":
    main()
