#!/usr/bin/env bash
# Move the OpenClaw Gateway from this laptop to the NUC.
#
# RUN THIS FROM A NORMAL TERMINAL ON THE LAPTOP, NOT THROUGH THE AGENT.
# Stopping the laptop Gateway ends the agent's session, so the agent cannot drive this itself.
#
#   nuc-cutover.sh --preflight   read-only checks, changes nothing (safe any time)
#   nuc-cutover.sh --go          stop laptop Gateway, snapshot, restore on NUC, start NUC Gateway, verify
#                                (asks you to type CUTOVER first; rolls back automatically on failure)
#   nuc-cutover.sh --rollback    put the laptop Gateway back and stop the NUC one
#
# Plan and background: projects/infra/NUC-PLAYBOOK.md (Phase B).
set -uo pipefail

NUC="${NUC:-williamdownard@100.79.228.2}"
BK="$HOME/Backups/openclaw"
TS="$(date +%Y%m%d-%H%M%S)"
SSH=(ssh -o BatchMode=yes -o ConnectTimeout=15 "$NUC")
# PATH for non-interactive ssh on the NUC (openclaw is in ~/.npm-global/bin, claude in ~/.local/bin)
NR='export PATH=$HOME/.local/bin:$HOME/.npm-global/bin:$PATH;'

ok()   { printf '  [ok]   %s\n' "$*"; }
bad()  { printf '  [FAIL] %s\n' "$*"; FAILED=1; }
note() { printf '\n== %s\n' "$*"; }
nuc()  { "${SSH[@]}" "$NR $*"; }

preflight() {
  FAILED=0
  note "Preflight (read-only)"
  nuc 'echo ssh-ok' >/dev/null 2>&1 && ok "SSH to NUC ($NUC)" || { bad "cannot SSH to NUC"; return 1; }
  [ "$(nuc 'hostname' 2>/dev/null)" = "nuc" ] && ok "NUC hostname is nuc" || bad "NUC hostname is not 'nuc' (sudo hostnamectl set-hostname nuc)"
  nuc 'openclaw --version' >/dev/null 2>&1 && ok "OpenClaw installed on NUC: $(nuc 'openclaw --version' 2>/dev/null | head -1)" || bad "OpenClaw missing on NUC"
  nuc 'claude -p "reply ok" 2>&1 | grep -qi ok' && ok "Claude Code works on NUC" || bad "Claude Code not logged in on NUC"
  [ "$(nuc 'loginctl show-user $(whoami) -p Linger --value' 2>/dev/null)" = "yes" ] && ok "linger enabled on NUC" || bad "linger off on NUC: run 'sudo loginctl enable-linger williamdownard' on the NUC"
  nuc 'test ! -e ~/.openclaw' && ok "NUC has no ~/.openclaw yet" || bad "NUC already has ~/.openclaw (move it aside first)"
  nuc 'systemctl is-enabled sleep.target suspend.target 2>/dev/null | grep -qv masked' && bad "NUC sleep targets not masked" || ok "NUC sleep masked"
  nuc 'nmcli -t -f DEVICE,TYPE,STATE device | grep -q "ethernet:connected"' && ok "NUC on Ethernet" || bad "NUC not on Ethernet"
  nuc 'test -x ~/openclaw-sites/bin/ffmpeg && test -d ~/openclaw-sites/browsers/chromium-1248 && ~/openclaw-sites/clips-venv/bin/python -c "import faster_whisper"' >/dev/null 2>&1 && ok "NUC tools present (ffmpeg, Chrome, whisper venv)" || bad "NUC tools incomplete"
  FREE_G="$(nuc 'df -BG --output=avail ~ | tail -1 | tr -dc 0-9' 2>/dev/null)"
  [ "${FREE_G:-0}" -ge 10 ] && ok "NUC free disk ${FREE_G} GB" || bad "NUC disk low (${FREE_G:-?} GB)"
  pgrep -f 'rsync.*clips-work' >/dev/null && bad "footage copy (rsync clips-work) still running; wait for it to finish" || ok "footage copy finished"
  systemctl --user is-active openclaw-gateway >/dev/null 2>&1 && ok "laptop Gateway is running (will be stopped by --go)" || bad "laptop Gateway not active (nothing to move?)"
  [ "$FAILED" = 0 ] && { echo; echo "Preflight PASSED."; return 0; } || { echo; echo "Preflight FAILED: fix the items above."; return 1; }
}

rollback() {
  note "ROLLBACK: restoring the laptop Gateway, stopping the NUC one"
  nuc 'openclaw gateway stop >/dev/null 2>&1; systemctl --user disable --now openclaw-gateway >/dev/null 2>&1; test -e ~/.openclaw && mv ~/.openclaw ~/.openclaw.failed-'"$TS"'; true'
  systemctl --user enable --now openclaw-gateway && ok "laptop Gateway enabled and started" || bad "could not start laptop Gateway: run 'openclaw gateway start'"
  sleep 5; openclaw status 2>&1 | head -8
  echo "Rolled back. Laptop is the Gateway again. NUC state kept at ~/.openclaw.failed-$TS for inspection."
}

go() {
  preflight || exit 1
  echo; echo "This stops the agent on this laptop for ~10-20 minutes while the NUC takes over."
  read -r -p "Type CUTOVER to continue: " A; [ "$A" = "CUTOVER" ] || { echo "Aborted."; exit 1; }

  note "1/6 Stop laptop Gateway"
  openclaw gateway stop || { bad "gateway stop failed"; exit 1; }
  systemctl --user disable openclaw-gateway >/dev/null 2>&1   # stays off after reboot; --rollback re-enables
  sleep 3; systemctl --user is-active openclaw-gateway >/dev/null 2>&1 && { bad "laptop Gateway still active"; rollback; exit 1; } || ok "stopped"

  note "2/6 Final snapshot (verified)"
  mkdir -p "$BK"
  openclaw backup create --output "$BK" --verify || { bad "backup failed"; rollback; exit 1; }
  A="$(ls -t "$BK"/*-openclaw-backup.tar.gz | head -1)"; ok "archive: $A ($(du -h "$A" | cut -f1))"

  note "3/6 Copy and restore on NUC"
  scp -q "$A" "$NUC:~/cutover-$TS.tar.gz" || { bad "scp failed"; rollback; exit 1; }
  nuc "openclaw backup restore ~/cutover-$TS.tar.gz --target ~/openclaw-restored-$TS >/dev/null" || { bad "restore failed"; rollback; exit 1; }
  nuc "P=\$(ls -d ~/openclaw-restored-$TS/*/payload/posix/home/williamdownard/.openclaw 2>/dev/null | head -1); test -n \"\$P\" && mv \"\$P\" ~/.openclaw" || { bad "could not place restored state"; rollback; exit 1; }
  ok "state placed at ~/.openclaw on NUC"

  note "4/6 Doctor (safe migrations) and service install"
  nuc 'openclaw doctor --fix --non-interactive' || { bad "doctor failed"; rollback; exit 1; }
  nuc 'openclaw gateway install --force' || { bad "gateway install failed"; rollback; exit 1; }

  note "5/6 Verify NUC Gateway"
  for i in 1 2 3 4 5 6 7 8 9 10 11 12; do nuc 'systemctl --user is-active openclaw-gateway' >/dev/null 2>&1 && break; sleep 5; done
  nuc 'systemctl --user is-active openclaw-gateway' >/dev/null 2>&1 && ok "NUC Gateway service active" || { bad "NUC Gateway not active"; rollback; exit 1; }
  sleep 20
  nuc 'openclaw status' 2>&1 | head -25
  nuc 'openclaw status' >/dev/null 2>&1 && ok "openclaw status runs on NUC" || { bad "openclaw status failed"; rollback; exit 1; }

  note "6/6 Done"
  echo "NUC is now the Gateway. Laptop Gateway is stopped and disabled (not deleted)."
  echo "Next: send a Telegram message to the agent and confirm a reply; then follow PLAYBOOK Phase B checklist and Phase C (laptop as node)."
  echo "Keep the laptop's ~/.openclaw for at least a week. Delete $A and the NUC's ~/cutover-$TS.tar.gz once everything checks out (they hold credentials)."
}

case "${1:-}" in
  --preflight) preflight ;;
  --go) go ;;
  --rollback) rollback ;;
  *) sed -n 2,13p "$0"; exit 1 ;;
esac
