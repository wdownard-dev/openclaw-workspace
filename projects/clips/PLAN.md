# Clips Project Plan: Shorts from streamers + GTA 6 launch

Goal: automated YouTube Shorts from permitted streamer clips (plus original Higgsfield content). GTA 6 launches **Nov 19, 2026** (preload Nov 12). Console only, no PC date. It has slipped twice, so keep the plan resilient to a delay.

Rules (decided with William, 2026-10-21):
- Only clip streamers who have given permission. No Content ID evasion tricks (mirroring, speed shifts, etc.).
- No licensed movie footage. Movies = trailers, own commentary, or original Higgsfield-generated scenes.
- Human approval (via Telegram) before every upload.
- Skip the Slots category (gambling, ad-unfriendly).

Interest areas: top 20 Twitch categories, GTA 6 launch. Focus: Twitch clipping only. (2026-10-21: Pokemon vending and POV tracks scratched for now.)
Goal: MONETIZATION (decided 2026-10-21). Higgsfield: deferred, no confirmed public API; maybe later for original intros/B-roll by hand.
Channel: sticks&bones (UC4BoAATq5PywoIYfClpJDVw), confirmed by William.

## Open questions
- [x] POV streamers: was only a spitballed idea, not a defined track. Revisit after launch window.
- [x] Monetization or growth first? -> Monetization
- [x] YouTube channel + Google Cloud project exist? -> yes (sticks&bones, project morpheus-clips)
- [x] Higgsfield plan: API access or web only? -> deferred, not needed now
- [ ] Rockstar content policy: what is allowed for monetized gameplay?
- [ ] Spoiler policy for captions/thumbnails

## Phase 1: Setup (Oct 21 - Oct 27)
- [x] Get Twitch developer credentials (store in secrets, never in chat)
- [x] Pull live top-25 categories via Twitch API (done 2026-10-21; works in shell via egress proxy sentinels)
- [x] Create/confirm YouTube channel (done 2026-10-21)
- [ ] Create Google Cloud project, enable YouTube Data API, request API audit (uploads stay private until it passes). DONE: project morpheus-clips, OAuth client, OAuth authorization (refresh token stored as GOOGLE_OAUTH_REFRESH_TOKEN, scopes youtube.upload + youtube.readonly). TO DO: confirm YouTube Data API v3 is enabled, verify token with a channels.list call (needs a fresh turn), switch OAuth app Testing -> In production, submit API audit form.
- [ ] Read Rockstar's content policy; note what it allows

## Phase 2: Permissions + pipeline build (Oct 28 - Nov 5)
- [ ] Shortlist 30-50 streamers (priority: large GTA V / RP streamers likely to move to GTA 6; plus Pokemon vending and POV picks). STARTED: 22 English GTA V candidates in `permissions.md` (2026-10-21), still need policy/contact research + Pokemon vending picks.
- [ ] Write outreach message + permission template
- [ ] Send outreach; track replies in `projects/clips/permissions.md`
- [ ] Build pipeline: detect moments, cut to 9:16, captions + hook
- [ ] Set up Telegram approval flow for previews

## Phase 3: Dry run (Nov 5 - Nov 12)
- [ ] Dry-run pipeline end to end on GTA V clips from permitted streamers
- [ ] Test upload (private) once API access is approved
- [ ] Confirm posting schedule and daily volume
- [ ] Preload week (Nov 12): final checks

## Phase 4: Launch window (Nov 19 - Nov 22)
- [ ] Detect clip-worthy moments, approve fast, post several Shorts per day
- [ ] Watch for spoilers; follow spoiler policy
- [ ] Log what was posted and early performance

## Phase 5: After launch
- [ ] Review which clips performed
- [ ] Expand to other games from the top 20
- [ ] Add Pokemon vending / POV tracks

## Log
- 2026-10-21: ffmpeg 7.0.2 static installed at ~/openclaw-sites/bin/ffmpeg (no sudo; python3-venv missing on host). upload.py TESTED end to end: private test video https://youtu.be/usrztp6lMq8 on channel sticks&bones (William confirmed keep that channel). Token + upload path work. Remaining for audit: screencast (unlisted) if Google asks; watch inbox for Google reply.
- 2026-10-21: YouTube API Services audit form SUBMITTED (confirmation page seen). Public pages live at https://wdownard-dev.github.io/morpheus-clips/ (+ /privacy.html). Diagrams in projects/clips/audit/. upload.py written but NOT yet tested; screencast not yet recorded (Google may ask for it). Watch William's inbox for Google's reply. Open: which channel the token is bound to (sticks&bones, 7 videos) vs intended; ffmpeg not installed (plan: bundled static binary, no sudo).
- 2026-10-21: Google OAuth client (Desktop app, project morpheus-clips) stored as GOOGLE_OAUTH_CLIENT_ID / GOOGLE_OAUTH_CLIENT_SECRET (hosts: accounts.google.com, oauth2.googleapis.com, www.googleapis.com, youtube.googleapis.com). STILL TO DO: one-time user authorization to get a refresh token (scope youtube.upload), store it as GOOGLE_OAUTH_REFRESH_TOKEN; switch OAuth app from Testing to In production before launch (Testing tokens expire in 7 days); submit YouTube API compliance audit form.
- 2026-10-21: Twitch Client ID/Secret stored (TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET, hosts api.twitch.tv + id.twitch.tv). Shell couldn't see them because secrets.egressProxy was off. Enabling it + Gateway restart. NEXT: after restart, in a fresh turn, get app token via id.twitch.tv/oauth2/token (client_credentials), pull helix/games/top?first=25, then tick the Twitch items in Phase 1.
- 2026-10-21: Plan created. Backups run daily via `scripts/backup.sh` (GitHub: wdownard-dev/openclaw-workspace).
