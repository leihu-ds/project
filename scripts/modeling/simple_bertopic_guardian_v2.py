"""
Improved BERTopic Reproduction Pipeline (v2)

Goal:
- Improve topic quality compared to v1
- Reduce noisy topic keywords
- Improve reproducibility and interpretability

Improvements over v1:
- Added preprocessing pipeline
- HTML cleaning with BeautifulSoup
- Lemmatization with spaCy
- Custom stopword filtering
- Explicit embedding model
- Reproducible UMAP configuration
- Minimum/maximum document frequency filtering
- Improved topic stability

Same as v1, this script remains intentionally simplified compared
to the original paper. The focus is reproducibility
rather than exact replication.
"""

from pathlib import Path
import json
import pandas as pd

from bertopic import BERTopic

from sklearn.feature_extraction.text import (
    CountVectorizer,
    ENGLISH_STOP_WORDS,
)

from umap import UMAP

import spacy
from bs4 import BeautifulSoup


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


# Load Data

documents = []

with open(INPUT_PATH, "r", encoding="utf-8") as f:

    for line in f:

        item = json.loads(line)

        title = item.get("title", "")

        body = item.get("content", {}).get("body", "")

        text = f"{title} {body}"

        # Remove very short documents
        if len(text.strip()) > 50:
            documents.append(text)

print(f"Loaded documents: {len(documents)}")


# Text Preprocessing

print("\nStarting text preprocessing...")

nlp = spacy.load("en_core_web_sm")


def clean_text(text):

    # Remove HTML tags
    soup = BeautifulSoup(text, "html.parser")
    text = soup.get_text()

    # Lowercase + spaCy processing
    doc = nlp(text.lower())

    tokens = []

    for token in doc:

        # Remove stopwords
        if token.is_stop:
            continue

        # Remove punctuation
        if token.is_punct:
            continue

        # Remove spaces
        if token.is_space:
            continue

        lemma = token.lemma_.strip()

        # Remove short tokens
        if len(lemma) < 3:
            continue

        tokens.append(lemma)

    return " ".join(tokens)


cleaned_documents = []

for doc in documents:

    cleaned_doc = clean_text(doc)

    # Remove very short cleaned documents
    if len(cleaned_doc.split()) > 30:
        cleaned_documents.append(cleaned_doc)

documents = cleaned_documents

print(f"Documents after preprocessing: {len(documents)}")

print("Finished preprocessing")


# Stopwords

custom_stopwords = list(ENGLISH_STOP_WORDS) + [
    "said",
    "say",
    "would",
    "could",
    "also",
    "one",
    "two",
    "new",
    "year",
    "people",
]


# Vectorizer with Custom Stopwords and Minimum Document Frequency

vectorizer_model = CountVectorizer(
    stop_words=custom_stopwords,
    ngram_range=(1, 2),
    min_df=1,
    max_df=1.0
)


# UMAP Configuration

umap_model = UMAP(
    n_neighbors=5,
    n_components=5,
    min_dist=0.0,
    metric="cosine",
    random_state=42,
)


# BERTopic Model

topic_model = BERTopic(
    embedding_model="all-MiniLM-L6-v2",
    vectorizer_model=vectorizer_model,
    umap_model=umap_model,
    min_topic_size=4,
    verbose=True,
)


# Train Model
topics, probs = topic_model.fit_transform(documents)


# Topic Information

topic_info = topic_model.get_topic_info()

print("\n================ TOPIC OVERVIEW ================\n")

print(topic_info.head(15))


# Save Topic Info

topic_info.to_csv(
    OUTPUT_DIR / "guardian_topic_info_v2.csv",
    index=False
)

print("\nSaved topic info")


# Save Topic Keywords

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
    OUTPUT_DIR / "guardian_topics_v2.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        topics_output,
        f,
        indent=2,
        ensure_ascii=False
    )

print("Saved topic keywords")


# Print Topics

print("\n================ TOPICS ================\n")

for topic_id in topic_info["Topic"].tolist():

    if topic_id == -1:
        continue

    print(f"\nTOPIC {topic_id}\n")

    print(topic_model.get_topic(topic_id))


print("\nPipeline completed successfully.")