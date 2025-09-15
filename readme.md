# WGU Accelerators – Prototype Data Explorer

This project is a **prototype** for exploring posts from the WGU Accelerators Facebook group.  
The dataset (217 posts, Sep 1–14) was **scraped manually** as a proof of concept.  
Only **top-level text posts** were included (no comments, images, or video).  
Usernames were anonymized and replaced with incremental IDs.

The goal is to demonstrate **LLM classification and clustering** for topic analysis.  
True automation would require Facebook admin privileges and a verified Facebook app (see below).

---

## Interacting with the Data

[View the data here](https://wgudataninja.github.io/fb_categorize_posts/) The viewer supports:  
- **All Columns**: every column, including **sentiment**, the LLM’s category assignment, rationale, and confidence  
- **LLM-Friendly view**: simplified view showing only category and text.  
- **Sorting**: click column headers to sort.  
- **Download**: use "this data as" links to export any view as CSV or JSON.  

---
## Sentiment

We used **VADER sentiment analysis** to score each post from **−1 (negative)** to **+1 (positive)**.  
Trained on social media text, VADER works well here.  
Sort by sentiment to see the most positive or negative posts.  

___

## Categorization

We used **ChatGPT 4o-mini** to classify posts into broad themes.  
Each classification includes a confidence score and, in full view, the model’s rationale.  
The total cost to classify all 217 posts was about **$0.01**.  

---

## Category Clusters

After classification, posts were **clustered with ChatGPT** into subcategories.  
Each category lists its subgroups and post IDs for a quick view of key discussion areas.  

---

<details>
<summary>course_help (76/216)</summary>

- *Course-specific help* (002, 027, 029, 030, 032, 036, 041, 045, 048, 057, 065, 067, 090, 095, 096, 098, 102, 104, 110, 112, 114, 124, 127, 133, 143, 146, 158, 162, 173, 177, 185, 186, 192, 193, 199, 201, 205)  
Requests for strategies, tips, or clarity on specific classes and tasks.

- *Acceleration and pacing* (008, 012, 025, 059, 064, 065, 095, 097, 108, 133, 146, 165, 169, 171, 186, 187)  
How to structure courses and finish faster without burning out.

- *Degree/program decisions* (049, 054, 055, 064, 072, 084, 111, 115, 128, 145, 167, 171, 175, 187, 188, 189, 190)  
Comparing programs, transfers, admissions, and next steps.

- *Pre-assessment and OA struggles* (017, 019, 021, 022, 023, 031, 052, 070, 112, 143, 184)  
Whether to take the PA early, test alignment, and retake experiences.

- *Emotional and motivational struggles* (008, 019, 021, 052, 067, 070, 113, 114, 184)  
Discouragement, burnout, and confidence with exams.

- *Admission and transfer logistics* (049, 072, 111, 115, 171, 175)  
Credit transfer, prerequisites, and starting-point choices.

- *Study aids and external resources* (163, 205)  
Apps, guides, vouchers, and tools that support studying.

</details>

---

<details>
<summary>general_experiences (30/216)</summary>

- *Assessment experiences* (id005, id011, id033, id082, id118, id119, id210, id215)  
Reflections on OAs, PAs, and assessment processes.

- *Progress updates & momentum* (id037, id071, id078, id089, id101, id183, id200)  
Milestones, CU counts, and pacing wins.

- *Degree planning & program decisions* (id050, id132, id142, id159, id179, id195, id203)  
Choosing paths, timing diplomas, and considering master’s.

- *Balancing life and school* (id010, id051, id085, id132, id157, id216)  
Managing studies with work, family, health, and life events.

- *Course frustrations* (id148, id149)  
Specific tough-course pain points.

- *Mindset reflections* (id172, id157)  
Motivation, comparison, and owning your pace.

</details>

---

<details>
<summary>admin_mentor (26/216)</summary>

- *Course access and mentor responsiveness* (003, 004, 093, 196, 202, 170, 182)  
Waiting on courses to open, check-ins, and timely responses.

- *General program and event questions* (077, 080, 088, 161, 181)  
Access to groups, tickets, workshops, and misc program info.

- *Program changes and degree planning* (062, 178, 136, 137)  
Switching programs and graduation timing questions.

- *Graduate transitions* (105, 160, 207)  
Moving from bachelor’s to master’s and access overlaps.

- *Enrollment documents and transcript policies* (129, 131, 134)  
Processing times, what shows on transcripts, GPA.

- *Acceleration and extensions* (044, 093, 136)  
End-of-term accelerations and deadline extensions.

- *Preceptor and collaboration logistics* (086, 151)  
Finding preceptors and structuring team work.

- *Mentor fit and communication style* (140, 182)  
Preferences for call cadence and support style.

</details>

---

<details>
<summary>celebrations_milestones (23/216)</summary>

- *Degree Completions & Confetti* (001, 007, 020, 026, 035, 083, 116, 120, 123, 138, 166, 191, 194, 212, 213)  
Finishing programs and capstones; timelines and reflections.

- *Graduation Gear & Traditions* (001, 058, 121, 154, 156, 198)  
Caps, gowns, stoles, and celebration ideas.

- *Course & Assessment Triumphs* (100, 103, 176)  
Quick wins on exams or tough classes.

</details>

---

<details>
<summary>tech_platforms (22/216)</summary>

- *Proctoring and exam issues* (016, 024, 053, 094, 099, 106, 150, 209)  
Setup problems, interruptions, unclear rules, and tech errors.

- *Portal and system errors* (015, 047, 144, 147)  
Lost submissions, expired keys, outages, logins.

- *Academic tools and reports* (079, 117, 174, 168)  
Grammarly/similarity confusion and authenticity warnings.

- *Evaluation speed* (153, 208)  
Slow/fast grading and turnaround expectations.

- *Software, devices, and apps* (075, 141)  
TTS on mobile, Office installs.

- *Course platforms and pacing* (068)  
Choosing Sophia vs Study.com.

</details>

---

<details>
<summary>career_jobs_networking (12/216)</summary>

- *Career entry challenges* (id038, id076, id109, id122)  
Landing first roles and changing fields.

- *Graduate program paths* (id040, id073, id107)  
MBA, accounting, edtech—fit for goals.

- *Job search support* (id063, id139, id180)  
Part-time options, resumes, and networking.

- *Networking opportunities* (id042, id197)  
Industry nights and commencement meetups.

</details>

---

<details>
<summary>motivation_fun (12/216)</summary>

- *Motivational celebrations* (id018, id028, id034, id066)  
Shoutouts and encouragement to keep going.

- *Acceleration journeys* (id009, id087, id135)  
One-term pushes and rapid pacing.

- *Challenges and setbacks* (id074, id130, id155)  
Stumbles in math and tough classes.

- *Study tools and accountability* (id056, id164)  
Groups, check-ins, and focus aids.

</details>

---

<details>
<summary>financial_aid_policy (11/216)</summary>

- *Program/credit policies impacting aid and pace* (060, 061, 152)  
Which programs finish fastest, second-bachelor considerations, and transfer-credit limits.

- *FAFSA and start timing for grad programs* (013, 014)  
Whether a new FAFSA is needed and self-pay timing vs term dates.

- *Refunds and disbursement schedule* (006, 046)  
Pell/grant refunds, split disbursements, and finishing early.

- *Processing delays and appeals* (039, 091)  
COA appeals and verification backlogs affecting aid release.

- *Paying out of pocket methods* (092)  
Credit card vs payment plans and saving on fees.

- *VA education benefits payment timing* (214)  
When Chapter 35 payments post and release.

</details>

---

<details>
<summary>motivational_fun (2/216)</summary>

- *Graduate school beginnings* (id204, id206)  
Day-one nerves and excitement starting a master’s.

</details>

---

<details>
<summary>other (2/216)</summary>

- *Merchandise and apparel concerns* (id081)  
Finding WGU gear that fits tall/lanky builds.

- *Course equivalency inquiries* (id125)  
Looking for Sophia/Study.com equivalents.

</details>

---

## Facebook Group Data Access (beyond prototype)

This prototype uses **manual scraping**.  
To properly analyze Facebook group data at scale, a business or group admin must follow the official Meta process:

1. **Create a Facebook App and Verify the Business**  
   - [Graph API docs](https://developers.facebook.com/docs/graph-api/)  
   - [Business Verification](https://developers.facebook.com/docs/development/verify-your-business)

2. **Request Permissions and App Review**  
   - [Groups API Reference](https://developers.facebook.com/docs/graph-api/reference/group)  
   - [Group Feed](https://developers.facebook.com/docs/graph-api/reference/group/feed/)  
   - [Permissions Reference](https://developers.facebook.com/docs/permissions/reference)  
   - [App Review guidelines](https://developers.facebook.com/docs/app-review/)

3. **Use Access Tokens**  
   - [Access Token Guide](https://developers.facebook.com/docs/facebook-login/access-tokens/)  
   - For groups, you typically need a **Page Access Token** or **System User Access Token**.

Only with these steps (and admin privileges) can Facebook group data be accessed programmatically.

---

## Project Contents

- **data/fb_accelerators_sep1-14_sentiment.csv** — the raw dataset with sentiment  
- **data/fb_accelerators_sep1-14_sentiment.db** — SQLite database used by Datasette Lite  
- **index.html** — homepage linking to Datasette views  
- **metadata.json** — optional settings for Datasette Lite (titles, facets)  
- **scripts/** — Python scripts used during preparation:
  - `parse_fb_accelerators_sep_1-14_csv.py` (clean raw CSV)  
  - `LLM_categorize_fb.py` (categorize posts with GPT)  
  - `vader_sentiment_fb_accel_1-14.py` (add sentiment column)  
- **README.md** — project overview, with category clusters and sentiment notes  


## Ethics and Privacy

Although the posts come from a public Facebook group, usernames have been anonymized and replaced with incremental user IDs.

---