#!/usr/bin/env python3
"""iCloud mail helper for the job search (william.downard@me.com).
Credential: ~/.openclaw/credentials/icloud-mail.secret (never printed).
  python3 -I mail.py recent [N] [--unseen]     list newest N message headers (default 15)
  python3 -I mail.py show UID                  print one message's text
  python3 -I mail.py send TO SUBJECT BODYFILE [ATTACHMENT ...]   send; only run after William approves the draft
"""
import imaplib, smtplib, os, sys, email, mimetypes
from email.header import decode_header, make_header
from email.message import EmailMessage

USER = "william.downard@me.com"
PW = open(os.path.expanduser("~/.openclaw/credentials/icloud-mail.secret")).read().strip()


def imap():
    m = imaplib.IMAP4_SSL("imap.mail.me.com", 993, timeout=30)
    m.login(USER, PW)
    m.select("INBOX", readonly=True)
    return m


def hdr(v):
    return str(make_header(decode_header(v or "")))


def recent(n=15, unseen=False):
    m = imap()
    _, d = m.uid("search", None, "UNSEEN" if unseen else "ALL")
    for uid in d[0].split()[-n:][::-1]:
        _, data = m.uid("fetch", uid, "(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])")
        msg = email.message_from_bytes(data[0][1])
        print(uid.decode(), "|", hdr(msg["Date"])[:25], "|", hdr(msg["From"])[:50], "|", hdr(msg["Subject"])[:80])


def show(uid):
    m = imap()
    _, data = m.uid("fetch", uid, "(BODY.PEEK[])")
    msg = email.message_from_bytes(data[0][1])
    for k in ("From", "To", "Date", "Subject"):
        print(k + ":", hdr(msg[k]))
    print()
    for part in msg.walk():
        if part.get_content_type() == "text/plain":
            print(part.get_payload(decode=True).decode(part.get_content_charset() or "utf8", "replace"))
            return
    print("(no plain-text part)")


def send(to, subject, bodyfile, attachments):
    msg = EmailMessage()
    msg["From"], msg["To"], msg["Subject"] = USER, to, subject
    msg.set_content(open(bodyfile).read())
    for a in attachments:
        ctype = mimetypes.guess_type(a)[0] or "application/octet-stream"
        main, sub = ctype.split("/", 1)
        msg.add_attachment(open(a, "rb").read(), maintype=main, subtype=sub, filename=os.path.basename(a))
    s = smtplib.SMTP("smtp.mail.me.com", 587, timeout=30)
    s.starttls()
    s.login(USER, PW)
    s.send_message(msg)
    s.quit()
    print("sent to", to)


if __name__ == "__main__":
    c = sys.argv[1:]
    if c[0] == "recent":
        recent(int(c[1]) if len(c) > 1 and c[1].isdigit() else 15, "--unseen" in c)
    elif c[0] == "show":
        show(c[1])
    elif c[0] == "send":
        send(c[1], c[2], c[3], c[4:])
