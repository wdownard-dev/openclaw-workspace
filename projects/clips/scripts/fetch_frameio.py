#!/usr/bin/env python3
"""Download a campaign-supplied Frame.io share the way a person would: open the link, click Download.

Usage (project venv): fetch_frameio.py SHARE_URL OUTFILE [--debug-dir DIR]

Only use on files a campaign or creator explicitly supplied for you to use (e.g. a Vyro brief's
'Content to use' link) and only after joining that campaign. Does not touch the player's stream URLs.
Playwright handles the browser download event. If clicking Download opens a menu, the first
'Download' / 'Original' style option is clicked. Screenshots are saved to --debug-dir on trouble.
"""
import os, sys, time
from playwright.sync_api import sync_playwright

CHROME = os.path.expanduser("~/openclaw-sites/browsers/chromium-1248/chrome-linux64/chrome")


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    url, out = sys.argv[1], sys.argv[2]
    dbg = sys.argv[sys.argv.index("--debug-dir") + 1] if "--debug-dir" in sys.argv else os.path.dirname(out)
    os.makedirs(dbg, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME, headless=True, args=["--no-sandbox"] if os.environ.get("PW_NOSANDBOX") else [])
        ctx = b.new_context(accept_downloads=True, viewport={"width": 1400, "height": 900})
        page = ctx.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_selector("button:has-text('Download')", timeout=60000)
        page.screenshot(path=f"{dbg}/frameio-1-loaded.png")
        btn = page.locator("button:has-text('Download')").first
        try:
            with page.expect_download(timeout=45000) as dl:
                btn.click()
            d = dl.value
        except Exception as e:  # menu or modal instead of an immediate download
            print("no immediate download:", type(e).__name__)
            page.wait_for_timeout(1500)
            page.screenshot(path=f"{dbg}/frameio-2-after-click.png")
            # Frame.io opens a menu: 'Original' (size text like '3.01 GB') and 'Proxy' options.
            # --pick SIZE_TEXT chooses the row showing that size (default: the Original row, 1st size shown).
            pick = sys.argv[sys.argv.index("--pick") + 1] if "--pick" in sys.argv else None
            if pick:
                target = page.get_by_text(pick, exact=False).first
            else:
                target = page.locator("text=Original").locator("xpath=following::*[contains(text(),'GB') or contains(text(),'MB')][1]")
            print("clicking menu option:", pick or "Original (first size row)")
            with page.expect_download(timeout=900000) as dl:
                target.click()
            d = dl.value
        print("suggested filename:", d.suggested_filename)
        t0 = time.time()
        d.save_as(out)
        print(f"saved {out} ({os.path.getsize(out)/1e6:.1f} MB in {time.time()-t0:.0f}s)")
        b.close()


if __name__ == "__main__":
    main()
