#!/usr/bin/env python3
"""Scan LinkedIn's public guest job endpoints and write candidates.json.
Usage: python3 -I scan.py OUTFILE
Read-only; no login, no applications.
"""
import json, re, sys, time, html, urllib.parse, urllib.request

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36"}
KEYWORDS = [
    "systems administrator", "system administrator", "IT administrator",
    "Microsoft 365 administrator", "Intune", "endpoint engineer",
    "systems engineer", "IT systems engineer", "security engineer Microsoft",
    "IT infrastructure", "Entra ID", "Azure administrator", "Jamf",
]
LOCS = [("Miami, Florida", None), ("United States", "2"), ("Miami, Florida", "2"), ("Miami, Florida", "3")]
TPR = "r1209600"  # last 14 days


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read().decode("utf8", "replace")


def parse_cards(page):
    out = []
    for m in re.finditer(r'<li>(.*?)</li>', page, re.S):
        c = m.group(1)
        link = re.search(r'href="(https://www\.linkedin\.com/jobs/view/[^"?]+)', c)
        if not link:
            continue
        jid = re.search(r'-(\d{6,})$', link.group(1))
        title = re.search(r'base-search-card__title[^>]*>\s*(.*?)\s*<', c, re.S)
        comp = re.search(r'base-search-card__subtitle[^>]*>.*?>\s*([^<]+?)\s*<', c, re.S)
        loc = re.search(r'job-search-card__location[^>]*>\s*(.*?)\s*<', c, re.S)
        date = re.search(r'datetime="([^"]+)"', c)
        out.append({
            "id": jid.group(1) if jid else None,
            "url": link.group(1),
            "title": html.unescape(title.group(1)) if title else "",
            "company": html.unescape(comp.group(1)) if comp else "",
            "location": html.unescape(loc.group(1)) if loc else "",
            "posted": date.group(1) if date else "",
        })
    return out


def main(outfile):
    seen = {}
    for kw in KEYWORDS:
        for loc, wt in LOCS:
            for start in (0, 25):
                q = {"keywords": kw, "location": loc, "f_TPR": TPR, "start": start}
                if wt:
                    q["f_WT"] = wt
                url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?" + urllib.parse.urlencode(q)
                try:
                    cards = parse_cards(get(url))
                except Exception as e:
                    print("ERR", kw, loc, wt, start, e, file=sys.stderr)
                    time.sleep(2)
                    continue
                for c in cards:
                    if c["id"] and c["id"] not in seen:
                        c["workplace"] = {None: "onsite-or-any", "2": "remote", "3": "hybrid"}[wt]
                        c["found_by"] = kw
                        seen[c["id"]] = c
                time.sleep(0.6)
                if len(cards) < 20:
                    break
    print("candidates:", len(seen), file=sys.stderr)
    for i, c in enumerate(seen.values()):
        try:
            d = get("https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/" + c["id"])
        except Exception as e:
            c["desc"] = ""
            continue
        desc = re.search(r'show-more-less-html__markup[^>]*>(.*?)</div>', d, re.S)
        txt = re.sub(r'<br\s*/?>|</p>|</li>', '\n', desc.group(1)) if desc else ""
        c["desc"] = html.unescape(re.sub(r'<[^>]+>', '', txt)).strip()
        sal = re.search(r'\$\s?[\d,]{2,}(?:\.\d+)?\s?[kK]?(?:\s?(?:-|to|–)\s?\$?\s?[\d,]{2,}(?:\.\d+)?\s?[kK]?)?', c["desc"])
        c["salary_hint"] = sal.group(0) if sal else ""
        time.sleep(0.5)
    json.dump(list(seen.values()), open(outfile, "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
