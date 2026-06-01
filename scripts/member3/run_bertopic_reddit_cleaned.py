from pathlib import Path

import pandas as pd
from bertopic import BERTopic
from umap import UMAP
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer


# =========================
# 1. Set paths
# =========================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "datasets" / "reddit" / "reddit_cleaned.jsonl"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "member3"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# =========================
# 2. Load cleaned data
# =========================

print("Loading Reddit cleaned data...")

df = pd.read_json(DATA_PATH, lines=True)

print("Columns:", df.columns.tolist())
print("Number of rows before filtering:", len(df))

df = df.dropna(subset=["clean_text"])
df["clean_text"] = df["clean_text"].astype(str)

df = df[df["clean_text_length"] > 20]

documents = df["clean_text"].tolist()

print("Number of documents used:", len(documents))


# =========================
# 3. Configure BERTopic
# Paper Table 2 Reddit best parameters:
# n_gram=3
# n_clusters=15
# n_components=15
# n_neighbors=15
# =========================

print("Configuring BERTopic model...")

vectorizer_model = CountVectorizer(
    ngram_range=(1, 3),
    stop_words="english"
)

umap_model = UMAP(
    n_neighbors=15,
    n_components=15,
    random_state=42
)

cluster_model = KMeans(
    n_clusters=15,
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
    OUTPUT_DIR / "reddit_bertopic_topic_info.csv",
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
    OUTPUT_DIR / "reddit_bertopic_topic_words.csv",
    index=False
)

doc_topics = df[
    [
        "post_id",
        "title",
        "subreddit",
        "created_utc",
        "url"
    ]
].copy()

doc_topics["topic"] = topics

doc_topics.to_csv(
    OUTPUT_DIR / "reddit_bertopic_document_topics.csv",
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
