Here’s an updated Dev Log & Project Spec, split cleanly between the scraper side and the LLM categorization work:

⸻

Facebook Group Scraper — Dev Log & Project Spec (concise)

Scope & Goal
	•	Goal: Parse a saved HTML snapshot of a Facebook group post page and extract compact JSON describing post, media, reactions, and comments.
	•	Input: Full-page HTML at
/Users/buddy/Desktop/projects/facebook_scraper/data/fb_group_raw.html
	•	Script:
/Users/buddy/Desktop/projects/facebook_scraper/scripts/parse_raw_html.py
(Python + BeautifulSoup / bs4)

⸻

Current Scraper Output (shape)
	•	record
	•	gid: group id (from /groups/<gid>/…)
	•	uid, author: poster’s user id and display name
	•	story: canonical story/post href (cleaned)
	•	text: main post text (de-“See more”)
	•	privacy: fixed "private_group"
	•	ts: currently null (no stable absolute timestamp yet)
	•	media[]: { fbid, set, img } from scontent- images
	•	reacts: map of reaction counts {like, love, …, total}
	•	comments_ct: derived count
	•	comments[]: { cid, name, uid, text, rel_ts }
	•	inspect (debug/forensics)
	•	permalink_anchors[]: { cid, rel_ts, href, parent_html_excerpt }
	•	group_user_links[]: { uid, name, href }

⸻

Scraping: Normalization & Compaction
	•	URL handling: strip domain, keep relative paths; whitelist query params.
	•	Group user hrefs: normalize to /groups/<gid>/user/<uid>/.
	•	HTML excerpts: remove heavy attrs, collapse whitespace, cap length (~220 chars).
	•	Post text: longest meaningful block, strip “See more”.
	•	Media: detect scontent- images; infer fbid heuristically.
	•	Reactions: regex scan labels+counts.
	•	Comments: anchor via comment_id=…, climb DOM to author + text, capture relative time.

⸻

Scraping: What We Know About FB Group Page Structure
	•	Articles: div[role="article"] with nearby /stories|/posts anchors.
	•	Group context: /groups/<gid>/…; members as /groups/<gid>/user/<uid>/.
	•	Story/permalinks: /stories/<id>/…, /groups/<gid>/posts/<id>.
	•	Authors: user anchors with aria-label/text, uid in /user/<uid>/ or profile.php?id=.
	•	Text blocks: [data-ad-preview="message"] + div/span[dir="auto"].
	•	Images: scontent-* CDNs; noisy params removable.
	•	Noise: attributionsrc, __cft__, __tn__ ignorable.

⸻

Scraping: Assumptions & Limitations
	•	Works on saved HTML; no live requests or JS.
	•	Captures relative timestamps only.
	•	DOM structure volatile; selectors may drift.
	•	Media.fbid inference heuristic only.

⸻

Scraping: Script Highlights
	•	simplify_href() → cleans and normalizes links.
	•	compact_html_excerpt() → trims parent snippets.
	•	find_article_root() → anchors to /stories|/posts.
	•	extract_* → modular parsing.
	•	CLI supports --out (default stdout).

⸻

Scraping: Recent Improvements
	•	URL truncation across story/comment/group links.
	•	Deduplicated + compact group_user_links.
	•	Leaner inspect.parent_html_excerpt.

⸻

Scraping: Next Steps
	1.	Absolute timestamp parsing.
	2.	Media normalization (canonical version).
	3.	Better post boundary selection.
	4.	Threaded/reply comment support.
	5.	Error reporting in inspect.
	6.	Snapshot-based unit tests.

⸻
