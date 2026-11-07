#!/usr/bin/env python3
"""Poll the Project Red Pill dry-run OpusClip projects; dump raw clip JSON per project when ready."""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opus

HERE = os.path.dirname(os.path.abspath(__file__))
jobs = json.load(open(os.path.join(HERE, "dryrun.json")))
done = set()
deadline = time.time() + 40 * 60
while time.time() < deadline and len(done) < len(jobs):
    for j in jobs:
        pid = j["resp"].get("id")
        if not pid or pid in done:
            continue
        try:
            st = opus.call("GET", f"/api/clip-projects/{pid}")
            stage = st.get("stage")
            if stage == "COMPLETE" or stage == "COMPLETED" or st.get("error"):
                res = opus.call("GET", f"/api/exportable-clips?q=findByProjectId&projectId={pid}")
                json.dump({"project": st, "clips": res}, open(os.path.join(HERE, "dryrun-clips", f"{pid}.json"), "w"), indent=1)
                done.add(pid)
                n = len(res if isinstance(res, list) else res.get("data", []))
                print(f"DONE {j['channel']} {pid} stage={stage} clips={n}", flush=True)
        except SystemExit as e:
            print(f"ERR {pid}: {e}", flush=True)
        except Exception as e:
            print(f"ERR {pid}: {e!r}", flush=True)
    if len(done) < len(jobs):
        time.sleep(45)
print(f"FINISHED {len(done)}/{len(jobs)} done", flush=True)
