import json, os, sys, time, urllib.request, urllib.parse

API = "https://api.apify.com/v2"
TOKEN = os.environ["APIFY_API_KEY"]
OUT = "/home/williamdownard/.openclaw/workspace/projects/clips/research/apify-data"
ACTOR = "clockworks~tiktok-hashtag-scraper"
TAGS = ["unpacked", "TotalDramaRoblox", "MW4", "MW4partner", "FamilyGuy"]
RESULTS_PER_TAG = 30
MAX_CHARGE_USD = 1.00  # hard per-run cap; the task budget is $2 total

def req(method, url, body=None):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"})
    with urllib.request.urlopen(r, timeout=120) as resp:
        return json.load(resp)["data"]

params = urllib.parse.urlencode({"maxTotalChargeUsd": MAX_CHARGE_USD})
run = req("POST", f"{API}/acts/{ACTOR}/runs?{params}",
          {"hashtags": TAGS, "resultsPerPage": RESULTS_PER_TAG,
           "shouldDownloadVideos": False, "shouldDownloadCovers": False,
           "downloadSubtitlesOptions": "NEVER_DOWNLOAD_SUBTITLES",
           "shouldDownloadSlideshowImages": False})
run_id = run["id"]
print("run_id", run_id, "status", run["status"], flush=True)

deadline = time.time() + 900
while True:
    run = req("GET", f"{API}/actor-runs/{run_id}")
    if run["status"] in ("SUCCEEDED", "FAILED", "TIMED-OUT", "ABORTED"):
        break
    if time.time() > deadline:
        print("poll deadline reached; aborting run", flush=True)
        req("POST", f"{API}/actor-runs/{run_id}/abort")
        break
    time.sleep(10)
print("final status", run["status"], "usage_usd", run.get("usageTotalUsd"), flush=True)

ds = run["defaultDatasetId"]
items = req("GET", f"{API}/datasets/{ds}/items?format=json&clean=true&limit=1000") \
    if False else None
# dataset items endpoint returns a raw JSON list, not the {data:} envelope
with urllib.request.urlopen(urllib.request.Request(
        f"{API}/datasets/{ds}/items?format=json&clean=false",
        headers={"Authorization": f"Bearer {TOKEN}"}), timeout=120) as resp:
    items = json.load(resp)
with open(os.path.join(OUT, "hashtag_raw_items.json"), "w") as f:
    json.dump(items, f, ensure_ascii=False)
meta = {"run_id": run_id, "actor": "clockworks/tiktok-hashtag-scraper",
        "status": run["status"], "usage_total_usd": run.get("usageTotalUsd"),
        "dataset_id": ds, "tags": TAGS, "results_per_tag_requested": RESULTS_PER_TAG,
        "item_count": len(items), "max_charge_cap_usd": MAX_CHARGE_USD}
with open(os.path.join(OUT, "run_meta.json"), "w") as f:
    json.dump(meta, f, indent=2)
print(json.dumps(meta, indent=2))
