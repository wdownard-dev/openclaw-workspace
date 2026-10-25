# After nuc-cutover.sh --go (read this first when William says the cutover finished)

You (Morpheus) are now running on the NUC. Verify, in order; report one short summary to William.
1. `openclaw status`, `systemctl --user status openclaw-gateway`: healthy. `hostname` = nuc.
2. Automations: `automations list` shows all jobs (heartbeat, Vyro scout, digest, mail watcher, tracker, outreach monitor, YouTube audit watcher, backup, checklist) with sane next-run times. Jobs disabled on purpose: "Vyro submit live posts (hourly)" 768c132c (released by the mail watcher on a Vyro approval). One-shot "Check Scout Haiku scan" may have been due during the downtime: run its check by hand (scout-report.md dated 2026-10-24, What changed section).
3. Secrets/tools from the NUC: `python3 -I projects/clips/scripts/sync_buffer.py --report` (Buffer), `scripts/check_vyro_mail.py` (Gmail), `pipeline/clip_job.py specs/example.json --dry-run`.
4. Browser: open https://app.vyro.com/campaigns/add-clips with the OpenClaw browser (one tab). Expect still signed in; if Vyro asks for a code, read it from Gmail. Chrome path in config must be ~/openclaw-sites/browsers/chromium-1248/chrome-linux64/chrome (copied).
5. Buffer: confirm scheduled posts still listed (mw4-07/08, tdr-01..04, mw4-09/10) and that mw4-07 (Sat 12:30 PM ET) published.
6. Local model/agents: spawn a tiny Editor or Scout task to confirm sub-agents run on the NUC.
7. Tell William: laptop Gateway is stopped and disabled (not deleted); keep its ~/.openclaw for a week; delete the archives (laptop ~/Backups/openclaw, NUC ~/cutover-*.tar.gz, ~/openclaw-restored-*) once happy: they hold credentials.
8. Then Phase C (laptop as a node): NUC-PLAYBOOK.md section 4. Also update the laptop's OpenClaw to match the NUC version (laptop 2026.10.5, NUC 2026.10.7).
9. Rollback if the NUC Gateway misbehaves: run `projects/infra/nuc-cutover.sh --rollback` from a laptop terminal.
Housekeeping: add Tailscale ACL/hostname notes; router DHCP reservation for 192.168.1.112; NUC BIOS "power on after AC loss".
