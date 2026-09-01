#!/usr/bin/env python3
"""
New Super Polymers — static site builder.

Composes the shared shell (head / header / footer) with per-page content and
writes plain static HTML. No runtime dependency: the output is deployable
to any host as-is. Re-run `python3 build.py` after editing content.
"""
import os, html

SITE   = "New Super Polymers India Pvt Ltd"
SHORT  = "New Super Polymers"
ORIGIN = "https://www.newsuperpolymers.com"

# Set to False once every specification below has been confirmed by the plant.
# While True, unverified figures carry a small "verify" flag in the spec tables.
DRAFT = True

TEL1   = "+91 97860 50000"
TEL1R  = "+919786050000"
TEL2   = "+91 78678 65777"
TEL2R  = "+917867865777"
MAILMD = "md@newsuperpolymers.com"
MAILSA = "sales@newsuperpolymers.com"
WA     = "https://wa.me/919786050000"
ADDR   = ("Tirupati Industrial Park, Saphire Building, First Floor,<br>"
          "Unit No. F1 / F9 / F10 / F11, Sativali Road,<br>"
          "Vasai East, Dist. Palghar 401208, Maharashtra, India")

# ---------------------------------------------------------------- colours
COLOURS = [
    ("Natural",  "#DCE6E8", "transparent"),
    ("Clear",    "#E4EEF1", "transparent"),
    ("White",    "#F1EFE9", "opaque"),
    ("Red",      "#CE3327", "coloured"),
    ("Blue",     "#1D5FA6", "coloured"),
    ("Green",    "#1E874A", "coloured"),
    ("Yellow",   "#F0BE28", "radium"),
    ("Orange",   "#E5761D", "radium"),
    ("Violet",   "#6A4CA6", "coloured"),
    ("Purple",   "#8E3FAD", "coloured"),
    ("Pink",     "#DE5A8E", "radium"),
    ("Black",    "#20242B", "opaque"),
]

# ---------------------------------------------------------------- specs
# v=True  -> published on the current site / confirmed by the client
# v=False -> sensible industry default, flagged for confirmation
BASE_SPEC = [
    ("Material",         "Flexible PVC (polyvinyl chloride)",            True),
    ("Form",             "Seamless lay-flat tube, wound on roll",        True),
    ("Gauge",            "0.05 – 0.40 mm",                               True),
    ("Thickness",        "50 – 400 micron (2 – 16 mil)",                 True),
    ("Lay-flat width",   "25 – 1000 mm (1&quot; – 40&quot;)",            False),
    ("Roll length",      "Made to order — typically 50 – 500 m",         False),
    ("Core",             "76 mm (3&quot;) ID paper core",                False),
    ("Gauge tolerance",  "&plusmn;5% on nominal",                        False),
    ("Width tolerance",  "&plusmn;2 mm",                                 False),
    ("Pattern",          "Plain (printing available to order)",          True),
    ("Packaging type",   "Tubing roll — poly-wrapped, palletised",       True),
    ("Lead time",        "45 – 60 days from confirmed order",            True),
    ("Minimum order",    "On request",                                   True),
    ("Terms",            "EXW Vasai · FOB Nhava Sheva · CIF on request", False),
]

def spec_rows(rows):
    out = []
    for k, v, ok in rows:
        flag = "" if (ok or not DRAFT) else "<em>verify</em>"
        out.append(f"<tr><th>{k}</th><td>{v}{flag}</td></tr>")
    return "\n".join(out)

# ---------------------------------------------------------------- products
P = lambda **k: k
PRODUCTS = [
 P(slug="lay-flat-tubing-transparent", name="Transparent Lay&nbsp;Flat Tubing",
   short="Transparent Lay Flat Tubing", img="roll-natural.svg",
   tags="tubing transparent",
   tag="Clear / natural", family="PVC Lay Flat Tubing",
   blurb="Optical clarity for packs that have to sell themselves. The product is the label.",
   intro="Our highest-clarity grade. Natural and clear PVC give a bright, glass-like wall that shows "
         "colour, print and finish underneath without haze — the right choice wherever the pack has to "
         "be read through, checked through, or merchandised on a shelf.",
   colours=["Natural", "Clear"],
   apps=["Retail and shelf-ready packaging", "Stationery, files and folders",
         "Textile and garment protection", "Component kitting and inspection",
         "Over-wrap where contents must stay visible"],
   note="Clarity is set at the die and the frost line. Gauge uniformity is what keeps the wall from "
        "reading cloudy, so this grade is scanned to the tightest tolerance we run."),

 P(slug="lay-flat-tubing-coloured", name="Coloured Lay&nbsp;Flat Tubing",
   short="Coloured Lay Flat Tubing", img="roll-red.svg",
   tags="tubing coloured opaque",
   tag="Ten stock colours", family="PVC Lay Flat Tubing",
   blurb="A full stock colour library — for line separation, grade coding and brand identity.",
   intro="Colour is the fastest instruction on a factory floor. Our stock library runs from red through "
         "violet, matched to a retained reference for every batch, so a roll delivered next year reads "
         "the same as the one on the bench today.",
   colours=["Red", "Blue", "Green", "Violet", "Purple", "Pink", "Orange", "Yellow"],
   apps=["Grade, size and batch colour-coding", "Line and shift separation on the floor",
         "Brand-matched retail packaging", "Light-sensitive contents",
         "Distribution channel identification"],
   note="Colour is compounded in, not printed on — it will not scuff off in transit. "
        "Custom shades matched to a supplied reference chip are available to order."),

 P(slug="lay-flat-tubing-radium", name="Radium Lay&nbsp;Flat Tubing",
   short="Radium Lay Flat Tubing", img="roll-yellow.svg",
   tags="tubing radium coloured",
   tag="Fluorescent", family="PVC Lay Flat Tubing",
   blurb="High-visibility fluorescent film for anything that must not be missed.",
   intro="Radium — fluorescent — grades carry pigments that return far more visible light than a "
         "standard colour. Under warehouse lighting they read as almost lit from within, which is "
         "exactly what you want on a priority pack, a hazard item or a returns lane.",
   colours=["Yellow", "Orange", "Pink"],
   apps=["Priority, hold and quarantine packs", "Hazard and safety identification",
         "High-traffic warehouse picking", "Returns and rework lanes",
         "Point-of-sale and promotional flashes"],
   note="Fluorescent pigment loading is higher than standard colour, which changes how the melt "
        "behaves. These grades run on their own schedule with their own frost-line settings."),

 P(slug="lay-flat-tubing-opaque", name="Opaque Lay&nbsp;Flat Tubing",
   short="Opaque Lay Flat Tubing", img="roll-white.svg",
   tags="tubing opaque",
   tag="Solid / blockout", family="PVC Lay Flat Tubing",
   blurb="A solid wall. Nothing goes in, nothing shows out.",
   intro="Where clarity is the wrong answer. Opaque white and black grades give a solid, non-reading "
         "wall that hides contents in transit, protects light-sensitive product and gives print a clean "
         "ground to sit on.",
   colours=["White", "Black"],
   apps=["Confidential and high-value despatch", "Light-sensitive contents",
         "A clean substrate for surface print", "Neutral over-wrap",
         "Contents concealment in open logistics"],
   note="White is the usual ground for printed work — it lifts ink density and keeps colour "
        "consistent across a run."),

 P(slug="pvc-sheet-roll", name="PVC Sheet Roll",
   short="PVC Sheet Roll", img="sheet-roll.svg",
   tags="sheet transparent coloured",
   tag="Single wall", family="PVC Sheet Roll",
   blurb="Flat film on the roll — for converters who cut, weld, fold and finish in-house.",
   intro="The same compound and the same line, slit open instead of left tubular. Sheet roll is single "
         "wall film supplied flat and wound to length, for customers running their own cutting, "
         "high-frequency welding, folding or lamination downstream.",
   colours=["Natural", "Clear", "White", "Red", "Blue", "Green", "Yellow", "Orange"],
   apps=["File, folder and document covers", "High-frequency welded pouches and wallets",
         "Book and stationery binding", "Protective interleaving and separation",
         "Second-stage conversion and lamination"],
   note="Supplied as a single flat web — not a tube. Tell us your finished width and we will "
        "slit to it rather than leave you trimming."),

 P(slug="printed-lay-flat-tubing", name="Printed Lay&nbsp;Flat Tubing",
   short="Printed Lay Flat Tubing", img="printed-tubing.svg",
   tags="tubing printed made-to-order coloured",
   tag="Made to order", family="PVC Lay Flat Tubing",
   blurb="Your mark, your batch code, your warnings — repeated down the whole roll.",
   intro="Surface-printed tubing carries brand marks, statutory warnings, batch windows and handling "
         "instructions in repeat along the roll, so the pack is identified the moment it is filled and "
         "cut — no second labelling operation, no label that peels off in transit.",
   colours=["Natural", "Clear", "White"],
   apps=["Branded retail and e-commerce packs", "Statutory warnings and handling marks",
         "Batch, date and lot windows", "Anti-counterfeit and tamper marking",
         "Promotional and seasonal runs"],
   note="Made to order against approved artwork. Send us a print-ready file and the repeat length "
        "and we will proof before the run."),

 P(slug="gusseted-lay-flat-tubing", name="Gusseted Lay&nbsp;Flat Tubing",
   short="Gusseted Lay Flat Tubing", img="gusseted-tubing.svg",
   tags="tubing made-to-order transparent coloured",
   tag="Made to order", family="PVC Lay Flat Tubing",
   blurb="Side folds that let a flat tube open into a square pack.",
   intro="A gusset is a fold worked into each side of the tube as it is flattened. It lets the pack open "
         "out to a squared box shape around bulky or rigid contents while still shipping to you as a "
         "compact flat roll — more usable volume for the same lay-flat width.",
   colours=["Natural", "Clear", "White", "Blue"],
   apps=["Bulky, boxed or rigid contents", "Squared-off retail presentation",
         "Palletised bulk liners", "Component and hardware kitting",
         "Anything that a flat tube wastes film around"],
   note="Made to order. Gusset depth is set on the collapsing frame, so it is fixed for the run — "
        "give us the finished pack dimensions and we will work back to the tube."),
]
PBY = {p["slug"]: p for p in PRODUCTS}

INDUSTRIES = [
 ("Packaging &amp; converting",
  "Converters who buy film by the tonne and turn it into bags, sleeves and pouches on their own "
  "sealing lines. Consistency roll to roll is the whole relationship.",
  ["Bag and pouch making", "Sealing and cutting lines", "Contract packing"]),
 ("Textiles &amp; garments",
  "Garment, hosiery and made-up protection where the pack has to be clear enough to read the "
  "product and tough enough to survive a container.",
  ["Garment and hosiery packing", "Fabric roll protection", "Export consolidation"]),
 ("Stationery &amp; printing",
  "File covers, folders, binding and document protection — where sheet roll and clear tubing both "
  "have a job, often on the same order.",
  ["File and folder covers", "Book and binder covers", "Document protection"]),
 ("Food &amp; FMCG",
  "Fast-moving goods that need a clean, consistent over-wrap at volume, with the documentation to "
  "back it up. Food-contact grade is quoted to specification.",
  ["Dry goods over-wrap", "Retail multipacks", "Shelf-ready presentation"]),
 ("Pharmaceutical &amp; medical",
  "Secondary packaging and device protection where batch traceability, retained samples and a "
  "documented change process are non-negotiable.",
  ["Secondary packaging", "Device and kit protection", "Batch-traceable supply"]),
 ("Agriculture &amp; horticulture",
  "Seed, nursery and produce handling — including the fluorescent grades that stay findable "
  "outdoors and in low light.",
  ["Seed and nursery packing", "Produce handling", "Field identification"]),
 ("Industrial &amp; hardware",
  "Fasteners, components, spares and tooling: colour-coded by grade, protected against handling "
  "damage, kitted and identified at the point of pack.",
  ["Component kitting", "Spares and service packs", "Grade colour-coding"]),
]

# ================================================================= shell

def LOGO(sfx="h"):
    return '''<svg class="brand-mark" viewBox="0 0 72 72" aria-hidden="true">
  <defs>
    <linearGradient id="tile%(s)s" x1=".12" y1="0" x2=".88" y2="1">
      <stop offset="0" stop-color="#E2F4F7" stop-opacity=".17"/>
      <stop offset=".52" stop-color="#E2F4F7" stop-opacity=".05"/>
      <stop offset="1" stop-color="#E2F4F7" stop-opacity=".015"/>
    </linearGradient>
    <linearGradient id="mono%(s)s" x1="0" y1="0" x2=".65" y2="1">
      <stop offset="0" stop-color="#FFF3DE"/>
      <stop offset=".5" stop-color="#E8C08A"/>
      <stop offset="1" stop-color="#C99A5F"/>
    </linearGradient>
    <linearGradient id="spec%(s)s" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity=".6"/>
      <stop offset=".6" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <rect x="1.6" y="1.6" width="68.8" height="68.8" rx="17"
        fill="url(#tile%(s)s)" stroke="#E2F4F7" stroke-opacity=".2" stroke-width="1.4"/>
  <path d="M19 2.6h34a16.4 16.4 0 0 1 16.4 16.4" fill="none"
        stroke="url(#spec%(s)s)" stroke-width="1.7" stroke-linecap="round"/>
  <g stroke="#E8C08A" fill="none" opacity=".14">
    <circle cx="36" cy="36" r="26.5"/><circle cx="36" cy="36" r="20.5"/>
  </g>
  <path d="M22 49.5V21.5l28 28v-28" fill="none" stroke="url(#mono%(s)s)"
        stroke-width="5.6" stroke-linecap="square" stroke-linejoin="miter"/>
  <path d="M22 58.5h28" stroke="#D9743C" stroke-width="2.4" stroke-linecap="round"/>
</svg>''' % {"s": sfx}


NAV = [
    ("products/",      "Products"),
    ("manufacturing.html", "Manufacturing"),
    ("quality.html",   "Quality"),
    ("industries.html","Industries"),
    ("about.html",     "About"),
]

def head(title, desc, pre, canon, extra=""):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{ORIGIN}/{canon}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{ORIGIN}/{canon}">
<meta name="theme-color" content="#050F15">
<script>document.documentElement.className+=" js";</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Instrument+Serif:ital@0;1&family=Schibsted+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{pre}assets/css/site.css">
<link rel="icon" href="{pre}assets/img/favicon.svg" type="image/svg+xml">
{extra}</head>'''

def header(active, pre, on_dark=True):
    CUR = ' aria-current="page"'
    items = "".join(
        f'<a href="{pre}{h}"{CUR if h == active else ""}>{t}</a>'
        for h, t in NAV)
    mitems = "".join(f'<a class="mn-link" href="{pre}{h}">{t}</a>' for h, t in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="hdr{' on-dark' if on_dark else ''}">
  <div class="wrap hdr-in">
    <a class="brand" href="{pre}index.html" aria-label="{SITE} — home">
      {LOGO('h')}
      <span class="brand-txt"><b>New Super Polymers</b><span>PVC film &amp; tubing</span></span>
    </a>
    <nav class="nav" aria-label="Primary">{items}</nav>
    <a class="btn hdr-cta" href="{pre}contact.html">Request a quote
      <svg class="arw" width="13" height="9" viewBox="0 0 13 9" fill="none" aria-hidden="true">
        <path d="M0 4.5h11M7.5 1l3.5 3.5L7.5 8" stroke="currentColor" stroke-width="1.4"/></svg></a>
    <button class="burger" aria-label="Menu" aria-expanded="false" aria-controls="mnav"><span></span></button>
  </div>
</header>
<div class="mobile-nav" id="mnav">
  <nav aria-label="Mobile">{mitems}<a class="mn-link" href="{pre}contact.html">Contact</a></nav>
  <div style="padding-top:2rem">
    <p class="mono" style="color:var(--fg-inv-3);margin-bottom:.75rem">Enquiries</p>
    <p><a href="mailto:{MAILSA}" style="color:var(--fg-inv)">{MAILSA}</a></p>
    <p><a href="tel:{TEL1R}" style="color:var(--fg-inv)">{TEL1}</a></p>
  </div>
</div>'''

def footer(pre):
    plinks = "".join(f'<li><a href="{pre}products/{p["slug"]}.html">{p["short"]}</a></li>' for p in PRODUCTS[:5])
    return f'''<footer class="ftr">
  <div class="wrap">
    <div class="ftr-grid">
      <div>
        <a class="brand" href="{pre}index.html" style="color:var(--fg-inv)">{LOGO('f')}
          <span class="brand-txt"><b>New Super Polymers</b><span>India Pvt Ltd</span></span></a>
        <p class="small" style="color:var(--fg-inv-2);margin-top:1.5rem;max-width:34ch">
          Manufacturer of PVC lay flat tubing and sheet roll. Established 2007.
          ISO&nbsp;9001:2015 certified.</p>
        <a class="badge" style="margin-top:1.5rem" href="{pre}quality.html"><span class="dot"></span>ISO 9001:2015</a>
      </div>
      <div><h5>Products</h5><ul>{plinks}
        <li><a href="{pre}products/">All products</a></li></ul></div>
      <div><h5>Company</h5><ul>
        <li><a href="{pre}manufacturing.html">Manufacturing</a></li>
        <li><a href="{pre}quality.html">Quality</a></li>
        <li><a href="{pre}industries.html">Industries</a></li>
        <li><a href="{pre}about.html">About us</a></li>
        <li><a href="{pre}contact.html">Contact</a></li></ul></div>
      <div><h5>Get in touch</h5>
        <address>
          <a href="tel:{TEL1R}">{TEL1}</a><br>
          <a href="tel:{TEL2R}">{TEL2}</a><br>
          <a href="{WA}" rel="noopener">WhatsApp</a><br><br>
          <a href="mailto:{MAILSA}">{MAILSA}</a><br>
          <a href="mailto:{MAILMD}">{MAILMD}</a><br><br>
          {ADDR}
        </address></div>
    </div>
    <div class="ftr-mark" aria-hidden="true">New Super Polymers</div>
    <div class="ftr-bot">
      <span>&copy; <span data-year></span> {SITE}</span>
      <span>Vasai East · Palghar · Maharashtra · India</span>
      <span>CIN U74999MH2019PTC · ISO 9001:2015</span>
    </div>
  </div>
</footer>
<script src="{pre}assets/js/site.js" defer></script>
</body>
</html>'''

ARW = ('<svg class="arw" width="13" height="9" viewBox="0 0 13 9" fill="none" aria-hidden="true">'
       '<path d="M0 4.5h11M7.5 1l3.5 3.5L7.5 8" stroke="currentColor" stroke-width="1.4"/></svg>')

def page(fname, title, desc, body, active="", pre="", schema=""):
    extra = f'<script type="application/ld+json">{schema}</script>\n' if schema else ""
    doc = (head(title, desc, pre, fname, extra) + '\n<body>\n'
           + header(active, pre) + '\n<main id="main">\n' + body + '\n</main>\n'
           + footer(pre))
    d = os.path.dirname(fname)
    if d: os.makedirs(d, exist_ok=True)
    open(fname, "w", encoding="utf-8").write(doc)
    return fname

# ---------------------------------------------------------------- fragments
def eyebrow(idx, text):
    return f'<p class="eyebrow"><span class="idx">{idx}</span><span>{text}</span></p>'

def swatch_grid(names=None):
    pick = COLOURS if names is None else [c for c in COLOURS if c[0] in names]
    out = []
    for n, hexc, kind in pick:
        out.append(f'''<div class="sw" style="color:{hexc}"><div class="sw-chip" style="background:{hexc}"></div>
          <span class="sw-name">{n}</span></div>''')
    return f'<div class="swatches">{"".join(out)}</div>'

def product_card(p, pre=""):
    return f'''<article class="card rv" data-tags="{p['tags']}">
  <div class="card-media"><img src="{pre}assets/img/{p['img']}" alt="{p['short']} — technical illustration" loading="lazy" width="800" height="600"></div>
  <div class="card-body">
    <span class="card-tag">{p['tag']}</span>
    <h3 class="h4"><a class="stretch" href="{pre}products/{p['slug']}.html">{p['name']}</a></h3>
    <p class="small muted">{p['blurb']}</p>
    <div class="card-foot"><span class="mono">View specification</span>{ARW}</div>
  </div>
</article>'''

def cta_band(pre=""):
    return f'''<section class="sec dark">
  <div class="wrap">
    <div class="split">
      <div class="rv">
        {eyebrow("→", "Next step")}
        <h2 class="h2">Tell us what<br>you need to pack.</h2>
      </div>
      <div class="rv rv-d1">
        <p class="lead" style="max-width:52ch">Tell us what you are wrapping, how you seal it and what
        it has to survive. We will come back with a gauge, a width and a colour — and a price against
        your volume.</p>
        <div class="btn-row" style="margin-top:2.25rem">
          <a class="btn" href="{pre}contact.html">Request a quote {ARW}</a>
          <a class="btn btn-ghost" href="{WA}" rel="noopener">WhatsApp us</a>
        </div>
        <p class="mono" style="margin-top:1.75rem;color:var(--fg-inv-3)">
          Typical reply within one working day · {TEL1}</p>
      </div>
    </div>
  </div>
</section>'''

# ================================================================= line schematic
SCHEMATIC = '''
<figure class="schematic rv">
<div class="sch-scroll">
<svg viewBox="0 0 1240 470" role="img" aria-labelledby="schTitle schDesc" class="sch">
<title id="schTitle">The New Super Polymers PVC blown-film line</title>
<desc id="schDesc">Compounding feeds a single-screw extruder. The melt turns vertical at an annular
die, is inflated into a bubble and cooled by an air ring, collapsed by a converging frame, flattened
at the nip rolls into lay-flat tubing, scanned for gauge, and wound to length.</desc>
<defs>
  <marker id="sar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
    <path d="M0 0L10 5L0 10z" fill="#DC5A28"/></marker>
  <linearGradient id="smelt" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#DC5A28"/><stop offset="1" stop-color="#F09A6E"/></linearGradient>
  <radialGradient id="sbub" cx="0.5" cy="0.6" r="0.6">
    <stop offset="0" stop-color="#DC5A28" stop-opacity=".22"/>
    <stop offset="1" stop-color="#DC5A28" stop-opacity="0"/></radialGradient>
</defs>

<g class="sch-grid" stroke="#22262E" stroke-width="1">
  <path d="M0 90H1240M0 190H1240M0 290H1240M0 390H1240"/>
</g>

<!-- 01 silos + mixer -->
<g class="sch-part">
  <path d="M44 322h34v26l-10 12H54l-10-12z"/><path d="M88 322h34v26l-10 12H98l-10-12z"/>
  <path d="M132 322h34v26l-10 12h-14l-10-12z"/>
  <path d="M34 380h146l-14 22H48z"/>
  <rect x="66" y="402" width="82" height="44" rx="5"/>
</g>
<path d="M148 424h44" class="sch-flow" marker-end="url(#sar)"/>

<!-- 02 extruder -->
<g class="sch-part">
  <rect x="196" y="398" width="44" height="48" rx="4"/>
  <path d="M266 346h48v26l-10 14h-28l-10-14z"/>
  <rect x="240" y="400" width="230" height="44" rx="9"/>
</g>
<g class="sch-screw">
  <path d="M256 404l10 36M282 404l10 36M306 404l10 36M328 404l9 36M348 404l8 36M366 404l8 36M383 404l7 36M399 404l7 36M414 404l6 36M428 404l6 36M441 404l6 36M453 404l6 36"/>
</g>
<path d="M290 386v10" class="sch-flow"/>

<!-- 03 annular die -->
<path d="M470 422 H 492 V 402" class="sch-melt"/>
<path d="M470 422 H 492 V 402" class="sch-pulse"/>
<g class="sch-part">
  <rect x="500" y="356" width="120" height="46" rx="4"/>
  <path d="M508 356h32l6-22h-38z"/><path d="M612 356h-32l-6-22h38z"/>
</g>
<path d="M534 332v-10" class="sch-flow" marker-end="url(#sar)"/>
<path d="M586 332v-10" class="sch-flow" marker-end="url(#sar)"/>

<!-- 04 bubble + air ring -->
<path d="M544 334 C 538 296, 508 282, 500 236 C 494 200, 500 168, 504 140
         L616 140 C 620 168, 626 200, 620 236 C 612 282, 582 296, 576 334 Z"
      fill="url(#sbub)"/>
<path d="M544 334 C 538 296, 508 282, 500 236 C 494 200, 500 168, 504 140" class="sch-film"/>
<path d="M576 334 C 582 296, 612 282, 620 236 C 626 200, 620 168, 616 140" class="sch-film"/>
<g class="sch-part">
  <path d="M452 320h56l8 18h-64z"/><path d="M668 320h-56l-8 18h64z"/>
</g>
<path d="M414 330h30" class="sch-air" marker-end="url(#sar)"/>
<path d="M706 330h-30" class="sch-air" marker-end="url(#sar)"/>
<path d="M478 262h164" class="sch-frost"/>

<!-- 05 collapsing frame -->
<path d="M504 140 L546 78" class="sch-rail"/><path d="M616 140 L574 78" class="sch-rail"/>
<g class="sch-roller">
  <circle cx="512" cy="130" r="5"/><circle cx="526" cy="110" r="5"/><circle cx="540" cy="88" r="5"/>
  <circle cx="608" cy="130" r="5"/><circle cx="594" cy="110" r="5"/><circle cx="580" cy="88" r="5"/>
</g>
<path d="M504 140 L546 78" class="sch-film"/><path d="M616 140 L574 78" class="sch-film"/>

<!-- 06 nip rolls -->
<g class="sch-part"><circle cx="546" cy="58" r="20"/><circle cx="574" cy="58" r="20"/></g>

<!-- flat film run right -->
<path d="M566 42 H 900 C 946 42, 960 70, 966 116" class="sch-film"/>
<path d="M566 42 H 900 C 946 42, 960 70, 966 116" class="sch-run"/>
<path d="M700 42h20" class="sch-flow" marker-end="url(#sar)"/>

<!-- 07 thickness scan -->
<g class="sch-part"><rect x="786" y="62" width="96" height="30" rx="4"/></g>
<path d="M834 62v-14" class="sch-dash"/>

<!-- 08 winder -->
<g class="sch-part"><circle cx="1040" cy="252" r="96"/></g>
<g class="sch-wind">
  <circle cx="1040" cy="252" r="26"/><circle cx="1040" cy="252" r="42"/>
  <circle cx="1040" cy="252" r="58"/><circle cx="1040" cy="252" r="74"/>
</g>
<circle cx="1040" cy="252" r="13" class="sch-core"/>
<path d="M966 116 C 976 150, 1000 168, 1016 178" class="sch-film"/>
<path d="M1040 348v42M998 390h84" class="sch-part-s"/>

<g class="sch-labels">
  <g data-node="s1"><path class="sch-lead" d="M107 296V396"/><circle cx="107" cy="288" r="6"/><text x="107" y="272">01 COMPOUND</text></g>
  <g data-node="s2"><path class="sch-lead" d="M355 296V394"/><circle cx="355" cy="288" r="6"/><text x="355" y="272">02 EXTRUDE</text></g>
  <g data-node="s3"><path class="sch-lead" d="M560 408V404"/><circle cx="560" cy="416" r="6"/><text x="560" y="440">03 DIE</text></g>
  <g data-node="s4"><path class="sch-lead" d="M728 236H630"/><circle cx="736" cy="236" r="6"/><text x="736" y="220">04 BUBBLE</text></g>
  <g data-node="s5"><path class="sch-lead" d="M448 110H518"/><circle cx="440" cy="110" r="6"/><text x="440" y="94">05 COLLAPSE</text></g>
  <g data-node="s6"><path class="sch-lead" d="M560 26V36"/><circle cx="560" cy="18" r="6"/><text x="560" y="8">06 NIP</text></g>
  <g data-node="s7"><path class="sch-lead" d="M834 118V94"/><circle cx="834" cy="126" r="6"/><text x="834" y="146">07 SCAN</text></g>
  <g data-node="s8"><path class="sch-lead" d="M1040 416V354"/><circle cx="1040" cy="424" r="6"/><text x="1040" y="446">08 WIND</text></g>
</g>
</svg>
</div>
<figcaption class="mono">One continuous line — dry blend in at 01, finished roll out at 08.</figcaption>
</figure>'''

STAGES = [
 ("s1", "Compounding", "mch-01-compounding.svg",
  "PVC resin, plasticiser, stabiliser and pigment are weighed to a batch recipe and blended hot, then "
  "cooled, until the mix is genuinely homogenous.",
  "Everything downstream inherits this step. A blend that varies by half a percent shows up 400 metres "
  "later as a gauge band or a colour drift, and no amount of control at the die will pull it back. "
  "Recipes are held against a batch record and pigment is matched to a retained reference chip."),
 ("s2", "Extrusion", "mch-02-extruder.svg",
  "A single screw carries the blend down a heated barrel through feed, compression and metering zones, "
  "turning it into a uniform melt.",
  "PVC is heat-sensitive — run it too hot or hold it too long and it degrades. The barrel is zoned and "
  "PID-controlled so melt temperature is held tight, and screw speed is matched to output rather than "
  "pushed for its own sake. Steady melt is what makes the bubble stand still."),
 ("s3", "The annular die", "mch-03-die.svg",
  "The melt turns through ninety degrees and is split around a spiral mandrel, rejoining as a single "
  "seamless tube that exits upward through a ring-shaped gap.",
  "This is where the tube becomes a tube. The spiral mandrel exists to erase the weld lines left by "
  "splitting the flow — done properly there is no seam anywhere in the finished product, which is "
  "exactly why lay flat tubing outperforms a side-welded bag under load."),
 ("s4", "Air ring and bubble", "mch-04-airring.svg",
  "Internal air inflates the soft tube into a bubble while an air ring cools it from outside. Where it "
  "stops expanding — the frost line — the film has set.",
  "Blow-up ratio decides the finished lay-flat width, and the height of the frost line decides how the "
  "film's strength is distributed between machine and cross direction. These two settings are the "
  "difference between film that tears and film that stretches. They are logged per product, not "
  "rediscovered every run."),
 ("s5", "Collapsing frame", "mch-05-collapsing.svg",
  "Converging rails carry the round bubble gradually inward until it is nearly flat, on rollers rather "
  "than dragging over a surface.",
  "The whole art here is patience. Collapse too sharply and you crease the folded edges permanently — "
  "a defect the customer finds when the pack splits along the fold. Length, angle and roller spacing "
  "are set so the film arrives at the nip already almost flat."),
 ("s6", "Nip rolls", "mch-06-nip.svg",
  "Two driven rolls close on the tube, expel the last of the air and lock the width. This is the step "
  "the product is named for.",
  "What leaves the nip is lay flat tubing: two walls, two folded edges, no seam, and a width that will "
  "not wander. Nip pressure and line speed also set the tension the whole line runs at, so this pair of "
  "rolls quietly governs everything behind it."),
 ("s7", "Gauge scan", "mch-07-winder.svg",
  "The web passes a thickness scan on its way to the winder, so a drift is caught while it is still "
  "correctable rather than after the roll is finished.",
  "Uniformity across the web matters more than the average. A roll that averages 100 micron but swings "
  "between 80 and 120 will seal inconsistently on your line, and you will feel it as rejects rather "
  "than read it as a number."),
 ("s8", "Winding and despatch", "mch-08-qc.svg",
  "Film is wound to length under controlled tension, sampled, documented, poly-wrapped and palletised "
  "against the order.",
  "Tension control is why a roll arrives round and unwinds cleanly instead of telescoping in transit. "
  "Every roll is sampled before it ships, samples are retained against the batch, and the paperwork "
  "goes out with the goods rather than after them."),
]

# ================================================================= HOME
def build_home():
    cards = "".join(product_card(p) for p in PRODUCTS[:4])
    why = [
      ("Seamless, not welded",
       "The tube is formed at the die, so there is no side seam to split. Under load that is the "
       "difference between a pack that holds and a pack that opens."),
      ("Colour compounded in",
       "Pigment goes into the blend, not onto the surface. It cannot scuff off in a container, and "
       "every batch is matched against a retained reference chip."),
      ("One gauge band, 50 to 400 micron",
       "Light retail over-wrap and heavy industrial liner come off the same line, to the same "
       "tolerance, from the same people who know your job."),
      ("Certified since before it was expected",
       "ISO 9001:2015. Batch records, retained samples and a documented change process — because "
       "buyers who audit their suppliers ask for all three."),
    ]
    whyhtml = "".join(
      f'<div class="fcard rv rv-d{i}"><span class="n">0{i+1}</span>'
      f'<h3 class="h4" style="margin-bottom:.75rem">{t}</h3>'
      f'<p class="small muted" style="max-width:38ch">{d}</p></div>'
      for i, (t, d) in enumerate(why))
    inds = "".join(
      f'<a class="fcard rv rv-d{i%4}" href="industries.html" style="display:block">'
      f'<span class="n">{i+1:02d}</span><h3 class="h3">{t}</h3></a>'
      for i, (t, _, _) in enumerate(INDUSTRIES))

    body = f'''
<section class="hero dark">
  <div class="hero-grid"></div><div class="hero-glow"></div><div class="hero-pane"></div>
  <div class="wrap hero-in">
    <div class="badge rv" style="margin-bottom:2.25rem"><span class="dot"></span>ISO 9001:2015 · Manufacturing since 2007</div>
    <h1 class="mega grade hero-lines" style="max-width:13ch"><span class="hl"><i>One tube.</i></span><span class="hl"><i>No joint.</i></span><span class="hl"><i>Made in India.</i></span></h1>
    <div class="split" style="margin-top:clamp(2.5rem,5vw,4rem);align-items:end">
      <p class="lead rv rv-d2" style="max-width:46ch">
        We make PVC lay flat tubing and sheet roll — ten colours, three finishes,
        50 to 400 micron. Supplied to packers, converters and manufacturers across India
        since 2007.</p>
      <div class="rv rv-d3 btn-row">
        <a class="btn" href="products/">See the range {ARW}</a>
        <a class="btn btn-ghost" href="manufacturing.html">Inside the line</a>
      </div>
    </div>
    <div class="stats rv rv-d4" style="margin-top:clamp(3.5rem,7vw,6rem)">
      <div class="stat"><b><span data-count="2007" data-plain>2007</span></b><span>Established</span></div>
      <div class="stat"><b><span data-count="10">10</span></b><span>Stock colours</span></div>
      <div class="stat"><b>50&ndash;400</b><span>Micron gauge range</span></div>
      <div class="stat"><b>ISO 9001</b><span>: 2015 certified</span></div>
    </div>
  </div>
</section>

<div class="dark">
  <div class="tape">
    <div class="tape-track">
      <span>PVC lay flat tubing</span><span>Sheet roll</span>
      <span>Transparent · radium · opaque</span><span>Seamless extrusion</span>
      <span>Ten stock colours</span><span>Custom colour matching</span>
      <span>Printed to order</span><span>Gusseted to order</span>
      <span>PVC lay flat tubing</span><span>Sheet roll</span>
      <span>Transparent · radium · opaque</span><span>Seamless extrusion</span>
      <span>Ten stock colours</span><span>Custom colour matching</span>
      <span>Printed to order</span><span>Gusseted to order</span>
    </div>
  </div>
</div>

<section class="sec">
  <div class="wrap split">
    <div class="rv">
      {eyebrow("01", "What we do")}
      <h2 class="h2">Made as one piece.</h2>
    </div>
    <div class="rv rv-d1 prose">
      <p class="lead">Lay flat tubing starts life as a bubble. Molten PVC leaves a ring-shaped die,
      air inflates it, cooled air sets it, and a pair of rolls presses it flat. What comes off the
      winder is a continuous tube with two folded edges and no join anywhere along it.</p>
      <p class="muted">That single fact is why it outlasts a side-welded bag. There is no weld to
      fail, no adhesive to age and no line of weakness running the length of the pack. You cut it to
      the length you need, seal one or both ends, and the only join in the finished article is the
      one you made yourself.</p>
      <p class="muted">We have been running that line in Vasai since 2007 — first as Super Polymers,
      incorporated as New Super Polymers India Pvt Ltd in 2019, ISO 9001:2015 certified throughout.</p>
      <p style="margin-top:2rem"><a class="link-arw" href="about.html">Our story {ARW}</a></p>
    </div>
  </div>
</section>

<section class="sec-sm paper-2">
  <div class="wrap">
    <div style="display:flex;flex-wrap:wrap;gap:1.5rem;justify-content:space-between;align-items:end;margin-bottom:clamp(2.5rem,4vw,3.5rem)">
      <div class="rv">{eyebrow("02", "The range")}<h2 class="h2">Four grades,<br>one specification.</h2></div>
      <a class="link-arw rv rv-d1" href="products/">All products {ARW}</a>
    </div>
    <div class="grid g-4">{cards}</div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="split" style="margin-bottom:clamp(2.5rem,4vw,3.5rem)">
      <div class="rv">{eyebrow("03", "Colour library")}<h2 class="h2">Ten stock colours.<br>Three finishes.</h2></div>
      <p class="lead rv rv-d1" style="max-width:48ch">Transparent to read the product through, radium
      to make sure it is never missed, opaque to make sure it is never seen. Colour is compounded into
      the film, matched to a retained reference and repeatable batch to batch. Custom shades are
      matched to a chip you send us.</p>
    </div>
    <div class="rv rv-d2">{swatch_grid()}</div>
    <p class="mono muted rv" style="margin-top:2rem">Screen renderings — physical samples on request.</p>
  </div>
</section>

<section class="sec dark">
  <div class="wrap">
    <div class="split" style="margin-bottom:clamp(2.5rem,5vw,4rem)">
      <div class="rv">{eyebrow("04", "Manufacturing")}<h2 class="h2">Eight stages,<br>one continuous line.</h2></div>
      <p class="lead rv rv-d1" style="max-width:50ch">Dry blend goes in at one end. A finished,
      documented roll comes off the other. Nothing is bought in half-made and nothing is
      subcontracted — which is why we can change a gauge, a width or a colour without renegotiating
      it with somebody else first.</p>
    </div>
    {SCHEMATIC}
    <p class="rv" style="margin-top:2.5rem"><a class="link-arw" href="manufacturing.html">Walk the line, stage by stage {ARW}</a></p>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="rv" style="margin-bottom:clamp(2.5rem,4vw,3.5rem)">
      {eyebrow("05", "Why buyers stay")}
      <h2 class="h2" style="max-width:18ch">Quality and capacity — in that order.</h2>
    </div>
    <div class="grid g-4">{whyhtml}</div>
  </div>
</section>

<section class="sec-sm paper-2">
  <div class="wrap">
    <div class="rv" style="margin-bottom:clamp(2rem,4vw,3rem)">
      {eyebrow("06", "Industries")}<h2 class="h2">Who buys this film.</h2>
    </div>
    <div class="grid g-4">{inds}</div>
  </div>
</section>

<section class="sec dark-2">
  <div class="wrap split">
    <div class="rv">
      {eyebrow("07", "Director's desk")}
      <div style="border:1px solid var(--ink-line);border-radius:3px;padding:2rem">
        <p class="h4" style="margin-bottom:.4rem">Khudbuddin Plasticwala</p>
        <p class="mono" style="color:var(--fg-inv-3)">Director</p>
        <hr class="rule" style="margin:1.5rem 0">
        <p class="small" style="color:var(--fg-inv-2)">
          <a href="mailto:{MAILMD}">{MAILMD}</a><br>
          <a href="tel:{TEL1R}">{TEL1}</a></p>
      </div>
    </div>
    <div class="rv rv-d1">
      <blockquote class="quote">&ldquo;We started with one line and one promise: the roll arrives when
      we said it would, and it is the same roll we sent last time. Everything else we have built —
      the colours, the certification, the capacity — sits on top of those two things.&rdquo;</blockquote>
      <p class="mono" style="margin-top:2rem;color:var(--fg-inv-3)">
        Established 2007 · Incorporated 2019 · Vasai East, Maharashtra</p>
      <p style="margin-top:2rem"><a class="link-arw" href="about.html">About the company {ARW}</a></p>
    </div>
  </div>
</section>

{cta_band()}'''
    schema = ('{"@context":"https://schema.org","@type":"Organization",'
              '"name":"New Super Polymers India Pvt Ltd","url":"' + ORIGIN + '",'
              '"foundingDate":"2007","email":"' + MAILSA + '","telephone":"' + TEL1 + '",'
              '"address":{"@type":"PostalAddress","streetAddress":"Tirupati Industrial Park, Sativali Road, Vasai East",'
              '"addressLocality":"Palghar","addressRegion":"Maharashtra","postalCode":"401208","addressCountry":"IN"}}')
    return page("index.html",
        "New Super Polymers — PVC Lay Flat Tubing & Sheet Roll Manufacturer",
        "ISO 9001:2015 certified manufacturer of seamless PVC lay flat tubing and sheet roll. "
        "Ten stock colours, transparent, radium and opaque finishes, 50 to 400 micron.",
        body, active="", pre="", schema=schema)

# ================================================================= PRODUCTS INDEX
def build_products_index():
    cards = "".join(product_card(p, pre="../") for p in PRODUCTS)
    chips = [("all","All products"),("tubing","Lay flat tubing"),("sheet","Sheet roll"),
             ("transparent","Transparent"),("radium","Radium"),("opaque","Opaque"),
             ("coloured","Coloured"),("made-to-order","Made to order")]
    chiphtml = "".join(
        f'<button class="chip" data-filter="{k}" aria-pressed="{"true" if k=="all" else "false"}">{v}</button>'
        for k, v in chips)
    body = f'''
<section class="hero dark" style="padding-block:clamp(8rem,14vh,11rem) clamp(3rem,6vh,5rem)">
  <div class="hero-grid"></div><div class="hero-glow"></div>
  <div class="wrap hero-in">
    {eyebrow("01", "Products")}
    <h1 class="h1 rv" style="max-width:16ch">Everything we make,<br>with the numbers.</h1>
    <p class="lead rv rv-d1" style="max-width:56ch;margin-top:2rem">
      Two families — seamless lay flat tubing and flat sheet roll — across three finishes and ten
      stock colours. Printed and gusseted variants are made to order. Every grade shares the same
      compound, the same line and the same tolerance.</p>
  </div>
</section>

<section class="sec-sm">
  <div class="wrap">
    <div class="filters rv" data-filters style="margin-bottom:clamp(2rem,4vw,3rem)">
      <span class="mono muted" style="margin-right:.75rem">Filter</span>{chiphtml}
    </div>
    <div class="grid g-3">{cards}</div>
    <p class="lead" data-empty hidden style="padding-block:3rem">Nothing in that combination — try another filter.</p>
  </div>
</section>

<section class="sec-sm paper-2">
  <div class="wrap split">
    <div class="rv">{eyebrow("02", "Colour")}<h2 class="h2">The stock library.</h2></div>
    <div class="rv rv-d1">
      <p class="lead" style="margin-bottom:2.5rem;max-width:48ch">Available across the grades below.
      Anything outside this set is matched to a physical chip you send us and held as a reference for
      repeat orders.</p>
      {swatch_grid()}
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="rv" style="margin-bottom:clamp(2rem,4vw,3rem)">
      {eyebrow("03", "Common specification")}
      <h2 class="h2">Shared across every grade.</h2>
    </div>
    <div class="split">
      <div class="rv"><table class="spec">{spec_rows(BASE_SPEC[:7])}</table></div>
      <div class="rv rv-d1"><table class="spec">{spec_rows(BASE_SPEC[7:])}</table></div>
    </div>
  </div>
</section>

{cta_band(pre="../")}'''
    return page("products/index.html",
        "Products — PVC Lay Flat Tubing & Sheet Roll | New Super Polymers",
        "Seamless PVC lay flat tubing in transparent, radium and opaque finishes, plus PVC sheet roll. "
        "Ten stock colours, 50 to 400 micron, printed and gusseted to order.",
        body, active="products/", pre="../")

# ================================================================= PRODUCT DETAIL
def build_product(p):
    pre = "../"
    others = [q for q in PRODUCTS if q["slug"] != p["slug"]][:3]
    rel = "".join(product_card(q, pre=pre) for q in others)
    apps = "".join(f"<li>{a}</li>" for a in p["apps"])
    cols = swatch_grid(p["colours"])
    spec = list(BASE_SPEC)
    if p["slug"] == "pvc-sheet-roll":
        spec = [("Material", "Flexible PVC (polyvinyl chloride)", True),
                ("Form", "Single-wall flat film, wound on roll", True)] + spec[2:]
        spec = [(k, v.replace("Tubing roll", "Sheet roll"), o) for k, v, o in spec]
        spec = [(("Sheet width" if k == "Lay-flat width" else k), v, o) for k, v, o in spec]
    finishes = ", ".join(sorted({c[2] for c in COLOURS if c[0] in p["colours"]}))
    body = f'''
<section class="hero dark" style="padding-block:clamp(8rem,14vh,11rem) clamp(3rem,6vh,5rem)">
  <div class="hero-grid"></div><div class="hero-glow"></div>
  <div class="wrap hero-in">
    <nav class="mono" aria-label="Breadcrumb" style="margin-bottom:2rem;color:var(--fg-inv-3)">
      <a href="{pre}index.html">Home</a> / <a href="{pre}products/">Products</a> / <span style="color:var(--fg-inv)">{p['short']}</span>
    </nav>
    <div class="split" style="align-items:end">
      <div>
        <p class="mono rv" style="color:var(--molten);margin-bottom:1.25rem">{p['tag']}</p>
        <h1 class="h1 rv rv-d1">{p['name']}</h1>
      </div>
      <p class="lead rv rv-d2" style="max-width:48ch">{p['blurb']}</p>
    </div>
  </div>
</section>

<section class="sec-sm">
  <div class="wrap split">
    <div class="rv">
      <img src="{pre}assets/img/{p['img']}" alt="{p['short']} — technical illustration"
           width="800" height="600" style="border:1px solid var(--line);border-radius:3px;background:#fff">
      <p class="mono muted" style="margin-top:1rem">Technical illustration · physical samples on request</p>
    </div>
    <div class="rv rv-d1 prose">
      {eyebrow("01", "Overview")}
      <p class="lead">{p['intro']}</p>
      <div class="notice" style="margin-top:2rem">
        <p class="mono" style="color:var(--molten);margin-bottom:.6rem">From the floor</p>
        <p class="small">{p['note']}</p>
      </div>
      <div class="btn-row" style="margin-top:2.25rem">
        <a class="btn" href="{pre}contact.html?product={p['slug']}">Request a quote {ARW}</a>
        <a class="btn btn-ghost" href="{WA}" rel="noopener">Ask on WhatsApp</a>
      </div>
    </div>
  </div>
</section>

<section class="sec-sm paper-2">
  <div class="wrap">
    <div class="split">
      <div class="rv">
        {eyebrow("02", "Specification")}
        <h2 class="h3" style="margin-bottom:2rem">Technical data</h2>
        <table class="spec">{spec_rows(spec)}</table>
        <p class="mono muted" style="margin-top:1.25rem">Finishes: {finishes}</p>
      </div>
      <div class="rv rv-d1">
        {eyebrow("03", "Applications")}
        <h2 class="h3" style="margin-bottom:2rem">Where it is used</h2>
        <ul class="chk">{apps}</ul>
        <hr class="rule" style="margin:2.5rem 0">
        {eyebrow("04", "Colours")}
        {cols}
      </div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="rv" style="margin-bottom:clamp(2rem,4vw,3rem)">
      {eyebrow("05", "Also from the line")}<h2 class="h2">Related grades</h2>
    </div>
    <div class="grid g-3">{rel}</div>
  </div>
</section>

{cta_band(pre=pre)}'''
    schema = ('{"@context":"https://schema.org","@type":"Product","name":"' + p["short"] +
              '","brand":{"@type":"Brand","name":"New Super Polymers"},'
              '"material":"Polyvinyl chloride",'
              '"description":"' + p["blurb"].replace('"', "'") + '",'
              '"manufacturer":{"@type":"Organization","name":"' + SITE + '"}}')
    return page(f"products/{p['slug']}.html",
        f"{p['short']} | New Super Polymers",
        p["blurb"] + " ISO 9001:2015 certified PVC film manufacturer, 50 to 400 micron.",
        body, active="products/", pre=pre, schema=schema)

# ================================================================= MANUFACTURING
def build_manufacturing():
    st = []
    for i, (nid, name, img, sub, detail) in enumerate(STAGES):
        st.append(f'''<div class="stage rv" data-stage="{nid}">
  <div class="stage-n">{i+1:02d}</div>
  <div>
    <h3 class="h3" style="margin-bottom:1rem">{name}</h3>
    <p class="lead" style="margin-bottom:1.25rem">{sub}</p>
    <p class="small" style="color:var(--fg-inv-2);max-width:52ch">{detail}</p>
  </div>
  <figure class="stage-fig" style="margin:0">
    <img src="assets/img/{img}" alt="{name} — technical diagram" loading="lazy" width="640" height="400">
  </figure>
</div>''')
    stages = "".join(st)
    facts = [("Established", "2007", "Sole proprietorship, incorporated 2019"),
             ("Plant", "Vasai East", "Tirupati Industrial Park, Palghar"),
             ("Team", "51&ndash;100", "Production, QC and despatch"),
             ("System", "ISO 9001:2015", "Certified quality management")]
    facthtml = "".join(
        f'<div class="fcard rv rv-d{i}"><span class="n">{i+1:02d}</span>'
        f'<p class="mono muted" style="margin-bottom:.6rem">{a}</p>'
        f'<p class="h3" style="margin-bottom:.5rem">{b}</p>'
        f'<p class="small muted">{c}</p></div>' for i, (a, b, c) in enumerate(facts))
    body = f'''
<section class="hero dark" style="padding-block:clamp(8rem,14vh,11rem) clamp(3rem,6vh,5rem)">
  <div class="hero-grid"></div><div class="hero-glow"></div>
  <div class="wrap hero-in">
    {eyebrow("01", "Manufacturing")}
    <h1 class="h1 rv" style="max-width:14ch">How a dry blend<br>becomes a roll.</h1>
    <p class="lead rv rv-d1" style="max-width:56ch;margin-top:2rem">
      Blown film extrusion is one of the few industrial processes you can watch from beginning to end
      and understand completely. Here is our line, stage by stage — including the settings that
      actually decide whether the film you receive performs.</p>
  </div>
</section>

<section class="sec-sm dark">
  <div class="wrap">
    {SCHEMATIC}
    <p class="mono muted rv" style="margin-top:1rem">Scroll the stages below — the schematic follows.</p>
  </div>
</section>

<section class="dark" style="padding-bottom:var(--sec)">
  <div class="wrap">{stages}</div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="split" style="margin-bottom:clamp(2.5rem,4vw,3.5rem)">
      <div class="rv">{eyebrow("02", "The plant")}<h2 class="h2">Where it happens.</h2></div>
      <p class="lead rv rv-d1" style="max-width:50ch">Everything above runs under one roof in Vasai
      East, outside Mumbai — compounding, extrusion, quality control and despatch. Nothing is
      subcontracted, which is why a change request lands with the people who will actually make it.</p>
    </div>
    <div class="grid g-4">{facthtml}</div>
    <div class="notice rv" style="margin-top:clamp(2.5rem,4vw,3.5rem)">
      <p class="mono" style="color:var(--molten);margin-bottom:.6rem">Visit us</p>
      <p class="small">Buyers placing volume orders are welcome at the plant. We will walk you down the
      line described on this page, show you the batch records behind your grade, and put physical
      samples in your hand before you commit to a run.
      <a class="link-arw" href="contact.html" style="margin-top:1rem">Arrange a visit {ARW}</a></p>
    </div>
  </div>
</section>

{cta_band()}'''
    return page("manufacturing.html",
        "Manufacturing — PVC Blown Film Extrusion | New Super Polymers",
        "Inside our PVC blown film line: compounding, single-screw extrusion, annular die, air ring "
        "and bubble, collapsing frame, nip rolls, gauge scanning and winding.",
        body, active="manufacturing.html", pre="")

# ================================================================= QUALITY
def build_quality():
    controls = [
      ("Incoming", "Resin, plasticiser, stabiliser and pigment are checked against the batch recipe "
                   "before anything is weighed. A blend is only as good as what goes into it."),
      ("In process", "Melt temperature, frost-line height and blow-up ratio are held to the recorded "
                     "settings for that grade — not reset by feel at the start of every shift."),
      ("On the web", "Gauge is scanned across the width, not just sampled at the edge. Uniformity is "
                     "what governs how the film seals on your line."),
      ("Before despatch", "Every roll is sampled for gauge, width and appearance. Samples are retained "
                          "against the batch so a query six months from now still has an answer."),
    ]
    ch = "".join(f'<div class="fcard rv rv-d{i}"><span class="n">{i+1:02d}</span>'
                 f'<h3 class="h4" style="margin-bottom:.75rem">{a}</h3>'
                 f'<p class="small muted" style="max-width:36ch">{b}</p></div>'
                 for i, (a, b) in enumerate(controls))
    tests = ["Thickness / gauge — digital micrometer, multiple points across the web",
             "Lay-flat width against nominal and tolerance",
             "Tensile strength and elongation at break",
             "Colour match against the retained reference chip",
             "Visual — gels, fish-eyes, edge condition, roll formation",
             "Roll length and net weight verification"]
    docs = ["Technical data sheet (TDS) per grade",
            "Certificate of analysis (COA) per batch, on request",
            "Batch and lot traceability to the compounding record",
            "Retained samples held against every despatch",
            "Declarations to a customer specification, where we can support them"]
    body = f'''
<section class="hero dark" style="padding-block:clamp(8rem,14vh,11rem) clamp(3rem,6vh,5rem)">
  <div class="hero-grid"></div><div class="hero-glow"></div>
  <div class="wrap hero-in">
    {eyebrow("01", "Quality")}
    <h1 class="h1 rv" style="max-width:15ch">The same roll,<br>every time.</h1>
    <p class="lead rv rv-d1" style="max-width:56ch;margin-top:2rem">
      Consistency is not a claim, it is a set of controls you can inspect. Here is what we measure,
      when we measure it, and what we can put in writing alongside your order.</p>
    <div class="badge rv rv-d2" style="margin-top:2.5rem"><span class="dot"></span>ISO 9001:2015 certified</div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="rv" style="margin-bottom:clamp(2.5rem,4vw,3.5rem)">
      {eyebrow("02", "Control points")}<h2 class="h2">Four places we stop and check.</h2>
    </div>
    <div class="grid g-4">{ch}</div>
  </div>
</section>

<section class="sec-sm paper-2">
  <div class="wrap split">
    <div class="rv">
      {eyebrow("03", "What we test")}<h2 class="h3" style="margin-bottom:2rem">In-house testing</h2>
      <ul class="chk">{"".join(f"<li>{t}</li>" for t in tests)}</ul>
    </div>
    <div class="rv rv-d1">
      {eyebrow("04", "What you get")}<h2 class="h3" style="margin-bottom:2rem">Documentation</h2>
      <ul class="chk">{"".join(f"<li>{d}</li>" for d in docs)}</ul>
    </div>
  </div>
</section>

<section class="sec dark">
  <div class="wrap split">
    <div class="rv">{eyebrow("05", "Compliance")}<h2 class="h2">Ask us in writing.</h2></div>
    <div class="rv rv-d1">
      <p class="lead" style="max-width:52ch">Our certified quality system is ISO 9001:2015. Beyond
      that, requirements differ by market and by application — food contact, medical secondary
      packaging, restricted-substance declarations and phthalate-free formulation are all quoted
      against the specific standard you need to meet.</p>
      <div class="notice" style="margin-top:2rem">
        <p class="mono" style="color:var(--molten);margin-bottom:.6rem">How we handle it</p>
        <p class="small">Send us the standard, the market and the application. We will tell you plainly
        what we hold today, what we can formulate to, and what would need third-party testing before
        we could certify it — rather than claiming a compliance we cannot evidence.</p>
      </div>
      <p style="margin-top:2rem"><a class="link-arw" href="contact.html">Send a compliance question {ARW}</a></p>
    </div>
  </div>
</section>

{cta_band()}'''
    return page("quality.html",
        "Quality & Compliance — ISO 9001:2015 | New Super Polymers",
        "ISO 9001:2015 certified PVC film manufacturing. In-process controls, gauge scanning, "
        "retained samples, batch traceability, TDS and COA documentation.",
        body, active="quality.html", pre="")

# ================================================================= INDUSTRIES
def build_industries():
    secs = []
    for i, (name, copy, uses) in enumerate(INDUSTRIES):
        ul = "".join(f"<li>{u}</li>" for u in uses)
        secs.append(f'''<div class="stage rv" style="border-top-color:var(--line);grid-template-columns:4.5rem minmax(0,1fr) minmax(0,.8fr)">
  <div class="stage-n">{i+1:02d}</div>
  <div><h3 class="h3" style="margin-bottom:1rem">{name}</h3>
    <p class="lead" style="max-width:50ch">{copy}</p></div>
  <div><p class="mono muted" style="margin-bottom:1.25rem">Typical uses</p><ul class="chk">{ul}</ul></div>
</div>''')
    body = f'''
<section class="hero dark" style="padding-block:clamp(8rem,14vh,11rem) clamp(3rem,6vh,5rem)">
  <div class="hero-grid"></div><div class="hero-glow"></div>
  <div class="wrap hero-in">
    {eyebrow("01", "Industries")}
    <h1 class="h1 rv" style="max-width:16ch">Seven industries.<br>One film.</h1>
    <p class="lead rv rv-d1" style="max-width:56ch;margin-top:2rem">
      The same tube protects a garment, a seed packet and a gearbox spare — the gauge, the colour and
      the finish are what change. If your sector is not listed, the specification conversation is
      identical: tell us the pack, not the part number.</p>
  </div>
</section>

<section class="sec-sm">
  <div class="wrap" style="padding-top:1rem">{"".join(secs)}</div>
</section>

{cta_band()}'''
    return page("industries.html",
        "Industries Served — PVC Film Applications | New Super Polymers",
        "PVC lay flat tubing and sheet roll for packaging converters, textiles, stationery, food and "
        "FMCG, pharmaceutical, agriculture and industrial hardware.",
        body, active="industries.html", pre="")

# ================================================================= ABOUT
def build_about():
    tl = [("2007", "Super Polymers is founded",
           "A sole proprietorship in Mumbai with one extrusion line and a single product: PVC lay flat "
           "tubing. The customers are local packers who need film that arrives when it was promised."),
          ("2007&ndash;2018", "The range widens",
           "Colours are added, then finishes — transparent, radium, opaque — then sheet roll for "
           "converters who wanted the flat web rather than the tube. Capacity grows with the order book."),
          ("2019", "Incorporated as New Super Polymers India Pvt Ltd",
           "The proprietorship becomes a private limited company. Nothing about the plant changes; the "
           "structure catches up with the size of the business."),
          ("Certified", "ISO 9001:2015",
           "The quality system is certified — batch records, retained samples, a documented change "
           "process — because buyers who audit their suppliers ask for all three."),
          ("Today", "51&ndash;100 people in Vasai East",
           "Compounding, extrusion, quality control and despatch under one roof at Tirupati Industrial "
           "Park, supplying packers, converters and manufacturers across India."),
          ("Next", "Beyond India",
           "We are opening the business to buyers in the United States and the Middle East. The film is "
           "the same. The documentation, the terms and the lead times are built for export.")]
    tlhtml = "".join(f'<li class="rv"><span class="yr">{y}</span>'
                     f'<h3 class="h4" style="margin-bottom:.75rem">{t}</h3>'
                     f'<p class="small muted" style="max-width:52ch">{d}</p></li>' for y, t, d in tl)
    vals = [("Say the real lead time",
             "45 to 60 days is what it takes, so that is what we quote. A date you can plan around beats "
             "a date that sounds better."),
            ("One roll is the whole relationship",
             "Buyers do not judge a supplier on the first order. They judge it on the fourth, when the "
             "colour has to match the one before it."),
            ("Answer the question you were asked",
             "If we cannot certify something, we say so and explain what it would take. That is a shorter "
             "conversation than the one that follows a claim we cannot evidence.")]
    valhtml = "".join(f'<div class="fcard rv rv-d{i}"><span class="n">{i+1:02d}</span>'
                      f'<h3 class="h4" style="margin-bottom:.75rem">{a}</h3>'
                      f'<p class="small muted" style="max-width:36ch">{b}</p></div>'
                      for i, (a, b) in enumerate(vals))
    body = f'''
<section class="hero dark" style="padding-block:clamp(8rem,14vh,11rem) clamp(3rem,6vh,5rem)">
  <div class="hero-grid"></div><div class="hero-glow"></div>
  <div class="wrap hero-in">
    {eyebrow("01", "About us")}
    <h1 class="h1 rv" style="max-width:15ch">Eighteen years<br>of one product.</h1>
    <p class="lead rv rv-d1" style="max-width:56ch;margin-top:2rem">
      New Super Polymers India Pvt Ltd has made PVC lay flat tubing in Vasai since 2007. We have added
      colours, finishes and capacity in that time. We have never added a second business.</p>
  </div>
</section>

<section class="sec">
  <div class="wrap split">
    <div class="rv">{eyebrow("02", "History")}<h2 class="h2">How we got here.</h2></div>
    <ul class="tl">{tlhtml}</ul>
  </div>
</section>

<section class="sec-sm paper-2">
  <div class="wrap split">
    <div class="rv">
      {eyebrow("03", "Director's desk")}
      <div class="card" style="padding:2rem">
        <p class="h3" style="margin-bottom:.4rem">Khudbuddin Plasticwala</p>
        <p class="mono muted">Director</p>
        <hr class="rule" style="margin:1.5rem 0">
        <p class="small"><a href="mailto:{MAILMD}">{MAILMD}</a><br>
        <a href="tel:{TEL1R}">{TEL1}</a></p>
        <p class="mono muted" style="margin-top:1.5rem">
          Photograph to be supplied &mdash; placeholder</p>
      </div>
    </div>
    <div class="rv rv-d1">
      <blockquote class="quote">&ldquo;Punctuality is not a soft quality in this business. A packer whose
      film is late has a line standing still and staff standing next to it. We have built the whole
      company around not being the reason that happens.&rdquo;</blockquote>
      <p class="mono muted" style="margin-top:2rem">Khudbuddin Plasticwala · Director</p>
      <hr class="rule" style="margin:2.5rem 0">
      <p class="lead">Quality and customer satisfaction are what we are known for, and on-time delivery
      is what earned us that. It has always been our intent to give the customer the best of the
      services, and punctuality.</p>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="rv" style="margin-bottom:clamp(2.5rem,4vw,3.5rem)">
      {eyebrow("04", "How we work")}<h2 class="h2">Three things we do not flex on.</h2>
    </div>
    <div class="grid g-3">{valhtml}</div>
  </div>
</section>

<section class="sec-sm dark">
  <div class="wrap">
    <div class="stats">
      <div class="stat"><b><span data-count="2007" data-plain>2007</span></b><span>Established</span></div>
      <div class="stat"><b><span data-count="100">100</span></b><span>People (51&ndash;100)</span></div>
      <div class="stat"><b>ISO 9001</b><span>: 2015 certified</span></div>
      <div class="stat"><b>Vasai East</b><span>Palghar, Maharashtra</span></div>
    </div>
  </div>
</section>

{cta_band()}'''
    return page("about.html",
        "About Us — Manufacturing PVC Film Since 2007 | New Super Polymers",
        "New Super Polymers India Pvt Ltd has manufactured PVC lay flat tubing in Vasai, Maharashtra "
        "since 2007. Incorporated 2019. ISO 9001:2015 certified.",
        body, active="about.html", pre="")

# ================================================================= CONTACT
def build_contact():
    popts = "".join(f'<option value="{p["slug"]}">{p["short"]}</option>' for p in PRODUCTS)
    copts = "".join(f'<option value="{c[0]}">{c[0]}</option>' for c in COLOURS)
    body = f'''
<section class="hero dark" style="padding-block:clamp(8rem,14vh,11rem) clamp(3rem,6vh,5rem)">
  <div class="hero-grid"></div><div class="hero-glow"></div>
  <div class="wrap hero-in">
    {eyebrow("01", "Contact")}
    <h1 class="h1 rv" style="max-width:15ch">Tell us what<br>you are wrapping.</h1>
    <p class="lead rv rv-d1" style="max-width:56ch;margin-top:2rem">
      The more you can tell us about the pack, the faster the quote. If you already know your gauge,
      width and colour, fill those in. If you do not, describe the job and we will work back to them.</p>
  </div>
</section>

<section class="sec-sm">
  <div class="wrap split" style="grid-template-columns:minmax(0,7fr) minmax(0,4fr)">
    <div class="rv">
      {eyebrow("02", "Request for quotation")}
      <!-- Wire `action` to your form endpoint (Formspree, Netlify Forms, or your own handler)
           before launch. Until then site.js intercepts submit and shows a confirmation. -->
      <form data-rfq="919786050000">
        <div class="grid g-2" style="gap:1.25rem">
          <div class="field"><label for="f-name">Your name <span class="req">*</span></label>
            <input id="f-name" name="name" required autocomplete="name"></div>
          <div class="field"><label for="f-co">Company <span class="req">*</span></label>
            <input id="f-co" name="company" required autocomplete="organization"></div>
          <div class="field"><label for="f-email">Email <span class="req">*</span></label>
            <input id="f-email" name="email" type="email" required autocomplete="email"></div>
          <div class="field"><label for="f-phone">Phone / WhatsApp</label>
            <input id="f-phone" name="phone" type="tel" autocomplete="tel"></div>
          <div class="field"><label for="f-country">Country <span class="req">*</span></label>
            <input id="f-country" name="country" required autocomplete="country-name"></div>
          <div class="field"><label for="f-city">Destination city or port</label>
            <input id="f-city" name="destination"></div>
        </div>
        <hr class="rule" style="margin:2rem 0">
        <div class="grid g-2" style="gap:1.25rem">
          <div class="field"><label for="f-prod">Product</label>
            <select id="f-prod" name="product"><option value="">Not sure yet</option>{popts}</select></div>
          <div class="field"><label for="f-colour">Colour</label>
            <select id="f-colour" name="colour"><option value="">Not sure yet</option>{copts}
              <option value="custom">Custom &mdash; I will send a reference</option></select></div>
          <div class="field"><label for="f-gauge">Gauge (micron)</label>
            <input id="f-gauge" name="gauge" inputmode="numeric" placeholder="50 &ndash; 400"></div>
          <div class="field"><label for="f-width">Lay-flat width (mm)</label>
            <input id="f-width" name="width" inputmode="numeric" placeholder="e.g. 250"></div>
          <div class="field"><label for="f-qty">Quantity</label>
            <input id="f-qty" name="quantity" placeholder="kg, rolls or metres"></div>
          <div class="field"><label for="f-terms">Preferred terms</label>
            <select id="f-terms" name="terms"><option value="">No preference</option>
              <option>EXW Vasai</option><option>FOB Nhava Sheva</option>
              <option>CIF destination port</option><option>Domestic delivery (India)</option></select></div>
        </div>
        <div class="field" style="margin-top:1.25rem">
          <label for="f-req">What are you packing? <span class="req">*</span></label>
          <textarea id="f-req" name="requirements" required
            placeholder="Describe the product, how you seal it, and what the pack has to survive."></textarea>
        </div>
        <div class="notice" data-rfq-ok hidden style="margin-top:1.5rem">
          <p class="mono" style="color:var(--molten);margin-bottom:.6rem">Ready to send</p>
          <p class="small">WhatsApp should have opened in a new tab with your enquiry already written
          out. If it did not, <a data-rfq-link href="{WA}" rel="noopener">open it here</a> &mdash;
          or <a data-rfq-mail href="mailto:{MAILSA}">send the same details by email</a>.</p>
        </div>
        <button class="btn" type="submit" style="margin-top:1.75rem">Send on WhatsApp {ARW}</button>
        <p class="mono muted" style="margin-top:1.25rem">
          Opens WhatsApp with your details filled in &middot; typical reply within one working day</p>
      </form>
    </div>

    <aside class="rv rv-d1">
      {eyebrow("03", "Direct")}
      <div class="card" style="padding:1.75rem;margin-bottom:1.25rem">
        <p class="mono muted" style="margin-bottom:.9rem">Sales</p>
        <p><a href="mailto:{MAILSA}">{MAILSA}</a></p>
        <hr class="rule" style="margin:1.25rem 0">
        <p class="mono muted" style="margin-bottom:.9rem">Director</p>
        <p class="h4" style="margin-bottom:.3rem">Khudbuddin Plasticwala</p>
        <p class="small"><a href="mailto:{MAILMD}">{MAILMD}</a></p>
      </div>
      <div class="card" style="padding:1.75rem;margin-bottom:1.25rem">
        <p class="mono muted" style="margin-bottom:.9rem">Phone &amp; WhatsApp</p>
        <p><a href="tel:{TEL1R}">{TEL1}</a></p>
        <p><a href="tel:{TEL2R}">{TEL2}</a></p>
        <a class="btn btn-ghost" href="{WA}" rel="noopener" style="margin-top:1.25rem;width:100%;justify-content:center">
          Open WhatsApp {ARW}</a>
        <p class="mono muted" style="margin-top:1rem">Mon&ndash;Sat · 10:00&ndash;19:00 IST (GMT+5:30)</p>
      </div>
      <div class="card" style="padding:1.75rem">
        <p class="mono muted" style="margin-bottom:.9rem">Plant &amp; office</p>
        <address style="font-style:normal;line-height:1.75;font-size:.9375rem">{ADDR}</address>
        <hr class="rule" style="margin:1.25rem 0">
        <p class="small muted">Buyers placing volume orders are welcome to visit the line.</p>
      </div>
    </aside>
  </div>
</section>

<section class="sec-sm dark">
  <div class="wrap">
    <div class="split">
      <div class="rv">{eyebrow("04", "Export")}<h2 class="h2">Shipping beyond India.</h2></div>
      <div class="rv rv-d1">
        <p class="lead" style="max-width:52ch">We supply the Indian market today and are opening the
        business to buyers in the United States and the Middle East. Quotes are available EXW Vasai,
        FOB Nhava Sheva or CIF to your port.</p>
        <table class="spec" style="margin-top:2rem">
          <tr><th>Lead time</th><td>45 &ndash; 60 days from confirmed order</td></tr>
          <tr><th>Loading port</th><td>Nhava Sheva (JNPT), Mumbai</td></tr>
          <tr><th>Terms quoted</th><td>EXW &middot; FOB &middot; CIF</td></tr>
          <tr><th>Documentation</th><td>Invoice, packing list, TDS; COA on request</td></tr>
          <tr><th>Duties</th><td>Import duty and tariff are the buyer&rsquo;s account unless quoted DDP</td></tr>
        </table>
      </div>
    </div>
  </div>
</section>'''
    return page("contact.html",
        "Contact & Request a Quote | New Super Polymers",
        "Request a quotation for PVC lay flat tubing or sheet roll. Vasai East, Maharashtra. "
        "Phone, WhatsApp and email. Lead time 45 to 60 days.",
        body, active="contact.html", pre="")

# ================================================================= 404 + seo
def build_404():
    body = f'''<section class="hero dark" style="min-height:74vh;display:flex;align-items:center">
  <div class="hero-grid"></div><div class="hero-glow"></div>
  <div class="wrap hero-in">
    {eyebrow("404", "Not found")}
    <h1 class="h1" style="max-width:14ch">Page not found.</h1>
    <p class="lead" style="max-width:44ch;margin-top:1.5rem">The link may be old, or the page may have
    moved. The product range is the best place to start.</p>
    <div class="btn-row" style="margin-top:2.5rem">
      <a class="btn" href="products/">See the range {ARW}</a>
      <a class="btn btn-ghost" href="index.html">Home</a>
    </div>
  </div>
</section>'''
    f = page("404.html", "Page not found | New Super Polymers",
             "The page you were looking for could not be found.", body, pre="")
    t = open(f, encoding="utf-8").read().replace(
        '<meta name="theme-color"', '<meta name="robots" content="noindex">\n<meta name="theme-color"')
    open(f, "w", encoding="utf-8").write(t)
    return f

def build_seo(pages):
    urls = "".join(
        f"  <url><loc>{ORIGIN}/{u}</loc><changefreq>monthly</changefreq>"
        f"<priority>{'1.0' if u=='index.html' else '0.8' if u.startswith('products') else '0.7'}</priority></url>\n"
        for u in pages if u != "404.html")
    open("sitemap.xml", "w").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n")
    open("robots.txt", "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {ORIGIN}/sitemap.xml\n")

# ================================================================= run
if __name__ == "__main__":
    made = [build_home(), build_products_index()]
    made += [build_product(p) for p in PRODUCTS]
    made += [build_manufacturing(), build_quality(), build_industries(),
             build_about(), build_contact(), build_404()]
    build_seo(made)
    print(f"Built {len(made)} pages:")
    for m in made:
        print("  ", m)
