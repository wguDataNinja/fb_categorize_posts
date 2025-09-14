import pandas as pd
import tiktoken

INPUT_CSV = "/Users/buddy/Desktop/projects/fb_categorize_posts/output/fb_accelerators_sep_1-14.csv"

def estimate_tokens(text: str, model="gpt-4o-mini"):
    enc = tiktoken.encoding_for_model(model)
    return len(enc.encode(text))

def summarize_tokens(df, text_col="text", model="gpt-4o-mini"):
    counts = df[text_col].fillna("").map(lambda t: estimate_tokens(str(t), model))
    return {
        "mean": counts.mean(),
        "p50": counts.median(),
        "p95": counts.quantile(0.95),
        "max": counts.max()
    }

if __name__ == "__main__":
    df = pd.read_csv(INPUT_CSV)   # <-- add this line
    stats = summarize_tokens(df)
    print("Token stats:", stats)