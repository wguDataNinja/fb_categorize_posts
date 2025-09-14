import pandas as pd

df = pd.read_csv("../data/fb_accelerators_sep1-14_sentiment.csv")

# desired order
new_order = [
    "username",
    "category",
    "confidence",
    "sentiment_compound",
    "rationale",
    "text"
]

df = df[new_order]
df.to_csv("../data/fb_accelerators_sep1-14_sentiment.csv", index=False)