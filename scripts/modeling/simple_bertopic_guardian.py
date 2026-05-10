"""
Simple BERTopic Reproduction Pipeline

Goal:
- Run a simplified BERTopic model
- Generate interpretable topics
- Produce reproducible outputs

This script is intentionally simplified compared to the original paper.
The focus is reproducibility rather than exact replication.
"""

from pathlib import Path
import json
import pandas as pd
from bertopic import BERTopic
from sklearn.feature_extraction.text import CountVectorizer

# Set Paths
ROOT = Path(__file__).resolve().parents[2]

INPUT_PATH = (
    ROOT
    / "datasets"
    / "processed"
    / "guardian"
    / "guardian_model_ready.jsonl"
)

OUTPUT_DIR = ROOT / "results" / "guardian"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# Load data
documents = []

with open(INPUT_PATH, "r", encoding="utf-8") as f:
    for line in f:
        item = json.loads(line)

        title = item.get("title", "")
        body = item.get("content", {}).get("body", "")

        text = f"{title} {body}"

        if len(text.strip()) > 50:
            documents.append(text)

print(f"Loaded documents: {len(documents)}")


# BERTopic model
vectorizer_model = CountVectorizer(
    stop_words="english",
    ngram_range=(1, 2),
)

topic_model = BERTopic(
    vectorizer_model=vectorizer_model,
    min_topic_size=15,
    verbose=True,
)

topics, probs = topic_model.fit_transform(documents)


# Topic info
topic_info = topic_model.get_topic_info()

print(topic_info.head())

topic_info.to_csv(
    OUTPUT_DIR / "guardian_topic_info.csv",
    index=False
)

print("\nSaved topic info")


# Save topic keywords
topics_output = []

for topic_id in topic_info["Topic"]:

    if topic_id == -1:
        continue

    words = topic_model.get_topic(topic_id)

    topic_words = [word for word, score in words]

    topics_output.append({
        "topic_id": int(topic_id),
        "keywords": topic_words
    })

with open(
    OUTPUT_DIR / "guardian_topics.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(topics_output, f, indent=2)

print("Saved topic keywords")

for topic_id in topic_info["Topic"].tolist():

    if topic_id == -1:
        continue

    print(f"\nTOPIC {topic_id}")

    print(topic_model.get_topic(topic_id))