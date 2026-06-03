#!/usr/bin/env python3
"""
Build the Go Green Scrap Pros blog from Markdown drafts.

Reads drafts/*.md (YAML frontmatter + Markdown body) and publishes every post
whose publish_date is on or before today into /blog/<slug>/index.html, matching
the site's nav, footer, and styling. Also builds /blog/index.html listing all
published posts (newest first).

Posts with a future publish_date are skipped, so the GitHub Action can run on a
schedule and each article goes live only when its date arrives.

Usage:
    python3 build_blog.py            # publish posts due today or earlier
    python3 build_blog.py --all      # publish every draft regardless of date (preview)
"""
import os
import re
import sys
import html
import json
import datetime

import markdown

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DRAFTS_DIR = os.path.join(BASE_DIR, "drafts")
BLOG_DIR = os.path.join(BASE_DIR, "blog")
BASE_URL = "https://gogreenscrappros.com"
PHONE = "720-675-7693"
PHONE_TEL = "7206757693"
BRAND = "Go Green Scrap Pros"
BRAND_SUFFIX = f" | {BRAND}"


# ─── Frontmatter parsing (no external YAML dependency) ───────────────────────
def parse_frontmatter(text):
    """Parse a simple YAML frontmatter block delimited by '---' lines.

    Supports flat key: value pairs with optional quotes. Returns (meta, body).
    """
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    _, fm, body = parts
    meta = {}
    for line in fm.strip().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, _, val = line.partition(":")
        val = val.strip()
        if len(val) >= 2 and val[0] in "\"'" and val[-1] == val[0]:
            val = val[1:-1]
        meta[key.strip()] = val
    return meta, body.lstrip("\n")


def clip(text, limit):
    """Word-boundary trim to <= limit chars."""
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    clipped = text[:limit]
    if " " in clipped:
        clipped = clipped[:clipped.rfind(" ")]
    return clipped.rstrip(" |,.;:-\u2014")


def page_title(meta):
    """Build a <=60 char <title>, appending the brand suffix only if it fits."""
    base = meta.get("title", "").strip()
    if len(base) + len(BRAND_SUFFIX) <= 60:
        return base + BRAND_SUFFIX
    return clip(base, 60)


# ─── HTML rendering ──────────────────────────────────────────────────────────
NAV = f'''  <nav class="site-nav">
    <div class="container">
      <a href="/" class="brand">{BRAND}</a>
      <div class="nav-links">
        <a href="/mattress-removal/">Mattress Removal</a>
        <a href="/scrap-metal-pickup/">Scrap Metal</a>
        <a href="/estate-cleanout/">Estate Cleanout</a>
        <a href="/blog/">Blog</a>
        <a href="/about/">About</a>
        <a href="/contact/">Contact</a>
      </div>
      <div class="nav-actions">
        <a href="tel:{PHONE_TEL}" class="nav-cta">Call {PHONE}</a>
        <a href="sms:{PHONE_TEL}" class="nav-sms">Text Us</a>
      </div>
    </div>
  </nav>'''

FOOTER = f'''  <footer>
    <div class="container">
      <div class="footer-nav">
        <a href="/">Home</a>
        <a href="/blog/">Blog</a>
        <a href="/about/">About</a>
        <a href="/contact/">Contact</a>
        <a href="/sitemap/">Site Map</a>
        <a href="/booking.html">Book Online</a>
      </div>
      <div class="footer-cities">
        <a href="/junk-removal-thornton/">Thornton</a>
        <a href="/junk-removal-arvada/">Arvada</a>
        <a href="/junk-removal-westminster/">Westminster</a>
        <a href="/junk-removal-golden/">Golden</a>
        <a href="/junk-removal-wheat-ridge/">Wheat Ridge</a>
        <a href="/junk-removal-broomfield/">Broomfield</a>
        <a href="/junk-removal-northglenn/">Northglenn</a>
      </div>
      <p>{BRAND} &mdash; Thornton, CO 80229 &mdash; {PHONE}</p>
      <p style="margin-top:1.5rem;font-size:0.9rem;">&copy; 2026 {BRAND}. All Rights Reserved.</p>
    </div>
  </footer>'''

HEAD_FONTS = '''  <link rel="stylesheet" href="/assets/style.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" as="style" onload="this.onload=null;this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap"></noscript>'''

# Minimal, theme-matching styles for blog content (scoped to .blog-* classes).
BLOG_CSS = '''  <style>
    .blog-article{max-width:760px;margin:0 auto;padding:2.5rem 1.25rem 3.5rem;}
    .blog-article > header{background:none;color:inherit;padding:0;text-align:left;box-shadow:none;}
    .blog-article h1{font-size:2rem;line-height:1.2;margin:.25rem 0 .5rem;color:#1e5a4a;text-shadow:none;letter-spacing:normal;font-weight:700;}
    .blog-meta{color:#5b6b5e;font-size:.95rem;margin-bottom:1.75rem;}
    .blog-meta time{color:#5b6b5e;}
    .blog-meta .cat{display:inline-block;background:#e8f3ea;color:#2e7d4f;border-radius:999px;padding:.15rem .7rem;font-weight:600;font-size:.8rem;margin-right:.6rem;}
    .blog-body{font-size:1.08rem;line-height:1.7;color:#26312a;}
    .blog-body h2{font-size:1.4rem;margin:2rem 0 .6rem;}
    .blog-body h3{font-size:1.15rem;margin:1.4rem 0 .4rem;}
    .blog-body p{margin:0 0 1rem;}
    .blog-body ul,.blog-body ol{margin:0 0 1.2rem 1.3rem;}
    .blog-body li{margin:.35rem 0;}
    .blog-body a{color:#2e7d4f;text-decoration:underline;}
    .blog-cta{margin-top:2.5rem;padding:1.5rem;background:#f3f8f4;border-radius:14px;text-align:center;}
    .blog-cta a.cta-button{margin-top:.75rem;}
    .breadcrumbs{max-width:760px;margin:0 auto;padding:1.25rem 1.25rem 0;font-size:.9rem;color:#5b6b5e;}
    .breadcrumbs a{color:#2e7d4f;text-decoration:none;}
    .blog-index{max-width:880px;margin:0 auto;padding:2.5rem 1.25rem 3.5rem;}
    .blog-index h1{font-size:2.1rem;margin-bottom:.4rem;}
    .post-card{display:block;padding:1.4rem 1.5rem;margin:1rem 0;border:1px solid #e1eae3;border-radius:14px;text-decoration:none;color:inherit;transition:box-shadow .15s,border-color .15s;}
    .post-card:hover{box-shadow:0 6px 20px rgba(46,125,79,.12);border-color:#bcd9c6;}
    .post-card .cat{display:inline-block;background:#e8f3ea;color:#2e7d4f;border-radius:999px;padding:.12rem .6rem;font-weight:600;font-size:.75rem;margin-bottom:.5rem;}
    .post-card h2{font-size:1.25rem;margin:.2rem 0 .35rem;}
    .post-card p{color:#46544a;margin:0;font-size:.98rem;}
    .post-card time{color:#7a8a7e;font-size:.85rem;}
  </style>'''


def render_article(meta, body_html, slug):
    url = f"{BASE_URL}/blog/{slug}/"
    title = page_title(meta)
    desc = clip(meta.get("description", ""), 160)
    pub = meta.get("publish_date", "")
    category = meta.get("category", "")
    keywords = meta.get("keywords", "")
    h1 = html.escape(meta.get("title", ""))
    img = f"{BASE_URL}/assets/images/logo.png"

    article_ld = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": meta.get("title", ""),
        "description": desc,
        "datePublished": pub,
        "dateModified": pub,
        "author": {"@type": "Organization", "name": BRAND},
        "publisher": {
            "@type": "Organization",
            "name": BRAND,
            "logo": {"@type": "ImageObject", "url": img},
        },
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "image": img,
    }
    breadcrumb_ld = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{BASE_URL}/blog/"},
            {"@type": "ListItem", "position": 3, "name": meta.get("title", ""), "item": url},
        ],
    }

    pretty_date = pub
    try:
        pretty_date = datetime.date.fromisoformat(pub).strftime("%B %-d, %Y")
    except ValueError:
        pass

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{html.escape(desc)}">
  <meta name="keywords" content="{html.escape(keywords)}">
  <meta name="author" content="{BRAND}">
  <meta property="og:title" content="{html.escape(meta.get('title',''))}">
  <meta property="og:description" content="{html.escape(desc)}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{img}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(meta.get('title',''))}">
  <meta name="twitter:description" content="{html.escape(desc)}">
  <meta name="twitter:image" content="{img}">
  <link rel="canonical" href="{url}">
  <meta name="robots" content="index, follow">
  <script type="application/ld+json">
{json.dumps(article_ld, indent=2)}
  </script>
  <script type="application/ld+json">
{json.dumps(breadcrumb_ld, indent=2)}
  </script>
  <title>{html.escape(title)}</title>
{HEAD_FONTS}
{BLOG_CSS}
</head>
<body>
{NAV}

  <nav class="breadcrumbs" aria-label="Breadcrumb">
    <a href="/">Home</a> &rsaquo; <a href="/blog/">Blog</a> &rsaquo; <span>{h1}</span>
  </nav>

  <main>
    <article class="blog-article">
      <header>
        <h1>{h1}</h1>
        <p class="blog-meta">{f'<span class="cat">{html.escape(category)}</span>' if category else ''}<time datetime="{pub}">{pretty_date}</time></p>
      </header>
      <div class="blog-body">
{body_html}
      </div>
      <div class="blog-cta">
        <p><strong>Need it hauled away?</strong> Call or text Adam at {PHONE} for a fast, free quote &mdash; same-day and next-day pickup available across the Denver metro.</p>
        <a href="tel:{PHONE_TEL}" class="cta-button">Call or Text {PHONE}</a>
      </div>
    </article>
  </main>

{FOOTER}
</body>
</html>
'''


def render_index(posts):
    """posts: list of meta dicts (published), newest first."""
    url = f"{BASE_URL}/blog/"
    cards = []
    for m in posts:
        slug = m["slug"]
        pub = m.get("publish_date", "")
        try:
            pretty = datetime.date.fromisoformat(pub).strftime("%B %-d, %Y")
        except ValueError:
            pretty = pub
        cat = m.get("category", "")
        cards.append(f'''      <a class="post-card" href="/blog/{slug}/">
        {f'<span class="cat">{html.escape(cat)}</span><br>' if cat else ''}
        <h2>{html.escape(m.get('title',''))}</h2>
        <p>{html.escape(clip(m.get('description',''),160))}</p>
        <time datetime="{pub}">{pretty}</time>
      </a>''')
    cards_html = "\n".join(cards) if cards else "      <p>New articles coming soon.</p>"

    desc = "Tips and local guides on junk removal, scrap metal, recycling, and estate cleanouts across the Denver metro area from Go Green Scrap Pros."
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{desc}">
  <meta name="author" content="{BRAND}">
  <meta property="og:title" content="Blog | {BRAND}">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{BASE_URL}/assets/images/logo.png">
  <link rel="canonical" href="{url}">
  <meta name="robots" content="index, follow">
  <title>Blog | {BRAND}</title>
{HEAD_FONTS}
{BLOG_CSS}
</head>
<body>
{NAV}

  <main>
    <section class="blog-index">
      <h1>Go Green Scrap Pros Blog</h1>
      <p class="blog-meta">Local guides on junk removal, scrap metal, recycling, and cleanouts across the Denver metro.</p>
{cards_html}
    </section>
  </main>

{FOOTER}
</body>
</html>
'''


def load_drafts():
    drafts = []
    if not os.path.isdir(DRAFTS_DIR):
        return drafts
    for fn in sorted(os.listdir(DRAFTS_DIR)):
        if not fn.endswith(".md"):
            continue
        with open(os.path.join(DRAFTS_DIR, fn), encoding="utf-8") as f:
            meta, body = parse_frontmatter(f.read())
        if not meta.get("slug"):
            meta["slug"] = fn[:-3]
        meta["_body"] = body
        drafts.append(meta)
    return drafts


def build(publish_all=False):
    today = datetime.date.today()
    drafts = load_drafts()
    published = []

    for meta in drafts:
        pub_str = meta.get("publish_date", "")
        try:
            pub_date = datetime.date.fromisoformat(pub_str)
        except ValueError:
            print(f"  ! skipping {meta.get('slug')}: invalid/missing publish_date")
            continue
        if not publish_all and pub_date > today:
            continue  # not due yet

        slug = meta["slug"]
        body_html = markdown.markdown(
            meta["_body"], extensions=["extra", "sane_lists"]
        )
        out_dir = os.path.join(BLOG_DIR, slug)
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(render_article(meta, body_html, slug))
        published.append(meta)
        print(f"  Published: /blog/{slug}/  (date {pub_str})")

    # Sort newest-first for the index
    published.sort(key=lambda m: m.get("publish_date", ""), reverse=True)
    os.makedirs(BLOG_DIR, exist_ok=True)
    with open(os.path.join(BLOG_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(render_index(published))
    print(f"  Blog index updated with {len(published)} post(s).")
    return published


def published_blog_paths():
    """Return site-relative paths for the published blog (for the sitemap).

    e.g. ['blog', 'blog/how-to-dispose-mattress-denver', ...]
    Only includes posts that already exist on disk under /blog/.
    """
    paths = []
    if os.path.isdir(BLOG_DIR):
        if os.path.isfile(os.path.join(BLOG_DIR, "index.html")):
            paths.append("blog")
        for name in sorted(os.listdir(BLOG_DIR)):
            d = os.path.join(BLOG_DIR, name)
            if os.path.isdir(d) and os.path.isfile(os.path.join(d, "index.html")):
                paths.append(f"blog/{name}")
    return paths


def refresh_sitemap():
    """Regenerate sitemap.xml (with fresh lastmod) so new blog posts are indexed."""
    try:
        from generate_pages import generate_sitemap
        generate_sitemap(BASE_DIR)
    except Exception as e:  # pragma: no cover - sitemap is best-effort
        print(f"  ! could not refresh sitemap: {e}")


if __name__ == "__main__":
    publish_all = "--all" in sys.argv
    print(f"Building blog (publish_all={publish_all})...")
    build(publish_all=publish_all)
    refresh_sitemap()
    print("Done!")
