#!/usr/bin/env python3
"""Bundle the multipage site into one self-contained HTML page with a hash router,
for publishing as a shareable hosted page. Does not alter the static site."""
import re, os, base64, json

OUT = "/private/tmp/claude-501/-Users-huzaifalaljiwala-Superpolymer/72683e1e-1bf4-471b-affb-3a687fce544c/scratchpad/nsp-site.html"

ROUTES = [
    ("home",            "index.html"),
    ("products",        "products/index.html"),
    ("p-lay-flat-tubing-transparent", "products/lay-flat-tubing-transparent.html"),
    ("p-lay-flat-tubing-coloured",    "products/lay-flat-tubing-coloured.html"),
    ("p-lay-flat-tubing-radium",      "products/lay-flat-tubing-radium.html"),
    ("p-lay-flat-tubing-opaque",      "products/lay-flat-tubing-opaque.html"),
    ("p-pvc-sheet-roll",              "products/pvc-sheet-roll.html"),
    ("p-printed-lay-flat-tubing",     "products/printed-lay-flat-tubing.html"),
    ("p-gusseted-lay-flat-tubing",    "products/gusseted-lay-flat-tubing.html"),
    ("manufacturing",   "manufacturing.html"),
    ("quality",         "quality.html"),
    ("industries",      "industries.html"),
    ("about",           "about.html"),
    ("contact",         "contact.html"),
]

def read(p): return open(p, encoding="utf-8").read()

def rewrite_links(s):
    """Turn file links into hash routes; strip ../ prefixes."""
    def sub(m):
        attr, url = m.group(1), m.group(2)
        if url.startswith(("http", "mailto:", "tel:", "#", "data:")):
            return m.group(0)
        u = url.split("?")[0].split("#")[0]
        u = re.sub(r"^(\.\./)+", "", u)
        if u in ("", "index.html"):            r = "#home"
        elif u in ("products/", "products/index.html"): r = "#products"
        elif u.startswith("products/"):        r = "#p-" + u[len("products/"):-len(".html")]
        elif u.endswith(".html"):              r = "#" + u[:-len(".html")]
        else:                                  return m.group(0)
        return '%s="%s"' % (attr, r)
    return re.sub(r'(href)="([^"]*)"', sub, s)

def collect_images():
    imgs = {}
    for f in sorted(os.listdir("assets/img")):
        if f.endswith(".svg"):
            b = open(os.path.join("assets/img", f), "rb").read()
            imgs[f] = "data:image/svg+xml;base64," + base64.b64encode(b).decode()
    return imgs

def deref_images(s):
    """Point <img> at a key in the runtime image map instead of a file path."""
    return re.sub(r'src="(?:\.\./)*assets/img/([^"]+)"', r'src="" data-img="\1"', s)

def uniq_ids(s, suffix):
    """Namespace the schematic's SVG ids so it can appear on two routes."""
    for i in ("schTitle", "schDesc", "sar", "smelt", "sbub"):
        s = s.replace('id="%s"' % i, 'id="%s%s"' % (i, suffix))
        s = s.replace('url(#%s)' % i, 'url(#%s%s)' % (i, suffix))
    s = s.replace('aria-labelledby="schTitle schDesc"',
                  'aria-labelledby="schTitle%s schDesc%s"' % (suffix, suffix))
    return s


def ascii_html(s):
    """Numeric-entity-encode non-ASCII so the page cannot mojibake."""
    return "".join(c if ord(c) < 128 else "&#%d;" % ord(c) for c in s)

def ascii_css(s):
    """CSS ignores HTML entities, so use CSS escapes instead."""
    out = []
    for c in s:
        out.append(c if ord(c) < 128 else "\\%04X " % ord(c))
    return "".join(out)

index = read("index.html")
header = re.search(r'<body>\n(.*?)\n<main id="main">', index, re.S).group(1)
footer = re.search(r'(<footer class="ftr">.*?</footer>)', index, re.S).group(1)
css    = ascii_css(read("assets/css/site.css"))
js     = "".join(c if ord(c) < 128 else "\\u%04x" % ord(c) for c in read("assets/js/site.js"))

panels = []
for route, path in ROUTES:
    main = re.search(r'<main id="main">\n(.*?)\n</main>', read(path), re.S).group(1)
    main = deref_images(rewrite_links(main))
    if route == "manufacturing":
        main = uniq_ids(main, "M")
    panels.append('<section class="rt" data-route="%s" hidden>\n%s\n</section>' % (route, ascii_html(main)))

header = ascii_html(rewrite_links(header))
footer = ascii_html(rewrite_links(footer))
imgs   = collect_images()

router = """
/* ---- hash router ---- */
(function () {
  var IMG = __IMGMAP__;
  document.querySelectorAll('img[data-img]').forEach(function (i) {
    var d = IMG[i.dataset.img]; if (d) i.src = d;
  });
  var panels = [].slice.call(document.querySelectorAll('.rt'));
  var titles = __TITLES__;
  function go(first) {
    var r = (location.hash || '#home').slice(1);
    if (!panels.some(function (p) { return p.dataset.route === r; })) r = 'home';
    panels.forEach(function (p) { p.hidden = p.dataset.route !== r; });
    document.querySelectorAll('.nav a, .mn-link').forEach(function (a) {
      var h = (a.getAttribute('href') || '').slice(1);
      var on = h === r || (h === 'products' && r.indexOf('p-') === 0);
      if (on) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current');
    });
    if (titles[r]) document.title = titles[r];
    document.body.classList.remove('menu-open');
    document.documentElement.style.overflow = '';
    var b = document.querySelector('.burger'); if (b) b.setAttribute('aria-expanded', 'false');
    if (!first) window.scrollTo(0, 0);
    var vis = panels.filter(function (p) { return !p.hidden; })[0];
    if (vis) vis.querySelectorAll('.rv').forEach(function (e) {
      var t = e.getBoundingClientRect().top;
      if (t < innerHeight) e.classList.add('in');
    });
    window.dispatchEvent(new Event('scroll'));
  }
  window.addEventListener('hashchange', function () { go(false); });
  go(true);
})();
"""
router = router.replace("__IMGMAP__", json.dumps(imgs))
router = router.replace("__TITLES__", json.dumps({
    r: (re.search(r"<title>(.*?)</title>", read(p), re.S).group(1)) for r, p in ROUTES}))

doc = """<meta charset="utf-8">
<title>New Super Polymers</title>
<script>document.documentElement.className+=" js";</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Instrument+Serif:ital@0;1&family=Schibsted+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
%s
/* ---- bundled-page overrides ---- */
.rt[hidden] { display: none; }
main { display: block; }
</style>
%s
<main id="main">
%s
</main>
%s
<script>
%s
%s
</script>
""" % (css, header, "\n".join(panels), footer, js, router)

open(OUT, "w", encoding="utf-8").write(doc)
print("wrote", OUT, "%.0f KB" % (len(doc.encode()) / 1024))
