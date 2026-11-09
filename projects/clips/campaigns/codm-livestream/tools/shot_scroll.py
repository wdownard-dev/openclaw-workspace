import os, sys
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
CHROME = os.path.expanduser("~/openclaw-sites/browsers/chromium-1248/chrome-linux64/chrome")
url, prefix = sys.argv[1], sys.argv[2]
pu = urlparse(os.environ["HTTPS_PROXY"])
proxy = {"server": f"http://{pu.hostname}:{pu.port}", "username": pu.username or "", "password": pu.password or ""}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME, headless=True, proxy=proxy)
    ctx = b.new_context(ignore_https_errors=True, viewport={"width": 1600, "height": 1600})
    page = ctx.new_page()
    page.goto(url, wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(8000)
    # find scrollable container
    h = page.evaluate("""() => { let best=null,bh=0; for (const e of document.querySelectorAll('*')) { if (e.scrollHeight>e.clientHeight+50 && e.clientHeight>400 && e.scrollHeight>bh){best=e;bh=e.scrollHeight;} } window.__sc=best; return best? [best.scrollHeight,best.clientHeight]:null; }""")
    print(h)
    if h:
        n = 0
        y = 0
        while y < h[0]:
            page.evaluate(f"window.__sc.scrollTo(0,{y})")
            page.wait_for_timeout(1500)
            page.screenshot(path=f"{prefix}-{n}.png")
            n += 1; y += h[1] - 200
    b.close()
