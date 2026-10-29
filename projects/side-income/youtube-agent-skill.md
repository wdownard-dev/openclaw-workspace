# YouTube agent skill: research and fit assessment

Date: 2026-10-29. Research only. Nothing was installed into the workspace and no code from the repo was run.

## 1. Finding the repo

**Found:** `https://github.com/Jakeschincariol/youtube-agent-skill` (MIT, owner Jake Schincariol). Its one-line description matches the TikTok caption word for word ("Eleven Claude skills that run a YouTube channel: scripts off 21 hook formulas...").

**Not confirmed:** that this is the repo behind @johann_andre's "link in bio". The TikTok profile page and video page return only a shell title through `web_fetch`, and yt-dlp metadata has no bio or link field. The creator has no GitHub account under that name. Ask William to check the bio link before trusting it. If the link points to one of the copies listed in section 4, do not use it.

**Routes tried:**
- `web_fetch` on the TikTok profile, short link and GitHub HTML search: worked, but the TikTok pages render no content and the GitHub HTML gave no repo links.
- `yt-dlp --skip-download --dump-json` on the video: worked. It gave the caption, uploader and upload date (2026-10-19), but no bio.
- GitHub REST search API (`api.github.com/search/repositories`): worked and was the route that found the repo.
- `raw.githubusercontent.com`: used to download the README, manifests, SKILL.md files and Python tools into `/tmp/ytskill-src` for reading only.
- Google/Bing search: not attempted.
- No signup, email entry or opt-in funnel was touched.

## 2. What the pack contains

Repo: one commit (2026-09-16), no releases, 3,592 stars, 1,134 forks, 85 open issues. Most open issues are non-substantive (random text, YouTube URLs). Licence MIT, copyright Jake Schincariol. The owner account dates from 2025-01 and has 22 repos.

| Command | What it does | Needs | Code |
|---|---|---|---|
| `/yt-script` | Five hooks from 21 formulas, scored | none | `hookscore.py` (local heuristic) |
| `/yt-package` | Title + thumbnail linted as one pair | none | `title.py` (local) |
| `/yt-edit` | Transcript to edit decision list (dead air, filler, retakes) | transcript (whisper or captions) | `deadair.py` (local) |
| `/yt-comment` | Triage and draft comment replies | pasted comments | prompt only |
| `/yt-plan` | Weekly upload plan | owner's hours | prompt only |
| `/yt-viral` | Ranks videos by multiple of own channel median | user-collected JSON (README suggests yt-dlp) | `swipe.py` (local) |
| `/yt-retention` | Reads Studio retention CSV, finds cliffs | owner's Studio export | `retention.py` (local) |
| `/yt-shorts` | Finds Shorts inside long videos | transcript | prompt only |
| `/yt-seo` | Description, tags, query test | none | prompt only |
| `/yt-chapters` | Chapters validated against YouTube rules | transcript | `chapters.py` (local) |
| `/yt-audit` | Whole-channel audit ending in one fix | pasted channel info | prompt only |

Cost: $0 for the pack and no API keys. Model usage is the only cost. Voice profile lives at `~/.claude/youtube/voice.md`.

**Virality code (`swipe.py`, read in full):** reads a JSON list of `{channel, title, views, url, duration}`, computes each video's views divided by its channel's median, drops channels with fewer than 4 videos, and labels each title with the best-matching formula from `hooks.json` by regex. It makes no network calls and uses only the standard library. The title labelling is a judgement about words, not a cause. Data collection is outside the tool.

**Safety scan:** `grep` across all Python tools found no network, subprocess, eval/exec or file-write calls. Only `swipe.py` was read in full; the other five were scanned by pattern. Nothing in the pack posts, uploads or logs in. The SKILL.md files are prompts that end each run with "ship it, or change it?". The prompts reference Claude Code paths (`~/.claude/...`) and the Claude plugin manifest; they would need path changes for OpenClaw.

## 3. Fit

- **YouTube clipping (current project):** weak to moderate. The pack targets long-form creators: scripts, retention exports, chapters, SEO. The only piece that maps to clip selection is `/yt-shorts` (prompt) plus `swipe.py`'s outlier ranking, which could rank candidate source videos for Scout's research. Campaign footage and rules are not covered.
- **TikTok focus (current):** `swipe.py` is platform-neutral, since any JSON list works. `hookscore.py` was calibrated on YouTube auto-captions, so its scores would need re-checking on TikTok.
- **Compared with generic advice:** the value is in the small, deterministic scripts. The prompts are standard YouTube advice.
- **Data-collection risk:** the virality route depends on `yt-dlp` scraping public YouTube listings. That is a Terms-of-Service grey area for a monetised channel. The YouTube Data API is the safer input source.

## 4. Risks and red flags

- **Copies:** at least seven repos carry the same description, created 2026-10-11 to 2026-10-29 under unrelated accounts (for example `AbdullahMalik17`, `02siteIQ`, `arzikaa604-droid/youtube-agent`, `mpromp893-hue/Ol-mekie-`, `aarushrpatel`). Several list GPL-3.0, Apache-2.0 or no licence, and their code was not read. Treat them as unvetted.
- **Stars versus activity:** 3.6k stars and 1.1k forks on a single commit six weeks old is an unusual pattern. I could not judge whether the stars are organic.
- **Maintenance:** no commits since 2026-09-16 and no releases. Open PR #91 (Spanish title support) is unmerged.
- **No code execution in the skills themselves.** The Python tools are small and offline.

## 5. Alternatives (MIT unless noted; only the README was read)

- `rediumvex/viral-hooks-skill`: 113 stars, last push 2026-05-05. Hook formulas for short-form (TikTok, Reels, Shorts). Prompt-only. Closest to the TikTok focus.
- `meshcode-ai/skills-video`: 0 stars, GitHub licence NOASSERTION (README says MIT). Shorts clipping, 9:16 reframing and captions. Most relevant to clipping, but the README excludes its scripts and dependencies, so it is criteria only.
- `Virlo-AI/Virlo-Agent-Plugin`: 3 stars, pushed 2026-10-27. TikTok and Shorts trend and outlier analysis through a hosted MCP (65 tools). Needs a Virlo account. Pricing is on the vendor site and was not checked.
- `adityaarsharma/youtube-marketing-skills`: 72 stars. Needs Google Cloud OAuth and YouTube Data and Analytics APIs. It writes SEO back to YouTube and publishes WordPress posts. That conflicts with a read-only stance unless its write features are removed.

## 6. Verdict

The pack is free, MIT and small, and its only non-trivial code is `swipe.py`'s channel-median outlier ranking. It does not post, but its virality route depends on scraping public listings, the repo has an odd star pattern with many copies in circulation, and it targets long-form YouTube rather than clipping or TikTok. Do not install the full pack. When YouTube returns to focus, consider taking the outlier logic and `hooks.json` (MIT) into a workspace-owned skill after reading them again, with a compliant data source.

## 7. Smallest $0 trial (when YouTube is back in focus)

1. Confirm the bio link points to `Jakeschincariol/youtube-agent-skill`. Record the commit SHA of `main` (currently the 2026-09-16 commit).
2. Make a new empty directory under `/tmp`. Download only `skills/yt-viral/swipe.py` and `skills/yt-script/hooks.json` from that SHA. Do not install or copy into the workspace.
3. Build `collected.json` from 4 public channels in one niche with at least 4 videos each, using the YouTube Data API free quota. Do not use yt-dlp.
4. Run `python3 -I swipe.py collected.json --min 2.0` with networking disabled (for example `unshare -n`).
5. **Pass:** runs offline; for two outliers, hand-computed views ÷ channel median matches the tool to 0.01; at least four of the top five formula labels fit their titles; channels with under 4 videos are skipped.
6. **Fail:** any arithmetic mismatch, a network call, or code that differs from the recorded SHA.

## Checks and limits

- Read in full: README, LICENSE, plugin.json, all SKILL.md files, `swipe.py`.
- Pattern-scanned only: `hookscore.py`, `title.py`, `deadair.py`, `chapters.py`, `retention.py`.
- Not checked: the TikTok bio link, copies' code, Virlo pricing, and whether William's TikTok account has any link to the repo.
