# USER.md - User Model

Store stable user preferences and profile facts as directives that can guide future sessions.

Use one directive per entry:

```md
<!-- observed: YYYY-MM-DD | status: active -->

- Prefer concise progress updates during implementation work.
```

- Begin each directive with an imperative such as `Always`, `Never`, or `Prefer`.
- Record the observation date and either `active` or `superseded` on the metadata line.
- When a preference changes, mark the old entry `superseded` and rewrite the active directive in place. Never append a contradictory active directive.
- Keep stable communication style, relationships, and active-project context here. Put durable non-profile facts and decisions in `MEMORY.md`.
- Save this file at the workspace root as `USER.md`. It loads every session with a separate 4,000-character budget.

## Directives

<!-- observed: 2026-10-23 | status: active -->

- Always treat William's data-over-short-term-money stance as the default for the clips project: prefer clean experiments and measured evidence over volume.

<!-- observed: 2026-10-23 | status: active -->

- Approve the clips myself (Morpheus) after Editor creates them, using the review gate in `projects/clips/pipeline/clip_job.py` (`--approve`); never send William a per-clip approval request. Send him only a summary of what was posted and where (clip, platform, time, link when live). Escalate only for: a new campaign to join, a rule conflict, anything touching money, accounts or legal terms, a streamer who has not approved, or a clip I rejected twice.

<!-- observed: 2026-10-23 | status: active -->

- Never post to Vyro, YouTube or any platform outside the Buffer TikTok and Instagram route without William's explicit go; the approval delegation covers campaign-supplied footage only, and only the platforms already connected.

<!-- observed: 2026-10-23 | status: active -->

- Own the "go" for starting clip work (Editor jobs, rendering, scheduling) on campaigns William has already joined: do not wait for his go on routine clip batches. Same limits as the approval delegation (campaign-supplied footage, Buffer TikTok and Instagram only); the go does not cover joining new campaigns, YouTube, Vyro submissions, money, accounts or legal terms. Delegated 2026-10-23 ("The 'go' is now your responsibility").

<!-- observed: 2026-10-23 | status: active -->

- Submit each live TikTok and Instagram post to its Vyro campaign as soon as it goes live ("Submit when they go live for tiktok and instagram", 2026-10-23), using only the Submit post form with "Use a link instead"; one submission per post, never twice. Scope: posts made through the Buffer route for campaigns William has joined (MW4, Total Drama Roblox). Still excluded: Join, payouts, connect/cash out/settings, YouTube posts beyond the earlier MW4 OK, anything money/account/legal. Stop and tell William on any unexpected prompt; if Vyro shows a "wait before posting again" or pending-limit dialog, stop, log it, and retry later (do not work around it).

<!-- observed: 2026-10-22 | status: active -->

- Always send any video preview he does ask for as a file (forceDocument on Telegram), because in-chat Telegram video looks stretched on his phone.

<!-- observed: 2026-10-22 | status: active -->

- Prefer to automate everything except steps that need his legal acceptance or manual posting; keep him out of the loop on routine runs and report outcomes honestly, including what failed.

<!-- observed: 2026-10-23 | status: active -->

- Join Vyro campaigns for William only through the per-campaign accept flow in `projects/clips/JOIN-PROCEDURE.md`: send him the campaign terms and a flag list on Telegram, and click Join only after his explicit written "Accept <campaign name>" for that campaign. Never treat silence, "ok", "sure" or an older accept as consent; never accept anything the package did not show him; stop on any payment, identity, payout or unexpected terms prompt.

## Related

- [Agent workspace](/concepts/agent-workspace)
