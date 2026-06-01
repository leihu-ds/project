from pathlib import Path
import re

import pandas as pd
from bertopic import BERTopic
from umap import UMAP
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer, ENGLISH_STOP_WORDS


# =========================
# 1. Set paths
# =========================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "datasets" / "twitter" / "twitter_cleaned.jsonl"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "member3"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# =========================
# 2. Load cleaned data
# =========================

print("Loading Twitter cleaned data...")

df = pd.read_json(DATA_PATH, lines=True)

print("Columns:", df.columns.tolist())
print("Number of rows before filtering:", len(df))

df = df.dropna(subset=["clean_text"])
df["clean_text"] = df["clean_text"].astype(str)

df = df[df["clean_text_length"] > 20]


# =========================
# 2.1 Twitter-specific model text cleaning
# =========================

CUSTOM_STOPWORDS = {
    "rt", "amp", "tweet", "twitter", "pic", "com", "http", "https", "www",
    "2020", "2021", "2022", "2023",
    "january", "february", "march", "april", "may", "june", "july",
    "august", "september", "october", "november", "december",
    "jan", "feb", "mar", "apr", "jun", "jul", "aug", "sep", "oct", "nov", "dec",
    "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday",
    "new", "join", "today", "check", "says", "said",
    "la", "di", "el", "en", "de"
}


def twitter_clean(text):
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+", " ", text)
    text = re.sub(r"@\w+", " ", text)
    text = re.sub(r"#", " ", text)
    text = re.sub(r"\b\d{1,4}\b", " ", text)
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


df["model_text"] = df["clean_text"].apply(twitter_clean)
df = df[df["model_text"].str.len() > 30]

documents = df["model_text"].tolist()

print("Number of documents used:", len(documents))


# =========================
# 3. Configure BERTopic
# Paper Table 2 Twitter best parameters:
# n_gram=2
# n_clusters=10
# n_components=10
# n_neighbors=10
# =========================

print("Configuring BERTopic model...")

stop_words = list(ENGLISH_STOP_WORDS.union(CUSTOM_STOPWORDS))

vectorizer_model = CountVectorizer(
    ngram_range=(1, 2),
    stop_words=stop_words,
    min_df=3
)

umap_model = UMAP(
    n_neighbors=10,
    n_components=10,
    random_state=42
)

cluster_model = KMeans(
    n_clusters=10,
    random_state=42,
    n_init=10
)

topic_model = BERTopic(
    vectorizer_model=vectorizer_model,
    umap_model=umap_model,
    hdbscan_model=cluster_model,
    calculate_probabilities=False,
    verbose=True
)


# =========================
# 4. Fit model
# =========================

print("Training BERTopic model...")

topics, probs = topic_model.fit_transform(documents)


# =========================
# 5. Save outputs
# =========================

print("Saving outputs...")

topic_info = topic_model.get_topic_info()

topic_info.to_csv(
    OUTPUT_DIR / "twitter_bertopic_v2_topic_info.csv",
    index=False
)

topic_words = []

for topic_id in topic_info["Topic"]:

    if topic_id == -1:
        continue

    words = topic_model.get_topic(topic_id)

    if words is None:
        continue

    for word, score in words:

        topic_words.append({
            "topic": topic_id,
            "word": word,
            "score": score
        })

topic_words_df = pd.DataFrame(topic_words)

topic_words_df.to_csv(
    OUTPUT_DIR / "twitter_bertopic_v2_topic_words.csv",
    index=False
)

doc_topics = df[
    [
        "tweet_id",
        "url",
        "recovery_method"
    ]
].copy()

doc_topics["topic"] = topics

doc_topics.to_csv(
    OUTPUT_DIR / "twitter_bertopic_v2_document_topics.csv",
    index=False
)


# =========================
# 6. Print summary
# =========================

print("\nDone.")
print("Topic info:")
print(topic_info)

print("\nTop words by topic:")
print(topic_words_df.groupby("topic").head(10))