#!/usr/bin/env python3
"""One-time YouTube OAuth for The Myth Ledger (separate Google account), stored apart from wrdclipz.

Step 1: yt_auth_ml.py url <public_client_id>
        Prints the consent URL (dots in the query percent-encoded so chat does not truncate it)
        and saves the PKCE verifier + state to .yt-auth-state.json (mode 600).
Step 2: William approves as the Myth Ledger account; the browser then fails to load
        http://127.0.0.1:8085/?state=...&code=... He does NOT paste it in chat (chat redacts it);
        the code goes in through `secrets request GOOGLE_OAUTH_CODE`.
Step 3: yt_auth_ml.py code   (needs GOOGLE_OAUTH_CODE, GOOGLE_OAUTH_CLIENT_ID/SECRET in env)
        Exchanges the code and stores the refresh token as GOOGLE_OAUTH_REFRESH_TOKEN_MYTHLEDGER.
        The wrdclipz token GOOGLE_OAUTH_REFRESH_TOKEN is never touched.
"""
import base64, hashlib, json, os, secrets, subprocess, sys, urllib.error, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = f"{HERE}/.yt-auth-state.json"
SCOPES = ("https://www.googleapis.com/auth/youtube.upload "
          "https://www.googleapis.com/auth/youtube.readonly "
          "https://www.googleapis.com/auth/yt-analytics.readonly")
REDIRECT = "http://127.0.0.1:8085"
SECRET_NAME = "GOOGLE_OAUTH_REFRESH_TOKEN_MYTHLEDGER"

mode = sys.argv[1] if len(sys.argv) > 1 else ""

if mode == "url" and len(sys.argv) > 2:
    verifier = secrets.token_urlsafe(64)
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
    state = secrets.token_urlsafe(16)
    with open(STATE, "w") as f:
        json.dump({"verifier": verifier, "state": state}, f)
    os.chmod(STATE, 0o600)
    q = urllib.parse.urlencode({
        "client_id": sys.argv[2], "redirect_uri": REDIRECT, "response_type": "code", "scope": SCOPES,
        "access_type": "offline", "prompt": "consent",
        "code_challenge": challenge, "code_challenge_method": "S256", "state": state})
    print("https://accounts.google.com/o/oauth2/v2/auth?" + q.replace(".", "%2E"))

elif mode == "code":
    saved = json.load(open(STATE))
    for k in ("GOOGLE_OAUTH_CLIENT_ID", "GOOGLE_OAUTH_CLIENT_SECRET", "GOOGLE_OAUTH_CODE"):
        if k not in os.environ:
            sys.exit(f"MISSING ENV: {k}")
    body = "&".join([
        "client_id=" + os.environ["GOOGLE_OAUTH_CLIENT_ID"],
        "client_secret=" + os.environ["GOOGLE_OAUTH_CLIENT_SECRET"],
        "code=" + os.environ["GOOGLE_OAUTH_CODE"],
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
    subprocess.run(["openclaw", "secrets", "store", "set", SECRET_NAME, "--kind", "secret",
                    "--allow-host", "oauth2.googleapis.com", "--allow-host", "youtube.googleapis.com",
                    "--allow-host", "www.googleapis.com", "--value-file", "-"],
                   input=tok["refresh_token"].encode(), check=True)
    os.remove(STATE)
    print(f"Refresh token stored as {SECRET_NAME} (value not shown).")

else:
    sys.exit(__doc__)
