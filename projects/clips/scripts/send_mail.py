#!/usr/bin/env python3
"""Send one plain-text email from the authorizing Gmail account (gmail.send scope).

Usage: send_mail.py --to ADDR --subject "..." --body-file PATH [--dry-run]

Credentials come from the environment (GMAIL_OAUTH_CLIENT_ID / _CLIENT_SECRET / _REFRESH_TOKEN),
which under the OpenClaw egress proxy are sentinels replaced on the wire. Prints the Gmail
message id and thread id on success so replies can be tracked.
--dry-run prints the message and exits without sending.
"""
import argparse, base64, json, os, sys, urllib.error, urllib.request
from email.message import EmailMessage


def call(req):
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read().decode(errors='replace')[:400]}")


def access_token():
    body = "&".join([
        "client_id=" + os.environ["GMAIL_OAUTH_CLIENT_ID"],
        "client_secret=" + os.environ["GMAIL_OAUTH_CLIENT_SECRET"],
        "refresh_token=" + os.environ["GMAIL_OAUTH_REFRESH_TOKEN"],
        "grant_type=refresh_token",
    ]).encode()
    tok = call(urllib.request.Request("https://oauth2.googleapis.com/token", data=body,
               headers={"Content-Type": "application/x-www-form-urlencoded"})).get("access_token")
    if not tok:
        sys.exit("Could not refresh access token.")
    return tok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--to", required=True)
    ap.add_argument("--subject", required=True)
    ap.add_argument("--body-file", required=True)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    msg = EmailMessage()
    msg["To"] = a.to
    msg["Subject"] = a.subject
    msg.set_content(open(a.body_file, encoding="utf-8").read())

    if a.dry_run:
        print(msg.as_string())
        return
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    req = urllib.request.Request(
        "https://gmail.googleapis.com/gmail/v1/users/me/messages/send",
        data=json.dumps({"raw": raw}).encode(), method="POST",
        headers={"Authorization": "Bearer " + access_token(), "Content-Type": "application/json"})
    res = call(req)
    print(f"SENT to {a.to} | message id {res['id']} | thread id {res['threadId']}")


if __name__ == "__main__":
    main()
