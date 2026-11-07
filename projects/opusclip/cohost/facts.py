"""Official-source fact tooling (stdlib only).
  facts.py fetch SLUG URL [URL...]   fetch pages with curl, store readable text in work/SLUG/sources/, print dates and headline
  facts.py find SLUG KEYWORD [KEYWORD...]   print source sentences containing the keywords (for picking quotes)
  facts.py verify SLUG               check work/SLUG/facts.json against the stored source text (also run by the guard)
facts.json = list of {id, claim, quote, url, date (YYYY-MM-DD or "Unknown"), source (publisher/page title)}.
A fact is valid only if: URL domain is an official domain, the page was fetched, the quote appears verbatim in that page's text,
and the date is ISO or Unknown. Nothing here invents anything: the agent selects quotes, this file checks them."""
import hashlib, html, json, os, re, subprocess, sys
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = json.load(open(os.path.join(HERE, "config.json")))


def norm(s):
    s = html.unescape(s)
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').replace("®", "").replace("™", "").replace("–", "-").replace("—", "-").replace(" ", " ")
    return re.sub(r"\s+", " ", s).strip().lower()


def to_text(raw):
    t = re.sub(r"(?s)<(script|style|noscript)[^>]*>.*?</\1>", " ", raw)
    t = re.sub(r"<[^>]+>", "\n", t)
    t = html.unescape(t)
    return re.sub(r"\n\s*\n+", "\n", t)


def domain_ok(url):
    host = (urlparse(url).hostname or "").lower()
    return any(host == d or host.endswith("." + d) for d in CFG["official_domains"])


def sdir(slug):
    d = os.path.join(HERE, "work", slug, "sources")
    os.makedirs(d, exist_ok=True)
    return d


def fetch(slug, url):
    if not domain_ok(url):
        print(f"REFUSED (not an official domain): {url}")
        return None
    d = sdir(slug)
    key = hashlib.sha1(url.encode()).hexdigest()[:10]
    raw = subprocess.run(["curl", "-sL", "-A", "Mozilla/5.0", "-m", "40", url], capture_output=True).stdout.decode("utf-8", "ignore")
    txt = to_text(raw)
    open(os.path.join(d, key + ".txt"), "w").write(txt)
    idx_p = os.path.join(d, "index.json")
    idx = json.load(open(idx_p)) if os.path.exists(idx_p) else {}
    idx[url] = key + ".txt"
    json.dump(idx, open(idx_p, "w"), indent=1)
    dates = re.findall(r"(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4}", txt)
    print(f"{url}\n  {len(txt)} chars, first dates: {dates[:3]}")
    return txt


def source_text(slug, url):
    idx_p = os.path.join(sdir(slug), "index.json")
    if not os.path.exists(idx_p):
        return None
    f = json.load(open(idx_p)).get(url)
    return open(os.path.join(sdir(slug), f)).read() if f else None


def verify(slug, facts=None):
    """returns (valid dict id->fact, problems list)"""
    facts = facts if facts is not None else json.load(open(os.path.join(HERE, "work", slug, "facts.json")))
    ok, problems = {}, []
    for f in facts:
        fid = f.get("id", "?")
        if not all(f.get(k) for k in ("id", "quote", "url", "date")):
            problems.append(f"{fid}: missing id/quote/url/date")
            continue
        if not domain_ok(f["url"]):
            problems.append(f"{fid}: {f['url']} is not an official domain")
            continue
        if f["date"] != "Unknown" and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", f["date"]):
            problems.append(f"{fid}: date must be YYYY-MM-DD or Unknown")
            continue
        txt = source_text(slug, f["url"])
        if txt is None:
            problems.append(f"{fid}: page not fetched (run facts.py fetch)")
            continue
        if norm(f["quote"]) not in norm(txt):
            problems.append(f"{fid}: quote NOT found verbatim on {f['url']}")
            continue
        if f["date"] != "Unknown":
            y, m, d = f["date"].split("-")
            month = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"][int(m) - 1]
            if norm(f"{month} {int(d):02d}, {y}") not in norm(txt) and norm(f"{month} {int(d)}, {y}") not in norm(txt):
                problems.append(f"{fid}: date {f['date']} not printed on the page (use Unknown or fix)")
                continue
        ok[fid] = f
    return ok, problems


if __name__ == "__main__":
    cmd, slug, rest = sys.argv[1], sys.argv[2], sys.argv[3:]
    if cmd == "fetch":
        for u in rest:
            fetch(slug, u)
    elif cmd == "find":
        idx = json.load(open(os.path.join(sdir(slug), "index.json")))
        kws = [k.lower() for k in rest]
        for url, f in idx.items():
            t = re.sub(r"\s+", " ", open(os.path.join(sdir(slug), f)).read())
            for s in re.split(r"(?<=[.!?])\s+", t):
                if any(k in s.lower() for k in kws) and len(s) < 400:
                    print(f"[{url}]\n   {s}")
    elif cmd == "verify":
        ok, pr = verify(slug)
        print(f"{len(ok)} verified facts")
        for p in pr:
            print("PROBLEM", p)
        sys.exit(1 if pr else 0)
