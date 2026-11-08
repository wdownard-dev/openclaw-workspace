#!/usr/bin/env python3
"""Finish YouTube OAuth using the auth code supplied via the protected store (GOOGLE_OAUTH_CODE).

Chat redacts long token-like strings, so the code is entered through masked secret entry instead of pasted.
Run `yt_auth_paste.py url <public_client_id>` first (saves PKCE verifier + state), then this script.
Token exchange uses egress-proxy sentinels for client id/secret/code; the refresh token is stored, never printed.
"""
import json, os, subprocess, sys, urllib.error, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
saved = json.load(open(f"{HERE}/../outbox/.yt-auth-state.json"))
for k in ("GOOGLE_OAUTH_CLIENT_ID", "GOOGLE_OAUTH_CLIENT_SECRET", "GOOGLE_OAUTH_CODE"):
    if k not in os.environ:
        sys.exit(f"MISSING ENV: {k}")
body = "&".join([
    "client_id=" + os.environ["GOOGLE_OAUTH_CLIENT_ID"],
    "client_secret=" + os.environ["GOOGLE_OAUTH_CLIENT_SECRET"],
    "code=" + os.environ["GOOGLE_OAUTH_CODE"],
    "code_verifier=" + saved["verifier"],
    "redirect_uri=http%3A%2F%2F127.0.0.1%3A8085",
    "grant_type=authorization_code",
]).encode()
req = urllib.request.Request("https://oauth2.googleapis.com/token", data=body,
                             headers={"Content-Type": "application/x-www-form-urlencoded"})
try:
    tok = json.load(urllib.request.urlopen(req, timeout=30))
except urllib.error.HTTPError as e:
    sys.exit("TOKEN EXCHANGE FAILED: %s %s" % (e.code, e.read().decode()[:300]))
print("scopes granted:", tok.get("scope"))
rt = tok.get("refresh_token")
if not rt:
    sys.exit("No refresh_token returned.")
subprocess.run(
    ["openclaw", "secrets", "store", "set", "GOOGLE_OAUTH_REFRESH_TOKEN", "--kind", "secret",
     "--allow-host", "oauth2.googleapis.com", "--allow-host", "www.googleapis.com",
     "--allow-host", "youtube.googleapis.com", "--value-file", "-"],
    input=rt.encode(), check=True)
print("Refresh token stored as GOOGLE_OAUTH_REFRESH_TOKEN (value not shown).")
