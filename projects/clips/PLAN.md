# Clips Project Plan: Shorts from streamers + GTA 6 launch

Goal: automated YouTube Shorts from permitted streamer clips (plus original Higgsfield content). GTA 6 launches **Nov 19, 2026** (preload Nov 12). Console only, no PC date. It has slipped twice, so keep the plan resilient to a delay.

Rules (decided with William, 2026-10-21):
- Only clip streamers who have given permission. No Content ID evasion tricks (mirroring, speed shifts, etc.).
- No licensed movie footage. Movies = trailers, own commentary, or original Higgsfield-generated scenes.
- Human approval (via Telegram) before every upload.
- Skip the Slots category (gambling, ad-unfriendly).

Interest areas: top 20 Twitch categories, GTA 6 launch, Pokemon vending clips, POV streamers (IRL walk-around vs first-person gameplay: still to decide).

## Open questions
- [x] POV streamers: was only a spitballed idea, not a defined track. Revisit after launch window.
- [ ] Monetization or growth first?
- [ ] YouTube channel + Google Cloud project exist?
- [ ] Higgsfield plan: API access or web only?
- [ ] Rockstar content policy: what is allowed for monetized gameplay?
- [ ] Spoiler policy for captions/thumbnails

## Phase 1: Setup (Oct 21 - Oct 27)
- [x] Get Twitch developer credentials (store in secrets, never in chat)
- [x] Pull live top-25 categories via Twitch API (done 2026-10-21; works in shell via egress proxy sentinels)
- [ ] Create/confirm YouTube channel
- [ ] Create Google Cloud project, enable YouTube Data API, request API audit (uploads stay private until it passes)
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
- 2026-10-21: Twitch Client ID/Secret stored (TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET, hosts api.twitch.tv + id.twitch.tv). Shell couldn't see them because secrets.egressProxy was off. Enabling it + Gateway restart. NEXT: after restart, in a fresh turn, get app token via id.twitch.tv/oauth2/token (client_credentials), pull helix/games/top?first=25, then tick the Twitch items in Phase 1.
- 2026-10-21: Plan created. Backups run daily via `scripts/backup.sh` (GitHub: wdownard-dev/openclaw-workspace).
