#!/usr/bin/env python3
"""Upload a LOCAL mp4 to OpusClip (3-step resumable upload) and create a no-clipping project, so it can be
posted with ../opusclip/opus.py post. Costs about 1 credit per source minute (a Short under 1 min = 1 credit).

  opus_upload.py FILE.mp4 [--title T]     prints the projectId when created
Needs OPUSCLIP_API_KEY (present under the OpenClaw exec tool). Nothing is posted here.
"""
import argparse, json, os, sys, urllib.request, urllib.error

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "opusclip"))
import opus  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--title", default="")
    a = ap.parse_args()

    link = opus.call("POST", "/api/upload-links", {"video": {"usecase": "LocalUpload"}})
    print("upload link ok, uploadId", link["uploadId"])

    req = urllib.request.Request(link["url"], data=b"", method="POST",
                                 headers={"x-goog-resumable": "start", "Content-Length": "0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        loc = r.headers["location"]
    print("resumable session started")

    size = os.path.getsize(a.file)
    with open(a.file, "rb") as f:
        put = urllib.request.Request(loc, data=f, method="PUT",
                                     headers={"Content-Type": "application/octet-stream", "Content-Length": str(size)})
        with urllib.request.urlopen(put, timeout=600) as r:
            print("file uploaded, HTTP", r.status, size, "bytes")

    body = {"videoUrl": link["uploadId"], "curationPref": {"skipCurate": True}}
    if a.title:
        body["uploadedVideoAttr"] = {"title": a.title}
    print(json.dumps(opus.call("POST", "/api/clip-projects", body), indent=2))


if __name__ == "__main__":
    main()
