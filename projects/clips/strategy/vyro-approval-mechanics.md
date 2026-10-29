# Vyro approval mechanics: three conflicting statements resolved against evidence

Written 2026-10-28 (Wed evening ET) by Strategist. Read-only: Vyro help-center pages via web_fetch (fetched 2026-10-29 00:18 UTC), PLAN.md, USER.md, vyro-snapshots.csv, vyro-submissions.json, research-track2.md, campaigns/mrbeast-gaming-mw4/brief.md, campaigns/total-drama-roblox/{brief.md, join-package.md, clipper-terms.txt}, strategy/2026-10-28.md. The logged-in Vyro app was NOT opened. The 'My posts' modal text is as relayed by Morpheus; I did not see it, so I do not know the N in "Waiting for views · N / 5,000". Line numbers are not cited because PLAN.md is a log; entries are cited by date and heading.

## The answer
- **(a) CONFIRMED, with one correction.** The block is a cap of 3 pending posts per campaign, not "no more posts until one is approved". It lifts per campaign at the first approval. William's report that approval is what lifts it is also confirmed.
- **(b) SPLIT.** "The block lifts when a post is approved" is CONFIRMED. "Vyro approves only at 5,000 views" is UNVERIFIED, and Vyro's own pages describe approval and the 5,000 threshold as two separate conditions. Our data is consistent with William's version but cannot tell it apart from slow review.
- **(c) UNVERIFIED, probably a definitions gap, not a true contradiction.** The help center says views are *counted* from submission, pending or not. The campaign dialogs and the new modal say only approved posts' views are *eligible* (payable). Both can be true at once. Nothing says whether pending-period views become payable if the post is approved later.
- **Strategy:** do not default-submit every post, and do not gate on traction either. Submit TikTok only, to the one campaign with budget (TDR), and keep one slot free for a post that shows traction in its first hour. Details in §2.

## 1. The three statements

### (a) PLAN.md 10/22: "a new account can't submit more posts until one is approved"; pending cap 3 per campaign
**CONFIRMED on the cap, CORRECTED on the wording.**
- Help center, https://vyro.com/help/clips-and-content/how-many-posts-can-i-submit (updated Sep 30, 2026): "Until one of your clips is approved in a campaign, you can have up to 3 clips waiting for review there. Once a clip is approved, that cap no longer applies to you in that campaign." Also: "Clippers can submit up to 5 posts per social account, per campaign, every 24 hours."
- The cap is per campaign: the same page says posting in one campaign does not use up the limit in another. Confirmed in practice: TDR accepted submissions on 10/26 while MW4 was blocked (PLAN.md 10/24 ~1:55 PM entry predicted this; vyro-submissions.json tdr-01 note says "TDR is not blocked by the new-account rule").
- It counts across platforms, not per social account: MW4 held 1 YouTube + 1 TikTok + 1 Instagram and then refused (PLAN.md 10/23 ~9:30 PM). So IG and YouTube submissions use the same 3 slots as TikTok.
- The dialog wording overstates it. Dialog (vyro-submissions.json, mw4-08 note): "you'll need to wait for one of your posts to be approved before you can submit another." Observed behaviour matches a cap of 3, not a cap of 1: with 1 pending (10/23), two more submissions were accepted with no approval (PLAN.md 10/23 ~9:25 and ~9:30 PM). The block returned at exactly 3 pending on MW4 (10/23, 10/25, 10/26) and on TDR (10/27, tdr-02 Instagram refused). That is n = 4 block events, all at 3 pending, plus 1 unblock when pending fell from 3 to 1.
- Not stated by Vyro: whether deleting a pending submission frees the slot permanently or carries any penalty. Evidence: it freed the slot on 10/23 (n=1), and on 10/28 three TDR submissions were deleted (no penalty visible yet).

### (b) USER.md 10/28 (William's report): "Vyro approves a post only when it reaches 5,000 views, and the new-account block lifts only then"
**Part 1, the block lifts at the first approval: CONFIRMED** (quote under (a)).
**Part 2, approval happens only at 5,000 views: UNVERIFIED. Vyro's text points the other way, our data cannot discriminate.**
- Against, from Vyro's own pages:
  - https://vyro.com/help/earnings-and-payments/how-many-views-do-i-need-before-i-can-start-earning (Aug 21, 2026): "Each approved post must reach a minimum of 5,000 views to start earning." Order is approved first, then 5,000.
  - Campaign dialog (join-package.md §2a, TDR, read 10/23): "After you post, clients review to confirm your post complies with all stated requirements, in its discretion. Only approved posts count toward your views" and, separately, "Each post must reach 5,000 views to be eligible for payout."
  - Clipper Terms (clipper-terms.txt): "Only when your Clipper Content has been approved and the Client Campaign requirements have been met, including ... the minimum view, impression, or other metric thresholds ... will such Payout amounts be earned." Approval and threshold are listed as two conditions. One ambiguous line leans William's way: "All Clipper Content is subject to Client's approval in accordance with the stated requirements, including, but not limited to the minimum views or impression requirements."
  - https://vyro.com/help/clips-and-content/when-will-my-post-be-reviewed (Aug 21, 2026): "Posts can sometimes take a few days to review due to the high volume of submissions." Nothing about a views trigger.
- For, from our data (consistent, not proof):
  - 0 approvals in 5-6 days: MW4 3 pending since 10/22-23, TDR 3 pending since 10/26-27 (vyro-snapshots.csv through 10/28 08:20: `approved` = 0 on all 10 rows). That is already beyond "a few days" for MW4.
  - No approval or rejection email either. Help says "You'll get an email when your clip is approved or rejected" (index at https://vyro.com/help/clips-and-content). PLAN.md 10/23 9:45 PM: Vyro mail so far is verification codes only. Zero rejections in 6 submissions suggests those posts have not been reviewed at all, which fits "review waits for 5,000" or a backlog equally well.
  - The new modal shows every row as "Waiting for views · N / 5,000" with Status "Pending". Ambiguous: it may be the payout gate, not the review gate.
- The test has never been run: every submitted post sits far below 5,000 (Vyro-counted views are 0 on every snapshot). The one post above 5,000, mw4-08 (8.5k TikTok views), was never submitted (vyro-submissions.json: blocked). So (b) is untested, not refuted.
- Not usable as evidence: MW4 "paid out" climbing 23% to 91% in five days. Help (when-will-my-post-be-reviewed) says pending views also count toward the campaign budget, so budget burn does not show that others are being approved.

### (c) Do views count from submission while pending (help), or do only approved posts count (dialog)?
**UNVERIFIED. The two statements answer different questions, and the new modal text leans toward "approved only" for payable views.**
- Help, https://vyro.com/help/clips-and-content/when-will-my-post-be-reviewed: "Your views start counting as soon as you submit your post on Vyro, even before it's reviewed. Those views also count toward the campaign budget while your clip is still pending." Also https://vyro.com/help/earnings-and-payments/why-is-there-a-difference-in-views (Oct 1, 2026): "Views start counting from the moment you submit your video to Vyro."
- Dialog/brief: TDR join-package.md §2a, "Only approved posts count toward your views"; MW4 brief.md, "Only client-approved posts count."
- New modal (relayed): "Eligible views: Views from approved posts earned while campaign budget was available." Help https://vyro.com/help/earnings-and-payments/what-are-eligible-views: "Eligible views are the views that count toward your potential earnings in a campaign."
- Reconciliation that fits all quotes: Vyro *tracks* views and burns budget from submission (help), but only views on *approved* posts are *eligible* (modal, dialogs). Unknown, and the key money question: when a pending post is approved later, do the views it earned while pending become eligible, or only views after approval?
- Weak supporting evidence for "approved only": the My-campaigns card Views stayed 0 on all 10 snapshots while a submitted post was gaining views. Example: mw4-01 TikTok was submitted 10/23 ~9:25 PM and William reported 95 TikTok views overnight (PLAN.md 10/24 ~10:25 AM), yet the card showed 0 on 10/24 10:20. n=1 post. I don't know what the card counts (unverified), and Vyro refreshes every 30 minutes.
- **Free check, no support ticket needed:** William can compare N in the modal for the mw4-01 TikTok row with the views that post gained in the TikTok app since 10/23 9:25 PM. If N is roughly that number, Vyro counts pending views and the help page is right on counting. If N is 0 with ~100+ real views, only approved posts are counted at all. This does not answer the retroactivity question.

## 2. What this means for strategy (TikTok weighted)

**Should Vyro posts be submitted only after traction? Not as a hard rule. Recommended provisional policy (William's call; it touches an account):**
1. **TikTok posts only, TDR only for now.** MW4 was 91% paid and locked on 10/28 (strategy/2026-10-28.md); new MW4 posts cannot be submitted at all. Of the 6 slots used so far, 3 went to Instagram/YouTube posts (mw4-01 YT, mw4-01 IG, tdr-01 IG) that got 0 views. Slots are shared across platforms, so each non-TikTok submission costs a TikTok slot.
2. **Submit the strongest 2 TikToks at post time; keep the third slot empty as a reserve.** If a post is clearly running (for example 1,000+ views within ~60 minutes), submit it into the reserve slot. Reason below. Effort: William or Morpheus must read TikTok views at +1 h (no API; Buffer lags, per the 10/28 brief), so this costs one manual check per post.
3. **Do not delete pending posts to recycle slots until (b) is answered.** If approval is slow and independent of views, deleting resets the review wait (TDR is now at 0 submissions after tonight's deletions, so this is the next test). If approval waits for 5,000, recycling a dud is free. We do not know which.

**Cost of late submission** (views before submission never count: https://vyro.com/help/clips-and-content/when-should-i-upload-my-content, example "you'll only earn for the 2,000 views after submission"):
- Likely larger than it looks. The modal counter is "N / 5,000" and Vyro counts from submission, so the 5,000 bar is probably measured on counted views, not lifetime views (inferred, unverified). Then a post submitted at 3,500 TikTok views needs 5,000 more, about 8,500 lifetime.
- Our only view curve: mw4-08 had 8,041 views at 2.75 h and 8,509 later (n=1; 94% in the first 2.75 h). A post of that shape submitted after ~3 h has under 500 views left and cannot clear 5,000 counted. So traction gating only works if the check happens within roughly the first hour. A day-later gate would forfeit nearly every post that matters.
- Dollar scale at an mw4-08-sized hit: 8.5k views × $2.50/1k (TDR) = about $21 if fully counted, about $13.75 if submitted at 3k views, $0 if submitted at 4k views (4.5k counted, under the bar). At MW4's $1.50/1k, the $12.75 in the 10/28 brief.

**Cost of wasting a slot:**
- Realized: mw4-08 (8.5k views, the only hit) was refused because MW4 already held 3 posts with 0, 128 and 0 views. The slots went to the first posts live, not the best ones. Forgone value about $12.75 at MW4's rate, if the budget had lasted.
- Structural: if (b) is true, a dud holds its slot until it reaches 5,000, which it will not (TikTok median 244 views, 1 of 8 posts at 5k+, n=8, from the 10/28 brief). Three duds take 100% of a campaign's submission capacity for its remaining life. P(at least one of 3 random posts clears 5k) ≈ 1 − (7/8)³ ≈ 33%, a crude figure from n=8.
- Cost of the reserve slot: one fewer immediate submission. Cost of not using it: a late hit that is unsubmittable, as happened with mw4-08.
- Scale check: a hit is worth about $10-$20 gross. This is a data business, not a pay business, until a post is approved and pays out.

## 3. If William ever asks Vyro support (DRAFT ONLY, nothing sent)
Ask these in one ticket (app.vyro.com/support), in this order:
1. What triggers review of a pending post: a views threshold, queue order, or client batches? What is the typical wait for a first-time clipper? Does a post need 5,000 views before it can be approved?
2. Does the 5,000-view bar count views from submission, or lifetime views on the platform?
3. If a pending post is approved later, do the views it gained while pending become eligible for payout, or only views after approval? What does "Waiting for views · N / 5,000" count?
4. Is the 3-pending cap per campaign across all connected accounts? Does deleting a pending submission free the slot at once, and does it carry any penalty? Can the same post be resubmitted after deletion (and do its views then count only from resubmission)?
5. Pending posts in a campaign that is locked or out of budget: are they ever reviewed? Do they earn anything?
6. Separate, and risky: is scheduling via Buffer, plus William submitting links, acceptable under the Clipper Terms line "promote or advertise ... through spam (e.g., mass messaging, comment spam, or automated posting)"? Our submissions have been browser-automated, so this question exposes that. William should decide whether to ask it, and whether to switch to manual submission first. The existing draft is outbox/vyro-support-draft.md (not read here).
Questions 1-5 are safe mechanics questions. Question 6 is the one that could change how we operate; do not bundle it unless William wants an answer on it.

## 4. What I could not verify, and access limits
- Whether approval depends on 5,000 views (the whole of (b) part 2). No Vyro page says either way; no approval has happened to us.
- The value of N in the modal, and what the My-campaigns card "Views" counts. I could not open the app (instructed not to).
- Whether pending-period views become eligible after approval; whether the 5,000 bar counts from submission.
- Whether deleting submissions has hidden costs, and whether a deleted post can be resubmitted.
- Help-center article https://vyro.com/help/clips-and-content/how-will-i-know-when-my-clip-is-approved returned only its title and date, no body text. I used the one-line summary on the Clips & Content index instead.
- Not read: Vyro help sections Getting Started and Account & Security, and the Vyro Terms of Service. No third-party reports of real approval timing were checked here; Scout found none on 10/24 (PLAN.md).
- Help-center pages carry dates between Aug 21 and Oct 1, 2026; the campaign dialogs were read 10/22-10/23. Either could have changed since.
- First-hand evidence is small: n = 6 submissions in the modal (3 MW4, 3 TDR; 3 TDR ones deleted tonight), 0 reviewed, 5-6 days. Confounders: campaign, platform, new account, view counts under 400 on every submitted post.

## 5. Update 2026-10-28 ~8:40 PM ET (Morpheus): answers from Vyro's in-app AI help agent, plus one measurement
William approved sending the mechanics questions (1-5; question 6 on automation was NOT asked). Vyro's support front door is an AI chat ("Vyro Help", bottom-right of app.vyro.com); I asked it questions only, with no account actions. These are an AI agent's answers, not an official policy page, and it answered "I don't have information about that yet" on the deletion question (a human escalation, "Contact us", was not used).
- **Approval trigger:** "Approval is based on view count, not a client review queue: a clip needs to reach the minimum of 5,000 views before it can be approved." Also: review "can take a few days", views count from submission. -> (b) now SUPPORTED by Vyro's agent (still not an official page; our 0 approvals in 5-6 days fits).
- **What counts toward 5,000:** "only counts views gained after you submit the post to Vyro" (example: 100 views at submission, 1,000 now -> Vyro counts 900); the "Waiting for views - N / 5,000" counter is that same post-submission count.
- **Retroactive eligibility:** once approved, "payout is calculated from the point it was submitted, not from the point of approval", so views gained while pending are eligible if budget was available.
- **Locked campaigns:** locking only stops new submissions; already-submitted pending posts are still reviewed and keep counting toward the budget; if the budget runs out it is "prorated across all clippers who already joined", so a pending post can still earn on the views it accumulated.
- **Not answered:** 3-pending cap across accounts, whether deleting a pending submission carries a penalty, whether a deleted post can be resubmitted.
- **Measurement (free check from section 1c, done):** mw4-01 TikTok row in the MW4 modal shows N = 78; TikTok itself shows 128 views (yt-dlp, 8:35 PM). So Vyro counts views while a post is pending (the 50-view gap is consistent with Vyro's hourly refresh lag, "Next update in 33m", plus the ~15 min before submission). The earlier TDR row (tdr-02 TikTok) showed 75 at deletion vs 302 on TikTok now, same pattern. n=2.
- **Consequences for strategy:** (1) late submission forfeits views (pre-submission views never count), so submit at post time, not 24 h later; traction-gating at 24 h would forfeit most of a hit's views. (2) Pending posts in locked MW4 can still earn if they reach 5,000 counted views (unlikely: 128 / 0 / 0). (3) We can read TikTok views for any public post without a login: `~/openclaw-sites/ytdlp-venv/bin/yt-dlp --skip-download --print "%(view_count)s" <url>`.
