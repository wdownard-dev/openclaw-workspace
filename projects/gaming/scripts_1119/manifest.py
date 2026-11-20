import json, os
O = "/home/williamdownard/.openclaw/workspace/projects/gaming/out/"
TG = ("Typical Gamer", "cyAPzaLcEsM", "1 HOUR of GTA 6 FREE-ROAM Gameplay! (New)")
XQ5 = ("xQc", "LUE2681HACI", "xQc Spends a day with Lucia | GTA 6 Playthrough #5")
XQ8 = ("xQc", "UAw-wZeA0F8", "xQc GTA 6 Playthrough #8")
XQ7 = ("xQc", "L7KXEeEePlo", "xQc GTA 6 Playthrough #7")
core = ["gta 6", "gta6", "grand theft auto 6", "grand theft auto vi", "gta vi", "rockstar games"]
def ts(s):
    s = int(s); return f"{s//3600}:{s%3600//60:02d}:{s%60:02d}" if s >= 3600 else f"{s//60}:{s%60:02d}"
def clip(file, sheet, src, start, end, title, hook, text, tags, why, caveat, hashtags="#GTA6 #GrandTheftAuto6 #GTAVI"):
    cr, vid, st = src
    dur = round(end - start, 1)
    return {"file": O + file, "contact_sheet": O + sheet, "source_video_id": vid, "source_title": st, "streamer": cr,
            "source_start_s": start, "source_end_s": end, "source_start_ts": ts(start), "source_end_ts": ts(end), "duration_s": dur,
            "title": title, "title_len": len(title),
            "description": f"{hook}\n\nVia {cr} (full video: https://www.youtube.com/watch?v={vid}&t={int(start)}s)\n\n{hashtags}",
            "tags": core + tags, "on_screen_text": text, "why_it_passes": why, "caveat": caveat}
M = []
M.append(clip("gta6_1119_highway_chaos.mp4", "gta6_1119_highway_chaos.contact.jpg", TG, 2996, 3042, "Highway Carjacking Chaos in GTA 6",
  "A multi-car pile-up, a carjacking and a getaway on one Vice City highway.", "This highway is chaos",
  ["gta 6 carjacking", "gta 6 highway", "gta 6 crash", "gta 6 free roam"],
  "Opens on a car pile-up in frame 1 (hook in 1 s). All frames GTA 6 gameplay with the streamer facecam; no cutscene, no black/loading frames, no watermark. Text line 'This highway is chaos' present 0.3-8 s. Fully viewed 10-frame sheet + first-7 s strip.",
  "Carjacking: an NPC is pulled from a car and lies on the road at ~25 s (no blood, no gore). Mild game violence only.", ))
M.append(clip("gta6_1119_train_chase.mp4", "gta6_1119_train_chase.contact.jpg", TG, 4895, 4940, "Police Car vs. a Train on the Tracks in GTA 6",
  "Cops, a train and a very bad place to park.", "Cops vs. a train",
  ["gta 6 police chase", "gta 6 train", "gta 6 wanted level", "gta 6 free roam"],
  "First frame: police car stuck on rails with a train's headlights bearing down, crash within 4 s. Climb onto the train roof afterwards. No blood (red = damage vignette / tail-lights), no cutscene, no black frames, no watermark. Text line 'Cops vs. a train' 0.3-8 s.",
  "Dark scene; red damage vignette in the last third. Facecam present. Also listed in out/today_posts_2026-11-19.json (not posted; no upload record).",
  hashtags="#GTA6 #GrandTheftAuto6 #GTAVI"))
M.append(clip("gta6_1119_vice_city_drive.mp4", "gta6_1119_vice_city_drive.contact.jpg", TG, 1272, 1318, "Racing a Blue Sports Car Through Vice City in GTA 6",
  "A blue sports car, a carjacking and a drift through the streets of Vice City.", "Vice City joyride",
  ["gta 6 vice city", "gta 6 sports car", "gta 6 driving", "gta 6 carjacking"],
  "Clean daytime free-roam gameplay: speed, a carjack at ~10-15 s, drifting. No cutscene, no black frames, no gore, no watermark. Text line 'Vice City joyride' 0.3-8 s.",
  "Weakest hook of the set (calm first 7 s; the action starts ~10 s). Use last in the posting order. Description wording kept generic on purpose.",
  hashtags="#GTA6 #ViceCity #GTAVI"))
M.append(clip("1119_final_tg_jet_takeoff.mp4", "1119_final_tg_jet_takeoff.contact.jpg", TG, 4163, 4205, "Taking Off in a Fighter Jet at Sunset in GTA 6",
  "Stealing a fighter jet at an airbase and taking off into a sunset.", "Fighter jet, sunset takeoff",
  ["gta 6 fighter jet", "gta 6 military base", "gta 6 wanted level", "gta 6 sunset"],
  "Clean gameplay (parachuting onto the airbase, jet takeoff, banking over water at sunset). Wanted stars visible. No cutscene, no black frames, no gore, no watermark. Text line added by me (out/1119_final_tg_jet_takeoff.mp4; raw 1119_tg_getmein.mp4 had none).",
  "Topic overlaps the fighter-jet Short already live on the channel (DE1LkoNOoik, from 57:50 of the same VOD, different moment). Space it from that or skip if variety matters. First 7 s is a parachute landing, hook is moderate.",
  hashtags="#GTA6 #GrandTheftAuto6 #GTAVI"))
M.append(clip("1119_final_xqc_miami_tunnel.mp4", "1119_final_xqc_miami_tunnel.contact.jpg", XQ5, 3778, 3824, "Miami Sunset Tunnel Drive in GTA 6 Looks Unreal",
  "That tunnel into a pink Miami sunset is the best-looking drive yet.", "Miami at sunset hits different",
  ["gta 6 graphics", "gta 6 miami", "gta 6 driving", "gta 6 sports car"],
  "Pure gameplay: sports car through a lit tunnel out onto a purple-pink sunset highway with the skyline ahead. Starts after the earlier cutscene (re-cut from raw 1119_lue_tunnel.mp4). No cutscene frames, no black, no watermark. Text line re-rendered at 52 pt with the clip_queue recipe (the older gta6_1119_miami_tunnel.mp4 text ran edge to edge).",
  "xQc's Twitch chat overlay is part of the source frame (small, left side) plus mission subtitles ('Keep up with Mattia'); no story reveal. No streamer reaction moment, it is a visual clip. Supersedes gta6_1119_miami_tunnel.mp4.",
  hashtags="#GTA6 #ViceCity #GTAVI"))
M.append(clip("1119_final_xqc_sunset_race.mp4", "1119_final_xqc_sunset_race.contact.jpg", XQ8, 2888, 2932, "Full-Grid Circuit Race at Sunset in GTA 6",
  "A multi-lap circuit race with a full grid, filmed at sunset.", "Sunset race, full grid",
  ["gta 6 racing", "gta 6 race", "gta 6 sunset", "gta 6 cars"],
  "Race start on the grid then lap action under a sunset. Trimmed 1.9 s off the raw cut to remove a white-out transition; first 7 s clean. No cutscene, no black frames, no gore, no watermark.",
  "Chat overlay + facecam in frame (xQc). Action level moderate (racing, no crash). Near-twin of the next clip (daytime race start): post one or space them well.",
  hashtags="#GTA6 #GrandTheftAuto6 #GTAVI"))
M.append(clip("1119_final_xqc_race_start.mp4", "1119_final_xqc_race_start.contact.jpg", XQ7, 4633.5, 4679, "Daytime Circuit Race Start in GTA 6",
  "The countdown, the grid and the first corner of a circuit race.", "Race start, full grid",
  ["gta 6 racing", "gta 6 race", "gta 6 cars", "gta 6 grid"],
  "Starts on the car on the grid, countdown, race launch into the first laps. Trimmed 0.5 s. No cutscene, no black/white frames, no gore, no watermark.",
  "Chat overlay + facecam in frame (xQc). Lowest-priority of the set; same mode as the sunset race so treat as alternate. Gameplay only; the streamer's speech was not reviewed.",
  hashtags="#GTA6 #GrandTheftAuto6 #GTAVI"))
rej = [
 ("out/1119_lue_miami_drive.mp4", "Opens on a story cutscene (character lying down, then cutscene car shots) in the first 7 s."),
 ("out/1119_lue_speedboat.mp4", "First frame is a cutscene shot; rest is calm boat driving with no hook."),
 ("out/1119_lue_what.mp4", "Weapon-crafting hold prompts and a stationary character, slow, no hook."),
 ("out/1119_xqc2_chad.mp4", "Shop/merch UI and a black frame; no action."),
 ("out/gta6_1119_miami_tunnel.mp4", "Superseded: text line ran edge to edge; replaced by 1119_final_xqc_miami_tunnel.mp4 (same footage)."),
 ("out/1119b_tg_trunk.mp4 (cyAPzaLcEsM 2292-2338)", "Slow police-car drifting in a parking garage; 'body in the trunk' context not shown, weak hook."),
 ("out/1119b_tg_cops.mp4 (cyAPzaLcEsM 3905-3951) and 1119_final_tg_seaplane.mp4", "It is a wheeled Cessna that skims water, not a seaplane touchdown (mislabel risk); 10 s of taxi at the start."),
 ("out/1119b_tg_roadrage.mp4 (cyAPzaLcEsM 2645-2691)", "Plain driving then ends on a map/pause menu."),
 ("out/1119b_tg_headon.mp4 (cyAPzaLcEsM 4705-4751)", "Dark night chase under a heavy red damage vignette throughout; overlaps the train chase."),
 ("out/1119b_xqc_card.mp4 (LUE 5236-5282)", "Signed collectible card moment is ~10 s; rest is phone/map menus."),
 ("out/1119b_xqc_racecrash.mp4 (UAw 2603-2649)", "Multi-second white-out after the crash and a lap restart mid-clip."),
 ("out/1119b_xqc_blowup.mp4 (RA9 1545-1591)", "Nothing blows up: slow bike ride on a bridge."),
 ("out/1119b_xqc_airescape.mp4 (RA9 4755-4801)", "Mission shootout from a plane with a 'Press to restart' fail prompt in the first 7 s; story/mission context."),
 ("xQc #6 MDxBl2tF9P0 top-14 windows", "Mined (audio+transcript+visual): hostage/knife cutscene, mission-fail retry menu, map menus, bus rides. No clean window."),
 ("xQc #3 Tg90IZCrd9g top-14 windows", "Mined: boat rides with phone/map menus, a shower/room-looting scene. No clean window."),
]
json.dump({"generated": "2026-11-19", "note": "Nothing posted or uploaded. ledger/queue/yt log show no upload of any 1119_* or gta6_1119_* file. Titles per METADATA_RULES.md. Posting order suggestion: train_chase, highway_chaos, miami_tunnel, sunset_race, jet_takeoff, vice_city_drive, race_start.",
  "clips": M, "rejected": [{"cut": a, "reason": b} for a, b in rej],
  "blockers": ["Typical Gamer HzzzoomJ-Os (live VOD, ~9h56m, ended) has no English auto-subs yet, so moment_pick cannot run; not mined. cyAPzaLcEsM leftovers used instead.",
               "xQc playthroughs #2 (UfmrSYPbvfw) not mined: time; #4/#5/#6/#7/#8/#3 mined. Most xQc footage is mission/story/menu heavy, so xQc yields are low."]},
  open(O + "1119_manifest.json", "w"), indent=1)
print(len(M))
