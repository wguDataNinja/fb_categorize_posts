# /Users/buddy/Desktop/projects/fb_categorize_posts/scripts/LLM_categorize_fb.py

import os, time, json, logging
from typing import Dict, List, Tuple
import pandas as pd
from pydantic import BaseModel, ValidationError
from openai import OpenAI
from config import openai_config

# -------- Paths --------
INPUT_CSV = "/Users/buddy/Desktop/projects/fb_categorize_posts/output/fb_accelerators_sep_1-14.csv"
OUTPUT_DIR = "//data"
OUTPUT_BASENAME = "fb_accelerators_sep1-14_labelled.csv"

# -------- Settings --------
MODEL_NAME = "gpt-4o-mini"
MAX_RETRIES = 5
RETRY_SLEEP_SECONDS = 2
TEXT_COL = "text"          # CSV has: username,text
LIMIT = None                 # None = all; or set int (e.g., 200)
BATCH_SIZE = 10            # number of posts per API call

# -------- Prompt --------
PROMPT = """You label Facebook posts for accelerator-topic analysis.

Return JSON with exactly:
- category: one of the following (choose the single best match):
    • celebrations_milestones: Posts about personal or group achievements, milestones, awards, graduations, anniversaries, or celebrations.
    • course_help: Requests for help or advice related to coursework, assignments, exams, or academic topics.
    • admin_mentor: Questions or information about program administration, logistics, mentors, degree plan, or confetti posts.
    • tech_platforms: Posts about portals, proctoring, exam systems, submissions, or technical issues.
    • financial_aid_policy: Questions or information about financial aid, scholarships, tuition, billing, or policy.
    • general_experiences: Sharing personal progress, reflection, or general feedback without a direct help request.
    • motivation_fun: Encouragement, motivation, community bonding, jokes, or lighthearted posts.
    • career_jobs_networking: Job searches, hiring, networking, career events/opportunities.
    • other: Anything that does not fit the above categories.
- rationale: brief reason for the label
- confidence: float in [0,1]
"""

# -------- Logging --------
logger = logging.getLogger("fb.classify_post")
logging.basicConfig(level=logging.INFO)

# -------- Schemas --------
class LabelOutput(BaseModel):
    category: str
    rationale: str
    confidence: float

class LabelItem(BaseModel):
    i: int
    category: str
    rationale: str
    confidence: float

class LabelBatch(BaseModel):
    items: List[LabelItem]

def _strictify_schema(schema_obj):
    # Enforce OpenAI schema mode strictness
    if isinstance(schema_obj, dict):
        if schema_obj.get("type") == "object":
            schema_obj["additionalProperties"] = False
            if "properties" in schema_obj:
                schema_obj["required"] = list(schema_obj["properties"].keys())
        for v in schema_obj.values():
            _strictify_schema(v)
    elif isinstance(schema_obj, list):
        for v in schema_obj:
            _strictify_schema(v)

def get_item_schema():
    schema = LabelOutput.model_json_schema()
    _strictify_schema(schema)
    return {
        "type": "json_schema",
        "json_schema": {
            "name": "fb_post_label",
            "description": "Label a single Facebook post with category, rationale, and confidence",
            "schema": schema,
            "strict": True
        }
    }

def get_batch_schema():
    schema = LabelBatch.model_json_schema()
    _strictify_schema(schema)
    return {
        "type": "json_schema",
        "json_schema": {
            "name": "fb_post_label_batch",
            "description": "Batch classify Facebook posts",
            "schema": schema,
            "strict": True
        }
    }

# -------- Single-item (fallback) --------
def call_model_single(client: OpenAI, post_text: str) -> Dict:
    system_msg = {"role": "system", "content": "You label Facebook posts. Respond with valid JSON that matches the schema."}
    user_msg = {"role": "user", "content": PROMPT + f"\n\nPost:\n{(post_text or '').strip()}"}

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            try:
                resp = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[system_msg, user_msg],
                    response_format=get_item_schema(),
                    temperature=0
                )
            except Exception as schema_error:
                logger.warning(f"Schema mode failed (attempt {attempt}): {schema_error}. Falling back to json_object.")
                resp = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[system_msg, user_msg],
                    response_format={"type": "json_object"},
                    temperature=0
                )

            data = json.loads(resp.choices[0].message.content)
            parsed = LabelOutput(**data)
            return parsed.model_dump()

        except (json.JSONDecodeError, ValidationError, Exception) as e:
            logger.error(f"Single classify attempt {attempt} failed: {type(e).__name__}: {e}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_SLEEP_SECONDS)

    return {"category": "other", "rationale": "fallback after repeated errors", "confidence": 0.0}

# -------- Batch classify --------
def call_model_batch(client: OpenAI, rows: List[Tuple[int, str]]) -> List[Dict]:
    """
    rows: list of (row_index, text)
    returns: list of dicts with keys i, category, rationale, confidence
    """
    system_msg = {"role": "system", "content": "Classify posts. Return only the specified JSON schema."}
    packed_posts = "\n".join(f"{i}: {((t or '').strip())}" for i, t in rows)
    user_msg = {"role": "user", "content": PROMPT + "\n\nPosts (id: text):\n" + packed_posts}

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            # Try schema mode
            try:
                resp = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[system_msg, user_msg],
                    response_format=get_batch_schema(),
                    temperature=0
                )
            except Exception as schema_error:
                logger.warning(f"Batch schema mode failed (attempt {attempt}): {schema_error}. Falling back to json_object.")
                resp = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[system_msg, user_msg],
                    response_format={"type": "json_object"},
                    temperature=0
                )

            data = json.loads(resp.choices[0].message.content)
            parsed = LabelBatch(**data)
            return [it.model_dump() for it in parsed.items]

        except (json.JSONDecodeError, ValidationError, Exception) as e:
            logger.error(f"Batch classify attempt {attempt} failed: {type(e).__name__}: {e}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_SLEEP_SECONDS)

    # Final fallback: mark each as other
    return [{"i": i, "category": "other", "rationale": "batch failure", "confidence": 0.0} for i, _ in rows]

# -------- Main --------
def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    client = OpenAI(api_key=openai_config.OPENAI_API_KEY)

    df = pd.read_csv(INPUT_CSV)
    if TEXT_COL not in df.columns:
        raise ValueError(f"Expected a '{TEXT_COL}' column in CSV.")

    if LIMIT is not None:
        df = df.head(int(LIMIT)).copy()

    # Ensure consistent, compact indexing for batch IDs
    df = df.reset_index(drop=True)

    # Ensure output columns exist
    for col in ["category", "rationale", "confidence"]:
        if col not in df.columns:
            df[col] = None

    # Process in batches
    n = len(df)
    for start in range(0, n, BATCH_SIZE):
        end = min(start + BATCH_SIZE, n)
        slice_rows = [(i, str(df.at[i, TEXT_COL])) for i in range(start, end)]
        results = call_model_batch(client, slice_rows)

        # Fill results; if any missing, fall back per item
        found = {r["i"] for r in results}
        for r in results:
            i = r["i"]
            df.at[i, "category"] = r.get("category")
            df.at[i, "rationale"] = r.get("rationale")
            df.at[i, "confidence"] = r.get("confidence")

        # Fallback for any row not returned by the batch
        missing = [i for i in range(start, end) if i not in found]
        for i in missing:
            single = call_model_single(client, str(df.at[i, TEXT_COL]))
            df.at[i, "category"] = single.get("category")
            df.at[i, "rationale"] = single.get("rationale")
            df.at[i, "confidence"] = single.get("confidence")

        # Optional: incremental save for resilience
        out_path = os.path.join(OUTPUT_DIR, OUTPUT_BASENAME)
        df.iloc[:end].to_csv(out_path, index=False)
        logger.info(f"Processed rows {start}-{end-1} / {n}")

    # Final save
    out_path = os.path.join(OUTPUT_DIR, OUTPUT_BASENAME)
    df.to_csv(out_path, index=False)
    print(f"Saved: {out_path}")

if __name__ == "__main__":
    main()