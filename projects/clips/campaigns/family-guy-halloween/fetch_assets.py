import os, sys
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
CHROME = os.path.expanduser("~/openclaw-sites/browsers/chromium-1248/chrome-linux64/chrome")
url, outdir = sys.argv[1], sys.argv[2]
os.makedirs(outdir, exist_ok=True)
pu = urlparse(os.environ["HTTPS_PROXY"])
proxy = {"server": f"http://{pu.hostname}:{pu.port}", "username": pu.username or "", "password": pu.password or ""}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME, headless=True, proxy=proxy)
    ctx = b.new_context(accept_downloads=True, ignore_https_errors=True, viewport={"width": 1400, "height": 900})
    page = ctx.new_page()
    page.goto(url, wait_until="domcontentloaded", timeout=60000)
    page.wait_for_selector("text=FG Halloween 2026 part", timeout=60000)
    page.wait_for_timeout(2000)
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 6
    rows = page.get_by_text("Team Vyro •")
    print("rows", rows.count(), flush=True)
    for i in range(int(sys.argv[4]) if len(sys.argv) > 4 else 0, n):
        row = rows.nth(i)
        # per-asset download icon is the svg right after the "Team Vyro • date" text
        btn = row.locator("xpath=following::*[name()='svg'][1]")
        try:
            with page.expect_download(timeout=90000) as dl:
                btn.click()
            d = dl.value
        except Exception as e:
            page.screenshot(path=f"{outdir}/err{i}.png"); print("fail", i, type(e).__name__, flush=True); continue
        out = os.path.join(outdir, d.suggested_filename)
        d.save_as(out)
        print("saved", out, os.path.getsize(out) / 1e6, flush=True)
    b.close()
