# TikTok multi-account research (Scout, TikTok side)

Date: 2026-10-26. Read-only research. No accounts created, nothing posted, nothing signed up.
Scope: what TikTok's own docs allow, what is risky, what is prohibited. Ban-evasion methods (fingerprint spoofing, device farms, proxy rotation) are out of scope. They exist as a topic in the community and are ban-evasion territory. Not researched or recommended here.

Verification key: **[verified]** = read on the cited page today. **[unverified]** = could not load the source or the source is silent. **[folklore]** = community claim with no official source.

---

## Source access problems (read this first)

- TikTok Community Guidelines, "Integrity & Authenticity" (tiktok.com/safety/en/policies-and-engagement/integrity-authenticity): fetch returned only the page header; body was cut off at 750 KB. The spam, duplicate-content and coordinated-behaviour sections are **[unverified]**.
- TikTok Creator Rewards / Creator Fund eligibility pages (creator-academy and creator-portal URLs) redirected to a generic landing page with no eligibility text. Section 5 is **[unverified]**.
- TikTok support pages on multiple accounts (support.tiktok.com/...managing-multiple-accounts, /multiple-accounts) returned empty content. Official multi-account and per-device rules are **[unverified]** from TikTok's help centre.
- TikTok's Terms of Service (Other regions, last updated 1 Dec 2025) loaded. Relevant clauses are below.
- TikTok for Developers pages (Direct Post, Query Creator Info) loaded. These are the best official sources in this report.
- Buffer pricing page loaded (fetched 2026-10-26).
- No live web search tool was available to me; I did not run broad community searches, so section 4 leans on what the official docs say and is marked accordingly.

---

## 1. TikTok's rules on multiple accounts

- **[verified] Terms of Service, General Terms, All Users** (https://www.tiktok.com/legal/page/row/terms-of-service/en, last updated 1 Dec 2025):
  - "Our Services are provided for private, non-commercial use." The Terms are written for personal use. Commercial use requires express written consent. Several accounts run as a business operation sit uneasily with this. The clause is general, so this is a reading, not a direct ban on multiple accounts.
  - You must "create an account" with accurate information. You may not "use or attempt to use another's account... or create a false identity."
  - "You agree that you are solely responsible... for the activity that occurs under your account."
  - TikTok may disable an account "at any time," including for activity that "might cause damage... or violate any applicable laws."
- **[unverified] Multi-account, per-device and per-person limits.** TikTok's help centre pages on this did not load. I could not confirm any stated cap on accounts per phone or per person.
- **[unverified] Business vs personal accounts.** The TOS language above suggests business use is a separate matter. Whether TikTok offers a Business Account that is the proper route for brand/client accounts needs checking on the TikTok for Business / help pages.
- **[unverified] Phone-verification and email requirements.** Not checked against an official source.

## 2. Policies that hit this model

- **[verified] Spam, commercial use, and automation (TOS, All Users):** The Terms prohibit using the Services "without our express written consent, for any commercial or unauthorized purpose... or spamming." They also prohibit "use automated scripts to collect information from or otherwise interact with the Services," and any "unsolicited or unauthorised advertising... 'spam,' 'chain letters'."
- **[verified] Account-level enforcement (TOS):** TikTok may disable accounts for violating the Terms or for activity that "would or might cause damage to or impair the Services." Enforcement is at TikTok's sole discretion.
- **[verified] Developer side (Direct Post docs):** The Content Posting API returns these error codes for enforcement:
  - `spam_risk_too_many_posts`: daily post cap reached for the user.
  - `spam_risk_user_banned_from_posting`: user banned from posting.
  - `reached_active_user_cap`: client's daily active-publishing quota reached.
  - `privacy_level_option_mismatch`: docs note that repeated occurrences "suggest violations to TikTok's product-use guidance."
- **[unverified] Duplicate or unoriginal content across accounts, reposting, coordinated accounts.** The Community Guidelines' integrity page would have covered these. I could not read it. Do not rely on any claim about it until someone reads the full page.
- **[folklore] What actually gets accounts limited or removed.** Creator reports on forums commonly cite: same video uploaded from several accounts, identical captions across accounts, many accounts sharing one device or network, and mass reposting of others' clips. None of this is verified against TikTok's own text. Treat it as hypothesis only.

## 3. Posting routes for several accounts

**TikTok Content Posting API (Direct Post)** [verified, developers.tiktok.com]
- Requires an app registered on TikTok for Developers, the Content Posting API product, and the `video.publish` scope approved for the app. Each target user must authorise the app for `video.publish`. The access token and open ID belong to the user who authorised.
- **Unaudited clients can only post privately.** Posts from unaudited clients are restricted to private viewing. Going public requires a client audit against TikTok's Terms. Audit page at developers.tiktok.com/application/content-posting-api returned a login wall; audit criteria are **[unverified]**.
- Rate limits: query creator info is 20 requests per minute per user token. Direct Post init is 6 requests per minute per user token.
- The creator must choose the privacy level from `privacy_level_options` returned by the API. Clients must display these options and honour the choice. This means the user (the account owner) approves each post. Fully automated posting that skips the user's per-post choice is outside the documented flow.
- Media: FILE_UPLOAD (chunked upload) or PULL_FROM_URL (requires a verified domain or URL prefix).
- Branding fields: `brand_content_toggle` (paid partnership) and `is_aigc` (AI label) exist. Paid-partnership disclosure is an official field, so use it for sponsored clips.

**Buffer** [verified, buffer.com/pricing, fetched 2026-10-26]
- Free: up to 3 channels, 10 scheduled posts per channel at a time, 1 user.
- Essentials: $5/month per channel billed yearly ($60/yr per channel), unlimited scheduled posts per channel. Team: $10/month per channel billed yearly ($120/yr per channel), unlimited scheduled posts, unlimited team members, approval workflows.
- Buffer prices per channel, so N accounts = N channel fees.
- Buffer's daily posting limit per TikTok account is **[unverified]**. The pricing page does not state it.
- Buffer's own TikTok integration limits, and whether it is an approved TikTok partner for Direct Post, are **[unverified]**. Check its TikTok help pages before relying on it.

**Other schedulers:** not checked in this pass.

Practical note, marked as my reading: any route that posts to several accounts from one API client will hit the audit gate. The audit gate needs a live app with its own privacy policy and Terms compliance, and TikTok's audit form was not readable to me.

## 4. Separate hardware or one device

- **[unverified, no official statement found]** TikTok's docs I could load say nothing about devices or hardware for multiple accounts. Device-based rules, if any, sit on the help pages I could not read.
- **[folklore]** Forum claims that TikTok flags accounts that share a phone or network, and that separate hardware is needed. No official source confirms either.
- Note for planning: the API route does not depend on device at all. Its controls are per-user token, per-user daily cap, and the audit. Any device- or network-based approach to avoid detection is ban-evasion territory and is excluded from this report.

## 5. Monetisation and eligibility

- **[unverified] Creator Rewards / Creator Fund eligibility:** official pages did not load. I cannot state current follower, view, or age thresholds from a verified source. Creator Rewards is reportedly tied to a single account's eligibility, so each account would need to qualify on its own. Treat this as unverified until read on TikTok's Creator Academy or Creator Rewards page.
- **[unverified] View-based campaign payouts:** not researched in this pass. Campaign platforms (Vyro etc.) set their own rules, including whether multiple accounts are allowed. Those rules are in the campaign terms and must be read per campaign.
- **[unverified]** Whether a Business account changes monetisation eligibility.
- Note for the project: campaign platforms often forbid the same clip posted to more than one account. That rule is more likely to bite than TikTok's own, so check each campaign's terms before any multi-account plan.

---

## Top 5 findings

1. **Unaudited API clients can only post privately.** Public posting through the Content Posting API needs a TikTok client audit. The audit form was unreadable here. (Verified: Direct Post docs.)
2. **The API requires per-post user consent.** The creator sees and chooses privacy options each time. A fully automated pipeline that bypasses this is outside the documented flow. (Verified: creator_info docs.)
3. **The Terms restrict personal use and forbid spam and automated interaction.** Several accounts run as a business operation is a grey zone under the Terms. (Verified: TOS.)
4. **Buffer prices per channel** ($5 or $10 per channel per month on yearly billing). Several accounts means several channel fees. Its TikTok posting cap is unverified. (Verified pricing; cap unverified.)
5. **Most of what decides enforcement is unverified.** The integrity/duplicate-content rules, multi-account limits and Creator Rewards eligibility did not load. Do not act on them until read.

## Rule conflicts and gaps

- **TOS "personal, non-commercial" vs. the business model.** The Terms say the Services are for private, non-commercial use, yet the clip model is commercial (paid campaigns, sponsorship). This is a conflict unless TikTok's business account terms cover it. Unresolved.
- **API per-post consent vs. scheduler automation.** The API requires the creator to pick privacy options per post. Scheduled, unattended posting is a gap between this and the Buffer model. Unresolved.
- **Campaign terms vs. multi-account posting.** Campaign platforms may forbid the same clip on several accounts. Unverified per campaign.

## Next steps (for Morpheus to decide)

- Read the full Community Guidelines integrity page (try a browser session, not web_fetch) and the TikTok help pages on multiple accounts.
- Read the TikTok Creator Rewards eligibility page.
- Check the Content Posting API audit criteria before any app is registered. Registration is outward-facing, so this needs your explicit go-ahead.
- Check the campaign terms for any multi-account rule before posting the same clip to two accounts.

Sources (dates as fetched 2026-10-26):
- https://www.tiktok.com/legal/page/row/terms-of-service/en (last updated 1 Dec 2025)
- https://developers.tiktok.com/docs/en/content-posting-api-get-started (last updated 4 Aug 2026)
- https://developers.tiktok.com/docs/en/content-posting-api-reference-direct-post
- https://developers.tiktok.com/docs/en/content-posting-api-reference-query-creator-info
- https://buffer.com/pricing
- Unavailable: tiktok.com/safety/en/policies-and-engagement/integrity-authenticity (truncated), TikTok creator-academy and support pages (no content), developers.tiktok.com/application/content-posting-api (login wall)
