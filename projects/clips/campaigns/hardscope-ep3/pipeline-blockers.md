# Pipeline blockers for HardScope Ep.3 (read from pipeline/clip_job.py, 2026-10-28)

Editor did NOT edit clip_job.py, format_short.py or permissions.md. Everything below is read from the code, plus what happened when I ran `--until thumbnail`.

## What works today (verified by running)
- `python3 -I pipeline/clip_job.py specs/hs3-0N.json --until thumbnail` passes lint, cuts, formats, verifies (1080x1920, audio, blackdetect) and writes thumbnail + contact sheets for hs3-01..04 (TikTok variant). Nothing external was touched.
- Campaign check: lint only requires `campaigns/<campaign>/brief.md` to exist for `"footage": "campaign-supplied"`. `brief.md` exists, so no registry or `permissions.md` edit is needed (permissions.md is only consulted for `{"streamer": ...}` footage).
- Hashtag lint: `required_tags: ["#unpacked"]` is compared against `#\w+` matches only. The `@hardscope` mention is not a hashtag, so lint neither requires nor blocks it. No "@" lint exists.

## Blockers for the FULL job (host -> schedule -> log). Local stages are unaffected.

1. **One video, one hook, one style per spec, but the campaign needs different posts per platform.** `clip_job.py` renders a single `<id>.mp4` from `hook`/`caption`/`style`, hosts it once, and posts the same file to TikTok and Instagram. Only the post text differs. Clip Farm's rule is that every post needs a new hook, CTA, caption and visual/pacing, so as-is both platforms would get the identical clip (same burned-in hook and caption, same cut).
   Minimal change: accept an optional `variants` (or `instagram_variant`) block in the spec with its own `start`, `end`, `hook`, `caption`, `style`; run cut/format/verify/thumbnail once per variant into `jobs/<id>/<platform>/`; keep `state["hosted"]` and the review `short_sha` per platform; have `schedule` use the platform's own URL. The spec files hs3-01..04 already carry `instagram_variant` (ignored today). The `--approve` overlap check must skip a spec's own variants.
   Workaround used: I rendered the Instagram variants from out-of-tree preview specs (`~/openclaw-sites/clips-work/campaigns/hardscope-ep3/ig-preview/hs3-0N-ig.json`, ids `hs3-0N-ig`) for review only. Do not schedule or host them. Cleanup if unwanted: `pipeline/jobs/hs3-0N-ig/` and `previews/*hs3-0N-ig*`.
   Do not make two real specs for one moment: `--approve` refuses when ranges overlap another spec from the same source.

2. **`schedule` is a required key, but there is no schedule yet.** `lint` errors with "spec missing 'schedule'". `"schedule": null` would crash (`.items()` on None). I used `"schedule": {}`, which passes lint. Danger: with `{}` the `host` stage still uploads to Cloudinary, then `schedule` and `log` silently do nothing, leaving a hosted file with no post.
   Minimal change: treat missing or empty `schedule` as "unscheduled" and stop before `host` with a clear message, or refuse to run `host` when `schedule` is empty.

3. **No `@mention` handling.** The brief requires `@hardscope` in every TikTok/Instagram caption. Nothing enforces it. Minimal change: a `required_mentions: ["@hardscope"]` spec field, linted like `required_tags` (each present exactly once, case-insensitive, no other `@` handles). I checked this by script in the spec generator only.

4. **No identical-caption or duplicate-hook check.** Lint never compares `tiktok_caption` with `instagram_caption`, nor hooks across variants or clips. Minimal change: normalise (strip tags/mentions, lowercase) and fail if the two captions match, or if the platform hooks match, or if a hook was already used by another spec for the same campaign.

5. **Buffer and mentions (unverified).** `createPost` sends `text` as a plain string. I did not call Buffer, so I cannot say whether `@hardscope` becomes a real mention on TikTok or Instagram or stays plain text. Minimal check: Morpheus schedules one clip and reads it in Buffer before the other three; if mentions do not link, post manually.

6. **`log` stage and tracking assume Vyro.** Notes hard-code "NOT submitted to Vyro", and the existing trackers are Vyro-based. This campaign is Whop/Clip Farm (post link submitted on Whop; support ticket with analytics recording after the minimum payout). Minimal change: a `submission` spec field (default "vyro") that sets the log note, plus a Whop views/earnings source for `results.csv`.

7. **Visual variation is thin.** `format_short.py` offers only three styles, which change fonts and colours. The layout (blurred fill with the sharp clip centered) is always the same. For "new visual/pacing" I varied the trim (start/end) and style per platform. Do not use speed changes or mirroring: those count as disguising footage. A cheap addition would be a second layout option (for example a tighter crop). Optional.

8. **Fixed Buffer channels.** `CHANNELS` are the MW4 TikTok/Instagram accounts. The brief does not require dedicated accounts, but William should confirm those accounts are meant for HardScope posts.

9. **Engagement-bait regex can false-positive.** `(like|comment|share|follow|subscribe)` followed by `this|below|now|if` in the same sentence fails lint. I avoided those words. Not a blocker; worth knowing when writing the CTA ("Full episode on @hardscope" is fine).

## Manual (unchanged)
Hook vs first 3 s check (done, see candidates.md), Morpheus review/approve, Whop submission, analytics screen recording after minimum payout.
