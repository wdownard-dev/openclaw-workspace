"""Download named assets from the campaign-supplied Frame.io share (public, no login), one click each.
Usage: fetch_assets.py SHARE_URL OUTDIR [--folder Trailers/Sub] NAME [NAME ...]   (NAME without .mp4 ok)"""
import os, sys
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
CHROME = os.path.expanduser("~/openclaw-sites/browsers/chromium-1248/chrome-linux64/chrome")
args = sys.argv[1:]
url, outdir = args[0], args[1]; rest = args[2:]
folder = None
if rest and rest[0] == "--folder":
    folder = rest[1]; rest = rest[2:]
names = rest
os.makedirs(outdir, exist_ok=True)
pu = urlparse(os.environ["HTTPS_PROXY"])
proxy = {"server": f"http://{pu.hostname}:{pu.port}", "username": pu.username or "", "password": pu.password or ""}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME, headless=True, proxy=proxy)
    ctx = b.new_context(accept_downloads=True, ignore_https_errors=True, viewport={"width": 1600, "height": 1600})
    page = ctx.new_page()
    page.goto(url, wait_until="domcontentloaded", timeout=60000)
    page.wait_for_selector("text=Created by", timeout=60000)
    page.wait_for_timeout(4000)
    if folder:
        for part in folder.split("/"):
            page.get_by_text(part, exact=True).first.dblclick()
            page.wait_for_timeout(6000)
        page.screenshot(path=f"{outdir}/_folder.png")
        for i in range(page.locator("button[aria-label$='Download Asset']").count()):
            print("ASSET", page.locator("button[aria-label$='Download Asset']").nth(i).get_attribute("aria-label"), flush=True)
    page.evaluate("""() => { let best=null,bh=0; for (const e of document.querySelectorAll('*')) { if (e.scrollHeight>e.clientHeight+50 && e.clientHeight>400 && e.scrollHeight>bh){best=e;bh=e.scrollHeight;} } window.__sc=best; }""")
    def find(n):
        sel = f"button[aria-label='{n}.mp4 Download Asset'], button[aria-label='{n} Download Asset']"
        page.evaluate("window.__sc && window.__sc.scrollTo(0,0)")
        for _ in range(12):
            if page.locator(sel).count():
                return page.locator(sel).first
            page.evaluate("window.__sc && window.__sc.scrollBy(0, 800)")
            page.wait_for_timeout(700)
        return None
    for n in names:
        btn = find(n)
        if btn is None:
            print("missing", n, flush=True); continue
        try:
            btn.scroll_into_view_if_needed()
            with page.expect_download(timeout=180000) as dl:
                btn.click()
            d = dl.value
            out = os.path.join(outdir, d.suggested_filename)
            d.save_as(out)
            print("saved", out, round(os.path.getsize(out) / 1e6, 1), "MB", flush=True)
        except Exception as e:
            page.screenshot(path=f"{outdir}/_err_{n}.png"); print("fail", n, type(e).__name__, str(e)[:200], flush=True)
    b.close()
