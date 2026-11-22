# BUILD BRIEF — news-image-20261122

Competition: news-image-20261122 — "Sum up 22 November's world news in one image"
Protocol: agent-fun/program/v1. Opens 2026-11-22T00:00:00Z, deadline
2026-11-24T00:00:00Z, results due 8 Dec 2026 15:00 WIB.
Free entry, $100 pot, top 50 paid (1st $20). 826 submissions already in
when the bounty was found. Kit bundle_sha256
00314c2cb5a445fd508bab7f92ae6a1a15dec902d84b7c9dcaa326beafe638bb.
NON-strict: transcripts_witnessed applies False — BUNDLE flow (transcripts
uploaded as bundle/loose files), do NOT use `makefun record` (HTTP 400).

## Judge criteria (RULES.txt, most important first)

1. One day's news, names that day: specific events of THAT day, date shown.
   -> Masthead: THE WORLD TODAY / SUNDAY 22 NOVEMBER 2026, footer repeats
   "ALL SIX STORIES HAPPENED OR WERE FIRST REPORTED ON SUNDAY 22 NOVEMBER
   2026". Every panel is a 22 Nov event or a development first reported
   on 22 Nov; Saturday items are kept in a separate "IN BRIEF - SATURDAY"
   box, honestly dated.
2. Selection and breadth: most consequential stories, across regions/fields.
   -> Six stories: Ukraine war (Europe), Gulf escalation (Middle East),
   Hong Kong vote (Asia), COP31 climate (global), Baltic ship attack
   (Europe), Estonia border (Europe). Plus two Saturday briefs (EU trade,
   Mexico capture).
3. Reads: viewer can tell what happened from the image alone.
   -> Big headlines + one plain caption per panel, no jargon, numbers in
   the subhead of the lead.
4. Faithful: what happened, as reported, no hype or speculation as fact.
   -> Numbers as reported by the sources below; the Gulf story says
   "Tehran claims" vs "Bahrain says" (conflicting accounts kept separate);
   the Peru quake (20 Nov) and the EU-Indonesia signing (21 Nov) were
   deliberately NOT used as 22 Nov stories.
5. Craft: one clear composition, legible at ~300px, no garbled text.
   -> Newspaper front page, flat clean vector art, hand-written 5x7 font,
   generous spacing, short words only.

## The news of Sunday 22 November 2026 (verified by web search)

1. UKRAINE (lead): Russia fired 50+ missiles and about 500 drones
   overnight Saturday into Sunday morning; five killed, including a
   family of four near Lviv; Poland scrambled jets as missiles neared
   its airspace. (Zelensky via The Times / usfijitimes, 22 Nov.)
2. THE GULF: Iran's IRGC claims missile and drone strikes on US Patriot
   radars at the al-Riffa and Awali bases in Bahrain; Bahrain says its
   defences intercepted the attack; a fire broke out at a civilian
   industrial compound, no injuries. Claim first reported Sunday.
   (Al Jazeera via webindia123, published 22 Nov 04:11 IST; euronews.)
3. HONG KONG: Voting begins Sunday for 723 contested seats on the
   1,500-person Election Committee; 856 candidates, 5,700 voters, polls
   9 AM to 6 PM. (Hong Kong Government, info.gov.hk; World Today Journal.)
4. COP31: UN climate talks deadlocked over fossil fuels and finance as
   the summit nears its end. (BBC, 22 Nov.)
5. THE BALTIC: Drones hit a Russia-bound cargo ship in the Gulf of
   Finland; Finland tightens security. (Times of India, 22 Nov; BBC.)
6. ESTONIA: Estonia to close its border with Russia; Moscow decries a
   "new Iron Curtain". (22 Nov headlines.)
Briefs (labelled SATURDAY): EU and Indonesia sign the IEU-CEPA trade
pact after 10 years of talks, scrapping tariffs on 98% of goods
(Reuters, signed Sat 21 Nov; presser Sun 22 Nov). Mexico captures FBI
most-wanted drug lord Fausto Isidro Meza Flores ("Chapo Isidro") in
Sinaloa; eleven killed (4 soldiers, 7 gunmen) (Reuters/CNN, announced
Sat 21 Nov).

## Build

- main.py, Python 3 stdlib only (no PIL, no network): hand-written 5x7
  bitmap font + pure-stdlib PNG encoder. Draws entry.png 1024x1024,
  <=1 MiB, deterministic (same bytes every run).
- Everything drawn from code. No downloaded/copied images.
- README.md (3 live make.fun badges + bounty link), LICENSE (MIT),
  .makefun/owner.json (wallet GkjG2osAv75kBkH7he6NeR2v19Dah1mCG9GAxtpYEKvn),
  .gitignore (excludes out/ and entry.png).

## Verification (this session, 22 Nov 2026 ~08:00 WIB)

- Ran main.py twice into separate output dirs: sha256 identical both runs.
- entry.png sha256:
  7d5db12748b14b3da490f51651c49fd24453ecda9331ebd5574613684d222c49
- Size: 25,200 bytes (<= 1,048,576). Dimensions: 1024 x 1024.
- Visual check: read the rendered image — masthead, dateline, all six
  panels, briefs and footer legible, no overlapping or clipped text.
  Two layout revisions made in-session: row heights rebalanced and the
  briefs box restructured (label on its own line) after the first render
  clipped the Mexico brief.
- git init -b main done locally; NOT committed (commit happens after the
  user creates the public repo lycann666/news-image-20261122).
- NOT pushed, NOT bundled, NOT checked, NOT submitted — parent handles
  repo creation, push, About, bundle, check and submit.

## Next step for parent

User creates empty public repo lycann666/news-image-20261122 (after
opens_at 2026-11-22T00:00:00Z — already open), then: commit + push this
directory (without out/), set About (website = bounty link, topic
makefun), bundle with prompt file
~/workspace/makefun/news-image-20261122-prompt.txt and flags
--mcp none --harness muse-app --harness-version 1 --provider ipnext
--model ipnext/avocado-5.17-v2 --effort default, check, submit.
Deadline 07:00 WIB 24 Nov 2026.
