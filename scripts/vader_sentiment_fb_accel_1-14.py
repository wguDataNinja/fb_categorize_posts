import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# load your CSV
df = pd.read_csv("../data/fb_accelerators_sep1-14_labelled.csv")

# set up analyzer
analyzer = SentimentIntensityAnalyzer()

df["sentiment_compound"] = df["text"].apply(lambda x: analyzer.polarity_scores(str(x))["compound"])

df.to_csv("../data/fb_accelerators_sep1-14_sentiment.csv", index=False)