"""Builds the Calm Edge site (static HTML) into an output folder.
  python build.py <out-dir>
Articles: articles/*.md with a JSON front matter block between '---' lines.
Tools: tools/*.html with the same front matter. Fails on broken internal links."""
import datetime, html, json, pathlib, re, shutil, sys
import markdown
from jinja2 import Environment, FileSystemLoader

ROOT = pathlib.Path(__file__).parent
CFG = json.loads((ROOT / "site.json").read_text())
SITE = CFG["site"].rstrip("/")
env = Environment(loader=FileSystemLoader(ROOT / "templates"), autoescape=False)
BASE = env.get_template("base.html")
VERSION = datetime.date.today().strftime("%Y%m%d")


def front(path):
    raw = path.read_text(encoding="utf-8")
    _, fm, body = raw.split("---\n", 2)
    meta = json.loads(fm)
    meta["body"] = body
    return meta


def callout(kind="app"):
    if kind == "freebie" and not CFG.get("freebie_url"):
        return ""  # the free kit isn't on Gumroad yet
    if kind == "freebie":
        return (f'<div class="callout"><div><b>Free: the Weekly Trading Review Kit</b><p>A one-page review checklist and 12 ready-made AI prompts for '
                f'Claude, ChatGPT or Gemini. Free PDF.</p></div><a class="btn" href="{CFG["freebie_url"]}">Get it free</a></div>')
    return (f'<div class="callout"><div><b>Track all of this automatically</b><p>Trading Journal AI is a desktop app for Windows &amp; Mac: '
            f'log a trade in ten fields and get your R, profit factor, drawdown and edge by setup. One click, and your own AI reviews your week.</p></div>'
            f'<a class="btn" href="{CFG["product_url"]}">See the app</a></div>')


def page(out, path, title, description, body, section="", jsonld=(), og_image=None, og_type=None):
    target = out / path.strip("/") / "index.html" if path != "/" else out / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(BASE.render(title=html.escape(title), description=html.escape(description), body=body, site=SITE, path=path,
                                  section=section, jsonld=list(jsonld), og_image=og_image, og_type=og_type, version=VERSION,
                                  product_url=CFG["product_url"], freebie_url=CFG["freebie_url"], year=datetime.date.today().year), encoding="utf-8")
    PAGES.append(path)


def faq_block(faq):
    if not faq:
        return "", None
    items = "".join(f"<details><summary>{html.escape(q)}</summary><p>{a}</p></details>" for q, a in faq)
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}} for q, a in faq]}
    return f'<section class="faq"><h2>Frequently asked questions</h2>{items}</section>', ld


PAGES = []


def build(out):
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    shutil.copytree(ROOT / "static", out / "static")
    articles = sorted((front(p) for p in (ROOT / "articles").glob("*.md")), key=lambda a: a["date"], reverse=True)
    tools = sorted((front(p) for p in (ROOT / "tools").glob("*.html")), key=lambda t: t.get("order", 9))

    # articles
    for a in articles:
        md = markdown.Markdown(extensions=["tables", "toc", "attr_list"])
        body = md.convert(a["body"].replace("{{app}}", callout()).replace("{{freebie}}", callout("freebie")))
        faq_html, faq_ld = faq_block(a.get("faq"))
        path = f"/learn/{a['slug']}/"
        ld = [{"@context": "https://schema.org", "@type": "Article", "headline": a["title"], "description": a["description"],
               "datePublished": a["date"], "dateModified": a.get("updated", a["date"]), "author": {"@type": "Organization", "name": "Calm Edge"},
               "publisher": {"@type": "Organization", "name": "Calm Edge", "logo": {"@type": "ImageObject", "url": f"{SITE}/static/img/logo.png"}},
               "mainEntityOfPage": f"{SITE}{path}"}]
        if faq_ld:
            ld.append(faq_ld)
        date = datetime.date.fromisoformat(a["date"]).strftime("%B %-d, %Y")
        body = (f'<article class="read article"><div class="crumbs"><a href="/learn/">Learn</a> ›</div><h1>{html.escape(a["title"])}</h1>'
                f'<div class="meta">Calm Edge · {date} · {a.get("minutes", 6)} min read</div>{body}{faq_html}{callout() if "{{app}}" not in a["body"] else ""}</article>')
        page(out, path, a.get("seo_title", a["title"]) + " | Calm Edge", a["description"], body, "learn", ld, og_type="article")

    # tools
    for t in tools:
        faq_html, faq_ld = faq_block(t.get("faq"))
        path = f"/tools/{t['slug']}/"
        ld = [{"@context": "https://schema.org", "@type": "WebApplication", "name": t["title"], "applicationCategory": "FinanceApplication",
               "operatingSystem": "Any", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "url": f"{SITE}{path}"}]
        if faq_ld:
            ld.append(faq_ld)
        body = (f'<div class="read article"><div class="crumbs"><a href="/tools/">Free tools</a> ›</div><h1>{html.escape(t["title"])}</h1>'
                f'<p class="lead muted">{t["intro"]}</p>{t["body"].replace("{{app}}", callout()).replace("{{freebie}}", callout("freebie"))}{faq_html}</div>')
        page(out, path, t.get("seo_title", t["title"]) + " | Calm Edge", t["description"], body, "tools", ld)

    # indexes
    card = lambda href, title, text, pill="": (f'<a class="card" href="{href}">{f"<span class=pill>{pill}</span>" if pill else ""}<h3>{html.escape(title)}</h3>'
                                                f'<p class="muted">{html.escape(text)}</p><span class="more">Open →</span></a>')
    tools_cards = "".join(card(f"/tools/{t['slug']}/", t["title"], t["description"], "Free") for t in tools)
    learn_cards = "".join(card(f"/learn/{a['slug']}/", a["title"], a["description"]) for a in articles)
    page(out, "/tools/", "Free trading calculators | Calm Edge", "Free position size, R multiple, profit factor and expectancy calculators for futures, stocks, forex and crypto traders.",
         f'<div class="wrap" style="padding-top:46px"><div class="kicker">Free tools</div><h1>Free trading calculators</h1>'
         f'<p class="lead muted" style="max-width:680px">Quick, private calculators that run in your browser. Nothing to sign up for.</p><div class="grid">{tools_cards}</div></div>', "tools")
    page(out, "/learn/", "Learn: trading journal, risk and performance | Calm Edge", "Plain-English guides to R multiples, profit factor, drawdown, position sizing and keeping a trading journal that actually helps.",
         f'<div class="wrap" style="padding-top:46px"><div class="kicker">Learn</div><h1>Trade with your real numbers</h1>'
         f'<p class="lead muted" style="max-width:680px">Plain-English guides to the numbers that tell you whether you have an edge.</p><div class="grid">{learn_cards}</div></div>', "learn")

    # product + home
    prod = (ROOT / "pages" / "product.html").read_text(encoding="utf-8")
    home = (ROOT / "pages" / "home.html").read_text(encoding="utf-8")
    fill = lambda s: (s.replace("{{product_url}}", CFG["product_url"]).replace("{{freebie_url}}", CFG["freebie_url"])
                      .replace("{{tools}}", tools_cards).replace("{{learn}}", "".join(card(f"/learn/{a['slug']}/", a["title"], a["description"]) for a in articles[:6]))
                      .replace("{{freebie}}", callout("freebie")).replace("{{price}}", CFG["price"]))
    app_ld = {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "Trading Journal AI", "operatingSystem": "Windows 10, Windows 11, macOS 11+",
              "applicationCategory": "FinanceApplication", "offers": {"@type": "Offer", "price": CFG["price"].strip("$"), "priceCurrency": "USD", "url": CFG["product_url"]},
              "image": f"{SITE}/static/img/01_cover.jpg", "description": "Desktop trading journal with a one-click AI weekly review in Claude, ChatGPT or Gemini."}
    page(out, "/trading-journal-ai/", "Trading Journal AI: desktop trading journal with one-click AI review", "A calm desktop trading journal for Windows & Mac. Log a trade in ten fields, find your edge by setup and hour, and get a one-click weekly review from Claude, ChatGPT or Gemini.",
         fill(prod), "product", [app_ld])
    page(out, "/", "Calm Edge: honest trading journal and free trading calculators", "Calm, honest tools for traders: Trading Journal AI for Windows & Mac, free position size and R multiple calculators, and plain-English guides.",
         fill(home), "", [{"@context": "https://schema.org", "@type": "Organization", "name": "Calm Edge", "url": SITE, "logo": f"{SITE}/static/img/logo.png"}])

    # privacy (also used by the social media publishing app)
    page(out, "/privacy/", "Privacy policy | Calm Edge", "How Calm Edge handles data on this site, in Trading Journal AI and in its social media publishing tool.",
         (ROOT / "pages" / "privacy.html").read_text(encoding="utf-8"))

    # 404, robots, sitemap
    page(out, "/404/", "Page not found | Calm Edge", "Page not found.", '<div class="read" style="padding-top:60px"><h1>Page not found</h1><p><a href="/">Back to the home page</a></p></div>')
    shutil.move(out / "404" / "index.html", out / "404.html"); (out / "404").rmdir(); PAGES.remove("/404/")
    (out / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    today = datetime.date.today().isoformat()
    urls = "".join(f"<url><loc>{SITE}{p}</loc><lastmod>{today}</lastmod></url>" for p in PAGES)
    (out / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    (out / ".nojekyll").write_text("")

    # internal link check
    bad = []
    for f in out.rglob("*.html"):
        for href in re.findall(r'href="(/[^"#?]*)', f.read_text(encoding="utf-8")):
            t = out / href.strip("/")
            if not (t.is_file() or (t / "index.html").is_file() or href == "/"):
                bad.append(f"{f.relative_to(out)} -> {href}")
    if bad:
        print("Broken links:\n" + "\n".join(bad)); sys.exit(1)
    print(f"{len(PAGES)} pages built")


if __name__ == "__main__":
    build(pathlib.Path(sys.argv[1]))
