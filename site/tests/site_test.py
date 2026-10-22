"""Checks every page on desktop and phone: no horizontal overflow, no console errors, calculators give the right numbers."""
import pathlib, subprocess, sys, time, os
from playwright.sync_api import sync_playwright
SITE = pathlib.Path(sys.argv[1]); SHOTS = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else None
PORT = 8812
srv = subprocess.Popen([sys.executable, "-m", "http.server", str(PORT), "-d", str(SITE)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(0.8)
pages = ["/" if p.parent == SITE else "/" + str(p.parent.relative_to(SITE)) + "/" for p in SITE.rglob("index.html")]
fails, errors = [], []
OVER = """() => { const bad = []; const W = document.documentElement.clientWidth;
  if (document.documentElement.scrollWidth > W + 1) bad.push('page scrolls sideways: ' + document.documentElement.scrollWidth + ' > ' + W);
  document.querySelectorAll('h1,h2,h3,p,li,a.btn,.res b,.card,.callout,.formula').forEach(e => { const r = e.getBoundingClientRect();
    if (r.width && r.right > W + 1 && !e.closest('table') && getComputedStyle(e).overflowX === 'visible') bad.push('off screen: ' + e.tagName + ' ' + e.textContent.trim().slice(0, 30)); });
  return bad.slice(0, 5); }"""
def check(c, m):
    if not c: fails.append(m)
try:
    with sync_playwright() as p:
        exe = os.environ.get("CHROME_PATH") or "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
        b = p.chromium.launch(executable_path=exe if os.path.exists(exe) else None)
        for vw, vh, tag in ((1280, 900, "desktop"), (390, 844, "phone")):
            pg = b.new_page(viewport={"width": vw, "height": vh})
            pg.on("console", lambda m: m.type == "error" and errors.append(m.text))
            pg.on("pageerror", lambda e: errors.append(str(e)))
            for path in sorted(pages):
                pg.goto(f"http://127.0.0.1:{PORT}{path}"); pg.evaluate("document.fonts.ready")
                bad = pg.evaluate(OVER); check(not bad, f"{tag} {path}: {bad}")
                check(pg.locator("h1").count() == 1, f"{path}: one h1")
                if SHOTS:
                    SHOTS.mkdir(exist_ok=True, parents=True)
                    pg.screenshot(path=str(SHOTS / f"{tag}_{path.strip('/').replace('/', '_') or 'home'}.png"), full_page=True)
            pg.close()
        pg = b.new_page()
        pg.goto(f"http://127.0.0.1:{PORT}/tools/position-size-calculator/")
        check(pg.text_content("#oSize") == "5 contracts", f"position size {pg.text_content('#oSize')}")
        check(pg.text_content("#oReal") == "$100.00", f"real risk {pg.text_content('#oReal')}")
        pg.select_option("#inst", "50"); check(pg.text_content("#oSize").startswith("0"), "ES too big")
        pg.goto(f"http://127.0.0.1:{PORT}/tools/r-multiple-calculator/")
        check(pg.text_content("#oR") == "+2.00R", f"R {pg.text_content('#oR')}")
        pg.select_option("#side", "Short"); check("wrong side" in pg.text_content("#oWarn"), "short stop warning")
        pg.goto(f"http://127.0.0.1:{PORT}/tools/profit-factor-calculator/")
        check(pg.text_content("#oPF") == "1.46", f"PF {pg.text_content('#oPF')}")
        b.close()
finally:
    srv.terminate()
print("pages:", len(pages), "failed:", len(fails)); [print(" -", f) for f in fails]
print("console errors:", len(errors)); [print(" -", e) for e in errors[:5]]
sys.exit(1 if fails or errors else 0)
