#!/usr/bin/env python3
"""Two-step Gmail OAuth re-authorization for use from a phone (no loopback listener needed).

Step 1: gmail_auth_paste.py url <public_client_id>
        Prints the Google consent URL; saves PKCE verifier + state to outbox/.gmail-auth-state.json.
Step 2: gmail_auth_paste.py finish '<pasted redirect URL>'
        William approves on his phone; the browser then fails to load http://127.0.0.1:8085/?state=...&code=...
        He copies that address-bar URL back. This step exchanges the code and stores the refresh token
        as GMAIL_OAUTH_REFRESH_TOKEN (never printed).

Token exchange uses GMAIL_OAUTH_CLIENT_ID / GMAIL_OAUTH_CLIENT_SECRET egress-proxy sentinels.
"""
import base64, hashlib, json, os, secrets, subprocess, sys, urllib.error, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = f"{HERE}/../outbox/.gmail-auth-state.json"
SCOPES = "https://www.googleapis.com/auth/gmail.send https://www.googleapis.com/auth/gmail.readonly"
REDIRECT = "http://127.0.0.1:8085"

mode = sys.argv[1] if len(sys.argv) > 1 else ""

if mode == "url" and len(sys.argv) > 2:
    verifier = secrets.token_urlsafe(64)
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
    state = secrets.token_urlsafe(16)
    json.dump({"verifier": verifier, "state": state}, open(STATE, "w"))
    os.chmod(STATE, 0o600)
    print("https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode({
        "client_id": sys.argv[2], "redirect_uri": REDIRECT, "response_type": "code", "scope": SCOPES,
        "access_type": "offline", "prompt": "consent",
        "code_challenge": challenge, "code_challenge_method": "S256", "state": state}))

elif mode == "finish" and len(sys.argv) > 2:
    saved = json.load(open(STATE))
    q = urllib.parse.parse_qs(urllib.parse.urlparse(sys.argv[2].strip()).query)
    if q.get("state", [""])[0] != saved["state"] or "code" not in q:
        sys.exit("AUTH ERROR: " + q.get("error", ["state mismatch or no code in pasted URL"])[0])
    body = "&".join([
        "client_id=" + os.environ["GMAIL_OAUTH_CLIENT_ID"],
        "client_secret=" + os.environ["GMAIL_OAUTH_CLIENT_SECRET"],
        "code=" + urllib.parse.quote(q["code"][0], safe=""),
        "code_verifier=" + saved["verifier"],
        "redirect_uri=" + urllib.parse.quote(REDIRECT, safe=""),
        "grant_type=authorization_code"]).encode()
    try:
        tok = json.load(urllib.request.urlopen(urllib.request.Request(
            "https://oauth2.googleapis.com/token", data=body,
            headers={"Content-Type": "application/x-www-form-urlencoded"}), timeout=30))
    except urllib.error.HTTPError as e:
        sys.exit(f"TOKEN EXCHANGE FAILED: {e.code} {e.read().decode()[:300]}")
    print("scopes granted:", tok.get("scope"))
    if not tok.get("refresh_token"):
        sys.exit("No refresh_token returned.")
    subprocess.run(["openclaw", "secrets", "store", "set", "GMAIL_OAUTH_REFRESH_TOKEN", "--kind", "secret",
                    "--allow-host", "oauth2.googleapis.com", "--allow-host", "gmail.googleapis.com",
                    "--allow-host", "www.googleapis.com", "--value-file", "-"],
                   input=tok["refresh_token"].encode(), check=True)
    os.remove(STATE)
    print("Refresh token stored as GMAIL_OAUTH_REFRESH_TOKEN (value not shown).")
else:
    sys.exit(__doc__)
