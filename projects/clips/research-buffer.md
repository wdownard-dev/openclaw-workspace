# Research: Buffer (free plan) + YouTube Shorts / TikTok / Instagram Reels for the Vyro MW4 campaign

Researched 2026-10-22 (read-only; no accounts created, nothing signed up, nobody contacted). Pages were fetched 2026-10-22/23 unless a page states its own date. "Unverified" means I could not read a primary source or sources conflict.

Vyro campaign requirements this has to satisfy: #MW4 and #MW4partner (or the platform's native paid-partnership label), comments ON, no collab or tags, posts stay public, every post submitted to Vyro.

---

## Bottom line and recommended setup order

**It works on the free plan, with two caveats.** One Buffer free account holds 3 channels (one YouTube, one TikTok, one Instagram), each with 10 scheduled posts at a time (refill as they publish). Buffer can auto-publish a plain vertical video with caption and hashtags to all three. Buffer cannot set the native paid-partnership toggles on any of them, so use the #MW4 / #MW4partner hashtags, which Vyro accepts. Caveats:

1. **Vyro's Content Requirements ban promoting a campaign through "spam (e.g., mass messaging, comment spam, or automated posting)"** (https://vyro.com/content-requirements, section 10). The context is spam, and scheduling your own clips is probably fine, but "automated posting" is named. Ask Vyro support before building automation: https://app.vyro.com/support. Unverified how they read it.
2. **The Buffer API has no file upload.** It only takes a public HTTPS video URL. The MW4 source clips would have to sit on a public host (Cloudflare R2, Cloudinary) until each post publishes. Check the campaign's rules on re-hosting footage before doing that. The web composer (drag-and-drop upload) has no such constraint.

**Setup order**
1. Ask Vyro support (item 1 above), and re-read the MW4 brief for per-platform restrictions. William's decision.
2. Create or convert the accounts: a YouTube channel (verify it, see section 1), a public TikTok, and an Instagram account switched to Creator or Business (Professional). Keep all three public.
3. Link the accounts to Vyro first (OAuth, section 5), so Vyro can see them.
4. William signs up to Buffer Free, connects the three channels in a desktop browser, and uses the Instagram-login route for Instagram.
5. Do one test post per platform through the composer in Automatic mode, using a real campaign clip. Confirm on each platform that: it is public, comments are on, the hashtags are live, and there are no collaborators or tags. Then submit each URL to Vyro.
6. Only then add the API (free key, 3,000 requests/month). Test `channels`, then one `createPost` with a video URL on one channel.
7. For new accounts, post 1 to 3 times a day per platform at most (Buffer's own advice for TikTok). Ramp slowly.

---

## 1. Account type and connecting

### Buffer + YouTube Shorts
- **Requirement:** a YouTube channel where you sign in to Google as the channel **Owner**. A Manager role on a Brand Account does not work. Newly created channels may need a day or two before Buffer can connect them. Buffer supports Shorts only, not long-form.
- **Verify the channel.** Unverified users are limited to 10 posts per 24 hours and cannot put external links in descriptions. Verified users have no limit.
- **Plan:** Shorts scheduling is on Buffer's current plans, free included (the Free plan lists "YouTube (Shorts)": automatic and notification publishing).
- **Connect:** log in to the owner Google account in one tab, then Buffer, Channels, Connect Channel, YouTube. Accept all permissions. If you decline analytics permission, you only get data from the day you connect.
- Sources: https://support.buffer.com/articles/using-youtube-shorts-with-buffer-Jl8iR6jIck.md ; https://support.buffer.com/articles/connecting-your-channels-to-buffer-HvWLgAJvL9.md ; https://buffer.com/pricing.md

### Buffer + TikTok
- **Account type: sources conflict.**
  - Buffer's current TikTok landing page FAQ says a Business account is **not** required and "Buffer supports both business and personal TikTok accounts", though TikTok may limit features by account type or region (https://buffer.com/tiktok).
  - Buffer's 2022 launch blog said a TikTok business account was needed (https://buffer.com/resources/tiktok-scheduling).
  - The pricing-page feature table still says "TikTok business profiles" for automatic publishing (https://buffer.com/pricing.md).
  - **Practical read:** try the normal account first; if Buffer refuses, switch to a Business account in the TikTok app (Settings and Privacy, Account, Switch to Business Account; per the 2022 blog, not possible from TikTok web). Unverified which one applies today.
- **Connect:** log in to the TikTok account in one browser tab, then Buffer, Channels, Connect Channel, TikTok. Approve all permissions it offers. If it disconnects later, reconnect (TikTok can expire publishing permission after security or account changes).
- **Age/follower minimums:** none stated in any Buffer page I read. Unverified for TikTok itself.
- Sources: https://support.buffer.com/articles/using-tiktok-with-buffer-oGEroY9Of2.md ; https://buffer.com/tiktok

### Buffer + Instagram Reels
- **Account type:** Instagram **Professional** (Creator or Business) for automatic publishing. A Personal account connects but is notification-only (reminder to phone, you finish posting by hand). Personal accounts also get no analytics or comments in Buffer.
- **Facebook Page link: not required.** Three connection routes:
  - Personal ("Setup a Personal account"): notifications only.
  - Professional via Instagram login: all plans, **recommended by Buffer for the Free plan**. Gives auto-publish, analytics and comment management. No locations, collaborators, liking mentions, or music on Reels.
  - Professional via a linked Facebook Page: needs Full control of a Page linked to the Instagram account, and 2FA on that Facebook account if the Page enforces it. Only needed for locations, collaborators and music.
  - The campaign forbids collab and tags, so the Instagram-login route is enough.
- **Follower/age minimums:** none stated by Buffer. Unverified for Instagram itself.
- **Gotcha:** Buffer connects whichever Instagram account is logged in in the browser (no account picker). Log in as only the account you want, ideally in a private window. Since April 2026, Meta lets several Instagram accounts share one login, and Buffer may then show only one; log out and back in as the target account (Buffer help, citing https://about.fb.com/news/2026/04/meta-account/). Instagram allows 5 active accounts per device.
- To convert a Personal account: Instagram app, menu, For professionals, Account type and tools, Switch to professional account. Choose Creator or Business.
- Sources: https://support.buffer.com/articles/connecting-your-instagram-account-to-buffer-n9Ad6veXsu.md ; https://support.buffer.com/articles/using-instagram-with-buffer-YSjg2dXFV8.md

**Free-plan channel limit:** 3 channels at once, and a lifetime cap of 8 distinct channels per network on Free (https://support.buffer.com/articles/connecting-your-channels-to-buffer-HvWLgAJvL9.md). Do not churn test accounts through Buffer.

---

## 2. Automatic publishing vs reminder only

| | Automatic publish | Reminder (notification) only |
|---|---|---|
| YouTube Shorts | Yes. Video up to 3 min. | If you pick "Notify Me", the video is over 3 min, or you want YouTube library sounds. |
| TikTok | Yes, many videos, when they meet TikTok's publishing requirements. | Videos over 10 min; anything needing trending sounds, polls or in-app effects. |
| Instagram Reels | Yes, on a Professional account, if the video is within Instagram's aspect-ratio range (4:5 to 9:16 for Reels). | Personal accounts always; out-of-range videos; music (unless connected via Facebook), stickers, links, product tags, topics. |

- The composer has an **Automatic / Notify Me** choice per post. A channel setting "Enable Notifications by default" can silently turn everything into reminders. Check it is off, since reminder posts show an orange phone icon in the queue.
- Notification publishing needs the Buffer mobile app and push notifications on. A missed notification leaves the post saved but unpublished.
- That setting "will only apply to posts created directly in Buffer", not to posts made through Zapier or Make.
- Sources: https://support.buffer.com/articles/using-notification-publishing-gvZQiMxVa2.md ; https://buffer.com/pricing.md (channel feature table: Instagram Business/Creator and TikTok business profiles and YouTube Shorts list both Automatic and Notification publishing; Instagram Personal is notification only).

---

## 3. Supported fields and file limits

### YouTube Shorts (Buffer web composer)
- **Title:** max 100 characters. Auto-filled from the first line of the caption until you edit it manually.
- **Description/caption:** up to 5,000 characters. Hashtags are typed into it and become links.
- **Thumbnail:** custom thumbnails **not** supported.
- **First comment:** not offered for YouTube (Buffer's first-comment feature is listed for Instagram, Facebook, LinkedIn; and is paid-only).
- **Category:** the help article says Buffer does not support changing the category and YouTube assigns it automatically. **But the API schema lists a category field** (YoutubePostMetadataInput; IDs include 20 = Gaming, 24 = Entertainment, "required on create; optional on edit" per the schema description), so via the API you can probably set Gaming. Not tested.
- **Paid promotion flag:** Buffer's YouTube metadata has no such field (fields: title, category, embeddable, AI-generated disclosure, license, made-for-kids, notify subscribers, privacy default public). **Not supported.** Options: rely on #MW4partner in the description, or tick it in YouTube Studio after publishing (unverified that Studio allows editing it after publish).
- Other API fields: privacy (default public), notifySubscribers (default true), madeForKids (default false).
- **Video:** up to 3 min, 10 GB or less, 1:1 or 9:16 (9:16 recommended), .mov .mp4 .mpg .mpeg .avi .WebM, one video per post.
- Sources: https://support.buffer.com/articles/using-youtube-shorts-with-buffer-Jl8iR6jIck.md ; https://developers.buffer.com/types/YoutubePostMetadataInput.html

### TikTok
- **Caption:** 2,200 characters. **Max 5 hashtags per post** (Buffer's limit). `#MW4 #MW4partner` fits, leave room for 3 more. Hashtags won't link in the composer but link once published. Typing an exact @handle creates a mention, so don't type any (campaign: no tags).
- **Title:** only for photo posts.
- **Cover:** a frame you pick in the composer ("Edit Thumbnail"). API: `thumbnailOffset` in ms.
- **First comment:** not supported on TikTok.
- **Branded content / paid partnership toggle: no evidence Buffer sets it.** Buffer's API TikTok metadata has only `isAiGenerated` (video) and `title` (photo). The Buffer TikTok help article never mentions it. TikTok's own rules say Direct Post clients must offer a content-disclosure toggle ("Your brand" / "Branded content" labelled "Paid partnership", https://developers.tiktok.com/docs/en/content-sharing-guidelines, updated 2026-08-04), so Buffer's composer may show one; I could not see the composer. **Unverified; check in the composer.** Fallback is the #MW4partner hashtag.
  - If Branded content is ever selected, TikTok says it cannot be private.
- **Comments on/off:** Buffer doesn't document a setting and the API metadata has none. TikTok's guidelines require clients to let users pick interactions, so the composer may have one. **Unverified.** Check on the first test post that comments are on.
- **Visibility:** Buffer says TikTok videos "publish publicly by default".
- **Video:** 3 s to 10 min, 1 GB or less, min 360 px height and width, MOV/MP4/WEBM, 23 to 60 fps recommended, one video per post. No Canva. No alt text.
- **No Promote** on posts sent through Buffer (Vyro bans paid boosting anyway).
- Sources: https://support.buffer.com/articles/using-tiktok-with-buffer-oGEroY9Of2.md ; https://developers.buffer.com/types/TikTokPostMetadataInput.html

### Instagram Reels
- **Caption:** 2,200 characters. **Instagram limits posts to 5 hashtags** (Buffer help). Same fit for `#MW4 #MW4partner`.
- **Title:** none.
- **Cover/thumbnail:** "Edit Thumbnail" slider (default first frame). Note: the pricing table lists "Custom video covers" as a paid-plan feature (Facebook, Instagram, TikTok) while the help article shows the slider with no plan note. **Conflict; unverified on Free.**
- **First comment:** supported for Reels, **paid plans only** (2,196 characters). Not available on Free.
- **Paid partnership label:**
  - Not in Buffer's Instagram metadata (fields: first comment, geolocation, AI-generated, Shop Grid link, share-to-feed, sticker fields, post type). So Buffer **cannot set it** as of 2026-10-23.
  - Meta added an API parameter `is_paid_partnership` (plus `branded_content_sponsor_ids`, up to 2 brand IDs) to Content Publishing in April 2026 (Meta blog 2026-04-22 and the Instagram Platform changelog, as summarized by search results; I could not fetch the Meta pages directly, so unverified at the source). Buffer has not exposed it. Watch https://developers.buffer.com/changelog.html.
  - Alternative: add the label by hand in the Instagram app after it publishes (Instagram's help page says app-only; I could not fetch it).
- **Collaborators:** up to 3, only via the Facebook-Page route. Don't add any.
- **Comments on/off:** no Buffer setting documented. Instagram defaults to comments on. Unverified, check the first post.
- **Reels video:** 5 s to 15 min, 300 MB or less, aspect 4:5 to 9:16, 25 Mbps video / 128 kbps audio max. Trial Reels exist; skip them (non-public).
- **Daily limit:** 50 posts per 24 h across posts, reels and stories.
- Sources: https://support.buffer.com/articles/using-instagram-with-buffer-YSjg2dXFV8.md ; https://developers.buffer.com/types/InstagramPostMetadataInput.html

**Free vs paid for this use case:** Essentials is $6/month per channel on monthly billing (about $5 on yearly; the pricing page itself shows both $5 and $6) and adds first-comment scheduling, hashtag manager, unlimited scheduled posts and 3 API keys. None of that is required for the campaign.

---

## 4. Gotchas for brand-new accounts

- **TikTok views:** Buffer's own FAQ says low or zero views are common in the first few weeks however you post. It says posts via Buffer get similar views to native posts, and that high-volume posting or automation (Zapier, Make, n8n, AI agents, the API) produces more zero-view posts. It advises 1 to 3 posts a day, original videos, no watermarks from other apps, no very short or GIF-only clips, no QR codes, and a public, fully set-up profile.
- **TikTok posting caps:** Buffer applies 25 posts per 24 h. TikTok's Direct Post cap is typically about 15 posts per day per creator account, shared across all API clients (TikTok developer guidelines).
- **TikTok private-only rule for unaudited clients:** TikTok restricts unaudited API clients to private posts and 5 users per day. Buffer's statement that videos publish publicly by default implies Buffer is audited. That is my inference, not a Buffer statement. Also note TikTok's rules say a tool that only uploads to accounts you or your team manage is not acceptable as an API client. That is why using Buffer, an existing audited client, is correct and building a direct TikTok API poster is not.
- **YouTube:** unverified channels get 10 posts per 24 h and no external links; a brand-new channel may not connect for a day or two.
- **Instagram:** 50 posts per 24 h cap; "Invalid session error 400" and wrong-account connects are the common failures. Linking via a Facebook Page is the fallback.
- **Review times / shadow limits:** no platform-published numbers found. Treat any claim of a "shadow ban" cap as unverified.
- **Platform rules on third-party scheduling:** all three connect through official APIs, which is permitted, but I did not read Meta's or YouTube's automation policies in full (Meta developer pages returned errors). TikTok's content-sharing guideline requires API clients not to add watermarks or promo text and to let users edit preset hashtags. Unverified for Instagram and YouTube beyond that Buffer uses the official APIs.
- **Vyro rule that bears on this:** see the first caveat above on "automated posting".

---

## 5. How Vyro handles TikTok and Instagram accounts

- **Linking method: OAuth through each platform's API, not a bio code.** Vyro's Clipper Terms (last modified 2025-12-20) section on Connected Accounts says you must connect the social accounts you use "through Instagram's API", and that this "may also apply to your YouTube, X, and TikTok accounts". You represent that you own or control the account. Vyro says each network required official review and approval of its integration, and you can disconnect any time (https://vyro.com/help/account-and-security/do-i-have-to-connect-my-social-media-accounts , updated 2026-08-21; https://vyro.com/help/account-and-security/is-linking-my-social-media-accounts-safe , updated 2026-09-02; https://vyro.com/clipper-terms).
- I found **no bio-code step in any Vyro page**. Bio-code verification appears on other clipping platforms (ClipCo, Clipping.net), not Vyro. Unverified for Vyro in practice; the in-app linking flow at https://app.vyro.com is authoritative.
- **Requirements stated by Vyro:** 18+, legal resident of a supported territory, at least one registered social account on an eligible platform, payment-processor onboarding for payouts. **No minimum followers, public-profile requirement or account-type requirement appears in the pages I read.** Vyro's one stated visibility point: for TikTok submissions, the video must be viewable globally (region/privacy settings can make submission fail).
- Vyro verifies "ownership" and pulls profile, media, and insight data through the APIs. That is probably why Professional (Creator/Business) Instagram accounts are needed in practice for insights, but Vyro does not say so. Unverified.
- **Posting rules from Vyro help:**
  - Up to 5 posts per social account, per campaign, per 24 h. Until a first approval in a campaign, at most 3 clips can wait for review.
  - Same clip on different platforms is fine. **Do not post the same video twice on the same platform, even across different accounts.**
  - Views count from the moment of submission. No paid boosts.
- Sources: https://vyro.com/help/clips-and-content ; https://vyro.com/help/clips-and-content/can-i-post-the-same-clip-on-multiple-accounts ; https://vyro.com/help/clips-and-content/im-having-trouble-submitting-my-post-on-vyro ; https://vyro.com/content-requirements

---

## 6. Buffer API

Docs: https://developers.buffer.com (guides fetched 2026-10-22).

- **What it is:** GraphQL at `https://api.buffer.com`. Free plan includes API access (1 API key, 1 OAuth app client).
- **Operations:** post create/delete/retrieve, idea create, account/organization/channel retrieval. Post metrics are readable with a personal API key.
- **Auth:** `Authorization: Bearer <API key>`, created at Settings, API in Buffer. The key acts for your whole account (all organizations and channels, no per-org scoping). For multi-user apps, OAuth 2.0 authorization code with PKCE; refresh tokens are single-use. Store the key as a secret, never in code.
- **Create/schedule a post:** `createPost(input: {text, channelId, schedulingType: automatic, mode: addToQueue | customScheduled, dueAt (ISO 8601 UTC), assets, metadata})`. Always select `... on MutationError { message }`. A full queue (10 on Free) returns a "queue limit reached" error.
- **Video:** `assets: [{ video: { url: "https://...", metadata: { thumbnailOffset: 2000 } } }]`. **There is no upload endpoint** (https://developers.buffer.com/guides/hosting-media.html). The URL must be:
  - public (no login, so Google Drive or Dropbox share links fail),
  - direct (the file itself, not a preview page),
  - HTTPS,
  - stable until the post publishes (Buffer fetches it at publish time; expiring or signed URLs can fail silently).
  Suggested free hosts: Cloudinary, Cloudflare R2.
- **Per-network metadata:** YouTube (title, category, privacy, etc.), TikTok (`isAiGenerated`, `title`), Instagram (`type: reel`, `firstComment` [paid plan only in the UI; whether the API enforces this is unverified], `shouldShareToFeed`, etc.). **No paid-partnership, branded-content or comment-toggle field exists** for any of the three.
- **TikTok via API: unverified.** `tiktok` is in the Service enum and in `PostInputMetaData`, but the Posts & Scheduling guide's "supported platforms" list names Instagram, YouTube and others and omits TikTok. Test with one post before planning around it.
- **Notification mode via API:** the schema mentions sticker fields "for reminder-based publishing", so a reminder mode exists; the exact `schedulingType` value is unverified. The guides only show `automatic`.
- **Rate limits (Free):** 100 requests per 15 min, **250 per 24 h**, **3,000 per 30 days**, per API key/client; MCP and AI-assistant connections share the key bucket. Responses carry `RateLimit` / `RateLimit-Policy` headers per window. Over the limit gives HTTP 429 with `Retry-After` (seconds); 429s don't consume quota. Query limits: complexity 175,000, depth 25, 30 aliases. Higher limits via developersupport@buffer.com. (Free-plan 24 h figure: 250 per both the pricing page and https://developers.buffer.com/guides/api-limits.md.)
- **Fit for this use:** 3 channels x a few posts a day is a handful of requests, so the limits are not a constraint. The 10-scheduled-posts-per-channel cap and the public-URL requirement are.
- Also listed: official integrations with Zapier, Make, n8n, Claude, ChatGPT, Cursor and others (https://developers.buffer.com/guides/integrations.html). Not evaluated here.

---

## Open items for William

1. **Decision:** is scheduler-based posting acceptable to Vyro given the "automated posting" wording? Ask support (https://app.vyro.com/support) before building automation. Hand-scheduling in the Buffer web composer is lower risk than API automation, but I can't say either is covered.
2. Check in the live Buffer composer (after signing up): TikTok account type accepted; whether TikTok disclosure and comment settings appear; whether "custom video cover" is allowed on Free; how comments are set on each platform.

## Key sources (all fetched 2026-10-22/23)
- Buffer pricing: https://buffer.com/pricing and https://buffer.com/pricing.md (page says prices last updated Nov 2025)
- Buffer help: Using Instagram / TikTok / YouTube Shorts, Connecting your channels, Connecting Instagram, Using notification publishing, Daily posting limits (URLs inline above)
- Buffer API: https://developers.buffer.com/guides/getting-started.html , /authentication.html , /your-first-post.html , /posts-and-scheduling.html , /hosting-media.html , /api-limits.md , /examples/create-video-post.html , /types/PostInputMetaData.html , /types/TikTokPostMetadataInput.html , /types/YoutubePostMetadataInput.html , /types/InstagramPostMetadataInput.html , /types/Service.html
- TikTok: https://developers.tiktok.com/docs/en/content-sharing-guidelines (updated 2026-08-04)
- Vyro: https://vyro.com/clipper-terms (2025-12-20), https://vyro.com/content-requirements, Vyro help articles (updated Aug/Sep 2026)
- Could not fetch (Meta returned errors): Meta developer blog 2026-04-22, Instagram Platform changelog, Instagram Help Center branded-content page. Facts from those come from search-result summaries only.
