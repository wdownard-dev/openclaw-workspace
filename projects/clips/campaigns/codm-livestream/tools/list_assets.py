import os, sys
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
CHROME = os.path.expanduser("~/openclaw-sites/browsers/chromium-1248/chrome-linux64/chrome")
url, shot = sys.argv[1], sys.argv[2]
pu = urlparse(os.environ["HTTPS_PROXY"])
proxy = {"server": f"http://{pu.hostname}:{pu.port}", "username": pu.username or "", "password": pu.password or ""}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME, headless=True, proxy=proxy)
    ctx = b.new_context(ignore_https_errors=True, viewport={"width": 1600, "height": 2400})
    page = ctx.new_page()
    page.goto(url, wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(8000)
    page.screenshot(path=shot)
    links = page.locator("a[aria-label^='Select asset']")
    print("count", links.count())
    for i in range(links.count()):
        print(links.nth(i).get_attribute("aria-label"))
    b.close()
