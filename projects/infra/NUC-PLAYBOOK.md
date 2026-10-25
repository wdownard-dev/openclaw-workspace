# Playbook: NUC as always-on Gateway, laptop and future machines as nodes

Written 2026-10-23. Commands come from the OpenClaw 2026.10.5 docs (install/migrating, gateway/index, gateway/pairing, gateway/tailscale, cli/node, nodes/*). Items marked UNVERIFIED have not been tested on this setup.

## 0. Target architecture

```
             Telegram / Control UI / phone
                        |
                [ NUC = GATEWAY ]  always on, hardwired
   agents, sessions, memory, secrets, automations, Telegram bot
        |  Tailscale (private, works while travelling)
   ------------------------------------------------------
   |                 |                    |              |
 laptop node     (future) render      (future) TikTok  (future) IG / YouTube
 screen, browser   node, heavy ffmpeg   node            nodes
```

Rules that never change:
- One Gateway only. Nodes are peripherals; there is no failover Gateway.
- Never run two Gateways against the same Telegram bot or the same state.
- State lives on the NUC (`~/.openclaw`). The laptop holds no source of truth after cutover.

## 1. Current state (inventory, 2026-10-23)

| Item | Here (laptop, host `pop-os`) |
|---|---|
| OpenClaw | 2026.10.5, systemd user service `openclaw-gateway` |
| State | `~/.openclaw` 1.2 GB (config, auth, sessions, automations, browser profile) |
| Workspace | `~/.openclaw/workspace`, `workspace-editor`, `workspace-scout` |
| Heavy tools | `~/openclaw-sites` 15 GB: ffmpeg at `bin/`, whisper venv `clips-venv`, Chrome for Testing `browsers/`, footage in `clips-work/` |
| Model runtime | `claude-cli` (Claude Code at `~/.local/bin/claude`) |
| Gateway bind / auth | default loopback, token auth |
| Not installed | tailscale, ollama, ffmpeg on PATH |

Hard-coded paths: many scripts use `/home/williamdownard/...`. Use the same Linux username on the NUC: `williamdownard`.

## 2. Phase A: prepare the NUC (no risk to the live system)

1. Install Linux (same distro family as this laptop if possible), user `williamdownard`, hardwire to the router, DHCP reservation or static IP.
2. Never sleep: `sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target`. In BIOS set "power on after AC loss".
3. `sudo apt install openssh-server`; test SSH from the laptop. Enable the firewall (`ufw allow ssh`; Tailscale needs nothing inbound).
4. Install Tailscale on the NUC and the laptop (`curl -fsSL https://tailscale.com/install.sh | sh`, then `sudo tailscale up`). Both join the same tailnet. Note the NUC's tailnet name.
5. Install OpenClaw without onboarding: `curl -fsSL https://openclaw.ai/install.sh | bash -s -- --no-onboard`. Confirm `openclaw --version` shows 2026.10.5 (match the laptop; update the laptop first if they differ).
6. Install Claude Code CLI on the NUC and sign in to the same account. Test: `claude -p "say ok"`.
7. Install the heavy tools. Copy or rebuild:
   - ffmpeg: copy `~/openclaw-sites/bin/ffmpeg` (static) to the same path.
   - whisper venv: rebuild (`python3 -m venv`; needs `python3-venv`, which this laptop lacked, so check) then reinstall faster-whisper; re-download the model.
   - Chrome for Testing: copy `~/openclaw-sites/browsers/` (or re-run the Playwright install used on 2026-10-22).
   - Footage in `clips-work/`: skip it. Re-download with `scripts/fetch_frameio.py`; only copy what you need.
8. Do NOT start the NUC Gateway yet.

## 3. Phase B: cutover (30-60 minutes; pick a quiet window)

Pre-check: no Buffer post due within 2 h is not required (Buffer publishes on its own), but avoid the window when the Vyro submit job has work. Currently the Vyro queue is paused.

1. On the laptop: tell Morpheus to pause automations that drive the browser, or accept a short gap.
2. Stop and snapshot:
   ```bash
   openclaw gateway stop
   mkdir -p ~/Backups/openclaw
   openclaw backup create --output ~/Backups/openclaw --verify
   ```
   Also copy anything outside `~/.openclaw` that the pipeline needs: `~/openclaw-sites/clips-work/campaigns/*/source*.json` (transcripts) and `~/.config/systemd/user/` is not needed.
3. Disable the laptop Gateway so it cannot return: `systemctl --user disable openclaw-gateway`. Keep it stopped.
4. Copy the archive to the NUC over Tailscale/SSH: `scp ~/Backups/openclaw/*.tar.gz williamdownard@<nuc>:~/`. Treat it as a secret (contains credentials); delete it from both machines after verification.
5. On the NUC: `openclaw backup restore <archive> --target ~/openclaw-restored`, then with the Gateway stopped move the state and workspace assets to their recorded destinations per `manifest.json` (mapping is in the restore output). Confirm ownership: `chown -R williamdownard:williamdownard ~/.openclaw`.
6. Reinstall plugin `node_modules` if doctor asks. Run:
   ```bash
   openclaw doctor
   openclaw gateway install      # creates the systemd user service
   sudo loginctl enable-linger $(whoami)
   openclaw gateway restart
   openclaw status
   ```
7. Check the telegram token is present without printing it: `awk -F= '/^(TELEGRAM_BOT_TOKEN)=/ { print $1 "=present" }' ~/.openclaw/.env` (only if the bot uses the env fallback).
8. Network exposure so nodes can join from anywhere (pick one, A recommended):
   - A: keep `gateway.bind: "loopback"` and use Tailscale Serve (`gateway.tailscale.mode: "serve"`), reachable at the NUC's tailnet HTTPS URL.
   - B: `gateway.bind: "tailnet"` with token auth. Do not use a public bind or Funnel.
   Keep token auth; set `gateway.auth.mode` explicitly. Doc: gateway/tailscale.md.
9. Verification checklist (all must pass before you call it done):
   - [ ] `openclaw status` healthy; `systemctl --user status openclaw-gateway` active.
   - [ ] Reboot the NUC; the Gateway comes back by itself (linger works).
   - [ ] Send me a Telegram message; I answer from the NUC.
   - [ ] `automations list` shows all 9 jobs with next-run times (tracker, digest, scout, watcher, etc).
   - [ ] Memory and sessions present; `projects/clips` files present; `git status` clean-ish.
   - [ ] Run `python3 -I projects/clips/scripts/sync_buffer.py --report` (secrets work).
   - [ ] Run `python3 -I projects/clips/scripts/check_vyro_mail.py` (Gmail works).
   - [ ] Browser: open https://app.vyro.com/campaigns/add-clips with the OpenClaw browser; confirm still signed in. If Vyro asks for a code, I can read it from Gmail.
   - [ ] A full dry run: `python3 -I projects/clips/pipeline/clip_job.py specs/example.json --dry-run`.
   - [ ] Pause 30 minutes, then confirm one scheduled automation fired (the 3-hourly tracker).
10. Rollback (if anything fails): stop the NUC Gateway, `systemctl --user enable --now openclaw-gateway` on the laptop. The laptop state is untouched until you delete it. Do not delete the laptop's `~/.openclaw` for at least a week.

## 4. Phase C: laptop as a node

1. In the Control UI (reach it via the NUC's tailnet URL): Devices > pairing dialog > Node host. Copy the one-paste command.
2. On the laptop, install the node host as a service so it reconnects after wake:
   ```bash
   openclaw node install --host <nuc-tailnet-name> --port 18789
   ```
   or the one-paste foreground form: `openclaw node run --pair "oc-pair://<setup-code>"` (link is single-use, 10 min). Do the pairing over Tailscale, not public internet.
3. Approve: `openclaw devices list`, then `openclaw devices approve <requestId>`.
4. Set the allowlist before use (local exec approvals default to full with ask off, which is too broad): `openclaw approvals allowlist add --node <laptop> "<absolute path>"`. Start with ffmpeg and the whisper venv python only.
5. Verify from the NUC: `openclaw nodes status`; run a harmless `exec` with `host=node node=<laptop>` such as `uname -a`.
6. Behavior to expect: when the laptop sleeps or leaves the network the node disconnects; the Gateway and automations keep running. Anything that needs the laptop (its screen) simply fails for that call.
7. Laptop-only extras worth keeping: its screen/browser as a second browser node, notifications, and as a place for local previews.

## 5. Phase D: future machines

Add any machine the same way (Section 4). Per role:

| Role | Purpose | Notes |
|---|---|---|
| Render node | ffmpeg, whisper transcription, footage downloads | Point `tools.exec.host=node`, `tools.exec.node=<name>` only for render jobs (or per call with `host=node`). The pipeline reads and writes local paths, so run a whole clip job on one machine; a shared disk (NFS/Syncthing) is needed to split steps. UNVERIFIED. |
| Local-model node | Ollama for cheap screening (transcript triage, hook drafts) | `node_inference` tool; install Ollama on that node. Keep any final judgment on Claude. |
| Browser node | Vyro, analytics, platform dashboards | Isolated signed-in sessions. Browser proxy is zero-config on a node (cli/node.md). |
| Session-host node | Run Editor/Scout sessions on that CPU | Set `nodeHost.workerRuns.enabled`; only on machines you fully control. Test with one Editor job before relying on it. UNVERIFIED. |

## 6. One machine per channel (TikTok, Instagram, YouTube)

Be clear on what this buys, because posting does not need it today:
- Posts go out through Buffer's API from the Gateway. No machine posts anything. A per-channel machine is only useful for an isolated, signed-in browser session per platform (checking analytics, a platform's own app for settings like the paid-partnership label), or for approaching a platform with no API route (YouTube uploads are blocked until the API audit passes).
- If you build it: name them `tiktok-node`, `instagram-node`, `youtube-node`; give each its own browser profile and the matching platform login; allowlist only the commands needed; no shared credentials between nodes.
- Limits and rules to respect: use only accounts that are yours, one account per platform per channel as today (rvclips6 on TikTok and Instagram, a separate YouTube channel). Do not use separate machines or networks to make multiple accounts look unrelated, or to get around platform or Vyro limits (Vyro's rules already flag automation, bots and scrapers; the open support question is unsent). That would risk the accounts and the earnings.
- Recommendation: do not buy more hardware for this yet. First measure whether anything is actually slow or blocked. The two real needs right now are 24/7 uptime (the NUC) and Vyro approval.

## 7. Operations after cutover

- Backups: the daily 3 AM workspace backup pushes to GitHub (workspace only). Add a state backup: `openclaw backup create --output ~/Backups/openclaw --verify` weekly on the NUC, copied off-machine and encrypted. Never copy live `.sqlite` files by hand.
- Updates: update the NUC first, then nodes (version skew order in nodes/pairing-and-status.md). Update the Gateway only through OpenClaw's own update path.
- Power: put the NUC on a small UPS if you can. Router reboot: the Gateway reconnects on its own.
- Monitoring: the 8:15 AM digest is the heartbeat. If you get no digest, the NUC or its network is down; check Tailscale and SSH first.
- Security: token auth stays on; Tailscale ACLs let only your devices reach the NUC; keep the NUC's SSH key-only.

## 8. Open items before starting

- NUC specs (RAM, disk) and chosen Linux distro; same username `williamdownard`.
- Confirm Claude Code CLI can sign in on a headless box (browser step may need your laptop).
- Whether the Vyro session survives a new IP and fingerprint (test in the Phase B checklist).
- Buffer cap: 8 of 10 scheduled posts per channel, plan or cadence change needed for more.

## Progress log
- 2026-10-24 ~12:00 PM ET: Phase A in progress. NUC = Pop!_OS 24.04, 12 cores, 23 GB RAM, 426 GB free, Tailscale 100.79.228.2, hostname pop-os (same as laptop; rename later), key SSH from laptop works, sleep masked. Installed: Node 24.22.1, OpenClaw 2026.10.7 (laptop is 2026.10.5; fine, doctor migrates), Claude Code 2.1.310. Copied ffmpeg, whisper models, Chrome for Testing; rebuilt clips-venv (pinned av==17.1.0 as on laptop; unpinned av 19 breaks faster-whisper). Tested on NUC: whisper (23 s clip in 1.6 s), Chrome headless. STILL TO DO: NUC on Ethernet (currently Wi-Fi), Claude Code login, remaining Phase A checks, then Phase B cutover. No Gateway started on the NUC.

- 2026-10-24 ~11:25 AM ET: NUC on Ethernet (enp112s0 192.168.1.112), hostname nuc, Claude Code logged in. Rehearsal backup (975 MB, verified, 42 s) restored to staging on NUC OK (nothing activated). Wrote nuc-cutover.sh (--preflight / --go / --rollback): run from a laptop terminal, NOT via the agent, because stopping the Gateway ends the agent session. Preflight currently fails only on: NUC linger (needs `sudo loginctl enable-linger williamdownard` on NUC) and the 14 GB footage rsync still running (managed job).

- 2026-10-24 ~12:50 PM ET: CUTOVER DONE; NUC is the Gateway (hostname nuc, OpenClaw 2026.10.7), running as the systemd user service (swapped from a hand-started terminal process at 12:38). Tailscale Serve enabled (gateway.tailscale.mode=serve, bind loopback): https://nuc.tail3d34d7.ts.net. Needed one-time Serve consent in the Tailscale admin console and the Tailscale operator set to williamdownard; a restart before that caused a crash loop 12:21-12:24 (systemd gave up after 10 fast restarts). Lesson: restart the Gateway only after Serve consent and operator are in place; never loop restarts. Laptop paired as node `pop-os` (100.122.185.55, 2026.10.7). Node exec policy set to security=allowlist, ask=off, askFallback=deny with allowlist ffmpeg, clips-venv python, /usr/bin/uname. Result: allowlist enforced (/usr/bin/id denied), but node refuses ffmpeg and python ("cannot safely bind this interpreter/runtime command"), so the laptop is a browser/screen node only; rendering stays on the NUC. William chose to leave it that way (option 1). Open: laptop's old ~/.openclaw and archives kept a week then delete (~/Backups/openclaw on laptop; ~/cutover-*.tar.gz, ~/openclaw-restored-* on NUC); router DHCP reservation for 192.168.1.112; NUC BIOS power-on after AC loss.
