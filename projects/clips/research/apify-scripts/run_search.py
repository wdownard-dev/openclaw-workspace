import json, os, time, urllib.request, urllib.parse
API = "https://api.apify.com/v2"
TOKEN = os.environ["APIFY_API_KEY"]
OUT = "/home/williamdownard/.openclaw/workspace/projects/clips/research/apify-data"
ACTOR = "clockworks~tiktok-scraper"
QUERIES = ["Total Drama Island Roblox", "HardScope unpacked clip", "MrBeast Gaming MW4 clip", "Family Guy Halloween hell"]
PER_QUERY = 25
MAX_CHARGE_USD = 0.75  # per-run cap; keeps total task spend under the $2 approval

def call(method, url, body=None, timeout=120):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"})
    with urllib.request.urlopen(r, timeout=timeout) as resp:
        return json.load(resp)

params = urllib.parse.urlencode({"maxTotalChargeUsd": MAX_CHARGE_USD})
run = call("POST", f"{API}/acts/{ACTOR}/runs?{params}", {
    "searchQueries": QUERIES, "resultsPerPage": PER_QUERY,
    "shouldDownloadVideos": False, "shouldDownloadCovers": False,
    "shouldDownloadSlideshowImages": False})["data"]
rid = run["id"]; print("run_id", rid, flush=True)
deadline = time.time() + 900
while True:
    run = call("GET", f"{API}/actor-runs/{rid}")["data"]
    if run["status"] in ("SUCCEEDED", "FAILED", "TIMED-OUT", "ABORTED"): break
    if time.time() > deadline:
        call("POST", f"{API}/actor-runs/{rid}/abort"); break
    time.sleep(10)
print("final", run["status"], "usd", run.get("usageTotalUsd"), flush=True)
ds = run["defaultDatasetId"]
with urllib.request.urlopen(urllib.request.Request(
        f"{API}/datasets/{ds}/items?format=json&clean=false",
        headers={"Authorization": f"Bearer {TOKEN}"}), timeout=120) as resp:
    items = json.load(resp)
json.dump(items, open(os.path.join(OUT, "search_raw_items.json"), "w"), ensure_ascii=False)
json.dump({"run_id": rid, "actor": "clockworks/tiktok-scraper", "status": run["status"],
           "usage_total_usd": run.get("usageTotalUsd"), "dataset_id": ds,
           "queries": QUERIES, "results_per_query_requested": PER_QUERY,
           "item_count": len(items), "max_charge_cap_usd": MAX_CHARGE_USD},
          open(os.path.join(OUT, "search_run_meta.json"), "w"), indent=2)
print("items", len(items))
