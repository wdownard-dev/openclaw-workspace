# Clip-policy research, batch 2 / Scope A part 2 (Minecraft + VALORANT)

Researched 2026-10-22. Read-only: nobody contacted, no accounts created, no Discords joined. Streamers: feinberg, drdonutttttt, linkzzey, shoomimi, subroza, zekken, shahzam, minny.

## Method and limits (read first)
- No Chromium on this host (the browser tool reports "No supported browser found"), so I could not render Twitch pages. Instead I read each channel's public About text, **text panels** and linked socials from Twitch's public web data endpoint (the same data twitch.tv/<login>/about renders, no login). Cited below as "Twitch About/panels".
- **Image-only panels** (many sponsor/link panels have no text) could not be read, and chat commands (`!website`, `!skinclub`, `!announcement`, etc.) and Discord rules/channels were not readable. Any policy that lives only there is **unverified**.
- X bios were read from the public profile page; emails marked "(X bio)" were read from the page's meta description or decoded from the standard Cloudflare-protected address. YouTube descriptions were read from each channel page; YouTube's "business email" field (behind a click) was not retrievable.
- Several obvious handles are the WRONG accounts (x.com/feinberg, x.com/zekken, x.com/DrDonutttttt, x.com/MinnyTv, youtube.com/@ShahZaM are unrelated people). Only handles linked from the streamer's own Twitch page are used below.
- Nothing here is permission. All 8 remain `candidate` until a written yes. Also, YouTube's reused-content rules can demonetize clip-only channels even with streamer approval; plan to add real commentary/editing.
- **Result: none of the 8 states any clip/reupload policy on any source I could read.** Policy status is "not stated (unverified)" for all eight.

---

## 1. Feinberg (feinberg) — policy: **not stated (unverified)**
- **Evidence:** No clip/reupload wording in Twitch About/panels (https://www.twitch.tv/feinberg/about: "top minecraft speedrunner :)"; panels are donations, business email, socials, bio) or YouTube https://www.youtube.com/@FeinbergMC ("top minecraft speedrunner and event player :p … home of one of a kind events and challenges and videos"). X bio https://x.com/feinberg_mc: "36x AA WR holder - former SSG + FSG WR. mcc winner + tourney dominator. 2x rank 1 speedrunner." ~38.6K followers.
- **Clipper program:** none found. He already runs his own highlight channels, linked from his Twitch: https://www.youtube.com/@FeinbergRocks ("feinberg stream highlights! … edits by feinberg funny") and https://www.youtube.com/channel/UCC9noN9nxjc9d_qZw-YvV4w ("edited stream highlights from the best minecraft player on twitch"). So the clip space is already covered by him and his editor. Discord exists (discord.gg/9gV2ZY6fvT, from his panel; not joined); any clip channel there is unverified.
- **Contact:** Twitch panel: "BUSINESS EMAIL: feinberg@valianttalent.com". Valiant Talent looks like a talent agency, so this is an **agency/management contact** (agency status inferred from the domain; unverified). X: @feinberg_mc.
- **Risks:** Low content risk (family-friendly speedrun/event Minecraft, no gambling seen; a panel links a streaming-sponsor shortlink strms.net, image-only). A search result (earlygame.com) reports a 2021 Twitch ban of an alt account named "feinbergsucks" that blocked his main channel; I did not verify details. Competing official highlight channels. Event/challenge videos may feature other creators (collab consent unclear). Minecraft's own usage guidelines are generally permissive for monetized video but are the game owner's, not his permission.

## 2. DrDonut (drdonutttttt) — policy: **not stated (unverified)**; has an official clipper-hiring form
- **Evidence:** Twitch About (https://www.twitch.tv/drdonutttttt/about): "streamer- Live Daily at: youtube.com/@DrDonutt/live - TikTok - Discord: discord.gg/donut - Instagram - Twitter: x.com/DrDonut099 - Join the Donut SMP: donutsmp.net". Panels: Discord and YouTube only. YouTube https://www.youtube.com/@DrDonutt ("Daily live streamer") links donutsmp.net, a Vertmix Studio page, and a Google form. No clip/reupload wording on any of these.
- **Clipper program: YES (official, paid/trial).** The Google form linked from his YouTube, https://forms.gle/tF4krzCtFmmiPwA96, is titled "Application for Position at DrDonut's Team": *"We are expanding DrDonut's content team and seeking talented video editors and creators passionate about Minecraft! … Stream clippers (short-form highlights and memes) … Short-form editors (YouTube Shorts, TikTok-style clips) … If selected for consideration, you'll go through a paid or trial editing process … No job is guaranteed until the trial is successfully completed."* Fields asked: contact info, Discord tag, location, availability, age, position. This is a hiring application for his own team (he'd own/approve the output), not a licence to run an independent channel. Whether independent clip channels are tolerated is unverified. A scraper site claims a "DrDonut Clips" channel is owned by him and run by others (old.fbpe.org; low quality, unverified).
- **Contact:** No business email found on Twitch/X/YouTube text. Paths: the application form above, Discord (https://discord.gg/donut, not joined), X @DrDonut099 (bio "daily youtube streamer"), YouTube About email field (unverified, behind a click). No agency seen.
- **Risks:** Likely very young audience and a kid-popular server (DonutSMP, run by him), so "made for kids"/limited-ads classification risk on YouTube; DonutSMP-related drama/scam allegations appear in search headlines (unverified, not read). Heavy server promotion in titles. Largely a YouTube-first streamer (Twitch ~1K viewers; ~617K followers), so he may guard his own clip supply. Applying would make you his contractor, which conflicts with running your own channel unless he agrees otherwise.

## 3. Linkzzey (linkzzey) — policy: **not stated (unverified)**
- **Evidence:** Twitch About (https://www.twitch.tv/linkzzey/about): "Hardcore Minecraft Content Creator. Come For The Builds, Stay For The Derps. LinkzzeyTVB@gmail.com". Panels contain only channel bio, YouTube/Twitter links and chat rules (no racism/politics/self-promo in chat). No clip wording. YouTube https://www.youtube.com/channel/UC2bxcqfXBUAGs6UbQxT6wmw: "Come for the builds stay for the derps!" (links Patreon, a Modrinth datapack, Twitch). X https://x.com/LinkzzeyMC: "King of Hardcore Minecraft - Live Everyday at 12 PST".
- **Clipper program:** none found. Discord exists (discord.gg/PXbCPRtMvx, from his Twitch; not joined); site linkzzeytv.com (Wix; no clip text found). Unverified.
- **Contact:** **LinkzzeyTVB@gmail.com** (direct business-style email on his own Twitch About; not an agency). X: @LinkzzeyMC.
- **Risks:** Lowest of the group: family-friendly hardcore Minecraft, no gambling or sponsor-heavy panels seen, no controversy found. Currently in a subathon (title: "SUBATHON DAY 6") so lots of long VOD material. Has his own YouTube and Patreon, so he may care about reuploads of full builds. Audience mix may include minors.

## 4. Shoomimi (shoomimi) — policy: **not stated (unverified)**
- **Evidence:** Twitch About (https://www.twitch.tv/shoomimi/about): "Brain in a jar vtuber! … Business Email: shoomimishoom@gmail.com". Panel rules: *"Content is for mature audiences! Watch at your own discretion"*, no suggestive/lewd chat, TTS min 100 bits. No clip wording. YouTube https://www.youtube.com/@Shoomimi (bio + twitch link) and a separate VODs channel https://www.youtube.com/@Shoomimivods (linked in a panel). X https://x.com/Shoomimishoom.
- **Clipper program:** none found. She already runs a VODs channel; Discord https://discord.com/invite/shoomimi (not joined); clip channel there unverified.
- **Contact:** **shoomimishoom@gmail.com** (direct, on her Twitch About). X: @Shoomimishoom. No agency seen.
- **Risks:** Self-labelled mature content (age-restriction and advertiser-friendly risk), VTuber model/art is commissioned from named artists (credited in a panel), so reuse of the avatar is the artists' IP question, not hers alone. Sponsor codes for soap/deodorant/toothpicks/supplements (mild). Gambling: none seen. Smaller (~31K followers, ~350 avg viewers).

## 5. Subroza (subroza) — policy: **not stated (unverified)**
- **Evidence:** Twitch About: "Pro VALORANT Player | Streamer | Business Inquires: subroza@iso-ent.com". Panels: sponsor/discount links (tilt.fyi, IQUNIX keyboard), donations, **"CRYPTO DONATIONS, SHOWS UP ON SCREEN!"** (1upcoin.com), settings, socials. YouTube https://www.youtube.com/@subrozatv: "LIVE ON TWITCH EVERYDAY ✉️ Business Inquires: subroza@iso-ent.com". X https://x.com/Subroza has the same email. Linktree https://linktr.ee/subrozayt (no readable text). No clip wording anywhere.
- **Clipper program:** none found. Discord https://discord.gg/subroza (not joined); unverified.
- **Contact:** **subroza@iso-ent.com** (Twitch, YouTube, X). The "iso-ent" domain suggests an entertainment/management company; agency status inferred, unverified. X/IG/TikTok: @Subroza / @SubrozaYT / @subroza.
- **Risks:** Highest of the Valorant group. Crypto-donation panel and a #tilt shortlink sponsor; a vlr.gg thread titled "Subroza promoting gambling" appears in search (title only, not read; treat as unverified). Stream title this week: "#1 HALAL STREAMER … LIVE EVERYWHERE EVERYDAY". Large (1.14M followers), likely agency-managed with rigid terms.

## 6. zekken (zekken) — policy: **not stated (unverified)**
- **Evidence:** Twitch About (https://www.twitch.tv/zekken/about): "21 y/o Valorant Player for @MIBRTV". Panels are image-only links (Lenovo Legion shortlink, MelGeek, Twitter, Streamlabs, YouTube). YouTube https://www.youtube.com/channel/UCQjfeGyQo2F4_mczJdE_pOw: *"Subscribe for more AIM... Valorant Player for MIBR. Represented by Prodigy Agency. Business inquiries: zekken@prodigy-seg.gg"* (links konect.gg/zekken, prodigy-agency.gg). X https://x.com/zekkenVAL has an obfuscated email that decodes to `zekken@prodigy-agency.gg` (X bio). No clip wording.
- **Clipper program:** none found.
- **Contact:** **Agency**: Prodigy Agency, via zekken@prodigy-seg.gg (YouTube) / zekken@prodigy-agency.gg (X); the two addresses differ, try the YouTube one first or both. X: @zekkenVAL.
- **Risks:** Pro player under a team contract (MIBR), so team/Riot-event content has extra rights holders; agency-managed means a formal approach. Gameplay-only content is otherwise low-risk (young, not known for gambling, but sponsors are image-only panels, unverified). Stream title mentions other orgs/teams (Loud, Cloud9, MIBR).

## 7. ShahZaM (shahzam) — policy: **not stated (unverified)**
- **Evidence:** Twitch About: "Professional CS:GO & Valorant player"; panels are mostly image-only sponsor shortlinks (adv.gg, tl.gg, bit.ly), donations and socials. YouTube https://www.youtube.com/channel/UCKNq_4ub5GACIkQfuVWEBtg: "Content Creator for Team Liquid"; links Opera GX, Discord. X https://x.com/ShahZaMk: "content creator @TeamLiquid … Inquiries: shahzamcsgo@gmail.com". No clip wording.
- **Clipper program:** none found. Discord https://discord.gg/shahzam (not joined).
- **Contact:** shahzamcsgo@gmail.com (X bio; a direct address, but he is under Team Liquid as a content creator, so the org may also have a say; unverified). X: @ShahZaMk.
- **Risks:** Current stream title is "ROAD TO RANK 1 **!skinclub**". `!skinclub` suggests a Skin.Club sponsorship, a CS skin/case-opening site (gambling-adjacent; the command's content is unread, so unverified). The Twitch page carries many sponsor links. Team Liquid contract adds a rights holder. Only ~490 viewers right now.

## 8. Minny (minny) — policy: **not stated (unverified)**
- **Evidence:** Twitch About is empty (https://www.twitch.tv/minny/about). Panels are image-only French sponsor links (Volvic, ALDI FR, Visa, TCL, Alpine, Hellowork, Lofi Girl/M8). X https://x.com/minnyfn: *"21 - @gentlemates Represented by @ProPlayersGG"*. Twitch links Instagram @realminny. No YouTube channel found.
- **Clipper program:** none found.
- **Contact:** No email found anywhere. Represented by ProPlayersGG (agency; via X bio) and plays for M8/Gentle Mates (per X bio). Handles: X @minnyfn, IG @realminny. X profile x.com/MinnyTv is a different account.
- **Risks:** Heavy brand sponsorship tied to the Gentle Mates org, team contract, bilingual stream ([ENG/CZ]) and French sponsors, agency-represented with no direct email. Smallest audience on this list (~430 viewers, ~88K followers). Nothing found on gambling or controversy, but little checked.

---

## Ranked: who to approach first
1. **Linkzzey**: direct email on his own Twitch About (LinkzzeyTVB@gmail.com), family-friendly, no gambling/sponsor red flags, daily long-form streams (subathon). Best odds of a quick yes. Risk: no stated policy.
2. **DrDonut**: the only one with an *official clipper program* (paid/trial application form, https://forms.gle/tF4krzCtFmmiPwA96) and a large audience. Caveats: it is a hiring form (you'd work for his team, not run your own channel), kid-heavy audience, no direct email found. Message via Discord/X first to ask whether independent Shorts channels are OK, and ask before applying.
3. **Feinberg**: clean content and a clear business email, but it goes to an agency (Valiant Talent) and he already runs two highlight channels, so expect a "no" or a formal deal.
4. **Shoomimi**: direct email and a VODs-friendly culture, but self-declared mature content hurts monetization; consider after the top three.
5. **zekken**: agency (Prodigy) plus team contract; low content risk but slow, formal process.

## Skip (for now)
- **Subroza**: crypto donations/sponsor-heavy, possible gambling-promotion controversy (unverified), agency email.
- **ShahZaM**: `!skinclub` sponsorship (gambling-adjacent), Team Liquid contract, small live audience.
- **Minny**: no contact path beyond an agency handle, EN/CZ/FR sponsor-heavy, low upside.

## Suggested next steps
- In a real browser (or by reading chat), check what `!website` (Linkzzey), `!skinclub` (ShahZaM) and `!announcement` (Subroza) say, and read Discord #rules / #clips for Linkzzey, DrDonut, Shoomimi and Feinberg. Many policies would live there.
- When asking, request written permission for: YouTube Shorts, monetized, with credit/link back, and say which VODs/games. Ask about collaborators on screen (Feinberg events, Shoomimi collabs).
