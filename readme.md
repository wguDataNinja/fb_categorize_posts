# WGU Accelerators – Prototype Data Explorer

This project is a **prototype** for exploring posts from the WGU Accelerators Facebook group.  
The data shown here was **scraped manually** as a proof of concept.  
These 217 posts are from **Sep 1 to Sep 14**, and only **top-level posts** (no comments) were scraped. 
Only posts with text were kept.

The intended use-case for this data is to demonstrate **LLM classification and summarization** for topic analysis.  
For ongoing analysis, true automation would require Facebook administrator privileges and a verified Facebook app.

**Known limitations:** Some posts contain images or video which are important for context, and not available to the LLM for categorization.

## Ethics and Privacy

Although the posts come from a public Facebook group, usernames have been anonymized and replaced with incremental user IDs.

---

## Interacting with the Data

The [Datasette Lite page](index.html) lets you browse the posts in different ways:

- **All posts view**: Shows every column, including the **LLM’s rationale** behind its classification.  
- **Category views**: Show only posts belonging to a given category, with rationale hidden.  
- **Sorting**: Click column headers to sort (e.g., by confidence or sentiment).  
- **Filtering**: Use the search boxes to narrow down posts.  
- **Download**: Export any view as CSV or JSON.

---

## Categorization

We used **ChatGPT 4o-mini** to classify posts into naturally occurring themes.  
Each classification includes a **confidence score** and, in the full view, a **rationale** explaining the decision.

### Categories

- **celebrations_milestones**: Achievements, graduations, awards, anniversaries, or other milestones.  
- **course_help**: Requests for help with coursework, assignments, or exams.  
- **admin_mentor**: Questions about program administration, mentors, degree plans, or logistics.  
- **tech_platforms**: Issues with portals, proctoring, submissions, or exam systems.  
- **financial_aid_policy**: Topics on financial aid, scholarships, tuition, billing, or policy.  
- **general_experiences**: Personal progress, reflections, or general feedback not seeking help.  
- **motivation_fun**: Encouragement, motivation, jokes, or community bonding.  
- **career_jobs_networking**: Posts about jobs, hiring, networking, or career opportunities.  
- **other**: Content not fitting the above categories.  

These categories can be adjusted before LLM classification depending on the topics of interest.

---

## Sentiment Analysis

To measure tone, we applied **VADER sentiment analysis**.  
VADER (Valence Aware Dictionary for sEntiment Reasoning) is well suited for short, social-media style text.  

It adds a `sentiment_compound` score from **−1 (very negative)** to **+1 (very positive)**.  
This helps highlight whether posts are celebratory, neutral, or frustrated, without needing manual review.

---

## Facebook Data Access (for real projects)

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

Only with these steps (and admin privileges) can Facebook group data be accessed programmatically and securely.

---

## Project Contents

- **data/fb_accelerators_sep1-14_sentiment.csv** — the dataset used in the prototype  
- **index.html** — homepage linking to different Datasette views  
- **metadata.json** — optional settings for Datasette Lite (titles, facets)  
- **scripts/** — Python scripts used during preparation:
  - `parse_fb_accelerators_sep_1-14_csv.py` (clean raw CSV)  
  - `LLM_categorize_fb.py` (categorize posts with GPT)  
  - `vader_sentiment_fb_accel_1-14.py` (add sentiment column)