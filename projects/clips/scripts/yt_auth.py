#!/usr/bin/env python3
"""One-time YouTube OAuth authorization (loopback + PKCE).

Usage: yt_auth.py <public_client_id> [port]

- The public client_id is only used to print the browser URL.
- The token exchange uses GOOGLE_OAUTH_CLIENT_ID / GOOGLE_OAUTH_CLIENT_SECRET from the
  environment (egress-proxy sentinels; the proxy substitutes real values on the wire).
- The refresh token is piped straight into the OpenClaw secret store as
  GOOGLE_OAUTH_REFRESH_TOKEN and is never printed.
"""
import base64, hashlib, http.server, json, os, secrets, subprocess, sys, threading, urllib.request, urllib.parse

SCOPES = "https://www.googleapis.com/auth/youtube.upload https://www.googleapis.com/auth/youtube.readonly"
public_id = sys.argv[1] if len(sys.argv) > 1 else "PASTE_CLIENT_ID_HERE"
port = int(sys.argv[2]) if len(sys.argv) > 2 else 8085
redirect_uri = f"http://127.0.0.1:{port}"

verifier = secrets.token_urlsafe(64)
challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
state = secrets.token_urlsafe(16)

params = {
    "client_id": public_id, "redirect_uri": redirect_uri, "response_type": "code",
    "scope": SCOPES, "access_type": "offline", "prompt": "consent",
    "code_challenge": challenge, "code_challenge_method": "S256", "state": state,
}
print("OPEN THIS URL:\n" + "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode(params), flush=True)

result = {}
done = threading.Event()

class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        if q.get("state", [""])[0] == state and "code" in q:
            result["code"] = q["code"][0]
            msg = b"Authorized. You can close this tab and return to chat."
        else:
            result["error"] = q.get("error", ["bad state or no code"])[0]
            msg = b"Authorization failed. Return to chat."
        self.send_response(200); self.send_header("Content-Type", "text/plain"); self.end_headers()
        self.wfile.write(msg); done.set()
    def log_message(self, *a): pass

srv = http.server.HTTPServer(("127.0.0.1", port), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()
print(f"Listening on {redirect_uri} (10 min timeout)...", flush=True)
if not done.wait(600):
    print("TIMEOUT waiting for authorization"); sys.exit(1)
srv.shutdown()
if "code" not in result:
    print("AUTH ERROR:", result.get("error")); sys.exit(1)

# Build body by hand: sentinels must not be re-encoded.
body = "&".join([
    "client_id=" + os.environ["GOOGLE_OAUTH_CLIENT_ID"],
    "client_secret=" + os.environ["GOOGLE_OAUTH_CLIENT_SECRET"],
    "code=" + urllib.parse.quote(result["code"], safe=""),
    "code_verifier=" + verifier,
    "redirect_uri=" + urllib.parse.quote(redirect_uri, safe=""),
    "grant_type=authorization_code",
]).encode()
req = urllib.request.Request("https://oauth2.googleapis.com/token", data=body,
                             headers={"Content-Type": "application/x-www-form-urlencoded"})
try:
    tok = json.load(urllib.request.urlopen(req, timeout=30))
except urllib.error.HTTPError as e:
    print("TOKEN EXCHANGE FAILED:", e.code, e.read().decode()[:300]); sys.exit(1)

rt = tok.get("refresh_token")
print("scopes granted:", tok.get("scope"))
if not rt:
    print("No refresh_token returned."); sys.exit(1)
subprocess.run(
    ["openclaw", "secrets", "store", "set", "GOOGLE_OAUTH_REFRESH_TOKEN", "--kind", "secret",
     "--allow-host", "oauth2.googleapis.com", "--allow-host", "www.googleapis.com",
     "--allow-host", "youtube.googleapis.com", "--value-file", "-"],
    input=rt.encode(), check=True)
print("Refresh token stored as GOOGLE_OAUTH_REFRESH_TOKEN (value not shown).")
